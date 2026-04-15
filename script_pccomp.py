import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
from datetime import datetime
import os

fecha_diaria = datetime.now().strftime("%Y-%m-%d")
base_path = "/mnt/bigdata/"

for carpeta in ['port', 'smart', 'comp']:
    os.makedirs(os.path.join(base_path, carpeta), exist_ok=True)

options = uc.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = uc.Chrome(options=options)

def extraer_categoria(url_base, max_paginas, path_final, componente_tag=None):
    resultados = []
    print(f"-> Iniciando: {url_base}")
    
    for pagina in range(1, max_paginas + 1):
        url = f"{url_base}?page={pagina}"
        try:
            driver.get(url)
            time.sleep(random.uniform(7, 12))
            
            productos = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="normal-link"]')
            
            if not productos:
                print(f"   Fin de categoría en página {pagina}")
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
                            "Tienda": "PcComponentes",
                            "Fecha": fecha_diaria
                        }
                        if componente_tag:
                            item["componente"] = componente_tag
                        
                        resultados.append(item)
                except:
                    continue
            
            print(f"   Página {pagina}: {len(resultados)} items.")
            
        except Exception as e:
            print(f"   Error: {e}")
            break
            
    if resultados:
        df = pd.DataFrame(resultados)
        file_exists = os.path.isfile(path_final)
        df.to_csv(path_final, mode='a', index=False, header=not file_exists, encoding="utf-8-sig")
        print(f"   OK: Guardado en {path_final}")
    else:
        print(f"   ERROR: No se capturaron datos.")

try:
    extraer_categoria("https://www.pccomponentes.com/portatiles", 9, f"{base_path}port/portátiles_PcComp_{fecha_diaria}.csv")
    
    extraer_categoria("https://www.pccomponentes.com/smartphone-moviles", 9, f"{base_path}smart/smartphones_PcComp_{fecha_diaria}.csv")

    path_unico_comp = f"{base_path}comp/componentes_PcComp_{fecha_diaria}.csv"
    if os.path.exists(path_unico_comp):
        os.remove(path_unico_comp)

    lista_componentes = ["monitores-pc", "fuentes-alimentacion", "discos-duros", "tarjetas-graficas", "placas-base"]
    for comp in lista_componentes:
        extraer_categoria(f"https://www.pccomponentes.com/{comp}", 9, path_unico_comp, componente_tag=comp)

finally:
    driver.quit()
    print("Navegador cerrado.")
