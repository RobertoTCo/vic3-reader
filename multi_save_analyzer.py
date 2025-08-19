"""
Multi-Save Analyzer
Recorre todos los saves de una carpeta y extrae métricas para análisis temporal
Estructura resultante: Filas=Años, Columnas=Tags, Hojas=Variables
"""

from pathlib import Path
from typing import Dict, List
import pandas as pd
from utils import read_file, save_as_json  # Reutilizar del main.py
from orchestrator import Orchestrator      # Reutilizar del main.py
from metrics import TAGS                   # Reutilizar del main.py
from main import manage_parsing            # Importar función existente de main.py


def extract_year_from_data(data: Dict) -> str:
    """Extraer año de los datos parseados - reutilizando lógica"""
    try:
        if 'date' in data:
            date_str = data['date']
            if isinstance(date_str, str) and '.' in date_str:
                year = date_str.split('.')[0]
                return year
    except Exception as e:
        print(f"Error extracting year: {e}")
    return "unknown"


def get_country_tag_mapping(data: Dict) -> Dict[str, str]:
    """
    Extraer mapeo ID -> TAG de 3 letras desde country_manager.country_database
    """
    tag_mapping = {}
    try:
        if 'country_manager' in data and 'country_database' in data['country_manager']:
            country_db = data['country_manager']['country_database']
            for country_id, country_info in country_db.items():
                if isinstance(country_info, dict) and 'definition' in country_info:
                    tag = country_info['definition']
                    tag_mapping[str(country_id)] = tag
            print(f"  📍 Mapeo de tags extraído: {len(tag_mapping)} países")
    except Exception as e:
        print(f"Error extrayendo mapeo: {e}")
    return tag_mapping


def process_single_save(save_path: Path) -> Dict[str, pd.DataFrame]:
    """
    Procesa un save reutilizando exactamente el flujo de main.py
    """
    print(f"📁 Procesando: {save_path.name}")
    
    try:
        # 1. Reutilizar lectura y parsing igual que main.py
        extension, text = read_file(save_path)
        data = manage_parsing(extension, text)
        
        if extension != '.json':
            save_as_json(save_path, data)  # cache igual que main.py
        
        # 2. Extraer año de los datos
        year = extract_year_from_data(data)
        if year == "unknown":
            # Fallback: usar nombre de archivo
            import re
            match = re.search(r'\b(\d{4})\b', save_path.name)
            if match:
                year = match.group(1)
            else:
                year = save_path.stem
        
        print(f"  📅 Año detectado: {year}")
        
        # 3. Extraer mapeo de tags (ID -> TAG de 3 letras)
        tag_mapping = get_country_tag_mapping(data)
        
        # 4. Reutilizar Orchestrator exactamente igual que main.py
        orchestrator = Orchestrator(
            data=data,
            wanted_tags=TAGS
        )
        
        # 5. Obtener DataFrame usando el orchestrator existente
        df = orchestrator.to_dataframe()
        print(f"  📊 DataFrame: {df.shape} - Columnas: {list(df.columns)}")
        
        # 6. Restructurar datos: cada métrica como DataFrame separado
        metrics_data = {}
        
        # Determinar estructura del DataFrame (si tiene columna 'tag' o tags en índice)
        if 'tag' in df.columns:
            # Formato: cada fila es un país, columna 'tag' + métricas
            for metric_col in df.columns:
                if metric_col != 'tag':
                    # Crear DataFrame: filas=años, columnas=tags (IDs por ahora)
                    metric_series = pd.Series(
                        df[metric_col].values, 
                        index=df['tag'].values, 
                        name=year
                    )
                    metric_df = pd.DataFrame([metric_series])
                    metrics_data[metric_col] = metric_df
        
        else:
            # Si tags están en el índice o estructura diferente
            print(f"  ⚠️  Estructura de DataFrame diferente, adaptando...")
            # Usar todas las columnas como métricas
            for metric_col in df.columns:
                metric_series = pd.Series(
                    df[metric_col].values, 
                    index=df.index, 
                    name=year
                )
                metric_df = pd.DataFrame([metric_series])
                metrics_data[metric_col] = metric_df
        
        print(f"  ✅ Extraídas {len(metrics_data)} métricas para el año {year}")
        return metrics_data
        
    except Exception as e:
        print(f"❌ Error procesando {save_path.name}: {e}")
        import traceback
        traceback.print_exc()
        return {}


