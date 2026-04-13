import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
import random
from datetime import datetime
from selenium.webdriver.chrome.options import Options

fecha_diaria=datetime.now().strftime("%Y-%m-%d")
output_dir = "/mnt/bigdata/port"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/google-chrome"

driver = uc.Chrome(options=options, headless=True)
data_por = []
try:
    for pagina in range(1, 10):
        url = f"https://www.pccomponentes.com/portatiles?page={pagina}"
        driver.get(url)
        
        time.sleep(random.uniform(5, 8))
        
        productos = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="normal-link"]')
        
        if not productos:
            break

        for producto in productos:
            try:
                nombre = producto.get_attribute("data-product-name")
                precio = producto.get_attribute("data-product-price")
                try:
                    valoracion = producto.find_element(By.CSS_SELECTOR, "span[class*='rating']").text
                except:
                    valoracion = "N/A"

                if nombre:
                    data_por.append({
                        "Nombre": nombre,
                        "Precio": float(precio) if precio else 0.0,
                        "Valoracion": valoracion,
                        "Fecha": fecha_diaria
                    })
            except:
                continue
finally:
    driver.quit()

if data_por:
    df_por = pd.DataFrame(data_por)
    csv_path = os.path.join(output_dir, f"portátiles_PcComp_{fecha_diaria}.csv")
    df_por.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Archivo guardado en: {csv_path}")
else:
    print("No se encontraron datos.")
