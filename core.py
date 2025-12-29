import math
from statistics import NormalDist
from decimal import Decimal, getcontext, ROUND_CEILING


# Redondeo hacia arriba usando Decimal para evitar errores binarios
def ceil_decimal(x: Decimal) -> int:
    """Redondea hacia arriba un número Decimal al entero más próximo."""
    return int(x.to_integral_value(rounding=ROUND_CEILING))


# Obtiene Z crítico para un nivel de confianza bilateral
def calcular_z(confianza: float) -> float:
    """Obtiene el valor Z crítico según el nivel de confianza."""
    # Validación del rango de confianza
    if confianza <= 0 or confianza >= 1:
        raise ValueError("La confianza debe estar entre 0 y 1 (ej: 0.95).")

    # Cálculo de alpha y Z por la inversa de la CDF normal estándar
    alpha = 1 - confianza
    z = NormalDist().inv_cdf(1 - alpha / 2)

    # Verificación de finitud de Z (confianzas extremas)
    if not math.isfinite(z):
        raise OverflowError(
            "La confianza es demasiado cercana a 1 y el valor Z se vuelve infinito."
        )

    return z


# Cálculo de tamaño muestral para media: n = (Z·σ/E)²
def calcular_media(confianza: float, sigma: float, margen_error: float):
    """Calcula tamaño de muestra para media: n = (Z·σ/E)²

    Retorna: valor Z, n sin redondear, n redondeado, y lista de supuestos.
    """
    # Validaciones de parámetros
    if sigma <= 0:
        raise ValueError("sigma debe ser mayor que 0.")
    if margen_error <= 0:
        raise ValueError("El margen de error E debe ser mayor que 0.")

    # Z crítico
    z = calcular_z(confianza)

    # Alta precisión decimal para el cálculo de n
    getcontext().prec = 80

    # Conversión a Decimal para evitar errores de punto flotante
    Z = Decimal(str(z))
    SIGMA = Decimal(str(sigma))
    E = Decimal(str(margen_error))

    # Cálculo de n crudo y redondeo hacia arriba
    ratio = (Z * SIGMA) / E
    n_crudo = ratio * ratio
    n_final = ceil_decimal(n_crudo)

    # Supuestos estadísticos del cálculo para media
    supuestos = [
        "Se asume muestreo aleatorio y representativo de la población.",
        "Se asume independencia entre observaciones.",
        "La desviación estándar utilizada (σ o S piloto) representa adecuadamente la variabilidad poblacional.",
        "El margen de error E se interpreta en las mismas unidades que la variable medida.",
    ]

    # Supuesto adicional según tamaño muestral (TCL vs normalidad)
    if n_final >= 30:
        supuestos.insert(
            2,
            "Dado que n ≥ 30, la aproximación normal para la media es razonable (Teorema Central del Límite).",
        )
    else:
        supuestos.insert(
            2,
            "Como n < 30, se asume que la variable en la población tiene una distribución aproximadamente normal.",
        )

    return z, str(n_crudo), n_final, supuestos


# Cálculo de tamaño muestral para proporción: n = (Z²·p(1-p))/E²
def calcular_proporcion(
    confianza: float, p: float, margen_error: float, uso_conservador: bool = False
):
    """Calcula tamaño de muestra para proporción: n = (Z²·p(1-p))/E²

    Retorna: valor Z, n sin redondear, n redondeado, y lista de supuestos.
    """
    # Validaciones de parámetros
    if margen_error <= 0:
        raise ValueError("El margen de error E debe ser mayor que 0.")
    if p <= 0 or p >= 1:
        raise ValueError("p debe cumplir 0 < p < 1.")

    # Z crítico
    z = calcular_z(confianza)

    # Alta precisión decimal para el cálculo de n
    getcontext().prec = 80

    # Conversión a Decimal para evitar errores de punto flotante
    Z = Decimal(str(z))
    P = Decimal(str(p))
    E = Decimal(str(margen_error))

    # Cálculo de n crudo y redondeo hacia arriba
    numerador = (Z * Z) * P * (Decimal("1") - P)
    denominador = E * E
    n_crudo = numerador / denominador
    n_final = ceil_decimal(n_crudo)

    # Supuestos estadísticos del cálculo para proporción
    supuestos = [
        "Se asume muestreo aleatorio y representativo de la población.",
        "Se asume independencia entre observaciones.",
        "El margen de error E se interpreta como proporción (por ejemplo, 0.05 = 5%).",
    ]

    # Verificación de validez de la aproximación normal (np y n(1-p))
    np_val = n_final * p
    n1p_val = n_final * (1 - p)

    if np_val >= 5 and n1p_val >= 5:
        supuestos.insert(
            2,
            f"Se cumple np = {np_val:.2f} ≥ 5 y n(1-p) = {n1p_val:.2f} ≥ 5; la aproximación normal es válida.",
        )
    else:
        supuestos.insert(
            2,
            f"No se cumple completamente np = {np_val:.2f} ≥ 5 y/o n(1-p) = {n1p_val:.2f} ≥ 5; la aproximación normal podría no ser adecuada.",
        )

    # Nota sobre caso conservador (p=0.5) o estimación previa
    if uso_conservador and abs(p - 0.5) < 1e-12:
        supuestos.append(
            "Se utilizó p = 0.5 como caso conservador (maximiza p(1-p) y produce el mayor n)."
        )
    else:
        supuestos.append(
            "La proporción p utilizada proviene de una estimación previa o datos piloto."
        )

    return z, str(n_crudo), n_final, supuestos
