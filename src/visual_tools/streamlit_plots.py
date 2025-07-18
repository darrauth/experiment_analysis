import streamlit as st
import pandas as pd
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