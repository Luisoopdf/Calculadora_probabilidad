
import math
from statistics import NormalDist
from decimal import Decimal, getcontext, ROUND_CEILING


#Redonde hacia arriba para numeros con desbordamiento
def ceil_decimal(x: Decimal) -> int:
    return int(x.to_integral_value(rounding=ROUND_CEILING))


# Calcular Z apartir de la confianza
def calcular_z(confianza: float) -> float:

    if confianza <= 0 or confianza >= 1:
        raise ValueError("La confianza debe estar entre 0 y 1 (ejemplo: 0.95).")

    alpha = 1 - confianza
    z = NormalDist().inv_cdf(1 - alpha / 2)

    # Si alguien mete una confianza absurdamente cercana a 1, z podría volverse infinito.
    if not math.isfinite(z):
        raise OverflowError( "La confianza es demasiado cercana a 1 y el valor Z se vuelve infinito. " "Usa una confianza menor (por ejemplo 0.999999 o menos)." )

    return z


# Calculo de la muestra dada la confianza, sigma y el margen de error
def calcular_media(confianza: float, sigma: float, margen_error: float):
    """
    Calcula tamaño de muestra para estimar una MEDIA.
    Fórmula: n = (Z * sigma / E)^2

    Retorna:
    - z (float)
    - n_crudo (str)  -> string para poder imprimir números gigantes sin overflow de float
    - n_final (int)
    - supuestos (list[str])
    """
    # Validaciones
    if sigma <= 0:
        raise ValueError("sigma debe ser mayor que 0.")
    if margen_error <= 0:
        raise ValueError("El margen de error debe ser mayor que 0.")

    # Calcular Z (float)
    z = calcular_z(confianza)

    # Configurar precisión alta para Decimal
    getcontext().prec = 80

    # Pasar datos a Decimal (evita problemas por representación binaria)
    Z = Decimal(str(z))
    SIGMA = Decimal(str(sigma))
    E = Decimal(str(margen_error))

    # Calcular con Decimal para evitar overflow
    ratio = (Z * SIGMA) / E
    n_crudo_dec = ratio * ratio
    n_final = ceil_decimal(n_crudo_dec)

    # Supuestos
    supuestos = []
    supuestos.append("Se asume muestreo aleatorio y representativo de la población.")
    supuestos.append("Se asume independencia entre observaciones.")
    if n_final >= 30:
        supuestos.append(
            "Dado que n ≥ 30, la aproximación normal para la media es razonable (Teorema Central del Límite)."
        )
    else:
        supuestos.append(
            "Como n < 30, se asume que la variable en la población tiene una distribución aproximadamente normal."
        )
    supuestos.append(
        "La desviación estándar utilizada (σ o S piloto) representa adecuadamente la variabilidad poblacional."
    )
    supuestos.append("El margen de error E se interpreta en las mismas unidades que la variable medida.")

    # Devolvemos n_crudo como string para imprimirlo completo
    return z, str(n_crudo_dec), n_final, supuestos


# Calculo de proporcion dada la confianza, p y magen de error
def calcular_proporcion(confianza: float, p: float, margen_error: float, uso_conservador: bool = False):
    """
    Calcula tamaño de muestra para estimar una PROPORCIÓN.
    Fórmula: n = (Z^2 * p(1-p)) / E^2

    Parámetro:
    - uso_conservador: True si el usuario eligió p=0.5 como caso conservador

    Retorna:
    - z (float)
    - n_crudo (str) -> string para imprimir números gigantes
    - n_final (int)
    - supuestos (list[str]) -> personalizados
    """
    
    # Validaciones
    if margen_error <= 0:
        raise ValueError("El margen de error debe ser mayor que 0.")
    if p <= 0 or p >= 1:
        raise ValueError("p debe cumplir 0 < p < 1.")

    # Calculo de z
    z = calcular_z(confianza)

    # Precisión Decimal
    getcontext().prec = 80

    # Convertir a Decimal
    Z = Decimal(str(z))
    P = Decimal(str(p))
    E = Decimal(str(margen_error))

    # Cálculo con Decimal
    numerador = (Z * Z) * P * (Decimal("1") - P)
    denominador = E * E
    n_crudo_dec = numerador / denominador
    n_final = ceil_decimal(n_crudo_dec)

    # Supuestos
    supuestos = []
    supuestos.append("Se asume muestreo aleatorio y representativo de la población.")
    supuestos.append("Se asume independencia entre observaciones.")

    # Condición de aproximación normal para proporciones (usando n_final como entero)
    np_val = n_final * p
    n1p_val = n_final * (1 - p)

    if np_val >= 5 and n1p_val >= 5:
        supuestos.append(
            f"Se cumple np = {np_val:.2f} ≥ 5 y n(1-p) = {n1p_val:.2f} ≥ 5; la aproximación normal es válida."
        )
    else:
        supuestos.append(
            f"No se cumple completamente np = {np_val:.2f} ≥ 5 y/o n(1-p) = {n1p_val:.2f} ≥ 5; "
            "la aproximación normal podría no ser adecuada."
        )

    if uso_conservador and abs(p - 0.5) < 1e-12:
        supuestos.append("Se utilizó p = 0.5 como caso conservador (maximiza p(1-p) y produce el mayor n).")
    else:
        supuestos.append("La proporción p utilizada proviene de una estimación previa o datos piloto.")

    supuestos.append("El margen de error E se interpreta como proporción (por ejemplo, 0.05 = 5%).")

    return z, str(n_crudo_dec), n_final, supuestos