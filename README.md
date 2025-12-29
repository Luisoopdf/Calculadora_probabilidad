# Calculadora de Tamaño de Muestra  
**Proyecto – Probabilidad y Estadística**

---

## a) Introducción y motivación del proyecto

En el ámbito de la **Probabilidad y la Estadística**, uno de los aspectos más importantes al diseñar un estudio es determinar **cuántas observaciones son necesarias** para obtener resultados confiables y estadísticamente válidos. Un tamaño de muestra mal calculado puede conducir a conclusiones erróneas, intervalos demasiado amplios o costos innecesarios.

La motivación principal de este proyecto es **automatizar el cálculo del tamaño de muestra**, evitando errores comunes como:
- el uso incorrecto de tablas de la distribución normal,
- el redondeo inapropiado del tamaño de muestra,
- la mala interpretación del margen de error,
- la omisión de los supuestos estadísticos.

Este proyecto busca funcionar como una **herramienta académica y práctica**, que no solo realice el cálculo, sino que también **explique el proceso estadístico**, mostrando las fórmulas utilizadas, el valor crítico Z y los supuestos que justifican el modelo.

---

## b) Modelado estadístico: Probabilidad y Estadística utilizados

El proyecto se fundamenta en la **estadística inferencial**, específicamente en el uso de **intervalos de confianza** y la **aproximación normal** para la estimación de parámetros poblacionales.

---

### 1. Distribución normal y valor crítico Z

Para ambos casos (estimación de la media y de la proporción), se utiliza la **distribución normal estándar**.  
El valor crítico \( Z \) se obtiene a partir del nivel de confianza mediante la expresión:

\[
Z = \Phi^{-1}\left(1 - \frac{\alpha}{2}\right)
\]

donde:
- \( \alpha = 1 - \text{nivel de confianza} \)
- \( \Phi^{-1} \) representa la función inversa de la distribución normal acumulada

Este procedimiento permite calcular el valor Z de forma precisa, sin necesidad de utilizar tablas estadísticas.

---

### 2. Tamaño de muestra para la media poblacional

Para estimar una media poblacional, el tamaño de muestra se calcula con la siguiente fórmula:


\[
n = \left(\frac{Z \cdot \sigma}{E}\right)^2
\]


donde:
- \( Z \) es el valor crítico asociado al nivel de confianza
- \( \sigma \) es la desviación estándar poblacional o una estimación piloto
- \( E \) es el margen de error máximo permitido

**Supuestos estadísticos:**
- El muestreo es aleatorio y representativo de la población
- Las observaciones son independientes
- Si \( n \ge 30 \), se justifica la aproximación normal por el Teorema Central del Límite
- Si \( n < 30 \), se asume que la variable sigue una distribución aproximadamente normal
- El margen de error se expresa en las mismas unidades que la variable medida

El resultado del tamaño de muestra se **redondea siempre hacia arriba**, garantizando que el margen de error se cumpla.

---

### 3. Tamaño de muestra para la proporción poblacional

Para la estimación de una proporción poblacional se emplea la fórmula:

\[
n = \frac{Z^2 \cdot p(1-p)}{E^2}
\]

donde:
- \( p \) es la proporción estimada
- \( E \) es el margen de error
- \( Z \) es el valor crítico

Cuando la proporción es desconocida, se utiliza el valor:

\[
p = 0.5
\]

Este valor maximiza el término \( p(1-p) \), produciendo el **tamaño de muestra más grande posible**, lo cual constituye un enfoque **conservador**.

**Condición para la aproximación normal en proporciones:**
- \( np \ge 5 \)
- \( n(1-p) \ge 5 \)

Estas condiciones son verificadas y explicadas en los resultados del programa.

---

## c) Descripción de la implementación

### 1. Arquitectura del programa

El proyecto fue desarrollado siguiendo una **arquitectura modular**, separando claramente la lógica estadística de la interacción con el usuario. Esto permite reutilizar el código y facilita futuras ampliaciones.

La estructura general del proyecto es la siguiente:

proyecto/
├── core.py        # Lógica estadística y modelos matemáticos
├── main.py        # Aplicación de consola (CLI)
├── app.py         # Aplicación web con Streamlit
├── assets/        # Recursos gráficos (logo)
│   └── tiburon.png
└── README.md      # Documentación



---

### 2. Descripción de los módulos

#### `core.py`
Este módulo contiene toda la **lógica matemática y estadística** del proyecto:
- Cálculo del valor crítico Z a partir del nivel de confianza
- Cálculo del tamaño de muestra para:
  - media poblacional
  - proporción poblacional
- Uso de alta precisión numérica para evitar errores de redondeo
- Redondeo siempre hacia arriba del tamaño de muestra
- Generación de supuestos estadísticos explicativos

