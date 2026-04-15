import pandas as pd
from thefuzz import process, fuzz
from datetime import datetime
import os

fecha_diaria = datetime.now().strftime("%Y-%m-%d")
base_output_path = "/mnt/bigdata/comparaciones/"
os.makedirs(base_output_path, exist_ok=True)

def realizar_comparativa_kaggle(path_tienda, path_referencia, nombre_salida):
    if not os.path.exists(path_tienda) or not os.path.exists(path_referencia):
        print(f"Archivo no encontrado para {nombre_salida}")
        return
    try:
        df_tienda = pd.read_csv(path_tienda).drop_duplicates(subset=['Nombre'])
        df_tienda = df_tienda.rename(columns={'Nombre': 'Nombre_Tienda', 'Precio': 'Precio_Tienda'})
        df_ref = pd.read_csv(path_referencia)

        if '2025_All_mobiles_Dataset.csv' in path_referencia:
            df_ref['Price'] = pd.to_numeric(df_ref['Price'].astype(str).str.replace(',', ''), errors='coerce')
            df_ref['Precio_Referencia'] = (df_ref['Price'] / 109.13).round(2)
            df_ref = df_ref[df_ref['Precio_Referencia'] > 50].drop_duplicates(subset=['Name'])
            col_ref_nombre = 'Name'
        elif 'prices_components.csv' in path_referencia:
            df_ref['prices'] = pd.to_numeric(df_ref['prices'].astype(str).str.replace(',', ''), errors='coerce')
            df_ref = df_ref.rename(columns={'prices': 'Precio_Referencia'}).drop_duplicates(subset=['items_Decribtion'])
            col_ref_nombre = 'items_Decribtion'
        
        nombres_ref_list = df_ref[col_ref_nombre].tolist()
        df_tienda['Match_Data'] = df_tienda['Nombre_Tienda'].apply(
            lambda x: process.extractOne(x, nombres_ref_list, scorer=fuzz.token_set_ratio)
        )
        df_tienda = df_tienda.dropna(subset=['Match_Data'])
        df_tienda['Nombre_Ref_Match'] = df_tienda['Match_Data'].apply(lambda x: x[0])
        df_tienda['Similitud %'] = df_tienda['Match_Data'].apply(lambda x: x[1])
        df_tienda = df_tienda[df_tienda['Similitud %'] >= 80]

        df_final = df_tienda.merge(df_ref, left_on='Nombre_Ref_Match', right_on=col_ref_nombre)
        df_final['Diferencia €'] = (df_final['Precio_Referencia'] - df_final['Precio_Tienda']).round(2)
        df_final['MayorPrecio'] = df_final['Diferencia €'].apply(
            lambda x: "Tienda Local" if x < 0 else ("Referencia/Kaggle" if x > 0 else "Mismo Precio")
        )
        
        columnas_finales = {'Nombre_Tienda': 'Producto', 'Precio_Tienda': 'Precio Tienda', 
                            'Precio_Referencia': 'Precio Referencia', 'Similitud %': 'Similitud %', 
                            'Diferencia €': 'Diferencia €', 'MayorPrecio': 'MayorPrecio'}
        
        if 'componente' in df_final.columns: columnas_finales['componente'] = 'Categoría'
        
        df_vista = df_final[list(columnas_finales.keys())].rename(columns=columnas_finales)
        df_vista['Fecha'] = fecha_diaria
        df_vista.to_csv(os.path.join(base_output_path, f"{nombre_salida}_{fecha_diaria}.csv"), index=False, encoding='utf-8-sig')
        print(f"Guardado Kaggle: {nombre_salida}")
    except Exception as e: print(f"Error Kaggle {nombre_salida}: {e}")

def realizar_comparativa_tiendas(path_tienda_a, path_tienda_b, nombre_salida, etiqueta_a, etiqueta_b):
    if not os.path.exists(path_tienda_a):
        print(f"Falta archivo: {path_tienda_a}")
        return
    if not os.path.exists(path_tienda_b):
        print(f"Falta archivo: {path_tienda_b}")
        return
        
    try:
        df_a = pd.read_csv(path_tienda_a)
        df_b = pd.read_csv(path_tienda_b)
        nombres_ref = df_b['Nombre'].tolist()

        df_a['Match'] = df_a['Nombre'].apply(
            lambda x: process.extractOne(x, nombres_ref, scorer=fuzz.token_set_ratio) if pd.notna(x) else None
        )
        df_a['Nombre_Ref'] = df_a['Match'].apply(lambda x: x[0] if x else None)
        df_a['Similitud'] = df_a['Match'].apply(lambda x: x[1] if x else 0)
        df_a['Marca_Ok'] = df_a.apply(
            lambda row: str(row['Nombre']).split()[0].upper() in str(row['Nombre_Ref']).upper() 
            if row['Nombre_Ref'] else False, axis=1
        )

        df_res = df_a[(df_a['Similitud'] >= 85) & (df_a['Marca_Ok'])].copy()
        
        if df_res.empty:
            print(f"Sin coincidencias para {nombre_salida}")
            return

        df_b_mini = df_b[['Nombre', 'Precio']].rename(columns={'Nombre': 'Nombre_Ref', 'Precio': 'Precio_Ref'})
        df_final = df_res.merge(df_b_mini, on='Nombre_Ref')
        
        df_final['Diferencia'] = (df_final['Precio'] - df_final['Precio_Ref']).round(2)
        df_final['MayorPrecio'] = df_final['Diferencia'].apply(
            lambda x: etiqueta_a if x > 0 else (etiqueta_b if x < 0 else "Igual")
        )
        
        df_vis = df_final[['Nombre', 'Precio', 'Precio_Ref', 'Similitud', 'Diferencia', 'MayorPrecio']].copy()
        df_vis.columns = ['Producto', f'Precio {etiqueta_a}', f'Precio {etiqueta_b}', 'Similitud (%)', 'Diferencia (€)', 'MayorPrecio']
        df_vis['Fecha'] = fecha_diaria
        
        df_vis.to_csv(os.path.join(base_output_path, f"{nombre_salida}_{fecha_diaria}.csv"), index=False, encoding='utf-8-sig')
        print(f"Guardado Tiendas: {nombre_salida}")
    except Exception as e: print(f"Error Tiendas {nombre_salida}: {e}")

# --- KAGGLE ---
realizar_comparativa_kaggle(f'smart/smartphones_PcBox_{fecha_diaria}.csv', 'dt_kaggle/2025_All_mobiles_Dataset.csv', 'comp_smart_PcBox_Kaggle')
realizar_comparativa_kaggle(f'comp/componentes_PcComp_{fecha_diaria}.csv', 'dt_kaggle/prices_components.csv', 'comp_componentes_PcComp_Kaggle')

# --- TIENDA VS TIENDA ---
realizar_comparativa_tiendas(f'port/portátiles_Coolmod_{fecha_diaria}.csv', f'port/portátiles_PcComp_{fecha_diaria}.csv', 'comp_port_PcComp_Coolmod', 'Coolmod', 'PcComponentes')
realizar_comparativa_tiendas(f'smart/smartphones_PcBox_{fecha_diaria}.csv', f'smart/smartphones_PcComp_{fecha_diaria}.csv', 'comp_smart_PcComp_PcBox', 'PcBox', 'PcComponentes')
