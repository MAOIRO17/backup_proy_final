import pandas as pd
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

output_dir = "/mnt/bigdata/smart"
fecha_diaria = time.strftime("%Y-%m-%d")
data_tel = []
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

options = Options()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://www.pcbox.com/smartphones-telefonia-y-wearables/smartphones")
    time.sleep(8)
    for i in range(10):
        print(f"Scrapeando página {i}...")
        try:
            boton_cargar_mas = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class*='vtex-button'][href*='page=']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_cargar_mas)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", boton_cargar_mas)
            time.sleep(random.uniform(4, 6))
        except Exception:
            break

    productos = driver.find_elements(By.TAG_NAME, 'article')
    for producto in productos:
        try:
            nombre_elem = producto.find_element(By.TAG_NAME, 'h3')
            entero_elem = producto.find_element(By.CLASS_NAME, 'ticnova-product-price-1-x-currencyInteger')
            fraccion_elem = producto.find_element(By.CLASS_NAME, 'ticnova-product-price-1-x-currencyFraction')
            nombre = nombre_elem.text.replace('TELEFONO MOVIL LIBRE', '').replace('SMARTPHONE', '').strip()
            entero = entero_elem.text.replace('.', '').replace(',', '').strip()
            fraccion = fraccion_elem.text.strip()
            precio_final = float(f"{entero}.{fraccion}")

            if nombre:
                data_tel.append({
                    "Nombre": nombre,
                    "Precio": precio_final,
                    "Tienda": "PCBOX",
                    "Fecha": fecha_diaria
                })
        except Exception:
            continue

finally:
    driver.quit()

if data_tel:
    df_tel = pd.DataFrame(data_tel)
    csv_path = os.path.join(output_dir, f"smartphones_PcBox_{fecha_diaria}.csv")
    df_tel.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Archivo guardado en {csv_path}")
else:
    print("No se encontraron datos")