Este módulo es reutilizado tanto por la aplicación de consola como por la interfaz gráfica.

---

#### `main.py`
Implementa una **aplicación de consola interactiva**, la cual:
- Solicita los datos al usuario mediante la terminal
- Valida que las entradas sean correctas
- Muestra el valor crítico Z, la fórmula utilizada y los resultados
- Explica los supuestos estadísticos asociados al cálculo
- Permite elegir entre el cálculo para media o proporción

---

#### `app.py`
Implementa una **aplicación web interactiva** utilizando el framework Streamlit:
- Interfaz gráfica moderna y amigable
- Dos pestañas principales: Media y Proporción
- Actualización automática de los resultados
- Visualización de fórmulas en formato LaTeX
- Validaciones en tiempo real de los parámetros ingresados

---

### 3. Librerías, frameworks y recursos utilizados

#### Python 3
Lenguaje de programación principal del proyecto.

**Requisito:**
- Python 3.9 o superior

---

#### Streamlit
Framework utilizado para desarrollar la interfaz web.

**Instalación:**
```bash
pip install streamlit
```

**Ejecución de la aplicación web:**
```bash
streamlit run app.py
```

---

#### statistics (librería estándar de Python)
Se utiliza la clase `NormalDist` para calcular el **valor crítico Z** correspondiente al nivel de confianza seleccionado, a partir de la distribución normal estándar.

**Uso dentro del proyecto:**
- Cálculo preciso del cuantil de la normal
- Eliminación del uso de tablas Z impresas
- Soporte para cualquier nivel de confianza válido

---

#### decimal (librería estándar de Python)
Esta librería se utiliza para manejar cálculos con **alta precisión numérica**, especialmente importante cuando el tamaño de muestra resulta muy grande.

**Uso dentro del proyecto:**
- Evitar errores de redondeo por punto flotante
- Representar números con gran cantidad de dígitos
- Redondear siempre el tamaño de muestra hacia arriba usando `ROUND_CEILING`

---

#### math (librería estándar de Python)
Se emplea para realizar validaciones matemáticas adicionales.

**Uso dentro del proyecto:**
- Verificación de valores finitos
- Control de errores numéricos extremos
- Apoyo en cálculos auxiliares

---

#### Pillow (PIL)
Librería utilizada para la carga y visualización de imágenes dentro de la interfaz gráfica.

**Uso dentro del proyecto:**
- Mostrar el logotipo de la aplicación en la interfaz web

**Instalación:**
```bash
pip install pillow
```
---

## d) Datos: fuente, descripción y preprocesamiento

### 1. Fuente de los datos

El proyecto **no utiliza bases de datos externas ni archivos de entrada**.  
Todos los datos empleados en los cálculos provienen directamente de **entradas proporcionadas por el usuario**, ya sea a través de la consola o de la interfaz web.

---

### 2. Descripción de los datos

Las variables utilizadas corresponden a los parámetros clásicos del cálculo del tamaño de muestra en estadística:

| Variable | Tipo | Descripción |
|--------|------|-------------|
| Nivel de confianza | Continua (0,1) | Nivel de confianza estadístico |
| Margen de error (E) | Continua > 0 | Error máximo permitido |
| Desviación estándar (σ) | Continua > 0 | Variabilidad de la variable |
| Proporción (p) | Continua (0,1) | Proporción estimada |

---

### 3. Limpieza y preprocesamiento

Antes de realizar cualquier cálculo, el programa aplica las siguientes validaciones y procesos:

- Verificación de rangos válidos para cada variable
- Rechazo de valores negativos o nulos
- Prevención de divisiones entre cero
- Control de valores extremos (por ejemplo, valores Z infinitos)
- Aplicación automática de \( p = 0.5 \) cuando se selecciona el modo conservador

Estas validaciones garantizan la **correcta aplicación de los modelos estadísticos**.

---

### 4. Variables utilizadas

Las variables se utilizan directamente en las **fórmulas estadísticas clásicas**, sin transformaciones artificiales, asegurando:
- coherencia matemática
- claridad académica
- interpretación estadística correcta

---

## Conclusión

Este proyecto implementa de manera correcta y clara los **modelos estadísticos para el cálculo del tamaño de muestra**, combinando fundamentos teóricos de Probabilidad y Estadística con una implementación computacional robusta.

La separación entre lógica estadística e interfaz de usuario, junto con las validaciones y explicaciones incluidas, convierten a esta aplicación en una **herramienta útil tanto para fines académicos como prácticos**, facilitando la comprensión del impacto del nivel de confianza y del margen de error en el tamaño de la muestra.
