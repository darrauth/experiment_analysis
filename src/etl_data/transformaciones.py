import pandas as pd
import numpy as np
from typing import Dict

def aplicar_transformacion_log(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """Aplica transformación logarítmica a una columna específica"""
    df_transformado = df.copy()
    df_transformado[f'{columna}_log'] = np.log(df[columna])
    return df_transformado

def obtener_estadisticas_comparativas(df: pd.DataFrame, columna_original: str, columna_transformada: str) -> Dict:
    """Compara estadísticas básicas entre datos originales y transformados"""
    
    original = df[columna_original]
    transformado = df[columna_transformada]
    
    return {
        'original': {
            'media': original.mean(),
            'std': original.std(),
            'asimetria': original.skew(),
            'curtosis': original.kurtosis(),
            'min': original.min(),
            'max': original.max()
        },
        'transformado': {
            'media': transformado.mean(),
            'std': transformado.std(),
            'asimetria': transformado.skew(),
            'curtosis': transformado.kurtosis(),
            'min': transformado.min(),
            'max': transformado.max()
        }
    }