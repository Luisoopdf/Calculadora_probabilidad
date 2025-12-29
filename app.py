import streamlit as st
from PIL import Image
from core import calcular_media, calcular_proporcion


# -----------------------------
# Configuración de página
# -----------------------------
st.set_page_config(
    page_title="Calculadora de Tamaño de Muestra",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# CSS moderno (glass + gradientes)
# -----------------------------
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
      rgba(30, 64, 175, 0.35),   /* azul medio */
      transparent 55%
    ),
    radial-gradient(
      1000px 650px at 85% 20%,
      rgba(15, 23, 42, 0.45),   /* azul muy oscuro */
      transparent 60%
    ),
    linear-gradient(
      180deg,
      #020617 0%,   /* casi negro azulado */
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
  padding-top: 3.2rem;   /* MÁS ESPACIO ARRIBA */
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
  min-height: 160px;        /* 🔑 MISMA ALTURA */
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.formula-box{
  min-height: 160px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch; /* <-- importante: que la caja ocupe todo el ancho */
}

.formula-label{
  text-align: left;
  margin-bottom: 8px;
}

/* Contenedor que centra la fórmula */
.latex-wrap{
  width: 100%;
  text-align: center;
}

/* Quitar márgenes raros del render */
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

/* Inputs redondeados */
[data-baseweb="input"] input,
[data-baseweb="select"] div,
[data-baseweb="textarea"] textarea{
  border-radius: 14px !important;
}


/* Tabs */
.stTabs [data-baseweb="tab"]{ font-weight: 650; color: rgba(255,255,255,0.75); }
.stTabs [aria-selected="true"]{ color: white !important; }

/* =========================================================
   ARREGLO CLAVE:
   Estilo premium para contenedores con border=True
   (Esto sí envuelve widgets reales en Streamlit)
   ========================================================= */
/* Contenedores border=True COMPLETAMENTE limpios */
/* Contenedores border=True como tarjetas (para fórmula y si lo usas en parámetros/resultados) */
[data-testid="stVerticalBlockBorderWrapper"]{
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 16px !important;
  box-shadow: none !important;
}

/* padding interno + altura consistente */
[data-testid="stVerticalBlockBorderWrapper"] > div{
  padding: 16px !important;
  min-height: 160px !important;   /* ✅ mismo alto que .metric */
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
}

/* Centrar LaTeX dentro de la tarjeta */
[data-testid="stVerticalBlockBorderWrapper"] .katex-display{
  margin: 0 !important;
  text-align: center !important;
}



/* Ocultar menú Streamlit */
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# -----------------------------
# Helpers UI
# -----------------------------
def format_big(n_str: str, max_len: int = 28) -> str:
    s = n_str.strip()
    if len(s) <= max_len:
        return s
    return f"{s[:14]}…{s[-10:]}"


def result_card(title: str, z: float, n_crudo_str: str, n_final: int, formula: str, supuestos: list[str]):
    # Todo dentro de un contenedor real para que el “card” cubra perfecto
    with st.container(border=True):
        # Header con flex (Z siempre arriba derecha)
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
            # Tarjeta real (container) para que st.latex quede DENTRO y no se salga
            with st.container(border=True):
                st.markdown('<div class="label">Fórmula</div>', unsafe_allow_html=True)
                st.latex(formula)


        st.markdown("<hr class='hr-soft'/>", unsafe_allow_html=True)
        st.markdown("**Supuestos**")
        for i, s in enumerate(supuestos, start=1):
            st.write(f"{i}. {s}")


# -----------------------------
# Header con logo (contenedor real)
# -----------------------------
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

tab_media, tab_prop = st.tabs(["📈 Media", "🧩 Proporción"])


# -----------------------------
# TAB: MEDIA
# -----------------------------
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
                help="Ej: 0.95 para 95% (intervalo bilateral).",
            )

        with colB:
            sigma = st.number_input(
                "Desviación estándar (σ o S piloto)",
                min_value=0.0,
                value=10.0,
                step=0.01,
                format="%.6f",
                key="sigma_media",
                help="Si no conoces σ, usa una S piloto (estimación).",
            )

        with colC:
            margen_error = st.number_input(
                "Margen de error (E)",
                min_value=0.0,
                value=2.0,
                step=0.01,
                format="%.6f",
                key="E_media",
                help="E en las mismas unidades que la variable.",
            )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Resultados auto-actualizados
    if sigma > 0 and margen_error > 0:
        try:
            z, n_crudo_str, n_final, supuestos = calcular_media(confianza, sigma, margen_error)
            result_card("Resultado — Media",z,n_crudo_str,n_final,r"n = \left(\frac{Z \cdot \sigma}{E}\right)^2",supuestos,)

        except Exception as e:
            st.error(f"No se pudo calcular: {e}")
    else:
        st.info("Ingresa valores válidos: σ > 0 y E > 0.")


# -----------------------------
# TAB: PROPORCIÓN
# -----------------------------
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
                help="Ej: 0.95 para 95% (intervalo bilateral).",
            )

        with colB:
            margen_error_p = st.number_input(
                "Margen de error (E)",
                min_value=0.0,
                value=0.05,
                step=0.0001,
                format="%.6f",
                key="E_prop",
                help="Ej: 0.05 equivale a 5%.",
            )

        with colC:
            conservador = st.toggle(
                "Usar p=0.5 (conservador)",
                value=True,
                help="Si no conoces p, p=0.5 maximiza p(1-p) y da n más grande.",
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

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    p_usada = 0.5 if conservador else float(p_val)

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


st.markdown(
    "<div class='small-muted' style='margin-top:18px;'>Hecho con Streamlit + core.py. Si n queda gigantesco, revisa si E es demasiado pequeño para tu contexto.</div>",
    unsafe_allow_html=True,
)
