import streamlit as st
import math
import pandas as pd

# Configuracion de la pagina
st.set_page_config(layout="wide")

# Función de evaluación matemática segura
def f(expr, x):
    env = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    env['x'] = x
    clean_expr = expr.replace('^', '**')
    return eval(clean_expr, {"__builtins__": {}}, env)

# Panel de entrada y presentacion
st.title("Calculadora de Integración Numérica (Método del Trapecio)")
st.write("Introduce la función matemática f(x), los límites de integración y el número de intervalos para calcular la aproximación del área bajo la curva.")

# Formularios de captura de datos (Con claves estructurales)
expr = st.text_input("Función matemática f(x):", value="x**2", key="func_trapecio")

col1, col2, col3 = st.columns(3)
with col1:
    a = st.number_input("Límite inferior (a):", value=0.0, format="%.4f", key="lim_a")
with col2:
    b = st.number_input("Límite superior (b):", value=1.0, format="%.4f", key="lim_b")
with col3:
    n = st.number_input("Intervalos (n):", value=10, min_value=1, max_value=10000, step=1, key="int_n")

# Ejecucion del proceso de calculo
if st.button("Ejecutar Cálculos"):
    try:
        h = (b - a) / n
        val_x = []
        val_fx = []
        val_abs = []

        # Algoritmo del Trapecio con captura de errores de dominio
        for i in range(int(n) + 1):
            xi = a + i * h
            try:
                fxi = float(f(expr, xi))
            except Exception:
                st.error(f"Error de evaluación en x = {xi:.4f}. El valor se encuentra fuera del dominio matemático de la función introducida.")
                st.stop()
            
            val_x.append(xi)
            val_fx.append(fxi)
            val_abs.append(abs(fxi))

        sigma_i = val_fx[0] + 2 * sum(val_fx[1:-1]) + val_fx[-1]
        sigma_a = val_abs[0] + 2 * sum(val_abs[1:-1]) + val_abs[-1]

        integral = (h / 2) * sigma_i
        area = (h / 2) * sigma_a

        # Despliegue de resultados en formato tabular usando Pandas
        st.markdown(f"### Tabla de Puntos Generados (h = {h:.4f})")
        df_datos = pd.DataFrame({
            "Iteración (i)": list(range(int(n) + 1)),
            "Punto (x)": val_x,
            "Evaluación f(x)": val_fx,
            "Valor Absoluto |f(x)|": val_abs
        })
        # Formateo de columnas a 4 decimales
        st.dataframe(df_datos.style.format({
            "Punto (x)": "{:.4f}",
            "Evaluación f(x)": "{:.4f}",
            "Valor Absoluto |f(x)|": "{:.4f}"
        }), use_container_width=True)

        # Resumen de métricas finales
        st.markdown("### Resultados Finales")
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="Sumatoria de la Integral (Σ I)", value=f"{sigma_i:.4f}")
            st.metric(label="Integral Definida Estimada", value=f"{integral:.4f}")
        with c2:
            st.metric(label="Sumatoria del Área (Σ A)", value=f"{sigma_a:.4f}")
            st.metric(label="Área Total Calculada", value=f"{area:.4f}")

        st.markdown("---")
        # Boton para reiniciar la aplicacion (Consistencia estricta)
        if st.button("Volver a empezar", key="reset_trapecio"):
            st.session_state.clear()
            st.rerun()

    # Intercepción de errores generales de sintaxis algebraica
    except Exception as e:
        st.error(f"Error en el análisis de la expresión o en el cálculo. Compruebe la sintaxis de la función. Detalle técnico: {e}")
