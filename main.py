import math                          # Para usar ceil (redondear hacia arriba)
from statistics import NormalDist    # Para calcular Z sin usar tabla


# Funcion para calcular Z, apartir del nivel de confianza
def calcular_z(confianza):
    # Validamos que la confianza esté en un rango válido
    if confianza <= 0 or confianza >= 1:
        raise ValueError("La confianza debe estar entre 0 y 1 (ejemplo: 0.95).")

    # alpha es la probabilidad de error
    alpha = 1 - confianza

    # Usamos la inversa de la normal estándar (intervalo bilateral)
    z = NormalDist().inv_cdf(1 - alpha / 2)

    return z

# Funcion para calcular la media
def Media():
    print("\n--- CÁLCULO DE TAMAÑO DE MUESTRA PARA LA MEDIA ---")

    # Pedimos nivel de confianza validando la entrada (unicamente numeros)
    try:
        confianza = float(input("Ingresa el nivel de confianza (ej. 0.95): ").strip())
    except ValueError:
        print("Error: La confianza debe ser un número.")
        return

    # Calculamos Z con la funcion definida
    try:
        z = calcular_z(confianza)
    except ValueError as error:
        print(f"Error: {error}")
        return

    # Pedimos Sigma o S (piloto) y validamos su entrada
    try:
        sigma = float(input("Ingresa la desviación estándar sigma (> 0): ").strip())
    except ValueError:
        print("Error: sigma debe ser un número.")
        return

    if sigma <= 0:
        print("Error: sigma debe ser mayor que 0.")
        return

    # Pedimos margen de error y validamos su entrada
    try:
        margen_error = float(input("Ingresa el margen de error E (> 0): ").strip())
    except ValueError:
        print("Error: El margen de error debe ser un número.")
        return

    if margen_error <= 0:
        print("Error: El margen de error debe ser mayor que 0.")
        return

    # Calculamos tamaño de muestra
    n_sin_redondeo = ((z * sigma) / margen_error) ** 2

    # Redondeamos siempre hacia arriba
    n_final = math.ceil(n_sin_redondeo)

    # MOSTRAR RESULTADOS
    print("\n--- RESULTADOS ---")
    print(f"Nivel de confianza: {confianza}")
    print(f"Valor Z utilizado: {z:.5f}")
    print("Fórmula utilizada: n = (Z * sigma / E)^2")
    print(f"Tamaño de muestra (sin redondear): {n_sin_redondeo:.4f}")
    print(f"Tamaño de muestra (redondeado): {n_final}")

    # SUPUESTOS
    print("\nSupuestos estadísticos:")
    print("- El muestreo es aleatorio y representativo.")
    print("- Las observaciones son independientes.")
    print("- La desviación estándar es conocida o bien estimada.")
    print("- La aproximación normal es válida o el tamaño de muestra es suficientemente grande.")

    input("\nPresiona ENTER para volver al menú...")

# Función Proporción
def Proporcion():
    print("\n--- CÁLCULO DE TAMAÑO DE MUESTRA PARA PROPORCIÓN ---")

    # Pedimos nivel de confianza
    try:
        confianza = float(input("Ingresa el nivel de confianza (ej. 0.95): ").strip())
    except ValueError:
        print("Error: La confianza debe ser un número.")
        return

    # Calculamos Z usando la función existente
    try:
        z = calcular_z(confianza)
    except ValueError as error:
        print(f"Error: {error}")
        return

    # Pedimos margen de error
    try:
        margen_error = float(input("Ingresa el margen de error E (> 0): ").strip())
    except ValueError:
        print("Error: El margen de error debe ser un número.")
        return

    if margen_error <= 0:
        print("Error: El margen de error debe ser mayor que 0.")
        return

    # 4. Preguntamos si desea usar el caso conservador
    opcion = input(
        "¿Deseas usar el caso conservador?\n"
        "1. Sí (p = 0.5)\n"
        "2. No\n"
        "Ingresa la opción: "
    ).strip()

    if opcion == "1":
        estimacion = 0.5
    elif opcion == "2":
        try:
            estimacion = float(input("Ingresa la estimación deseada (p): ").strip())
        except ValueError:
            print("Error: La estimación debe ser un número.")
            return

        if estimacion <= 0 or estimacion >= 1:
            print("Error: la estimación p debe cumplir 0 < p < 1.")
            return
    else:
        print("Opción no válida.")
        return

    # 5. Cálculo del tamaño de muestra
    # Fórmula: n = (Z^2 * p * (1 - p)) / E^2
    n_sin_redondeo = (z ** 2 * estimacion * (1 - estimacion)) / (margen_error ** 2)

    # Redondeo hacia arriba
    n_final = math.ceil(n_sin_redondeo)

    # 6. Mostrar resultados
    print("\n--- RESULTADOS (PROPORCIÓN) ---")
    print(f"Nivel de confianza: {confianza}")
    print(f"Valor Z utilizado: {z:.5f}")
    print("Fórmula utilizada: n = (Z^2 * p * (1 - p)) / E^2")
    print(f"Estimación utilizada (p): {estimacion}")
    print(f"n (sin redondear): {n_sin_redondeo:.4f}")
    print(f"n (redondeado): {n_final}")

    # 7. Supuestos
    print("\nSupuestos estadísticos:")
    print("- Muestreo aleatorio y representativo.")
    print("- Observaciones independientes.")
    print("- Aproximación normal válida para proporciones.")
    print("- Si p es desconocida, p = 0.5 produce el tamaño de muestra más conservador.")

    input("\nPresiona ENTER para volver al menú...")
 

# MENÚ PRINCIPAL
def main():
    salida = False

    while not salida:
        print("\n------ CALCULADORA DE TAMAÑO MUESTRAL ------")
        print("1. Calcular para MEDIA")
        print("2. Calcular para PROPORCIÓN")
        print("0. Salir")

        opcion = input("Ingresa una opción: ").strip()

        if opcion == "1":
            Media()
        elif opcion == "2":
            Proporcion()
        elif opcion == "0":
            print("Programa terminado.")
            salida = True
        else:
            print("Opción no válida. Intenta nuevamente.")


# =========================
# PUNTO DE ENTRADA
# =========================
main()
