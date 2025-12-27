# Calculadora de Tamaño de Muestra  
**Proyecto 4 – Aplicación de Consola**

---

## 1. Descripción general del proyecto

Este proyecto consiste en el desarrollo de una **aplicación de consola en Python** cuyo propósito es **calcular el tamaño de muestra necesario** para realizar estudios estadísticos confiables.

La aplicación permite calcular el tamaño de muestra requerido para:

- **Estimación de una media poblacional**
- **Estimación de una proporción poblacional**

utilizando como parámetros:
- un **nivel de confianza**
- un **margen de error**
- información adicional como desviación estándar o proporción estimada

El programa está diseñado para ser **simple, claro y académico**, cumpliendo con los requerimientos esenciales del proyecto.

---

## 2. Objetivo del proyecto

El objetivo principal es:

> Desarrollar una herramienta que aplique correctamente las fórmulas estadísticas del tamaño de muestra, explique el proceso de cálculo y ayude a comprender cómo influyen el margen de error y el nivel de confianza en el tamaño de la muestra.

### Objetivos específicos
- Aplicar correctamente las fórmulas estadísticas para media y proporción
- Mostrar de forma explícita:
  - la fórmula utilizada
  - el valor crítico Z
  - el tamaño de muestra sin redondear
  - el tamaño de muestra redondeado hacia arriba
- Validar los datos de entrada del usuario
- Explicar los **supuestos estadísticos** del cálculo
- Ejecutarse completamente desde la **consola**

---

## 3. Alcance del proyecto

### Incluye
- Aplicación de consola
- Cálculo de tamaño de muestra para:
  - media
  - proporción
- Uso de proporción conservadora `p = 0.5`
- Validaciones básicas
- Explicación de supuestos

### No incluye (por ahora)
- Interfaz gráfica
- Corrección por población finita
- Lectura de archivos externos
- Gráficas

*(Estas funcionalidades se consideran posibles mejoras futuras.)*

---

## 4. Fundamento estadístico

### 4.1 Tamaño de muestra para la media

Se utiliza la fórmula:

\[
n = \left(\frac{Z \cdot \sigma}{E}\right)^2
\]

Donde:
- \( Z \) = valor crítico asociado al nivel de confianza
- \( \sigma \) = desviación estándar poblacional (o estimada)
- \( E \) = margen de error máximo permitido

El resultado se **redondea siempre hacia arriba**, ya que no es posible tomar fracciones de individuos y el redondeo garantiza cumplir el margen de error.

---

### 4.2 Tamaño de muestra para la proporción

Se utiliza la fórmula:

\[
n = \frac{Z^2 \cdot p(1-p)}{E^2}
\]

Donde:
- \( p \) = proporción estimada
- \( E \) = margen de error
- \( Z \) = valor crítico del nivel de confianza

Cuando no se conoce la proporción, se usa:

\[
p = 0.5
\]

Esto genera el **tamaño de muestra más grande posible**, por lo que es un enfoque **conservador**.

---

## 5. Supuestos estadísticos

Los cálculos realizados por el programa asumen que:

- El muestreo es **aleatorio y representativo**
- Las observaciones son **independientes**
- Se puede usar la **aproximación normal**
- En proporciones:
  - \( np \) y \( n(1-p) \) deben ser suficientemente grandes
- Si la proporción es desconocida, usar \( p = 0.5 \) es una práctica estándar

Estos supuestos se muestran explícitamente en la salida del programa.

---

## 6. Tecnologías utilizadas

### 6.1 Lenguaje de programación: Python 3

**Razones para usar Python:**
- Sintaxis clara y fácil de entender
- Muy utilizado en estadística y ciencia de datos
- Excelente soporte para matemáticas y validaciones
- Ideal para aplicaciones de consola
- Fácil de extender a interfaz gráfica en el futuro

---

### 6.2 Librerías utilizadas

#### `scipy`
**Uso en el proyecto:**
- Calcular el valor crítico **Z** a partir del nivel de confianza

**Justificación:**
- Proporciona resultados precisos
- Evita el uso manual de tablas Z
- Permite trabajar con cualquier nivel de confianza

---

#### `math` (librería estándar)
**Uso en el proyecto:**
- Redondeo hacia arriba (`ceil`)

**Justificación:**
- Es la forma correcta de redondear tamaños de muestra
- Garantiza que el margen de error se cumpla

---

#### `dataclasses` (librería estándar)
**Uso en el proyecto:**
- Organizar los resultados del cálculo en una estructura clara

**Justificación:**
- Mejora la legibilidad del código
- Facilita mostrar resultados ordenados

---

## 7. Estructura del proyecto

