import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
import os
from datetime import datetime

fecha_diaria = datetime.now().strftime("%Y-%m-%d")

for carpeta in ["port", "smart", "comp"]:
    if not os.path.exists(f"/mnt/bigdata/{carpeta}"):
        os.makedirs(f"/mnt/bigdata/{carpeta}")

options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = uc.Chrome(options=options)

def scrapear_pccomponentes(categorias_dict):
    for categoria, info in categorias_dict.items():
        print(f"Escrapeando PcComponentes")
        lista_datos = []
        
        for p in info['urls']:
            for pagina in range(1, 10):
                print(f"scrapeando página {pagina}")
                url = f"https://www.pccomponentes.com/{p}?page={pagina}"
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
                            item = {
                                "Nombre": nombre,
                                "Precio": float(precio) if precio else 0.0,
                                "Valoracion": valoracion,
                                "Fecha": fecha_diaria,
                                "Tienda": "PcComponentes"
                            }
                            if 'extra_key' in info:
                                item[info['extra_key']] = p
                            lista_datos.append(item)
                    except:
                        continue
        
        if lista_datos:
            df = pd.DataFrame(lista_datos)
            df.to_csv(f"/mnt/bigdata/{info['path']}_{fecha_diaria}.csv", index=False, encoding="utf-8-sig")

try:
    config = {
        "Portátiles": {
            "urls": ["portatiles"],
            "path": "port/portátiles_PcComp"
        },
        "Smartphones": {
            "urls": ["smartphone-moviles"],
            "path": "smart/smartphones_PcComp"
        },
        "Componentes": {
            "urls": ["monitores-pc", "fuentes-alimentacion", "discos-duros", "tarjetas-graficas", "placas-base"],
            "path": "comp/componentes_PcComp",
            "extra_key": "componente"
        }
    }
    scrapear_pccomponentes(config)
finally:
    driver.quit()
