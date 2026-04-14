import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
import os
from datetime import datetime

fecha_diaria = datetime.now().strftime("%Y-%m-%d")
output_dir = "/mnt/bigdata/smart"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = uc.Chrome(options=options)

data_tel = []

try:
    print("Scrapeando PcBox...")
    url = "https://www.pcbox.com/smartphones-telefonia-y-wearables/smartphones"
    driver.get(url)
    time.sleep(8) 

    for i in range(10):
        try:
            print(f"scrapeando página {i+1}")
            boton_cargar_mas = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.vtex-button[href*='page=']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_cargar_mas)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", boton_cargar_mas)
            time.sleep(random.uniform(4, 6))
        except:
            break

    productos = driver.find_elements(By.CSS_SELECTOR, 'section.vtex-product-summary-2-x-container')

    for producto in productos:
        try:
            nombre = producto.find_element(By.CSS_SELECTOR, 'span.vtex-product-summary-2-x-productBrand').text
            entero = producto.find_element(By.CLASS_NAME, 'ticnova-product-price-1-x-currencyInteger').text
            fraccion = producto.find_element(By.CLASS_NAME, 'ticnova-product-price-1-x-currencyFraction').text
            
            nombre_limpio = nombre.replace('TELEFONO MOVIL LIBRE','').replace('SMARTPHONE','').strip()
            entero = entero.replace('.', '').replace(',', '')
            precio_final = float(f"{entero}.{fraccion}")
            
            if nombre_limpio:
                data_tel.append({
                    "Nombre": nombre_limpio,
                    "Precio": precio_final,
                    "Tienda": "PCBOX",
                    "Fecha": fecha_diaria
                })
        except:
            continue

finally:
    driver.quit()

if data_tel:
    df_tel = pd.DataFrame(data_tel)
    filename = f"{output_dir}/smartphones_PcBox_{fecha_diaria}.csv"
    df_tel.to_csv(filename, index=False, encoding="utf-8-sig")
