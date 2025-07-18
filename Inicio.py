import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Prueba Técnica - David",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header principal
st.title("🧪 Prueba Técnica - Diseño Experimental")
st.markdown("---")

# Saludo personalizado
st.header("¡Hola Angélica! 👋")

st.markdown("""
### Bienvenida a la prueba técnica de David

La idea de esta prueba es que puedas evaluar mis competencias en los siguientes componentes:

""")

# Crear columnas para mostrar las competencias
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 📊 **Análisis Estadístico**
    - Análisis exploratorio de datos
    - Verificación de supuestos estadísticos
    - Interpretación de resultados
    - Transformaciones de datos
    
    #### 🧪 **Diseño de Experimentos**
    - Diseño de Bloques Completos Aleatorizados (RCBD)
    - Análisis de varianza (ANOVA)
    """)

with col2:
    st.markdown("""
    #### 💻 **Buenas Prácticas de Desarrollo de Software**
    - Código modular y reutilizable
    - Estructura de proyecto organizada
    - Control de versiones con GIT
    
    #### 📈 **Análisis de Negocio**
    - Interpretación práctica de resultados
    - Recomendaciones accionables
    - Comunicación efectiva de hallazgos
    - Toma de decisiones basada en datos
    """)

st.markdown("---")

# Información del proyecto
st.subheader("📋 Sobre este Proyecto")

st.markdown("""
Este proyecto analiza el efecto de una **intervención experimental** sobre la variable **HTLS** utilizando:

- **Factor de bloqueo:** Management (diferentes gerencias)
- **Tratamientos:** Grupo Test vs Control  
- **Metodología:** Comparación entre Diseño Completamente Aleatorizado y RCBD

**Objetivos principales:**
1. Evaluar el efecto de la intervención controlando por gerencias
2. Demostrar la eficiencia del bloqueo vs análisis independientes
3. Proporcionar recomendaciones de negocio basadas en evidencia estadística
""")

st.markdown("---")

# Navegación
st.subheader("🧭 Navegación")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 📊 **Análisis Técnico**
    - **Calidad de Datos:** Verificaciones de integridad
    - **Análisis Exploratorio:** Distribuciones y transformaciones
    - **Análisis RCBD:** Modelo de bloques completos
    - **Comparación de Modelos:** Eficiencia del bloqueo
    """)

with col2:
    st.markdown("""
    #### 💼 **Insights de Negocio**
    - **Resultados Principales:** Efectos de la intervención
    - **Análisis por Gerencia:** Resultados específicos
    - **Recomendaciones:** Acciones sugeridas
    - **Impacto:** Cuantificación de beneficios
    """)

# Instrucciones de uso
st.info("""
💡 **Instrucciones:** Utiliza el menú lateral para navegar entre las diferentes secciones. 
Cada sección está diseñada para mostrar un aspecto específico de las competencias evaluadas.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Desarrollado por David </strong></p>
    <p> | 💼 LinkedIn: <a href="https://www.linkedin.com/in/david-rodriguez-data-scientist/" target="_blank">david-rodriguez-data-scientist</a></p>
    <p>🚀 Prueba Técnica | 17 de Julio de 2025</p>
</div>
""", unsafe_allow_html=True)