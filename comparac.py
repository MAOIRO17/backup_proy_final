import pandas as pd
from thefuzz import process, fuzz
from datetime import datetime
import os

fecha = datetime.now().strftime("%Y-%m-%d")
out_path = "/mnt/bigdata/datasets/comparaciones/"
os.makedirs(out_path, exist_ok=True)

def cargar_y_limpiar(path, col_nombre):
    if not os.path.exists(path): return None
    df = pd.read_csv(path).drop_duplicates(subset=[col_nombre]).dropna(subset=[col_nombre])
    return df

def realizar_comparativa_kaggle(path_tienda, path_ref, salida):
    df_t = cargar_y_limpiar(path_tienda, 'Nombre')
    df_r = cargar_y_limpiar(path_ref, 'Name' if '2025' in path_ref else 'items_Decribtion')
    
    if df_t is None or df_r is None: return

    col_r = 'Name' if '2025' in path_ref else 'items_Decribtion'
    
    if '2025' in path_ref:
        df_r['P_Ref'] = (pd.to_numeric(df_r['Price'].astype(str).str.replace(',', ''), errors='coerce') / 109.13).round(2)
    else:
        df_r['P_Ref'] = pd.to_numeric(df_r['prices'].astype(str).str.replace(',', ''), errors='coerce')

    nombres_r = df_r[col_r].tolist()
    
    def buscar(n):
        res = process.extractOne(n, nombres_r, scorer=fuzz.token_set_ratio)
        return res if res and res[1] >= 80 else None

    df_t['Match'] = df_t['Nombre'].apply(buscar)
    df_t = df_t.dropna(subset=['Match'])
    df_t['Nombre_Ref'] = df_t['Match'].apply(lambda x: x[0])
    df_t['Similitud'] = df_t['Match'].apply(lambda x: x[1])

    df_fin = df_t.merge(df_r, left_on='Nombre_Ref', right_on=col_r)
    df_fin['Diferencia'] = (df_fin['P_Ref'] - df_fin['Precio']).round(2)
    
    df_fin[['Nombre', 'Precio', 'P_Ref', 'Similitud', 'Diferencia']].to_csv(f"{out_path}{salida}_{fecha}.csv", index=False)
    print(f"OK Kaggle: {salida}")

def realizar_comparativa_tiendas(path_a, path_b, salida, etiqueta_a, etiqueta_b):
    df_a = cargar_y_limpiar(path_a, 'Nombre')
    df_b = cargar_y_limpiar(path_b, 'Nombre')

    if df_a is None or df_b is None: return

    nombres_b = df_b['Nombre'].tolist()

    def buscar_tienda(n):
        res = process.extractOne(n, nombres_b, scorer=fuzz.token_set_ratio)
        if res and res[1] >= 85 and n.split()[0].upper() == res[0].split()[0].upper():
            return res
        return None

    df_a['Match'] = df_a['Nombre'].apply(buscar_tienda)
    df_res = df_a.dropna(subset=['Match']).copy()
    df_res['Nombre_Ref'] = df_res['Match'].apply(lambda x: x[0])

    df_fin = df_res.merge(df_b[['Nombre', 'Precio']], left_on='Nombre_Ref', right_on='Nombre', suffixes=('_A', '_B'))
    df_fin['Diferencia'] = (df_fin['Precio_A'] - df_fin['Precio_B']).round(2)

    df_fin.to_csv(f"{out_path}{salida}_{fecha}.csv", index=False)
    print(f"OK Tiendas: {salida}")

realizar_comparativa_kaggle(f'datasets/smart/smartphones_PcBox_{fecha}.csv', 'datasets/dt_kaggle/2025_All_mobiles_Dataset.csv', 'comp_smart_PcBox_Kaggle')
realizar_comparativa_kaggle(f'datasets/comp/componentes_PcComp_{fecha}.csv', 'datasets/dt_kaggle/prices_components.csv', 'comp_componentes_PcComp_Kaggle')

realizar_comparativa_tiendas(f'datasets/port/portátiles_Coolmod_{fecha}.csv', f'datasets/port/portátiles_PcComp_{fecha}.csv', 'comp_port_PcComp_Coolmod', 'Coolmod', 'PcComp')
realizar_comparativa_tiendas(f'datasets/smart/smartphones_PcBox_{fecha}.csv', f'datasets/smart/smartphones_PcComp_{fecha}.csv', 'comp_smart_PcComp_PcBox', 'PcBox', 'PcComp')
