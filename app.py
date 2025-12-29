import streamlit as st
import pandas as pd
from PIL import Image
from core import calcular_media, calcular_proporcion


# CONFIGURACIÓN INICIAL DE LA PÁGINA
# Define las propiedades generales de la aplicación Streamlit:
# - Título y icono que aparecen en la pestaña del navegador
# - Layout "wide" para aprovechar más ancho de pantalla
# - Sidebar colapsado por defecto para más espacio central
st.set_page_config(
    page_title="Calculadora de Tamaño de Muestra",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ESTILOS CSS PERSONALIZADOS
# Define un tema oscuro y moderno con variables CSS reutilizables.
# Incluye:
# - Paleta de colores: fondos oscuros, bordes sutiles, texto claro
# - Gradientes de fondo con efecto visual moderno
# - Componentes estilizados: tarjetas (cards), pills, métricas
# - Oculta elementos por defecto de Streamlit (menú, footer, header)
CSS = """
<style>
:root{
  --bg1:#0b1020; --bg2:#0f172a;
  --card: rgba(255,255,255,0.06);
  --stroke: rgba(255,255,255,0.12);
  --text: rgba(255,255,255,0.92);
  --muted: rgba(255,255,255,0.72);
  --shadow: 0 18px 55px rgba(0,0,0,0.45);
}

.stApp{
  background:
    radial-gradient(
      1200px 700px at 15% 10%,
      rgba(30, 64, 175, 0.35),
      transparent 55%
    ),
    radial-gradient(
      1000px 650px at 85% 20%,
      rgba(15, 23, 42, 0.45),
      transparent 60%
    ),
    linear-gradient(
      180deg,
      #020617 0%,
      #020617 15%,
      #020617 30%,
      #020617 45%,
      #020617 60%,
      #020617 75%,
      #020617 90%,
      #020617 100%
    );
  color: var(--text);
}

.block-container{
  padding-top: 3.2rem;
  padding-bottom: 2.2rem;
  max-width: 1150px;
}

h1,h2,h3,h4{ color: var(--text) !important; }
.small-muted{ color: var(--muted); font-size: 0.92rem; }

.pill{
  display:inline-flex; align-items:center; gap:8px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--stroke);
  background: rgba(255,255,255,0.05);
  color: var(--muted);
  font-size: 0.85rem;
  white-space: nowrap;
}

.metric{
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 16px;
  min-height: 160px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.formula-box{
  min-height: 160px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}

.formula-label{
  text-align: left;
  margin-bottom: 8px;
}

.latex-wrap{
  width: 100%;
  text-align: center;
}

.formula-box .katex-display{
  margin: 0 !important;
}

.metric .label{ color: var(--muted); font-size: 0.86rem; }
.metric .value{ font-size: 1.55rem; font-weight: 700; letter-spacing: .2px; }

.hr-soft{
  height: 1px;
  background: rgba(255,255,255,0.10);
  border: none;
  margin: 14px 0;
}

[data-baseweb="input"] input,
[data-baseweb="select"] div,
[data-baseweb="textarea"] textarea{
  border-radius: 14px !important;
}

.stTabs [data-baseweb="tab"]{ font-weight: 650; color: rgba(255,255,255,0.75); }
.stTabs [aria-selected="true"]{ color: white !important; }

[data-testid="stVerticalBlockBorderWrapper"]{
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 16px !important;
  box-shadow: none !important;
}

[data-testid="stVerticalBlockBorderWrapper"] > div{
  padding: 16px !important;
  min-height: 160px !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
}

[data-testid="stVerticalBlockBorderWrapper"] .katex-display{
  margin: 0 !important;
  text-align: center !important;
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# FUNCIONES AUXILIARES DE UTILIDAD

def format_big(n_str: str, max_len: int = 28) -> str:
    """
    Formatea números muy grandes truncándolos de forma legible.
    Si el número excede max_len caracteres, muestra inicio + "…" + final.
    Evita que números gigantescos desordenen la interfaz.
    """
    s = n_str.strip()
    if len(s) <= max_len:
        return s
    return f"{s[:14]}…{s[-10:]}"


def result_card(title: str, z: float, n_crudo_str: str, n_final: int, formula: str, supuestos: list[str]):
    """
    Construye y renderiza la tarjeta de resultados.
    
    Esta función organiza la presentación visual de los cálculos en una tarjeta que incluye:
    - Título y descripción del cálculo realizado
    - Badge con el valor Z crítico obtenido
    - Tres columnas con métricas: n redondeado, n crudo, y fórmula LaTeX
    - Separador visual (línea horizontal)
    - Listado de supuestos estadísticos necesarios
    
    Parámetros:
      title: Texto principal de la tarjeta
      z: Valor Z crítico calculado
      n_crudo_str: Tamaño de muestra sin redondear (como string para precisión)
      n_final: Tamaño de muestra redondeado hacia arriba (entero)
      formula: Fórmula en LaTeX para renderizar
      supuestos: Lista de supuestos estadísticos a mostrar
    """
    with st.container(border=True):
        # Encabezado: título, descripción y badge con Z crítico
        st.markdown(
            f"""
            <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:12px;">
              <div>
                <div style="font-size:2.0rem; font-weight:800; line-height:1.15; margin:0;">
                  {title}
                </div>
                <div class="small-muted" style="margin-top:6px;">
                  Resultados calculados con Z crítico (normal estándar, bilateral) + redondeo hacia arriba.
                </div>
              </div>
              <div class="pill" style="margin-top:2px;">Z = {z:.5f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Tres columnas con métricas principales
        # Col1: n redondeado (valor principal a usar)
        # Col2: n crudo (valor matemático exacto)
        # Col3: Fórmula matemática
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="metric"><div class="label">n (redondeado)</div><div class="value">{n_final}</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="metric"><div class="label">n (crudo)</div><div class="value" style="font-size:1.05rem; font-weight:650;">{format_big(n_crudo_str)}</div></div>',
                unsafe_allow_html=True,
            )
        with c3:
            with st.container(border=True):
                st.markdown('<div class="label">Fórmula</div>', unsafe_allow_html=True)
                st.latex(formula)

        # Separador visual
        st.markdown("<hr class='hr-soft'/>", unsafe_allow_html=True)
        
        # Sección de supuestos: lista numerada de condiciones estadísticas
        st.markdown("**Supuestos**")
        for i, s in enumerate(supuestos, start=1):
            st.write(f"{i}. {s}")


# ENCABEZADO DE LA APLICACIÓN
# Carga y renderiza el logo (tiburón) junto con el título y descripción general.
# Estructura: logo a la izquierda (16% ancho) + título a la derecha (84% ancho)
# Esto crea una presentación profesional e identificable.
logo = Image.open("assets/tiburon.png")

col_logo, col_title = st.columns([0.16, 0.84], vertical_alignment="center")

with col_logo:
    st.markdown(
        """
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
        ">
        """,
        unsafe_allow_html=True,
    )
    st.image(logo, width=120)
    st.markdown("</div>", unsafe_allow_html=True)

with col_title:
    st.markdown("## 🦈 Calculadora de Tamaño de Muestra")
    st.markdown(
        "<div class='small-muted'>"
        "Esta aplicación permite <b>calcular el tamaño de muestra requerido</b> para estudios estadísticos, "
        "tanto en la estimación de una <b>media poblacional</b> como de una <b>proporción</b>, "
        "a partir del nivel de confianza, el margen de error y parámetros estadísticos relevantes. "
        "Incluye validaciones, supuestos estadísticos y redondeo adecuado del tamaño muestral."
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)


# SISTEMA DE PESTAÑAS (TABS)
# Divide la interfaz en dos secciones principales: Media y Proporción
# Esto permite organizar lógicamente dos flujos de cálculo independientes
tab_media, tab_prop = st.tabs(["📈 Media", "🧩 Proporción"])


# PESTAÑA 1: CÁLCULO PARA MEDIA
with tab_media:
    # Sección de entrada de parámetros en contenedor con borde
    with st.container(border=True):
        st.markdown("### Parámetros")
        colA, colB, colC = st.columns(3)

        # Tres inputs en columnas paralelas para mejor UX:
        # - Nivel de confianza (0-1)
        # - Desviación estándar σ o estimación piloto
        # - Margen de error E
        with colA:
            confianza = st.number_input(
                "Nivel de confianza (0–1)",
                min_value=0.000001,
                max_value=0.999999,
                value=0.95,
                step=0.0001,
                format="%.6f",
                key="conf_media",
                help="Intervalo bilateral.",
            )

        with colB:
            sigma = st.number_input(
                "Desviación estándar (σ o S piloto)",
                min_value=0.0,
                value=10.0,
                step=0.01,
                format="%.6f",
                key="sigma_media",
                help="Si no conoces σ, usa una estimación piloto.",
            )

        with colC:
            margen_error = st.number_input(
                "Margen de error (E)",
                min_value=0.0,
                value=2.0,
                step=0.01,
                format="%.6f",
                key="E_media",
                help="En las mismas unidades que la variable.",
            )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Lógica de cálculo y visualización con validaciones
    # Solo calcula si los valores son válidos (σ > 0 y E > 0)
    if sigma > 0 and margen_error > 0:
        try:
            z, n_crudo_str, n_final, supuestos = calcular_media(confianza, sigma, margen_error)
            result_card("Resultado — Media",z,n_crudo_str,n_final,r"n = \left(\frac{Z \cdot \sigma}{E}\right)^2",supuestos,)

            st.markdown("### 📉 Sensibilidad (Media)")

            col_left, col_right = st.columns(2)

            # -------- Gráfica 1: n vs E --------
            with col_left:
                st.markdown("**n vs margen de error (E)**")

                e_min = st.number_input("E mínimo", min_value=0.000001, value=0.5, step=0.000001, format="%.6f", key="e_min")
                e_max = st.number_input("E máximo", min_value=0.000001, value=5.0, step=0.000001, format="%.6f", key="e_max")

                if e_max <= e_min:
                    st.warning("E máximo debe ser mayor que E mínimo.")
                else:
                    pasos = 80
                    lista_e = [e_min + (e_max - e_min) * i / (pasos - 1) for i in range(pasos)]

                    datos_e = []
                    for e in lista_e:
                        _, _, n_calc, _ = calcular_media(confianza, sigma, e)
                        datos_e.append({"E": e, "n": n_calc})

                    df_e = pd.DataFrame(datos_e)
                    st.line_chart(df_e, x="E", y="n")
                    st.caption(
                        f"Parámetros usados: "
                        f"σ = {sigma}, "
                        f"nivel de confianza = {confianza}, "
                        f"Z = {round(z, 4)}"
                    )
                    st.info(
                        "📌 **Interpretación:**\n\n"
                        "Esta gráfica muestra cómo el tamaño de muestra requerido depende del margen de error (E), "
                        "manteniendo fijo el nivel de confianza y la desviación estándar.\n\n"
                        "Dado que el margen de error aparece en el denominador de la fórmula, "
                        "una reducción en E provoca un incremento cuadrático en el tamaño de muestra."
                    )


            # -------- Gráfica 2: n vs Confianza --------
            with col_right:
                st.markdown("**n vs nivel de confianza**")

                conf_min = st.number_input(
                    "Confianza mínima", min_value=0.50, max_value=0.999999, value=0.80, step=0.01, format="%.6f", key="conf_min"
                )
                conf_max = st.number_input(
                    "Confianza máxima", min_value=0.50, max_value=0.999999, value=0.99, step=0.01, format="%.6f", key="conf_max"
                )

                if conf_max <= conf_min:
                    st.warning("Confianza máxima debe ser mayor que confianza mínima.")
                else:
                    pasos = 80
                    lista_conf = [conf_min + (conf_max - conf_min) * i / (pasos - 1) for i in range(pasos)]

                    datos_c = []
                    for c in lista_conf:
                        _, _, n_calc, _ = calcular_media(c, sigma, margen_error)  # aquí E se queda fijo (el E actual)
                        datos_c.append({"Confianza": c, "n": n_calc})

                    df_c = pd.DataFrame(datos_c)
                    st.line_chart(df_c, x="Confianza", y="n")
                    st.caption(
                        f"Parámetros usados: "
                        f"E = {margen_error}, "
                        f"σ = {sigma}"
                    )

                    st.info(
                        "📌 **Interpretación:**\n\n"
                        "Esta gráfica muestra cómo el tamaño de muestra requerido aumenta al exigir un mayor nivel de confianza, "
                        "manteniendo fijo el margen de error y la desviación estándar.\n\n"
                        "El crecimiento se debe a que el valor crítico Z aumenta rápidamente "
                        "a niveles de confianza altos."
                    )



        except Exception as e:
            st.error(f"No se pudo calcular: {e}")
    else:
        st.info("Ingresa valores válidos: σ > 0 y E > 0.")


# PESTAÑA 2: CÁLCULO PARA PROPORCIÓN
with tab_prop:
    # Sección de entrada de parámetros en contenedor con borde
    with st.container(border=True):
        st.markdown("### Parámetros")
        colA, colB, colC, colD = st.columns([1.1, 1, 1, 1])

        # Cuatro controles dispuestos horizontalmente:
        # - Nivel de confianza
        # - Margen de error
        # - Toggle para usar caso conservador (p=0.5)
        # - Input de proporción p (habilitado solo si toggle está desactivado)
        with colA:
            confianza_p = st.number_input(
                "Nivel de confianza (0–1)",
                min_value=0.000001,
                max_value=0.999999,
                value=0.95,
                step=0.0001,
                format="%.6f",
                key="conf_prop",
                help="Intervalo bilateral.",
            )

        with colB:
            margen_error_p = st.number_input(
                "Margen de error (E)",
                min_value=0.0,
                value=0.05,
                step=0.0001,
                format="%.6f",
                key="E_prop",
                help="Como proporción decimal.",
            )

        with colC:
            conservador = st.toggle(
                "Usar p=0.5 (conservador)",
                value=True,
                help="Si no conoces p, maximiza p(1-p) y da n más grande.",
            )

        with colD:
            # Este input se deshabilita cuando conservador=True
            # Esto guía al usuario hacia una elección clara
            p_val = st.number_input(
                "Proporción p",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.0001,
                format="%.6f",
                key="p_prop",
                disabled=conservador,
                help="Desactiva el conservador para editar p.",
            )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Define qué valor de p usar basado en el toggle
    p_usada = 0.5 if conservador else float(p_val)

    # Lógica de cálculo y visualización con validaciones
    # Solo calcula si los valores son válidos (E > 0 y 0 < p < 1)
    if margen_error_p > 0 and 0 < p_usada < 1:
        try:
            z, n_crudo_str, n_final, supuestos = calcular_proporcion(
                confianza_p, p_usada, margen_error_p, uso_conservador=conservador
            )
            result_card("Resultado — Proporción",z,n_crudo_str,n_final,r"n = \frac{Z^2 \cdot p(1-p)}{E^2}",supuestos,)

        except Exception as e:
            st.error(f"No se pudo calcular: {e}")
    else:
        st.info("Ingresa valores válidos: E > 0 y 0 < p < 1.")


# PIE DE PÁGINA
st.markdown(
    "<div class='small-muted' style='margin-top:18px;'>"
    "Autores: Luis Enrique Cruz Estrella y Ángel Sánchez Rangel. "
    "© ESCOM IPN."
    "</div>",
    unsafe_allow_html=True,
)
