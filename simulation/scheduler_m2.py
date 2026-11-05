
# SensorOS-Lite ft
# M2: Comparacion de algoritmos de planificacion
# Simulacion para Windows

import time

TRABAJOS_BASE = [
    {"pid": 1, "nombre": "Muestreo", "rafagas": 5, "prioridad": 1},
    {"pid": 2, "nombre": "Rasgos", "rafagas": 3, "prioridad": 2},
    {"pid": 3, "nombre": "Modelo", "rafagas": 4, "prioridad": 2},
    {"pid": 4, "nombre": "Registro", "rafagas": 2, "prioridad": 3},
    {"pid": 5, "nombre": "Salida", "rafagas": 2, "prioridad": 3},
    {"pid": 6, "nombre": "Monitor", "rafagas": 3, "prioridad": 4},
]


def preparar_trabajos():
    trabajos = []

    for original in TRABAJOS_BASE:
        trabajos.append({
            **original,
            "restante": original["rafagas"],
            "llegada": 0,
            "primera_respuesta": None,
            "fin": None,
            "espera": 0,
        })

    return trabajos


def ejecutar_fcfs():
    trabajos = preparar_trabajos()
    reloj = 0
    eventos = []

    for trabajo in trabajos:
        trabajo["primera_respuesta"] = reloj
        eventos.append((reloj, trabajo["pid"], "FCFS"))

        reloj += trabajo["rafagas"]
        trabajo["fin"] = reloj

    return trabajos, eventos, reloj


def ejecutar_rr(quantum):
    trabajos = preparar_trabajos()
    reloj = 0
    cola = list(trabajos)
    eventos = []

    while cola:
        trabajo = cola.pop(0)

        if trabajo["restante"] <= 0:
            continue

        if trabajo["primera_respuesta"] is None:
            trabajo["primera_respuesta"] = reloj

        duracion = min(quantum, trabajo["restante"])
        eventos.append((reloj, trabajo["pid"], "RR"))

        trabajo["restante"] -= duracion
        reloj += duracion

        if trabajo["restante"] == 0:
            trabajo["fin"] = reloj
        else:
            cola.append(trabajo)

    return trabajos, eventos, reloj


def ejecutar_prioridades_envejecimiento():
    trabajos = preparar_trabajos()
    reloj = 0
    eventos = []
    pendientes = list(trabajos)

    # La prioridad numerica mas baja es la mas alta.
    # Cada unidad de espera mejora la prioridad efectiva.
    while pendientes:
        for trabajo in pendientes:
            trabajo["espera"] = reloj - trabajo["llegada"]

        elegido = min(
            pendientes,
            key=lambda t: (
                max(1, t["prioridad"] - t["espera"] // 3),
                t["pid"]
            )
        )

        if elegido["primera_respuesta"] is None:
            elegido["primera_respuesta"] = reloj

        eventos.append((reloj, elegido["pid"], "PRIORIDADES"))

        reloj += elegido["rafagas"]
        elegido["fin"] = reloj
        pendientes.remove(elegido)

    return trabajos, eventos, reloj


def mostrar_resultados(nombre, resultado):
    trabajos, eventos, tiempo_total = resultado

    print("\n=== {} ===".format(nombre))
    print("Orden:", [evento[1] for evento in eventos])
    print("PID | Espera | Retorno | Respuesta")

    for t in trabajos:
        espera = t["primera_respuesta"] - t["llegada"]
        retorno = t["fin"] - t["llegada"]
        respuesta = t["primera_respuesta"] - t["llegada"]

        print(
            "{:3d} | {:6d} | {:7d} | {:9d}".format(
                t["pid"], espera, retorno, respuesta
            )
        )

    print("Tiempo total:", tiempo_total, "unidades")


def main():
    print("SensorOS-Lite - M2")
    print("Simulacion de planificacion")

    while True:
        print("\nSelecciona un algoritmo:")
        print("1. FCFS")
        print("2. Round Robin (quantum 1)")
        print("3. Round Robin (quantum 2)")
        print("4. Prioridades con envejecimiento")
        print("5. Ejecutar todos")
        print("0. Salir")

        opcion = input("Opcion: ").strip()

        if opcion == "1":
            mostrar_resultados("FCFS", ejecutar_fcfs())
        elif opcion == "2":
            mostrar_resultados("Round Robin Q=1", ejecutar_rr(1))
        elif opcion == "3":
            mostrar_resultados("Round Robin Q=2", ejecutar_rr(2))
        elif opcion == "4":
            mostrar_resultados(
                "Prioridades con envejecimiento",
                ejecutar_prioridades_envejecimiento()
            )
        elif opcion == "5":
            mostrar_resultados("FCFS", ejecutar_fcfs())
            mostrar_resultados("Round Robin Q=1", ejecutar_rr(1))
            mostrar_resultados("Round Robin Q=2", ejecutar_rr(2))
            mostrar_resultados(
                "Prioridades con envejecimiento",
                ejecutar_prioridades_envejecimiento()
            )
        elif opcion == "0":
            print("Fin de M2.")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()
