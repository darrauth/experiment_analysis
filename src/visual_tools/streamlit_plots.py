import streamlit as st
import pandas as pd
from typing import Dict
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from typing import Dict


def mostrar_resumen_valores_faltantes(info_faltantes: Dict):
    """Muestra resumen de valores faltantes en Streamlit"""
    if info_faltantes['tiene_faltantes']:
        st.error(f"🚨 Valores faltantes encontrados: {info_faltantes['total_faltantes']} ({info_faltantes['porcentaje']:.2f}%)")
        st.write("**Valores faltantes por columna:**")
        st.write(info_faltantes['faltantes_por_columna'])
    else:
        st.success("✅ No hay valores faltantes en los datos")

def mostrar_resumen_duplicados(info_duplicados: Dict, columna_id: str):
    """Muestra resumen de duplicados en Streamlit"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total filas", info_duplicados['total_filas'])
    with col2:
        st.metric(f"{columna_id} únicos", info_duplicados['ids_unicos'])
    with col3:
        st.metric("Duplicados", info_duplicados['cantidad_duplicados'])
    
    if info_duplicados['tiene_duplicados']:
        st.error(f"🚨 {info_duplicados['cantidad_duplicados']} duplicados encontrados")
        st.write("**Filas duplicadas:**")
        st.dataframe(info_duplicados['filas_duplicadas'])
    else:
        st.success(f"✅ No hay duplicados en {columna_id}")

def mostrar_resumen_estadistico(info_estadisticas: Dict, nombre_columna: str):
    """Muestra resumen estadístico en Streamlit"""
    st.subheader(f"📊 Resumen Estadístico - {nombre_columna.upper()}")
    
    # Estadísticas descriptivas
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Estadísticas Descriptivas:**")
        df_estadisticas = pd.DataFrame({
            'Estadística': ['Conteo', 'Media', 'Desv. Std', 'Mínimo', '25%', '50%', '75%', 'Máximo'],
            'Valor': [
                f"{info_estadisticas['estadisticas_descriptivas']['count']:,.0f}",
                f"{info_estadisticas['estadisticas_descriptivas']['mean']:,.2f}",
                f"{info_estadisticas['estadisticas_descriptivas']['std']:,.2f}",
                f"{info_estadisticas['estadisticas_descriptivas']['min']:,.2f}",
                f"{info_estadisticas['estadisticas_descriptivas']['25%']:,.2f}",
                f"{info_estadisticas['estadisticas_descriptivas']['50%']:,.2f}",
                f"{info_estadisticas['estadisticas_descriptivas']['75%']:,.2f}",
                f"{info_estadisticas['estadisticas_descriptivas']['max']:,.2f}"
            ]
        })
        st.dataframe(df_estadisticas, hide_index=True)
    
    with col2:
        st.write("**Estadísticas Adicionales:**")
        df_adicionales = pd.DataFrame({
            'Estadística': ['Asimetría', 'Curtosis', 'Rango', 'RIQ', 'CV (%)'],
            'Valor': [
                f"{info_estadisticas['asimetria']:.3f}",
                f"{info_estadisticas['curtosis']:.3f}",
                f"{info_estadisticas['rango']:,.2f}",
                f"{info_estadisticas['riq']:,.2f}",
                f"{info_estadisticas['cv_porcentaje']:.1f}%"
            ]
        })
        st.dataframe(df_adicionales, hide_index=True)
    
    # Verificaciones especiales
    st.write("**Verificaciones Especiales:**")
    col_verif1, col_verif2, col_verif3 = st.columns(3)
    with col_verif1:
        st.metric("Valores negativos", info_estadisticas['valores_negativos'])
    with col_verif2:
        st.metric("Valores cero", info_estadisticas['valores_cero'])
    with col_verif3:
        st.metric("Outliers (Q3+1.5*RIQ)", info_estadisticas['outliers_superiores'])
    
    # Percentiles extremos
    st.write("**Percentiles Extremos:**")
    df_percentiles = pd.DataFrame({
        'Percentil': list(info_estadisticas['percentiles_extremos'].keys()),
        'Valor': [f"{v:,.2f}" for v in info_estadisticas['percentiles_extremos'].values()]
    })
    st.dataframe(df_percentiles, hide_index=True)

def mostrar_resumen_categoricas(info_categoricas: Dict):
    """Muestra resumen de variables categóricas en Streamlit"""
    st.write("**Variables Categóricas:**")
    for columna, valores in info_categoricas.items():
        st.write(f"- **{columna}:** {valores}")

#############################################################################################################


def crear_graficos_antes_despues(df: pd.DataFrame, columna_original: str, columna_transformada: str):
    """Crea gráficos comparativos antes y después de la transformación"""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # FILA 1: Datos Originales
    # Histograma original
    axes[0,0].hist(df[columna_original], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0,0].set_title('Histograma - Datos Originales', fontweight='bold')
    axes[0,0].set_xlabel(columna_original)
    axes[0,0].grid(True, alpha=0.3)
    
    # Q-Q plot original
    stats.probplot(df[columna_original], dist="norm", plot=axes[0,1])
    axes[0,1].set_title('Q-Q Plot - Datos Originales')
    axes[0,1].grid(True, alpha=0.3)
    
    # Boxplot original por grupo
    if 'group' in df.columns:
        sns.boxplot(data=df, x='group', y=columna_original, ax=axes[0,2])
        axes[0,2].set_title('Boxplot por Grupo - Originales')
        axes[0,2].grid(True, alpha=0.3)
    
    # FILA 2: Datos Transformados
    # Histograma transformado
    axes[1,0].hist(df[columna_transformada], bins=30, alpha=0.7, color='lightcoral', edgecolor='black')
    axes[1,0].set_title('Histograma - Datos Transformados (log)', fontweight='bold')
    axes[1,0].set_xlabel(columna_transformada)
    axes[1,0].grid(True, alpha=0.3)
    
    # Q-Q plot transformado
    stats.probplot(df[columna_transformada], dist="norm", plot=axes[1,1])
    axes[1,1].set_title('Q-Q Plot - Datos Transformados (log)')
    axes[1,1].grid(True, alpha=0.3)
    
    # Boxplot transformado por grupo
    if 'group' in df.columns:
        sns.boxplot(data=df, x='group', y=columna_transformada, ax=axes[1,2])
        axes[1,2].set_title('Boxplot por Grupo - Transformados (log)')
        axes[1,2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def mostrar_comparacion_estadisticas_simple(estadisticas: Dict):
    """Muestra comparación simple de estadísticas antes y después"""
    
    st.subheader("📊 Comparación Estadística: Antes vs Después")
    
    # Crear DataFrame comparativo
    df_comparacion = pd.DataFrame({
        'Estadística': ['Media', 'Desv. Estándar', 'Asimetría', 'Curtosis', 'Mínimo', 'Máximo'],
        'Datos Originales': [
            f"{estadisticas['original']['media']:.2f}",
            f"{estadisticas['original']['std']:.2f}",
            f"{estadisticas['original']['asimetria']:.3f}",
            f"{estadisticas['original']['curtosis']:.3f}",
            f"{estadisticas['original']['min']:.2f}",
            f"{estadisticas['original']['max']:.2f}"
        ],
        'Datos Transformados (log)': [
            f"{estadisticas['transformado']['media']:.3f}",
            f"{estadisticas['transformado']['std']:.3f}",
            f"{estadisticas['transformado']['asimetria']:.3f}",
            f"{estadisticas['transformado']['curtosis']:.3f}",
            f"{estadisticas['transformado']['min']:.3f}",
            f"{estadisticas['transformado']['max']:.3f}"
        ]
    })
    
    st.dataframe(df_comparacion, hide_index=True)
    
    # Métricas clave
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mejora_asimetria = abs(estadisticas['original']['asimetria']) - abs(estadisticas['transformado']['asimetria'])
        st.metric(
            "Mejora en Asimetría", 
            f"{mejora_asimetria:.2f}",
            delta=f"{mejora_asimetria:.2f}"
        )
    
    with col2:
        asimetria_original = abs(estadisticas['original']['asimetria'])
        st.metric(
            "Asimetría Original", 
            f"{asimetria_original:.2f}",
            delta=None
        )
    
    with col3:
        asimetria_transformada = abs(estadisticas['transformado']['asimetria'])
        st.metric(
            "Asimetría Transformada", 
            f"{asimetria_transformada:.2f}",
            delta=None
        )




def crear_boxplots_categoricas(df: pd.DataFrame, variable_respuesta: str, variables_categoricas: list):
    """Crea boxplots de la variable respuesta vs cada variable categórica"""
    
    n_vars = len(variables_categoricas)
    fig, axes = plt.subplots(1, n_vars, figsize=(8*n_vars, 6))
    
    # Si solo hay una variable, axes no es una lista
    if n_vars == 1:
        axes = [axes]
    
    for i, var_cat in enumerate(variables_categoricas):
        sns.boxplot(data=df, x=var_cat, y=variable_respuesta, ax=axes[i])
        axes[i].set_title(f'{variable_respuesta.upper()} por {var_cat.title()}', fontweight='bold', fontsize=14)
        axes[i].set_xlabel(var_cat.title(), fontsize=12)
        axes[i].set_ylabel(variable_respuesta.upper(), fontsize=12)
        axes[i].grid(True, alpha=0.3)
        
        # Agregar número de observaciones por grupo
        for j, grupo in enumerate(df[var_cat].unique()):
            n_obs = len(df[df[var_cat] == grupo])
            axes[i].text(j, axes[i].get_ylim()[0], f'n={n_obs}', 
                        ha='center', va='top', fontsize=10, 
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    return fig