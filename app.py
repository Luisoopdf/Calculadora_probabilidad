# Importaciones y utilidades principales de la app
import streamlit as st
import altair as alt
import pandas as pd
from PIL import Image
from core import calcular_media, calcular_proporcion

def grafica_sensibilidad(df, x_col, y_col, x_actual, y_actual, titulo, etiqueta_x):
    base = alt.Chart(df).mark_line(
        color="white",
        strokeWidth=2
    ).encode(
        x=alt.X(
            f"{x_col}:Q",
            title=etiqueta_x,
            axis=alt.Axis(labelColor="white", titleColor="white")
        ),
        y=alt.Y(
            f"{y_col}:Q",
            title="n (tamaño de muestra)",
            axis=alt.Axis(labelColor="white", titleColor="white")
        )
    )

    regla = alt.Chart(
        pd.DataFrame({x_col: [x_actual]})
    ).mark_rule(
        color="white",
        strokeDash=[6, 6],
        strokeWidth=2
    ).encode(
        x=f"{x_col}:Q"
    )

    punto = alt.Chart(
        pd.DataFrame({x_col: [x_actual], y_col: [y_actual]})
    ).mark_point(
        color="white",
        size=120
    ).encode(
        x=f"{x_col}:Q",
        y=f"{y_col}:Q",
        tooltip=[x_col, y_col]
    )

    texto = alt.Chart(
        pd.DataFrame({x_col: [x_actual], y_col: [y_actual]})
    ).mark_text(
        color="white",
        align="left",
        dx=8,
        dy=-8
    ).encode(
        x=f"{x_col}:Q",
        y=f"{y_col}:Q",
        text=alt.value(f"actual: {x_actual} → n={y_actual}")
    )

    st.altair_chart(
        (base + regla + punto + texto)
        .properties(
            title=alt.TitleParams(
                text=titulo,
                color="white"
            )
        )
        .interactive(),
        use_container_width=True
    )


st.set_page_config(
    page_title="Calculadora de Tamaño de Muestra",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = """
<style>
/* Variables de tema y colores base */
:root{
  --bg1:#0b1020; --bg2:#0f172a;
  --card: rgba(255,255,255,0.06);
  --stroke: rgba(255,255,255,0.12);
  --text: rgba(255,255,255,0.92);
  --muted: rgba(255,255,255,0.72);
  --shadow: 0 18px 55px rgba(0,0,0,0.45);
}

/* Fondo con gradientes y texto principal */
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

/* Contenedor: espaciado y ancho máximo */
.block-container{
  padding-top: 3.2rem;
  padding-bottom: 2.2rem;
  max-width: 1150px;
}

/* Tipografía y texto auxiliar */
h1,h2,h3,h4{ color: var(--text) !important; }
.small-muted{ color: var(--muted); font-size: 0.92rem; }

/* Insignias compactas de información (pill) */
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

/* Tarjetas de métricas (n redondeado / crudo) */
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

/* Caja que contiene fórmula LaTeX */
.formula-box{
  min-height: 160px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}

/* Etiqueta de fórmula y ajuste de LaTeX */
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

/* Estilos de texto dentro de métricas */
.metric .label{ color: var(--muted); font-size: 0.86rem; }
.metric .value{ font-size: 1.55rem; font-weight: 700; letter-spacing: .2px; }

/* Separador suave */
.hr-soft{
  height: 1px;
  background: rgba(255,255,255,0.10);
  border: none;
  margin: 14px 0;
}

/* Inputs redondeados */
[data-baseweb="input"] input,
[data-baseweb="select"] div,
[data-baseweb="textarea"] textarea{
  border-radius: 14px !important;
}

/* Pestañas y selección activa */
.stTabs [data-baseweb="tab"]{ font-weight: 650; color: rgba(255,255,255,0.75); }
.stTabs [aria-selected="true"]{ color: white !important; }

/* Contenedores con borde para secciones */
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

/* Oculta menú y pie nativos de Streamlit */
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
</style>
"""
# Inyección del CSS en la app
st.markdown(CSS, unsafe_allow_html=True)


def format_big(n_str: str, max_len: int = 28) -> str:
    """Formatea números muy grandes truncándolos de forma legible."""
    s = n_str.strip()
    if len(s) <= max_len:
        return s
    return f"{s[:14]}…{s[-10:]}"

# Construye la tarjeta de resultados (título, métricas, fórmula y supuestos)
def result_card(title: str, z: float, n_crudo_str: str, n_final: int, formula: str, supuestos: list[str]):
    """Construye y renderiza la tarjeta de resultados."""
    with st.container(border=True):
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

        st.markdown("<hr class='hr-soft'/>", unsafe_allow_html=True)
        st.markdown("**Supuestos**")
        for i, s in enumerate(supuestos, start=1):
            st.write(f"{i}. {s}")


logo = Image.open("assets/tiburon.png")
col_logo, col_title = st.columns([0.16, 0.84], vertical_alignment="center")

# Muestra del logotipo
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

# Título y descripción de la aplicación
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

# Separador visual
st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)


