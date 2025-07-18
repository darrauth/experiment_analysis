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
from etl_data.transformaciones import aplicar_transformacion_log, obtener_estadisticas_comparativas
from visual_tools.streamlit_plots import (
    mostrar_resumen_valores_faltantes, mostrar_resumen_duplicados,
    mostrar_resumen_estadistico, mostrar_resumen_categoricas,
    crear_graficos_antes_despues, mostrar_comparacion_estadisticas_simple,
    crear_boxplots_categoricas
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
    
    # Crear tabs
    tab1, tab2, tab3 = st.tabs(["Datos Originales", "Transformación Logarítmica", "Análisis Gráfico"])
    
    with tab1:
        # Análisis estadístico de HTLS original
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
    
    with tab2:
        st.subheader("🔄 Transformación Logarítmica")
        
        # Aplicar transformación
        with st.spinner("Aplicando transformación logarítmica..."):
            df_transformado = aplicar_transformacion_log(df_test, 'htls')
            estadisticas_comparativas = obtener_estadisticas_comparativas(df_transformado, 'htls', 'htls_log')
        
        st.success("✅ Transformación logarítmica aplicada exitosamente")
        
        # Mostrar gráficos comparativos
        st.subheader("📊 Comparación Visual: Antes vs Después")
        fig_comparacion = crear_graficos_antes_despues(df_transformado, 'htls', 'htls_log')
        st.pyplot(fig_comparacion)
        
        # Mostrar estadísticas comparativas
        mostrar_comparacion_estadisticas_simple(estadisticas_comparativas)
        
        # Conclusión
        st.markdown("---")
        st.subheader("✅ Resultado de la Transformación")
        
        mejora_asimetria = abs(estadisticas_comparativas['original']['asimetria']) - abs(estadisticas_comparativas['transformado']['asimetria'])
        
        if mejora_asimetria > 10:
            st.success("🎉 **Excelente mejora** en la distribución")
        elif mejora_asimetria > 5:
            st.success("👍 **Buena mejora** en la distribución")
        else:
            st.info("📊 **Mejora moderada** en la distribución")
        
        st.markdown(f"""
        ### 📋 Conclusión de Transformación
        
        La transformación logarítmica mejora significativamente la distribución de HTLS:
        - **Asimetría reducida** de {estadisticas_comparativas['original']['asimetria']:.2f} a {estadisticas_comparativas['transformado']['asimetria']:.2f}
        - **Distribución más simétrica** para análisis ANOVA
        - **Todas las observaciones preservadas**
        
        **Decisión Final:** Utilizar log(HTLS) para todos los análisis estadísticos posteriores.
        """)
    
    with tab3:
        st.subheader("📊 Análisis Gráfico por Variables Categóricas")
        
        # Crear selectbox para elegir qué datos usar
        tipo_datos = st.selectbox(
            "Selecciona los datos a visualizar:",
            ["Datos Originales (HTLS)", "Datos Transformados (log-HTLS)"],
            index=1
        )
        
        if tipo_datos == "Datos Originales (HTLS)":
            variable_respuesta = 'htls'
            df_analisis = df_test
        else:
            # Aplicar transformación si no existe
            if 'htls_log' not in df_test.columns:
                df_analisis = aplicar_transformacion_log(df_test, 'htls')
            else:
                df_analisis = df_test
            variable_respuesta = 'htls_log'
        
        # Crear boxplots
        st.write("**Distribución de la variable respuesta por categorías:**")
        variables_categoricas = ['group', 'management']
        
        fig_boxplots = crear_boxplots_categoricas(df_analisis, variable_respuesta, variables_categoricas)
        st.pyplot(fig_boxplots)
        
        # Mostrar estadísticas básicas por grupo
        st.subheader("📋 Estadísticas Descriptivas por Grupo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Por Tratamiento (Group):**")
            stats_group = df_analisis.groupby('group')[variable_respuesta].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(3)
            st.dataframe(stats_group)
        
        with col2:
            st.write("**Por Bloque (Management):**")
            stats_management = df_analisis.groupby('management')[variable_respuesta].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(3)
            st.dataframe(stats_management)
        
        # Interpretación rápida
        st.markdown("---")
        st.subheader("💡 Interpretación Visual")
        
        # Análisis automático básico
        media_test = df_analisis[df_analisis['group'] == 'Test'][variable_respuesta].mean()
        media_control = df_analisis[df_analisis['group'] == 'Control'][variable_respuesta].mean()
        diferencia = media_test - media_control
        
  
        
        st.info(f"""
        **Observación inicial:** El grupo Test muestra una media ligeramente mayor que el de Control 
        (diferencia: {diferencia:.3f}).
        
        **Variabilidad entre bloques (Management):** Se observan diferencias entre gerencias, 
        lo que justifica el uso del diseño de bloques para controlar esta fuente de variación.
        
        **Próximo paso:** Análisis ANOVA formal para determinar significancia estadística.
        """)

elif seccion_analisis == "Análisis RCBD":
    st.header("🧪 Análisis RCBD")
    st.info("Sección en desarrollo...")

elif seccion_analisis == "Comparación de Modelos":
    st.header("⚖️ Comparación de Modelos")
    st.info("Sección en desarrollo...")