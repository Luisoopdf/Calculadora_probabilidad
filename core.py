import math
from statistics import NormalDist

#Calcular Z dada la confianza, validando intervalo de confianza
def calcular_z(confianza):
    if confianza <= 0 or confianza >= 1:
        raise ValueError("La confianza debe estar entre 0 y 1.")
    
    alpha = 1 - confianza
    return NormalDist().inv_cdf(1 - alpha / 2)

# Calcula la media dada la confianza, sigma y el margen de error validando sus entradas
def calcular_media(confianza, sigma, margen_error):
    if sigma <= 0:
        raise ValueError("sigma debe ser mayor que 0.")
    if margen_error <= 0:
        raise ValueError("El margen de error debe ser mayor que 0.")

    z = calcular_z(confianza)
    n_sin_redondeo = (z * sigma / margen_error) ** 2
    n_final = math.ceil(n_sin_redondeo)

    return z, n_sin_redondeo, n_final

# Calculo de la proporcion dada la confianza, p y margen de error, validando sus entradas
def calcular_proporcion(confianza, p, margen_error):
    if margen_error <= 0:
        raise ValueError("El margen de error debe ser mayor que 0.")
    if p <= 0 or p >= 1:
        raise ValueError("p debe cumplir 0 < p < 1.")

    z = calcular_z(confianza)
    n_sin_redondeo = (z ** 2 * p * (1 - p)) / (margen_error ** 2)
    n_final = math.ceil(n_sin_redondeo)

    return z, n_sin_redondeo, n_final