tab_media, tab_prop = st.tabs(["📈 Media", "🧩 Proporción"])


with tab_media:
    with st.container(border=True):
        st.markdown("### Parámetros")
        colA, colB, colC = st.columns(3)

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

    # Espaciado entre parámetros y resultados
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    if sigma > 0 and margen_error > 0:
        try:
            # Cálculo principal y render de tarjeta
            z, n_crudo_str, n_final, supuestos = calcular_media(confianza, sigma, margen_error)
            result_card("Resultado — Media", z, n_crudo_str, n_final, r"n = \left(\frac{Z \cdot \sigma}{E}\right)^2", supuestos)

            # Gráficas de sensibilidad para media
            st.markdown("### 📉 Sensibilidad (Media)")
            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown("**n vs margen de error (E)**")
                e_min = st.number_input("E mínimo", min_value=0.000001, value=0.5, step=0.000001, format="%.6f", key="e_min")
                e_max = st.number_input("E máximo", min_value=0.000001, value=5.0, step=0.000001, format="%.6f", key="e_max")

                if e_max <= e_min:
                    st.warning("E máximo debe ser mayor que E mínimo.")
                else:
                    # Generación de datos n para diferentes E
                    pasos = 80
                    lista_e = [e_min + (e_max - e_min) * i / (pasos - 1) for i in range(pasos)]
                    datos_e = []
                    for e in lista_e:
                        _, _, n_calc, _ = calcular_media(confianza, sigma, e)
                        datos_e.append({"E": e, "n": n_calc})

                    # Gráfica n vs E y anotación del punto actual
                    df_e = pd.DataFrame(datos_e)
                    grafica_sensibilidad(
                        df=df_e,
                        x_col="E",
                        y_col="n",
                        x_actual=margen_error,
                        y_actual=n_final,
                        titulo="n vs E (Media) — Punto actual marcado",
                        etiqueta_x="Margen de error (E)"
                    )

                    st.caption(f"Punto actual: E = {margen_error}  →  n = {n_final}  |  σ = {sigma}  |  confianza = {confianza}  |  Z = {z:.5f}")

                    st.info(
                        "📌 **Interpretación:**\n\n"
                        "Esta gráfica muestra cómo el tamaño de muestra requerido depende del margen de error (E), "
                        "manteniendo fijo el nivel de confianza y la desviación estándar.\n\n"
                        "Dado que el margen de error aparece en el denominador de la fórmula, "
                        "una reducción en E provoca un incremento cuadrático en el tamaño de muestra."
                    )

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
                    # Generación de datos n para diferentes niveles de confianza
                    pasos = 80
                    lista_conf = [conf_min + (conf_max - conf_min) * i / (pasos - 1) for i in range(pasos)]
                    datos_c = []
                    for c in lista_conf:
                        _, _, n_calc, _ = calcular_media(c, sigma, margen_error)
                        datos_c.append({"Confianza": c, "n": n_calc})

                    # Gráfica n vs confianza y anotación del punto actual
                    df_c = pd.DataFrame(datos_c)
                    grafica_sensibilidad(
                        df=df_c,
                        x_col="Confianza",
                        y_col="n",
                        x_actual=confianza,
                        y_actual=n_final,
                        titulo="n vs Confianza (Media) — Punto actual marcado",
                        etiqueta_x="Nivel de confianza"
                    )
                    # Detalle del punto actual y parámetros fijos
                    st.caption(f"Punto actual: confianza = {confianza}  →  n = {n_final}  |  E = {margen_error}  |  σ = {sigma}  |  Z = {z:.5f}")

                    st.caption(f"Punto actual: confianza = {confianza}  →  n = {n_final}  |  E = {margen_error}  |  σ = {sigma}  |  Z = {z:.5f}")

                    st.info(
                        "📌 **Interpretación:**\n\n"
                        "Esta gráfica muestra cómo el tamaño de muestra requerido aumenta al exigir un mayor nivel de confianza, "
                        "manteniendo fijo el margen de error y la desviación estándar.\n\n"
                        "El crecimiento se debe a que el valor crítico Z aumenta rápidamente "
                        "a niveles de confianza altos."
                    )

        except Exception as e:
            # Mensaje de error ante entradas inválidas o fallos de cálculo
            st.error(f"No se pudo calcular: {e}")
    else:
        # Ayuda inicial para entradas inválidas
        st.info("Ingresa valores válidos: σ > 0 y E > 0.")


