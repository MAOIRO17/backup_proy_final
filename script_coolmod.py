import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import datetime

fecha_diaria = datetime.now().strftime("%Y-%m-%d")
options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = uc.Chrome(options=options)
data_por = []

try:
    print("Scrapeando Coolmod")
    for pagina in range(1, 10):
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
    df = pd.DataFrame(data_por)
    df.to_csv(f"/mnt/bigdata/datasets/port/portátiles_Coolmod_{fecha_diaria}.csv", index=False, encoding="utf-8-sig")

