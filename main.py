import streamlit as st
import pandas as pd
import json
import time
import numpy as np
import os
import plotly.graph_objects as go
import plotly.express as px
from scipy.interpolate import griddata

# Set page configuration with SEO-friendly title and layout
st.set_page_config(
    page_title="QuimicAI - Química Inteligente",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Functions to load external markdown and JSON files (or use default content)
def load_md(filename, default_text):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return default_text

def load_json(filename, default_data):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return default_data

# Load advanced markdown texts for each example
chem_md_text = load_md("chem_reaction.md", 
"""
## Reacción Química Avanzada: Polimerización de Etileno (PE-UHMW)

La **polimerización de etileno con catalizadores de Ziegler-Natta** es uno de los procesos más importantes de la industria petroquímica.  
En este método, el **etileno** (C₂H₄) reacciona en presencia de **tri-etil-aluminio (TEA)** como co-catalizador y un catalizador Ziegler-Natta basado en **TiCl₃**. La cadena polimérica crece mediante la adición sucesiva de monómeros en el centro metálico activo.

Las propiedades del polímero resultante, especialmente el peso molecular, dependen de:

- Concentración de TiCl₃ (mol/L)
- Relación Al/Ti (mol/mol)
- Temperatura de reacción (°C)
- Presión de etileno (atm)

**QuimicAI** optimiza virtualmente estos parámetros, permitiendo aumentar el peso molecular, mejorar el rendimiento y reducir costos.  
Además, se reduce la generación de residuos químicos y se ahorran **horas y miles de euros** en experimentos.
""")

material_md_text = load_md("material_engineering.md", 
"""
## Ingeniería de Materiales Avanzada: Superaleaciones de Níquel

Para la **fabricación de componentes en turbinas de gas**, se utilizan superaleaciones de base níquel que resisten altas temperaturas y mantienen resistencia mecánica.  
La microestructura depende de:

- Porcentaje de Ni y Cr
- Temperatura de solubilización (°C)
- Tiempo de envejecimiento (h)

El **endurecimiento por precipitación** es clave para la resistencia a la fluencia y la durabilidad de las piezas.  
**QuimicAI** permite simular tratamientos térmicos y composiciones, reduciendo la necesidad de prototipos físicos, y ahorrando tiempo y dinero, a la vez que minimiza residuos.
""")

bio_md_text = load_md("biologic_materials.md", 
"""
## Materiales Biológicos Avanzados: Producción de Anticuerpos Monoclonales

En la industria farmacéutica, la **producción de anticuerpos monoclonales (mAbs)** se realiza en biorreactores con células CHO.  
Las variables críticas incluyen:

- Concentración de glucosa (g/L)
- pH
- Velocidad de agitación (rpm)
- Estrategia de alimentación (0=batch, 1=perfusión)

Estos factores influyen en la densidad celular, productividad y calidad del anticuerpo.  
**QuimicAI** optimiza el proceso, permitiendo escalar la producción de forma más rápida y económica, reduciendo tanto el costo como los residuos biológicos.
""")

# Load advanced JSON data for each example
chem_data = load_json("chem_data.json", {
    "variables": {
        "Concentración de TiCl3 (mol/L)": [0.05, 0.1, 0.2, 0.3, 0.4, 0.5],
        "Relación Al/Ti (mol/mol)": [3, 5, 7, 9, 11, 13],
        "Temperatura (°C)": [60, 70, 80, 90, 100, 110],
        "Presión (atm)": [1, 3, 5, 10, 15, 20]
    },
    "metrics": {
        "Peso molecular (g/mol)": [2800000, 3300000, 3800000, 4400000, 5100000, 5900000],
        "Rendimiento (%)": [60, 70, 80, 85, 90, 95],
        "Costo (€)": [3000, 3200, 3600, 4000, 4500, 5000]
    }
})

material_data = load_json("material_data.json", {
    "variables": {
        "Porcentaje de Ni (%)": [60, 65, 70, 72, 75, 78],
        "Porcentaje de Cr (%)": [10, 12, 13, 14, 15, 16],
        "Temperatura de Solubilización (°C)": [1100, 1120, 1140, 1150, 1170, 1200],
        "Tiempo de Envejecimiento (h)": [2, 3, 4, 5, 6, 8]
    },
    "metrics": {
        "Resistencia a Fluencia (MPa)": [550, 600, 650, 700, 750, 800],
        "Ductilidad (%)": [20, 19, 18, 17, 16, 15],
        "Costo (€)": [7000, 7500, 8000, 9000, 9500, 10000]
    }
})

bio_data = load_json("bio_data.json", {
    "variables": {
        "Concentración de Glucosa (g/L)": [2, 4, 6, 5, 8, 10],
        "pH": [6.8, 7.0, 7.2, 7.0, 7.2, 7.4],
        "Velocidad de Agitación (rpm)": [100, 150, 200, 180, 220, 250],
        "Estrategia de Alimentación (0=batch, 1=perfusión)": [0, 0, 0, 1, 1, 1]
    },
    "metrics": {
        "Productividad (g/L)": [1.0, 1.5, 2.0, 2.2, 2.8, 3.2],
        "Calidad (% mAb funcional)": [90, 92, 93, 95, 96, 97],
        "Costo (€)": [5000, 5500, 6000, 6500, 7000, 7500]
    }
})

# Function to simulate optimization and display saving metrics
def simulate_optimization(data, exp_type):
    with st.spinner("Optimizando parámetros..."):
        time.sleep(10)  # Simulate time-consuming optimization
    st.success("Optimización completada. (Código confidencial, no disponible)")
    # Calculate money saved as difference between maximum and minimum cost
    cost_values = np.array(data["metrics"]["Costo (€)"])
    money_saved = cost_values.max() - cost_values.min()
    # Define a fixed time saving for demonstration
    if exp_type == 'chem':
        time_saved = "48 horas"
    elif exp_type == 'mat':
        time_saved = "24 horas"
    elif exp_type == 'bio':
        time_saved = "36 horas"
    st.metric("Ahorro en dinero (€)", f"{money_saved:.2f} €", delta=f"-{money_saved:.2f} € comparado con pruebas reales")
    st.metric("Ahorro en tiempo", time_saved)

# Function to plot smooth 2D curve or 3D surface using interpolation
def plot_data_smooth(selected_vars, output_var, data):
    if len(selected_vars) == 1:
        # 2D plot: smooth curve via polynomial fitting
        x = np.array(data["variables"][selected_vars[0]])
        y = np.array(data["metrics"][output_var])
        # Ensure data is sorted for interpolation
        sorted_indices = np.argsort(x)
        x = x[sorted_indices]
        y = y[sorted_indices]
        x_new = np.linspace(x.min(), x.max(), 300)
        degree = min(3, len(x)-1)
        coeffs = np.polyfit(x, y, degree)
        poly_func = np.poly1d(coeffs)
        y_new = poly_func(x_new)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Datos originales'))
        fig.add_trace(go.Scatter(x=x_new, y=y_new, mode='lines', name='Curva suave'))
        fig.update_layout(title=f"{output_var} vs {selected_vars[0]}",
                          xaxis_title=selected_vars[0],
                          yaxis_title=output_var)
        st.plotly_chart(fig, use_container_width=True)
    elif len(selected_vars) == 2:
        # 3D surface: smooth surface via griddata interpolation
        x_arr = np.array(data["variables"][selected_vars[0]])
        y_arr = np.array(data["variables"][selected_vars[1]])
        metric_values = np.array(data["metrics"][output_var])
        # Assume each index corresponds to a paired experiment
        points = np.array(list(zip(x_arr, y_arr)))
        grid_x, grid_y = np.mgrid[x_arr.min():x_arr.max():50j, y_arr.min():y_arr.max():50j]
        grid_z = griddata(points, metric_values, (grid_x, grid_y), method='cubic')
        fig = go.Figure(data=[go.Surface(x=grid_x, y=grid_y, z=grid_z, colorscale='Viridis')])
        fig.update_layout(title=f"{output_var} en función de {selected_vars[0]} y {selected_vars[1]}",
                          scene=dict(
                              xaxis_title=selected_vars[0],
                              yaxis_title=selected_vars[1],
                              zaxis_title=output_var))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Por favor, selecciona 1 o 2 variables de entrada para visualizar la curva o superficie.")

# Main title and introduction
st.title("QuimicAI: Optimización de Procesos Químicos, Materiales y Biológicos con IA")
st.markdown("""
### Ahorro de tiempo y dinero en simulaciones de procesos complejos  
Con QuimicAI se reducen los costos y el tiempo invertido en experimentos costosos.  
Nuestro sistema simula procesos reales, ahorrando **horas de experimentación** y reduciendo el uso de materiales caros,  
lo que conlleva a una **disminución de residuos** y a una producción más limpia y sostenible.
""")

# Create tabs for the three examples and a contact section
tabs = st.tabs(["Reacción Química", "Ingeniería de Materiales", "Materiales Biológicos", "Contacto"])

# --------- Tab 1: Reacción Química ---------
with tabs[0]:
    st.header("Ejemplo: Polimerización de Etileno (PE-UHMW)")
    st.markdown(chem_md_text)
    
    st.subheader("Parámetros y Métricas")
    col1, col2 = st.columns(2)
    with col1:
        st.json(chem_data)
    with col2:
        selected_vars = st.multiselect("Selecciona 1 o 2 variables de entrada", 
                                       list(chem_data["variables"].keys()), 
                                       default=list(chem_data["variables"].keys())[:1],
                                       key="chem_multiselect")
        output_var = st.selectbox("Selecciona la métrica a maximizar", 
                                  list(chem_data["metrics"].keys()),
                                  key="chem_selectbox")
        importance_coef = st.slider("Coeficiente de importancia (peso de rendimiento vs costo)", 
                                    0.0, 1.0, 0.5, key="chem_slider")
    
    if st.button("Optimizar Parámetros", key="chem_button"):
        simulate_optimization(chem_data, 'chem')
    
    st.subheader("Visualización de Resultados")
    if selected_vars:
        plot_data_smooth(selected_vars, output_var, chem_data)
    else:
        st.warning("Por favor, selecciona al menos una variable de entrada.")

# --------- Tab 2: Ingeniería de Materiales ---------
with tabs[1]:
    st.header("Ejemplo: Superaleaciones de Níquel")
    st.markdown(material_md_text)
    
    st.subheader("Parámetros y Métricas")
    col1, col2 = st.columns(2)
    with col1:
        st.json(material_data)
    with col2:
        selected_vars = st.multiselect("Selecciona 1 o 2 variables de entrada", 
                                       list(material_data["variables"].keys()), 
                                       default=list(material_data["variables"].keys())[:1],
                                       key="mat_multiselect")
        output_var = st.selectbox("Selecciona la métrica a maximizar", 
                                  list(material_data["metrics"].keys()),
                                  key="mat_selectbox")
        importance_coef = st.slider("Coeficiente de importancia (peso de resistencia vs costo)", 
                                    0.0, 1.0, 0.5, key="mat_slider")
    
    if st.button("Optimizar Parámetros", key="mat_button"):
        simulate_optimization(material_data, 'mat')
    
    st.subheader("Visualización de Resultados")
    if selected_vars:
        plot_data_smooth(selected_vars, output_var, material_data)
    else:
        st.warning("Por favor, selecciona al menos una variable de entrada.")

# --------- Tab 3: Materiales Biológicos ---------
with tabs[2]:
    st.header("Ejemplo: Producción de Anticuerpos Monoclonales")
    st.markdown(bio_md_text)
    
    st.subheader("Parámetros y Métricas")
    col1, col2 = st.columns(2)
    with col1:
        st.json(bio_data)
    with col2:
        selected_vars = st.multiselect("Selecciona 1 o 2 variables de entrada", 
                                       list(bio_data["variables"].keys()), 
                                       default=list(bio_data["variables"].keys())[:1],
                                       key="bio_multiselect")
        output_var = st.selectbox("Selecciona la métrica a maximizar", 
                                  list(bio_data["metrics"].keys()),
                                  key="bio_selectbox")
        importance_coef = st.slider("Coeficiente de importancia (peso de productividad vs costo)", 
                                    0.0, 1.0, 0.5, key="bio_slider")
    
    if st.button("Optimizar Parámetros", key="bio_button"):
        simulate_optimization(bio_data, 'bio')
    
    st.subheader("Visualización de Resultados")
    if selected_vars:
        plot_data_smooth(selected_vars, output_var, bio_data)
    else:
        st.warning("Por favor, selecciona al menos una variable de entrada.")

# --------- Tab 4: Contacto ---------
with tabs[3]:
    st.header("Contacto")
    st.markdown("""¿Quieres optimizar tus procesos y reducir costes con inteligencia artificial?\n
Déjanos tus datos y cuéntanos tus necesidades. Nuestro equipo de expertos en QuimicAI se pondrá en contacto contigo a la mayor brevedad para ofrecerte una solución personalizada.""")
    
    with st.form("contact_form"):
        name = st.text_input("Nombre", key="contact_name")
        email = st.text_input("Correo Electrónico", key="contact_email")
        message = st.text_area("Mensaje", key="contact_message")
        submit = st.form_submit_button("Enviar")
        if submit:
            # Simulate sending an email to quimicai.sevilla@gmail.com (not implemented for confidentiality)
            st.success("¡Gracias por contactarnos! Nos pondremos en contacto contigo pronto.")

# SEO meta tags (injected into the page header)
st.markdown(
    """
    <meta name="description" content="QuimicAI optimiza reacciones químicas, ingeniería de materiales y producción de anticuerpos con inteligencia artificial, ahorrando tiempo y dinero en experimentos.">
    <meta name="keywords" content="QuimicAI, Optimización, Reacciones Químicas, Ingeniería de Materiales, Anticuerpos, IA">
    """, unsafe_allow_html=True
)
