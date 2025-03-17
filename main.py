import streamlit as st
import numpy as np
import time
import plotly.graph_objects as go
import plotly.express as px

# Configuración de la página, logo y eslogan
st.set_page_config(
    page_title="QuimicAI - Química Inteligente",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Define custom CSS for the layout
st.html(
    """
    <style>
    /* Container for the entire header */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 20px;
        background-color: #ffffff;
        border-bottom: 1px solid #e6e6e6;
        position: -webkit-sticky; /* For Safari */
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    /* Logo styling */
    .logo {
        max-width: 150px;
        height: auto;
    }
    /* Header content styling */
    .header-content {
        flex-grow: 1;
        padding-left: 20px;
    }
    .header-title {
        margin: 0;
        font-size: 24px;
        color: #4CAF50;
    }
    .header-subtitle {
        margin: 5px 0 0;
        font-size: 16px;
        color: #555;
    }
    .header-description {
        margin: 10px 0 0;
        font-size: 14px;
        color: #777;
    }
    .divider {
        border-left: 2px solid gray;
        height: 5em;
        position: absolute;
        left: 50%;
        top: 0;
    }
    </style>
    """
)
# Define the columns with specified width ratios
col1, sep, col2 = st.columns([0.15, 0.05, 0.8])

# Column 1: Display the logo
with col1:
    st.image("static/logo.png", use_container_width =True)

# Column 2: Display the header content
with col2:
    st.markdown(
        """
        <h1 style='margin-bottom: 0;'>QuimicAI - <span style='color: #4CAF50;'>Química Inteligente</span></h1>
        <h3 style='color: #555; margin-top: 5px;'>Optimización inteligente de procesos complejos</h3>
        <p style='font-size: 1.1em; margin-bottom: 5em;'>
            Con <strong>QuimicAI</strong> reduces costes y acortas tiempos en ensayos experimentales mediante simulaciones continuas y precisas.<br>
            Descubre cómo optimizar reacciones, materiales y procesos biológicos con funciones continuas personalizadas.
        </p>
        """,
        unsafe_allow_html=True
    )



#############################
# Utilidades y funciones generales
#############################

def default_value(rng):
    """Retorna el promedio del rango."""
    return sum(rng)/2

def evaluate_metric_function(metric_func, parameters, selected_vars, range_inputs, n_points):
    """
    Evalúa la función métrica de forma continua.
    Si se varía 1 parámetro: retorna vectores (x, y).
    Si se varían 2 parámetros: retorna matrices (X, Y, Z).
    Los parámetros no seleccionados se fijan a su valor promedio.
    """
    fixed_values = {key: default_value(rng) for key, rng in parameters.items()}
    if len(selected_vars) == 1:
        var = selected_vars[0]
        low, high = range_inputs[var]
        x = np.linspace(low, high, n_points)
        y = []
        for val in x:
            args = {key: (val if key == var else fixed_values[key]) for key in parameters}
            y.append(metric_func(**args))
        return x, np.array(y)
    elif len(selected_vars) == 2:
        var1, var2 = selected_vars
        low1, high1 = range_inputs[var1]
        low2, high2 = range_inputs[var2]
        x = np.linspace(low1, high1, n_points)
        y = np.linspace(low2, high2, n_points)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for i in range(n_points):
            for j in range(n_points):
                args = {}
                for key in parameters:
                    if key == var1:
                        args[key] = X[i, j]
                    elif key == var2:
                        args[key] = Y[i, j]
                    else:
                        args[key] = fixed_values[key]
                Z[i, j] = metric_func(**args)
        return X, Y, Z

def plot_continuous_metric(selected_vars, range_inputs, n_points, metric_func, display_metric, display_names):
    """
    Genera la visualización interactiva de la función continua:
      - Curva suave en 2D (si se selecciona 1 variable).
      - Superficie en 3D (si se seleccionan 2 variables).
    """
    if len(selected_vars) == 1:
        x, y = evaluate_metric_function(metric_func, current_parameters, selected_vars, range_inputs, n_points)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Datos calculados'))
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Curva continua'))
        fig.update_layout(title=f"{display_metric} vs {display_names[selected_vars[0]]}",
                          xaxis_title=display_names[selected_vars[0]],
                          yaxis_title=display_metric)
        st.plotly_chart(fig, use_container_width=True)
    elif len(selected_vars) == 2:
        X, Y, Z = evaluate_metric_function(metric_func, current_parameters, selected_vars, range_inputs, n_points)
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
        fig.update_layout(title=f"{display_metric} en función de {display_names[selected_vars[0]]} y {display_names[selected_vars[1]]}",
                          scene=dict(
                              xaxis_title=display_names[selected_vars[0]],
                              yaxis_title=display_names[selected_vars[1]],
                              zaxis_title=display_metric))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Por favor, selecciona 1 o 2 variables para visualizar la función continua.")

def simulate_optimization(metric_func, parameters, range_inputs, selected_vars, n_points, exp_type):
    """Simula la optimización (código confidencial) y calcula métricas de ahorro."""
    with st.spinner("Optimizando parámetros..."):
        time.sleep(10)  # Simulación de proceso intensivo
    st.success("Optimización completada. (Código confidencial, no disponible)")
    # Evaluar la función en la malla y calcular el rango de la métrica
    if len(selected_vars) == 1:
        x, y = evaluate_metric_function(metric_func, parameters, selected_vars, range_inputs, n_points)
        value_range = y.max() - y.min()
    elif len(selected_vars) == 2:
        X, Y, Z = evaluate_metric_function(metric_func, parameters, selected_vars, range_inputs, n_points)
        value_range = Z.max() - Z.min()
    else:
        value_range = 0
    # Valores ficticios de ahorro (para demostración)
    if exp_type == 'chem':
        time_saved = "72 horas"
    elif exp_type == 'mat':
        time_saved = "48 horas"
    elif exp_type == 'bio':
        time_saved = "60 horas"
    money_saved = f"{value_range*0.001:.2f} €"  # Factor de escala arbitrario
    st.metric("Ahorro en dinero", money_saved, delta=f"-{money_saved} comparado con pruebas reales")
    st.metric("Ahorro en tiempo", time_saved)

#############################
# FUNCIONES CONTINUAS CON BASE GAUSSIANA
#############################

# --- Ejemplo: Reacción Química (Polimerización de Etileno) ---
chem_parameters = {
    "TiCl3": (0.05, 0.5),
    "Al_Ti": (3, 13),
    "Temp": (60, 110),
    "Presion": (1, 20)
}
chem_display_names = {
    "TiCl3": "Concentración de TiCl3 (mol/L)",
    "Al_Ti": "Relación Al/Ti (mol/mol)",
    "Temp": "Temperatura (°C)",
    "Presion": "Presión (atm)"
}
def chem_peso_molecular(TiCl3, Al_Ti, Temp, Presion):
    base = 2800000
    gain = 3100000
    # Parámetros óptimos y desviaciones estándar
    opt = {"TiCl3": 0.3, "Al_Ti": 9, "Temp": 90, "Presion": 10}
    sigma = {"TiCl3": 0.1, "Al_Ti": 1.5, "Temp": 10, "Presion": 3}
    term = ((TiCl3 - opt["TiCl3"])/sigma["TiCl3"])**2 + ((Al_Ti - opt["Al_Ti"])/sigma["Al_Ti"])**2 \
           + ((Temp - opt["Temp"])/sigma["Temp"])**2 + ((Presion - opt["Presion"])/sigma["Presion"])**2
    return base + gain * np.exp(-0.5*term)

def chem_rendimiento(TiCl3, Al_Ti, Temp, Presion):
    base = 60
    gain = 35
    opt = {"TiCl3": 0.3, "Al_Ti": 9, "Temp": 90, "Presion": 10}
    sigma = {"TiCl3": 0.1, "Al_Ti": 1.5, "Temp": 10, "Presion": 3}
    term = ((TiCl3 - opt["TiCl3"])/sigma["TiCl3"])**2 + ((Al_Ti - opt["Al_Ti"])/sigma["Al_Ti"])**2 \
           + ((Temp - opt["Temp"])/sigma["Temp"])**2 + ((Presion - opt["Presion"])/sigma["Presion"])**2
    return base + gain * np.exp(-0.5*term)

def chem_costo(TiCl3, Al_Ti, Temp, Presion):
    base = 5000
    reduction = 2000
    opt = {"TiCl3": 0.3, "Al_Ti": 9, "Temp": 90, "Presion": 10}
    sigma = {"TiCl3": 0.1, "Al_Ti": 1.5, "Temp": 10, "Presion": 3}
    term = ((TiCl3 - opt["TiCl3"])/sigma["TiCl3"])**2 + ((Al_Ti - opt["Al_Ti"])/sigma["Al_Ti"])**2 \
           + ((Temp - opt["Temp"])/sigma["Temp"])**2 + ((Presion - opt["Presion"])/sigma["Presion"])**2
    return base - reduction * np.exp(-0.5*term)

chem_metric_functions = {
    "Peso molecular (g/mol)": chem_peso_molecular,
    "Rendimiento (%)": chem_rendimiento,
    "Costo (€)": chem_costo
}

# --- Ejemplo: Ingeniería de Materiales (Superaleaciones de Níquel) ---
material_parameters = {
    "Ni": (60, 78),
    "Cr": (10, 16),
    "Temp": (1100, 1200),
    "Tiempo": (2, 8)
}
material_display_names = {
    "Ni": "Porcentaje de Ni (%)",
    "Cr": "Porcentaje de Cr (%)",
    "Temp": "Temperatura de Solubilización (°C)",
    "Tiempo": "Tiempo de Envejecimiento (h)"
}
def material_resistencia(Ni, Cr, Temp, Tiempo):
    base = 550
    gain = 250
    opt = {"Ni": 72, "Cr": 13, "Temp": 1150, "Tiempo": 5}
    sigma = {"Ni": 3, "Cr": 2, "Temp": 25, "Tiempo": 1.5}
    term = ((Ni - opt["Ni"])/sigma["Ni"])**2 + ((Cr - opt["Cr"])/sigma["Cr"])**2 \
           + ((Temp - opt["Temp"])/sigma["Temp"])**2 + ((Tiempo - opt["Tiempo"])/sigma["Tiempo"])**2
    return base + gain * np.exp(-0.5*term)

def material_ductilidad(Ni, Cr, Temp, Tiempo):
    base = 15
    gain = 5
    opt = {"Ni": 68, "Cr": 12, "Temp": 1130, "Tiempo": 4}
    sigma = {"Ni": 4, "Cr": 2, "Temp": 30, "Tiempo": 1.5}
    term = ((Ni - opt["Ni"])/sigma["Ni"])**2 + ((Cr - opt["Cr"])/sigma["Cr"])**2 \
           + ((Temp - opt["Temp"])/sigma["Temp"])**2 + ((Tiempo - opt["Tiempo"])/sigma["Tiempo"])**2
    return base + gain * np.exp(-0.5*term)

def material_costo(Ni, Cr, Temp, Tiempo):
    base = 10000
    reduction = 3000
    opt = {"Ni": 72, "Cr": 13, "Temp": 1150, "Tiempo": 5}
    sigma = {"Ni": 3, "Cr": 2, "Temp": 25, "Tiempo": 1.5}
    term = ((Ni - opt["Ni"])/sigma["Ni"])**2 + ((Cr - opt["Cr"])/sigma["Cr"])**2 \
           + ((Temp - opt["Temp"])/sigma["Temp"])**2 + ((Tiempo - opt["Tiempo"])/sigma["Tiempo"])**2
    return base - reduction * np.exp(-0.5*term)

material_metric_functions = {
    "Resistencia a Fluencia (MPa)": material_resistencia,
    "Ductilidad (%)": material_ductilidad,
    "Costo (€)": material_costo
}

# --- Ejemplo: Materiales Biológicos (Producción de Anticuerpos Monoclonales) ---
bio_parameters = {
    "Glucosa": (2, 10),
    "pH": (6.8, 7.4),
    "Agitacion": (100, 250),
    "Estrategia": (0, 1)  # Se trata como continua: 0 = batch, 1 = perfusión
}
bio_display_names = {
    "Glucosa": "Concentración de Glucosa (g/L)",
    "pH": "pH",
    "Agitacion": "Velocidad de Agitación (rpm)",
    "Estrategia": "Estrategia de Alimentación (0=batch, 1=perfusión)"
}
def bio_productividad(Glucosa, pH, Agitacion, Estrategia):
    base = 1.0
    gain = 2.0
    opt = {"Glucosa": 6, "pH": 7.1, "Agitacion": 200, "Estrategia": 1}
    sigma = {"Glucosa": 1.5, "pH": 0.2, "Agitacion": 30, "Estrategia": 0.1}
    term = ((Glucosa - opt["Glucosa"])/sigma["Glucosa"])**2 + ((pH - opt["pH"])/sigma["pH"])**2 \
           + ((Agitacion - opt["Agitacion"])/sigma["Agitacion"])**2 + ((Estrategia - opt["Estrategia"])/sigma["Estrategia"])**2
    return base + gain * np.exp(-0.5*term)

def bio_calidad(Glucosa, pH, Agitacion, Estrategia):
    base = 90
    gain = 10
    opt = {"Glucosa": 6, "pH": 7.1, "Agitacion": 200, "Estrategia": 1}
    sigma = {"Glucosa": 1.5, "pH": 0.2, "Agitacion": 30, "Estrategia": 0.1}
    term = ((Glucosa - opt["Glucosa"])/sigma["Glucosa"])**2 + ((pH - opt["pH"])/sigma["pH"])**2 \
           + ((Agitacion - opt["Agitacion"])/sigma["Agitacion"])**2 + ((Estrategia - opt["Estrategia"])/sigma["Estrategia"])**2
    return base + gain * np.exp(-0.5*term)

def bio_costo(Glucosa, pH, Agitacion, Estrategia):
    base = 7500
    reduction = 1500
    opt = {"Glucosa": 6, "pH": 7.1, "Agitacion": 200, "Estrategia": 1}
    sigma = {"Glucosa": 1.5, "pH": 0.2, "Agitacion": 30, "Estrategia": 0.1}
    term = ((Glucosa - opt["Glucosa"])/sigma["Glucosa"])**2 + ((pH - opt["pH"])/sigma["pH"])**2 \
           + ((Agitacion - opt["Agitacion"])/sigma["Agitacion"])**2 + ((Estrategia - opt["Estrategia"])/sigma["Estrategia"])**2
    return base - reduction * np.exp(-0.5*term)

bio_metric_functions = {
    "Productividad (g/L)": bio_productividad,
    "Calidad (% mAb funcional)": bio_calidad,
    "Costo (€)": bio_costo
}

#############################
# Mapas para mostrar opciones en la interfaz
#############################
chem_display_to_key = {v: k for k, v in chem_display_names.items()}
material_display_to_key = {v: k for k, v in material_display_names.items()}
bio_display_to_key = {v: k for k, v in bio_display_names.items()}

#############################
# Widget personalizado para las pestañas de experimentos
#############################
def render_experiment_tab(exp_type, title, description, parameters, display_names, metric_functions, mapping):
    st.header(title)
    st.markdown(description)
    
    # Selección de variables a variar (mostrando nombres en español)
    display_options = list(mapping.keys())
    selected_display_vars = st.multiselect("Selecciona 1 o 2 variables de entrada", 
                                             display_options, 
                                             default=display_options[:1],
                                             key=f"{exp_type}_multiselect")
    selected_vars = [mapping[name] for name in selected_display_vars]
    
    # Selección de la métrica a optimizar
    metric_option = st.selectbox("Selecciona la métrica a optimizar", 
                                 list(metric_functions.keys()),
                                 key=f"{exp_type}_selectbox")
    global current_parameters
    current_parameters = parameters
    global display_names_global
    display_names_global = display_names  # para usar en la función de plot
    metric_func = metric_functions[metric_option]
    
    # Definir el rango de los parámetros a explorar
    range_inputs = {}
    st.markdown("#### Define el rango de los parámetros a explorar:")
    for var in selected_vars:
        allowed_range = parameters[var]
        range_val = st.slider(f"Rango para {display_names[var]}",
                              min_value=float(allowed_range[0]),
                              max_value=float(allowed_range[1]),
                              step=float(allowed_range[1]-allowed_range[0])/100,
                              value=(float(allowed_range[0]), float(allowed_range[1])),
                              key=f"{exp_type}_range_{var}")
        range_inputs[var] = range_val
    n_points = st.slider("Número de puntos en la malla", 1, 100, 50, key=f"{exp_type}_points")
    
    if st.button("Optimizar Parámetros", key=f"{exp_type}_button"):
        simulate_optimization(metric_func, parameters, range_inputs, selected_vars, n_points, exp_type)
    
    st.subheader("Visualización de la función continua")
    if selected_vars:
        plot_continuous_metric(selected_vars, range_inputs, n_points, metric_func, metric_option, display_names)
    else:
        st.warning("Por favor, selecciona al menos una variable de entrada.")

#############################
# Interfaz: pestañas para cada ejemplo y contacto
#############################
tabs = st.tabs(["Reacción Química", "Ingeniería de Materiales", "Materiales Biológicos", "Contacto"])

# --- Pestaña 1: Reacción Química ---
with tabs[0]:
    render_experiment_tab(
        exp_type="chem",
        title="Ejemplo: Polimerización de Etileno (PE-UHMW)",
        description="""
La polimerización de etileno mediante catalizadores Ziegler-Natta es un proceso crítico en la industria petroquímica.  
Optimiza parámetros como la concentración de TiCl₃, relación Al/Ti, temperatura y presión para maximizar el peso molecular, el rendimiento o minimizar costos.
        """,
        parameters=chem_parameters,
        display_names=chem_display_names,
        metric_functions=chem_metric_functions,
        mapping=chem_display_to_key
    )

# --- Pestaña 2: Ingeniería de Materiales ---
with tabs[1]:
    render_experiment_tab(
        exp_type="mat",
        title="Ejemplo: Superaleaciones de Níquel",
        description="""
En la fabricación de componentes para turbinas de gas, la composición y el tratamiento térmico de superaleaciones de níquel determinan su resistencia y ductilidad.  
Optimiza el porcentaje de Ni, Cr, la temperatura de solubilización y el tiempo de envejecimiento para mejorar la resistencia o reducir costos.
        """,
        parameters=material_parameters,
        display_names=material_display_names,
        metric_functions=material_metric_functions,
        mapping=material_display_to_key
    )

# --- Pestaña 3: Materiales Biológicos ---
with tabs[2]:
    render_experiment_tab(
        exp_type="bio",
        title="Ejemplo: Producción de Anticuerpos Monoclonales",
        description="""
En la producción a gran escala de anticuerpos monoclonales, optimizar parámetros como la concentración de glucosa, pH, velocidad de agitación y estrategia de alimentación es clave para mejorar la productividad y calidad, reduciendo costos y residuos.
        """,
        parameters=bio_parameters,
        display_names=bio_display_names,
        metric_functions=bio_metric_functions,
        mapping=bio_display_to_key
    )

# --- Pestaña 4: Contacto ---
with tabs[3]:
    st.header("Contacto")
    st.markdown("""
¿Quieres optimizar tus procesos y reducir costes con inteligencia artificial?  
Déjanos tus datos y cuéntanos tus necesidades. Nuestro equipo de expertos en QuimicAI se pondrá en contacto contigo lo antes posible para ofrecerte una solución personalizada.
    """)
    with st.form("contact_form"):
        name = st.text_input("Nombre", key="contact_name")
        email = st.text_input("Correo Electrónico", key="contact_email")
        message = st.text_area("Mensaje", key="contact_message")
        submit = st.form_submit_button("Enviar")
        if submit:
            # Aquí se implementaría el envío de correo a quimicai.sevilla@gmail.com (no implementado por confidencialidad)
            st.success("¡Gracias por contactarnos! Nos pondremos en contacto contigo pronto.")

# SEO: etiquetas meta para mejorar el posicionamiento
st.markdown(
    """
    <meta name="description" content="QuimicAI - Química Inteligente optimiza reacciones químicas, ingeniería de materiales y producción de anticuerpos con IA, ahorrando tiempo y dinero en procesos complejos.">
    <meta name="keywords" content="QuimicAI, Optimización, Química, Ingeniería de Materiales, Anticuerpos, IA">
    """, unsafe_allow_html=True
)
