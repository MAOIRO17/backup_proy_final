import pandas as pd
from thefuzz import process, fuzz
from datetime import datetime
import os

fecha = datetime.now().strftime("%Y-%m-%d")
base_path = "/mnt/bigdata/datasets/"
out_path = f"{base_path}comparaciones/"
os.makedirs(out_path, exist_ok=True)

def cargar_y_limpiar(path, col_nombre):
    if not os.path.exists(path):
        print(f"Archivo no encontrado: {path}")
        return None
    df = pd.read_csv(path)
    df = df.dropna(subset=[col_nombre]).drop_duplicates(subset=[col_nombre])
    return df

def realizar_comparativa_kaggle(path_tienda, path_ref, salida):
    df_t = cargar_y_limpiar(path_tienda, 'Nombre')
    col_r = 'Name' if '2025' in path_ref else 'items_Decribtion'
    df_r = cargar_y_limpiar(path_ref, col_r)

    if df_t is None or df_r is None: return

    if '2025' in path_ref:
        df_r['P_Ref'] = (pd.to_numeric(df_r['Price'].astype(str).str.replace(',', ''), errors='coerce') / 109.13).round(2)
    else:
        df_r['P_Ref'] = pd.to_numeric(df_r['prices'].astype(str).str.replace(',', ''), errors='coerce')

    df_r = df_r.dropna(subset=['P_Ref'])
    nombres_r = df_r[col_r].unique().tolist()

    def buscar(n):
        if not n: return None
        res = process.extractOne(str(n), nombres_r, scorer=fuzz.token_set_ratio)
        return res if res and res[1] >= 80 else None

    print(f"Procesando Kaggle: {salida}")
    df_t['Match'] = df_t['Nombre'].apply(buscar)
    df_t = df_t.dropna(subset=['Match']).copy()
    
    df_t['Nombre_Ref'] = df_t['Match'].apply(lambda x: x[0])
    df_fin = df_t.merge(df_r, left_on='Nombre_Ref', right_on=col_r)
    df_fin['Diferencia'] = (df_fin['P_Ref'] - df_fin['Precio']).round(2)

    df_fin.to_csv(f"{out_path}{salida}_{fecha}.csv", index=False, encoding='utf-8-sig')
    print(f"Finalizado Kaggle: {salida} | Coincidencias: {len(df_fin)}")

def realizar_comparativa_tiendas(path_a, path_b, salida, etiqueta_a, etiqueta_b):
    df_a = cargar_y_limpiar(path_a, 'Nombre')
    df_b = cargar_y_limpiar(path_b, 'Nombre')

    if df_a is None or df_b is None: return

    nombres_b = df_b['Nombre'].unique().tolist()

    def buscar_tienda(n):
        if not n: return None
        res = process.extractOne(str(n), nombres_b, scorer=fuzz.token_set_ratio)
        if res and res[1] >= 85:
            if str(n).split()[0].upper() == str(res[0]).split()[0].upper():
                return res
        return None

    print(f"Procesando Tiendas: {salida}")
    df_a['Match'] = df_a['Nombre'].apply(buscar_tienda)
    df_res = df_a.dropna(subset=['Match']).copy()

    if df_res.empty:
        print(f"Sin coincidencias: {salida}")
        return

    df_res['Nombre_Ref'] = df_res['Match'].apply(lambda x: x[0])
    df_fin = df_res.merge(
        df_b[['Nombre', 'Precio']], 
        left_on='Nombre_Ref', 
        right_on='Nombre', 
        suffixes=(f'_{etiqueta_a}', f'_{etiqueta_b}')
    )

    df_fin.to_csv(f"{out_path}{salida}_{fecha}.csv", index=False, encoding='utf-8-sig')
    print(f"Finalizado Tiendas: {salida} | Coincidencias: {len(df_fin)}")

realizar_comparativa_kaggle(
    f'{base_path}smart/smartphones_PcBox_{fecha}.csv',
    f'{base_path}dt_kaggle/2025_All_mobiles_Dataset.csv',
    'comp_smart_PcBox_Kaggle'
)

realizar_comparativa_kaggle(
    f'{base_path}comp/componentes_PcComp_{fecha}.csv',
    f'{base_path}dt_kaggle/prices_components.csv',
    'comp_componentes_PcComp_Kaggle'
)

realizar_comparativa_tiendas(
    f'{base_path}port/portatiles_Coolmod_{fecha}.csv',
    f'{base_path}port/portatiles_PcComp_{fecha}.csv',
    'comp_port_PcComp_Coolmod', 'Coolmod', 'PcComp'
)

realizar_comparativa_tiendas(
    f'{base_path}smart/smartphones_PcBox_{fecha}.csv',
    f'{base_path}smart/smartphones_PcComp_{fecha}.csv',
    'comp_smart_PcComp_PcBox', 'PcBox', 'PcComp'
)
