import pandas as pd
import numpy as np
from typing import Dict, Tuple

def cargar_datos_test(ruta_archivo: str) -> pd.DataFrame:
    """Carga los datos de test desde archivo CSV"""
    return pd.read_csv(ruta_archivo)

def verificar_valores_faltantes(df: pd.DataFrame) -> Dict:
    """Verifica valores faltantes en el DataFrame"""
    faltantes = df.isnull().sum()
    total_celdas = df.size
    porcentaje_faltantes = (faltantes.sum() / total_celdas) * 100 if total_celdas > 0 else 0
    
    return {
        'faltantes_por_columna': faltantes,
        'total_faltantes': faltantes.sum(),
        'porcentaje': porcentaje_faltantes,
        'tiene_faltantes': faltantes.sum() > 0
    }

def verificar_duplicados(df: pd.DataFrame, columna_id: str) -> Dict:
    """Verifica duplicados en la columna ID especificada"""
    total_filas = len(df)
    ids_unicos = df[columna_id].nunique()
    cantidad_duplicados = total_filas - ids_unicos
    
    resultado = {
        'total_filas': total_filas,
        'ids_unicos': ids_unicos,
        'cantidad_duplicados': cantidad_duplicados,
        'tiene_duplicados': cantidad_duplicados > 0
    }
    
    if resultado['tiene_duplicados']:
        resultado['filas_duplicadas'] = df[df[columna_id].duplicated(keep=False)].sort_values(columna_id)
    
    return resultado

def obtener_tipos_datos(df: pd.DataFrame) -> pd.Series:
    """Obtiene los tipos de datos del DataFrame"""
    return df.dtypes

def obtener_resumen_categoricas(df: pd.DataFrame, columnas_categoricas: list) -> Dict:
    """Obtiene resumen de variables categóricas"""
    resumen = {}
    for col in columnas_categoricas:
        if col in df.columns:
            resumen[col] = sorted(df[col].unique())
    return resumen

def obtener_resumen_estadistico(df: pd.DataFrame, columna_numerica: str) -> Dict:
    """Genera resumen estadístico completo para una columna numérica"""
    serie = df[columna_numerica]
    estadisticas = serie.describe()
    
    # Estadísticas adicionales
    asimetria = serie.skew()
    curtosis = serie.kurtosis()
    cv = (estadisticas['std'] / estadisticas['mean']) * 100
    
    # Verificaciones especiales
    valores_negativos = (serie < 0).sum()
    valores_cero = (serie == 0).sum()
    riq = estadisticas['75%'] - estadisticas['25%']
    outliers_superiores = (serie > estadisticas['75%'] + 1.5 * riq).sum()
    
    # Percentiles extremos
    percentiles = [0.01, 0.05, 0.10, 0.90, 0.95, 0.99]
    percentiles_extremos = {f"{p*100:.1f}%": serie.quantile(p) for p in percentiles}
    
    return {
        'estadisticas_descriptivas': estadisticas,
        'asimetria': asimetria,
        'curtosis': curtosis,
        'cv_porcentaje': cv,
        'rango': estadisticas['max'] - estadisticas['min'],
        'riq': riq,
        'valores_negativos': valores_negativos,
        'valores_cero': valores_cero,
        'outliers_superiores': outliers_superiores,
        'percentiles_extremos': percentiles_extremos
    }