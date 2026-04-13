import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from datetime import datetime
from selenium.webdriver.chrome.options import Options

fecha_diaria = datetime.now().strftime("%Y-%m-%d")
output_dir = "/mnt/bigdata/smart"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/google-chrome"

driver = uc.Chrome(options=options, headless=True)
data_tel=[]

try:
    url = "https://www.pcbox.com/smartphones-telefonia-y-wearables/smartphones"
    driver.get(url)
    time.sleep(8) 

    for i in range(10):
        print("Scraping PcBox")
	print(f"Scrapeando página {i}...")
	try:
            boton_cargar_mas = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.vtex-button[href*='page=']"))
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
            nombre = producto.find_element(By.TAG_NAME, 'h3').text
            entero = producto.find_element(By.CLASS_NAME, 'ticnova-product-price-1-x-currencyInteger').text
            fraccion = producto.find_element(By.CLASS_NAME, 'ticnova-product-price-1-x-currencyFraction').text
            nombre = nombre.replace('TELEFONO MOVIL LIBRE','').replace('SMARTPHONE','')
            entero = entero.replace('.', '').replace(',', '')
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
	df_tel=pd.Dataframe(data_tel)
	csv_path=os.path.join(output_dir,f"smartphones_PcBox_{fecha_diaria}.csv")
	df_tel.to_csv(csv_path,index=False,encoding="utf-8-sig")
	print(f"archivo guardado en {csv_path}")
else:
	print("No se encontraron datos")
