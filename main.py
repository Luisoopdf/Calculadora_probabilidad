from core import calcular_media, calcular_proporcion

# Función para calcular tamaño muestral de una media (entrada, cálculo y salida)
def Media():
    """Calcula el tamaño de muestra para estimar una media poblacional."""
    print("\n--- CÁLCULO PARA MEDIA ---")
    try:
        # Lectura de parámetros desde consola
        confianza = float(input("Confianza (ej 0.95): ").strip())
        sigma = float(input("Desviación estándar (σ o S piloto) (>0): ").strip())
        E = float(input("Margen de error E (>0): ").strip())
        # Cálculo central con la función del núcleo
        z, n_crudo, n_final, supuestos = calcular_media(confianza, sigma, E)
    except Exception as e:
        # Manejo de errores por entradas inválidas o cálculo
        print(f"Error: {e}")
        return

    # Impresión de resultados y supuestos
    print("\n--- RESULTADOS (MEDIA) ---")
    print(f"Z: {z:.5f}")
    print("Fórmula: n = (Z·σ/E)^2")
    print(f"n crudo: {n_crudo}")
    print(f"n redondeado: {n_final}")
    print("\nSupuestos:")
    for i, s in enumerate(supuestos, start=1):
        print(f"{i}. {s}")

    input("\nENTER para volver al menú...")

# Función para calcular tamaño muestral de una proporción (entrada, cálculo y salida)
def Proporcion():
    """Calcula el tamaño de muestra para estimar una proporción poblacional."""
    print("\n--- CÁLCULO PARA PROPORCIÓN ---")
    try:
        # Lectura de parámetros desde consola
        confianza = float(input("Confianza (ej 0.95): ").strip())
        E = float(input("Margen de error E (>0) (ej 0.05): ").strip())
        op = input("¿Caso conservador p=0.5? (1=Sí, 2=No): ").strip()

        # Selección de p según modo conservador
        if op == "1":
            p = 0.5
            uso_conservador = True
        elif op == "2":
            p = float(input("p (0<p<1): ").strip())
            uso_conservador = False
        else:
            print("Opción inválida.")
            return

        # Cálculo central con la función del núcleo
        z, n_crudo, n_final, supuestos = calcular_proporcion(confianza, p, E, uso_conservador)
    except Exception as e:
        # Manejo de errores por entradas inválidas o cálculo
        print(f"Error: {e}")
        return

    # Impresión de resultados y supuestos
    print("\n--- RESULTADOS (PROPORCIÓN) ---")
    print(f"Z: {z:.5f}")
    print("Fórmula: n = (Z²·p(1−p))/E²")
    print(f"p: {p}")
    print(f"n crudo: {n_crudo}")
    print(f"n redondeado: {n_final}")
    print("\nSupuestos:")
    for i, s in enumerate(supuestos, start=1):
        print(f"{i}. {s}")

    input("\nENTER para volver al menú...")

# Menú principal: navegación entre opciones y salida
def main():
    """Menú principal que gestiona la navegación entre opciones."""
    while True:
        print("\n------ CALCULADORA DE TAMAÑO MUESTRAL ------")
        print("1) Media")
        print("2) Proporción")
        print("0) Salir")
        opcion = input("Opción: ").strip()

        # Enrutamiento según opción
        if opcion == "1":
            Media()
        elif opcion == "2":
            Proporcion()
        elif opcion == "0":
            print("Listo.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    # Punto de entrada del script
    main()