with tab_prop:
    with st.container(border=True):
        st.markdown("### Parámetros")
        colA, colB, colC, colD = st.columns([1.1, 1, 1, 1])

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

    # Espaciado entre parámetros y resultados
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    p_usada = 0.5 if conservador else float(p_val)

    if margen_error_p > 0 and 0 < p_usada < 1:
        try:
            # Cálculo principal y render de tarjeta
            z, n_crudo_str, n_final, supuestos = calcular_proporcion(
                confianza_p, p_usada, margen_error_p, uso_conservador=conservador
            )
            result_card("Resultado — Proporción", z, n_crudo_str, n_final, r"n = \frac{Z^2 \cdot p(1-p)}{E^2}", supuestos,)

            st.markdown("### 📉 Sensibilidad (Proporción)")
            st.markdown(
                "<div class='small-muted'>"
                "Estas gráficas muestran cómo cambia el tamaño de muestra <b>n</b> cuando modificas un parámetro, "
                "manteniendo los demás fijos (basado en el intervalo de confianza para proporciones)."
                "</div>",
                unsafe_allow_html=True,
            )

            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown("**1) n vs margen de error (E)**")

                e_min_g = st.number_input(
                    "E mínimo (gráfica)",
                    min_value=0.000001,
                    value=0.01,
                    step=0.01,
                    format="%.6f",
                    key="prop_e_min_graf",
                    help="E es proporción decimal. Ej: 0.05 = 5%. No puede ser 0.",
                )
                e_max_g = st.number_input(
                    "E máximo (gráfica)",
                    min_value=0.000002,
                    value=0.20,
                    step=0.01,
                    format="%.6f",
                    key="prop_e_max_graf",
                    help="Recomendación: no uses E demasiado grande, porque la estimación pierde utilidad.",
                )

                if e_max_g <= e_min_g:
                    st.warning("E máximo debe ser mayor que E mínimo.")
                else:
                    pasos = 60
                    lista_e = [e_min_g + (e_max_g - e_min_g) * i / (pasos - 1) for i in range(pasos)]

                    datos = []
                    for e in lista_e:
                        _z, _n_crudo, _n_final, _ = calcular_proporcion(
                            confianza_p, p_usada, e, uso_conservador=conservador
                        )
                        datos.append({"E": e, "n": _n_final})

                    df = pd.DataFrame(datos)
                    grafica_sensibilidad(
                        df=df,
                        x_col="E",
                        y_col="n",
                        x_actual=margen_error_p,
                        y_actual=n_final,
                        titulo="n vs E (Proporción) — Punto actual marcado",
                        etiqueta_x="Margen de error (E)"
                    )

                    st.caption(f"Punto actual: E = {margen_error_p}  →  n = {n_final}  |  p = {p_usada}  |  confianza = {confianza_p}  |  Z = {z:.5f}")

                    st.info(
                        "📌 **Interpretación:**\n\n"
                        "Aquí solo cambia **E**. Si reduces el margen de error, el intervalo de confianza se hace más estrecho "
                        "y necesitas más observaciones para lograr esa precisión. Por eso **n crece rápido** cuando E baja "
                        "(relación tipo 1/E²)."
                    )

            with col_right:
                st.markdown("**2) n vs nivel de confianza**")

                conf_min_g = st.number_input(
                    "Confianza mínima (gráfica)",
                    min_value=0.50,
                    max_value=0.9999,
                    value=0.80,
                    step=0.01,
                    format="%.2f",
                    key="prop_conf_min_graf",
                )
                conf_max_g = st.number_input(
                    "Confianza máxima (gráfica)",
                    min_value=0.50,
                    max_value=0.9999,
                    value=0.99,
                    step=0.01,
                    format="%.2f",
                    key="prop_conf_max_graf",
                )

                if conf_max_g <= conf_min_g:
                    st.warning("Confianza máxima debe ser mayor que confianza mínima.")
                else:
                    pasos = 60
                    lista_c = [conf_min_g + (conf_max_g - conf_min_g) * i / (pasos - 1) for i in range(pasos)]

                    datos = []
                    for c in lista_c:
                        _z, _n_crudo, _n_final, _ = calcular_proporcion(
                            c, p_usada, margen_error_p, uso_conservador=conservador
                        )
                        datos.append({"Confianza": c, "n": _n_final})

                    df = pd.DataFrame(datos)
                    grafica_sensibilidad(
                        df=df,
                        x_col="Confianza",
                        y_col="n",
                        x_actual=confianza_p,
                        y_actual=n_final,
                        titulo="n vs Confianza (Proporción) — Punto actual marcado",
                        etiqueta_x="Nivel de confianza"
                    )

                    st.caption(f"Punto actual: confianza = {confianza_p}  →  n = {n_final}  |  E = {margen_error_p}  |  p = {p_usada}  |  Z = {z:.5f}")


                    st.info(
                        "📌 **Interpretación:**\n\n"
                        "Aquí solo cambia la **confianza**. Al subir la confianza, aumenta el valor crítico **Z**, "
                        "lo que ensancha el intervalo. Para mantener el mismo margen de error **E**, "
                        "se requiere una muestra mayor, por eso **n aumenta**."
                    )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            st.markdown("**3) n vs proporción p**")

            colp1, colp2 = st.columns([1, 1])
            with colp1:
                p_min_g = st.number_input(
                    "p mínimo (gráfica)",
                    min_value=0.01,
                    max_value=0.49,
                    value=0.01,
                    step=0.01,
                    format="%.2f",
                    key="prop_p_min_graf",
                )
            with colp2:
                p_max_g = st.number_input(
                    "p máximo (gráfica)",
                    min_value=0.51,
                    max_value=0.99,
                    value=0.99,
                    step=0.01,
                    format="%.2f",
                    key="prop_p_max_graf",
                )

            if p_max_g <= p_min_g:
                st.warning("p máximo debe ser mayor que p mínimo.")
            else:
                pasos = 80
                lista_p = [p_min_g + (p_max_g - p_min_g) * i / (pasos - 1) for i in range(pasos)]

                datos = []
                for p_tmp in lista_p:
                    _z, _n_crudo, _n_final, _ = calcular_proporcion(
                        confianza_p, p_tmp, margen_error_p, uso_conservador=False
                    )
                    datos.append({"p": p_tmp, "n": _n_final})

                df = pd.DataFrame(datos)
                st.line_chart(df, x="p", y="n")

                st.caption(
                    f"Parámetros fijos: E = {margen_error_p:.6f} · confianza = {confianza_p:.4f} · "
                    f"Z = {z:.5f} · p actual usado en resultado = {p_usada:.4f}"
                )

                st.info(
                    "📌 **Interpretación:**\n\n"
                    "Esta gráfica muestra cómo afecta **p** a n. El término **p(1−p)** es máximo en **p = 0.5**, "
                    "por eso ahí se obtiene el **n más grande**. "
                    "Esto justifica el **caso conservador** (usar p=0.5 cuando no se conoce p)."
                )


        except Exception as e:
            # Mensaje de error ante entradas inválidas o fallos de cálculo
            st.error(f"No se pudo calcular: {e}")
    else:
        # Ayuda inicial para entradas inválidas
        st.info("Ingresa valores válidos: E > 0 y 0 < p < 1.")

st.markdown(
    "<div class='small-muted' style='margin-top:18px;'>"
    "Luis Enrique Cruz Estrella | Ángel Sánchez Rangel | Raul Contreras Martinez"
    "© ESCOM IPN."
    "</div>",
    unsafe_allow_html=True,
)

