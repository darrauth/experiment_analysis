import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Agregar directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from etl_data.eda import (
    cargar_datos_test, verificar_valores_faltantes, verificar_duplicados, 
    obtener_tipos_datos, obtener_resumen_categoricas, obtener_resumen_estadistico
)
from visual_tools.streamlit_plots import (
    mostrar_resumen_valores_faltantes, mostrar_resumen_duplicados,
    mostrar_resumen_estadistico, mostrar_resumen_categoricas
)

# Configuración de la página
st.set_page_config(page_title="Análisis Técnico", page_icon="📊", layout="wide")

st.title("📊 Análisis Técnico - Diseño Experimental")
st.markdown("---")

# Sidebar para navegación
st.sidebar.title("Navegación")
seccion_analisis = st.sidebar.selectbox(
    "Seleccionar sección:",
    ["Calidad de Datos", "Análisis Exploratorio", "Análisis RCBD", "Comparación de Modelos"]
)

# =======================================
# SECCIÓN: CALIDAD DE DATOS
# =======================================

if seccion_analisis == "Calidad de Datos":
    st.header("🔍 Verificación de Calidad de Datos")
    
    # Cargar datos
    try:
        df_test = cargar_datos_test('data/raw/test.csv')
        st.success(f"✅ Datos cargados exitosamente: {df_test.shape[0]:,} filas, {df_test.shape[1]} columnas")
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        st.stop()
    
    # Crear tabs para organizar el análisis
    tab1, tab2, tab3, tab4 = st.tabs(["Valores Faltantes", "Duplicados", "Tipos de Datos", "Variables Categóricas"])
    
    with tab1:
        st.subheader("📋 Verificación de Valores Faltantes")
        info_faltantes = verificar_valores_faltantes(df_test)
        mostrar_resumen_valores_faltantes(info_faltantes)
    
    with tab2:
        st.subheader("🔄 Verificación de Duplicados")
        info_duplicados = verificar_duplicados(df_test, 'client_id')
        mostrar_resumen_duplicados(info_duplicados, 'client_id')
    
    with tab3:
        st.subheader("📝 Tipos de Datos")
        tipos_datos = obtener_tipos_datos(df_test)
        st.dataframe(pd.DataFrame({'Columna': tipos_datos.index, 'Tipo': tipos_datos.values}), hide_index=True)
    
    with tab4:
        st.subheader("🏷️ Variables Categóricas")
        info_categoricas = obtener_resumen_categoricas(df_test, ['management', 'group'])
        mostrar_resumen_categoricas(info_categoricas)

# =======================================
# SECCIÓN: ANÁLISIS EXPLORATORIO
# =======================================

elif seccion_analisis == "Análisis Exploratorio":
    st.header("📈 Análisis Exploratorio de Datos")
    
    # Cargar datos
    try:
        df_test = cargar_datos_test('data/raw/test.csv')
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        st.stop()
    
    # Análisis estadístico de HTLS
    info_estadisticas = obtener_resumen_estadistico(df_test, 'htls')
    mostrar_resumen_estadistico(info_estadisticas, 'htls')
    
    # Resumen de hallazgos
    st.markdown("---")
    st.subheader("📋 Resumen de Hallazgos")
    
    # Crear alerta basada en asimetría
    if abs(info_estadisticas['asimetria']) > 2:
        tipo_alerta = "error"
        icono_alerta = "🚨"
        texto_alerta = "CRÍTICO"
    elif abs(info_estadisticas['asimetria']) > 1:
        tipo_alerta = "warning"
        icono_alerta = "⚠️"
        texto_alerta = "MODERADO"
    else:
        tipo_alerta = "success"
        icono_alerta = "✅"
        texto_alerta = "ACEPTABLE"
    
    if tipo_alerta == "error":
        st.error(f"{icono_alerta} **Problemas de distribución {texto_alerta}**")
    elif tipo_alerta == "warning":
        st.warning(f"{icono_alerta} **Problemas de distribución {texto_alerta}**")
    else:
        st.success(f"{icono_alerta} **Distribución {texto_alerta}**")
    
    st.markdown("""
    ### Resumen de Hallazgos
    
    La variable HTLS presenta una distribución extremadamente asimétrica (asimetría = 16.2) con alta variabilidad (CV = 229.7%) y 921 outliers, violando severamente los supuestos de normalidad y homoscedasticidad requeridos para ANOVA. La ausencia de valores negativos o cero permite implementar transformación logarítmica como estrategia correctiva obligatoria. 
    
    **Decisión:** Proceder con log(HTLS) para el análisis, validando posteriormente los supuestos mediante pruebas de normalidad y homoscedasticidad, con métodos no paramétricos como contingencia si persisten las violaciones.
    """)

elif seccion_analisis == "Análisis RCBD":
    st.header("🧪 Análisis RCBD")
    st.info("Sección en desarrollo...")

elif seccion_analisis == "Comparación de Modelos":
    st.header("⚖️ Comparación de Modelos")
    st.info("Sección en desarrollo...")