def analyze_saves_directory(saves_dir: str = "saves") -> Dict[str, pd.DataFrame]:
    """
    Analiza todos los saves usando el flujo reutilizado de main.py
    """
    saves_path = Path(saves_dir)
    
    if not saves_path.exists():
        print(f"❌ Directorio {saves_dir} no encontrado")
        return {}
    
    # Buscar archivos JSON primero (más rápidos)
    json_saves_path = saves_path / "json_saves"
    json_files = []
    if json_saves_path.exists():
        json_files = list(json_saves_path.glob("*.json"))
        print(f"� Encontrados {len(json_files)} archivos JSON en json_saves/")
    
    # Luego archivos .v3 en directorio principal
    save_files = list(saves_path.glob("*.v3"))
    
    all_files = json_files + save_files
    
    if not all_files:
        print(f"❌ No se encontraron archivos de save en {saves_dir}")
        return {}
    
    print(f"📁 Total: {len(all_files)} archivos ({len(json_files)} JSON + {len(save_files)} V3)")
    
    # Consolidar métricas de todos los saves
    consolidated_metrics = {}
    # Guardar mapeos de tags por año (para usar el último de cada año)
    year_tag_mappings = {}
    
    for i, save_file in enumerate(all_files, 1):
        print(f"\n🔄 [{i}/{len(all_files)}] Procesando...")
        save_metrics = process_single_save(save_file)
        
        # Extraer año y mapeo de tags para este save
        try:
            extension, text = read_file(save_file)
            data = manage_parsing(extension, text)
            year = extract_year_from_data(data)
            tag_mapping = get_country_tag_mapping(data)
            
            # Usar mapeo más reciente por año
            if tag_mapping:
                year_tag_mappings[year] = tag_mapping
                print(f"  🏷️ Mapeo de tags guardado para año {year}: {len(tag_mapping)} países")
        except Exception as e:
            print(f"    ⚠️ Error extrayendo mapeo para {save_file.name}: {e}")
        
        # Consolidar cada métrica
        for metric_name, metric_df in save_metrics.items():
            if metric_name not in consolidated_metrics:
                consolidated_metrics[metric_name] = metric_df
            else:
                # Añadir nueva fila (año) al DataFrame consolidado
                try:
                    consolidated_metrics[metric_name] = pd.concat([
                        consolidated_metrics[metric_name],
                        metric_df
                    ], axis=0)
                except Exception as e:
                    print(f"    ⚠️ Error consolidando {metric_name}: {e}")
    
    # Limpiar y ordenar DataFrames finales
    for metric_name in consolidated_metrics:
        df = consolidated_metrics[metric_name]
        # Remover años duplicados (mantener último)
        df = df[~df.index.duplicated(keep='last')]
        # Ordenar por año
        df = df.sort_index()
        consolidated_metrics[metric_name] = df
    
    # Aplicar mapeo de tags de 3 letras a las columnas usando el último mapeo de cada año
    print(f"\n🏷️ Aplicando mapeo de tags de 3 letras...")
    consolidated_metrics = apply_tag_mapping_to_metrics(consolidated_metrics, year_tag_mappings)
    
    return consolidated_metrics


