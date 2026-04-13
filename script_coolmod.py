import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from datetime import datetime
from selenium.webdriver.chrome.options import Options

fecha_diaria = datetime.now().strftime("%Y-%m-%d")
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
        print("Scrapeando Coolmod")
	print(f"Scrapeando página {pagina}...")
        driver.get(f"https://www.coolmod.com/portatiles-portatiles/?pagina={pagina}")
        time.sleep(8)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        articulos = driver.find_elements(By.TAG_NAME, 'article')

        for art in articulos:
            try:
                enlace = art.find_element(By.TAG_NAME, 'a')
                nombre = enlace.get_attribute("data-itemname")
                precio = enlace.get_attribute("data-itemprice")

                if nombre and precio:
                    data_por.append({
                        "Nombre": nombre.strip(),
                        "Precio": float(precio),
                        "Tienda": "Coolmod",
                        "Fecha": fecha_diaria
                    })
            except:
                continue

finally:
    driver.quit()

if data_por:
    df_por = pd.DataFrame(data_por)
    csv_path = os.path.join(output_dir, f"portátiles_Coolmod_{fecha_diaria}.csv")
    df_por.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Archivo guardado en: {csv_path}")
else:
    print("No se encontraron datos.")
