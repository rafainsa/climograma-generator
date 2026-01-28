import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Generador de Climogramas", layout="centered")

st.title("📊 Generador de Climogramas Profesional")
st.write("Introduce los datos de tu ciudad para generar el gráfico y la clasificación climática.")

# 1. Entrada de nombre
ciudad = st.text_input("Nombre de la ciudad:", "Madrid")

# 2. Tabla de entrada de datos
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

st.subheader("🌡️ Temperaturas y 🌧️ Precipitaciones")
col1, col2 = st.columns(2)

temps = []
precs = []

with col1:
    st.write("**Temperaturas (°C)**")
    for i in range(6):
        temps.append(st.number_input(f"Temp {meses[i]}", value=10.0, step=0.1))
with col2:
    st.write("**Temperaturas (°C)**")
    for i in range(6, 12):
        temps.append(st.number_input(f"Temp {meses[i]}", value=10.0, step=0.1))

st.divider()
col3, col4 = st.columns(2)

with col3:
    st.write("**Precipitaciones (mm)**")
    for i in range(6):
        precs.append(st.number_input(f"Prec {meses[i]}", value=50.0, step=1.0))
with col4:
    st.write("**Precipitaciones (mm)**")
    for i in range(6, 12):
        precs.append(st.number_input(f"Prec {meses[i]}", value=50.0, step=1.0))

# Lógica de clasificación (Köppen y Martonne)
def clasificar_todo(temps, precs):
    tm = sum(temps)/12
    pt = sum(precs)
    tmax, tmin = max(temps), min(temps)
    # Martonne
    martonne = pt / (tm + 10)
    # Köppen Simplificado
    grupo = "C" if tmin > -3 else "D"
    if pt < 20 * tm: grupo = "B"
    return martonne, grupo

if st.button("Generar Climograma"):
    idx_m, kop = clasificar_todo(temps, precs)
    
    fig, ax1 = plt.subplots(figsize=(10, 8))
    ax2 = ax1.twinx()
    
    # Escalas P=2T
    lim_p = max(max(precs), max(temps)*2, 40)
    ax1.set_ylim(min(min(temps)*2, 0), lim_p + 10)
    ax2.set_ylim(min(min(temps), 0), (lim_p + 10)/2)
    
    x = np.arange(12)
    ax1.bar(x, precs, color='blue', alpha=0.7, width=1.0, edgecolor='white')
    ax2.plot(x, temps, color='red', marker='o', linewidth=2)
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(meses)
    ax1.set_ylabel("Precipitación (mm)", color="blue")
    ax2.set_ylabel("Temperatura (°C)", color="red")
    
    st.pyplot(fig)
    
    st.success(f"**Análisis:** Índice Martonne {idx_m:.1f} | Grupo Köppen: {kop}")