def apply_tag_mapping_to_metrics(metrics_data: Dict[str, pd.DataFrame], year_tag_mappings: Dict[str, Dict[str, str]]) -> Dict[str, pd.DataFrame]:
    """
    Aplica el mapeo de tags de 3 letras a las columnas de los DataFrames
    Usa el mapeo del último save por año para manejar tags dinámicos
    """
    if not year_tag_mappings:
        print("⚠️ No hay mapeos de tags disponibles")
        return metrics_data
    
    # Obtener el mapeo más completo (último año con más países)
    best_mapping = {}
    for year, mapping in year_tag_mappings.items():
        if len(mapping) > len(best_mapping):
            best_mapping = mapping
    
    print(f"🏷️ Usando mapeo con {len(best_mapping)} países")
    
    updated_metrics = {}
    
    for metric_name, df in metrics_data.items():
        print(f"  📊 Aplicando mapeo a métrica: {metric_name}")
        
        # Crear diccionario de renombrado para las columnas
        rename_dict = {}
        renamed_count = 0
        
        for col in df.columns:
            # Intentar mapear usando el ID como string
            tag = best_mapping.get(str(col))
            if tag and tag != col:
                rename_dict[col] = tag
                renamed_count += 1
            # Si no encuentra mapeo, mantener el nombre original
        
        # Aplicar renombrado si hay cambios
        if rename_dict:
            df_renamed = df.rename(columns=rename_dict)
            updated_metrics[metric_name] = df_renamed
            print(f"    🏷️ Renombrados {renamed_count} países a tags de 3 letras")
        else:
            updated_metrics[metric_name] = df
            print(f"    ℹ️ No se aplicaron cambios")
    
    return updated_metrics


def save_to_excel(metrics_data: Dict[str, pd.DataFrame], output_file: str = "victoria3_metrics_analysis.xlsx"):
    """
    Guarda las métricas en un archivo Excel con múltiples hojas
    """
    if not metrics_data:
        print("❌ No hay datos para guardar")
        return
    
    try:
        print(f"💾 Guardando datos en {output_file}...")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for metric_name, df in metrics_data.items():
                # Clean sheet name (Excel limitations)
                sheet_name = metric_name.replace('/', '_')[:31]
                df.to_excel(writer, sheet_name=sheet_name)
                print(f"   ✅ Métrica '{metric_name}' → hoja '{sheet_name}'")
        
        print(f"🎉 Archivo Excel guardado: {output_file}")
        
    except Exception as e:
        print(f"❌ Error guardando Excel: {e}")


def print_summary(metrics_data: Dict[str, pd.DataFrame]):
    """Imprime resumen del análisis"""
    if not metrics_data:
        print("❌ No hay datos para mostrar")
        return
    
    print("\n" + "="*60)
    print("📊 RESUMEN DEL ANÁLISIS MULTI-SAVE")
    print("="*60)
    
    all_years = set()
    all_countries = set()
    
    for metric_name, df in metrics_data.items():
        years = list(df.index)
        countries = list(df.columns)
        all_years.update(years)
        all_countries.update(countries)
        
        print(f"\n📈 {metric_name}:")
        print(f"   Años: {len(years)} ({min(years)} - {max(years)})")
        print(f"   Países: {len(countries)}")
        print(f"   Dimensiones: {df.shape[0]} años × {df.shape[1]} países")
    
    print(f"\n🌍 Resumen global:")
    print(f"   Total años únicos: {len(all_years)}")
    print(f"   Total países únicos: {len(all_countries)}")
    print(f"   Métricas disponibles: {len(metrics_data)}")


def show_sample_data(metrics_data: Dict[str, pd.DataFrame]):
    """Muestra una muestra de los datos estructurados"""
    if not metrics_data:
        return
    
    print("\n" + "="*60)
    print("👀 MUESTRA DE DATOS ESTRUCTURADOS")
    print("="*60)
    
    # Show first metric as example
    sample_metric = list(metrics_data.keys())[0]
    df = metrics_data[sample_metric]
    
    print(f"\n📊 Métrica de ejemplo: {sample_metric}")
    print("   Estructura: Filas=Años, Columnas=Países (Tag IDs)")
    print("-" * 50)
    print(df.head())
    
    # Show evolution for one country
    if len(df.columns) > 0:
        sample_country = df.columns[0]
        print(f"\n📈 Evolución temporal para país '{sample_country}':")
        country_data = df[sample_country].dropna()
        for year, value in country_data.items():
            print(f"   {year}: {value:.2f}")


if __name__ == "__main__":
    print("🎮 Victoria 3 Multi-Save Analyzer")
    print("="*50)
    print("Reutilizando código de main.py y orchestrator.py")
    
    # Ejecutar análisis
    results = analyze_saves_directory()
    
    if results:
        print_summary(results)
        show_sample_data(results)
        save_to_excel(results)
        print("\n✨ ¡Análisis completado!")
    else:
        print("❌ No se procesaron archivos")
