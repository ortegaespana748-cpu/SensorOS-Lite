
# SensorOS-Lite
# M1: Procesos y PCB
# Primera version de simulacion del kernel

import time

ESTADOS = (
    "NUEVO",
    "LISTO",
    "EJECUCION",
    "BLOQUEADO",
    "TERMINADO"
)


class PCB:
    def __init__(self, pid, nombre, prioridad):
        self.pid = pid
        self.nombre = nombre
        self.estado = "NUEVO"
        self.prioridad = prioridad
        self.activaciones = 0
        self.unidades_trabajo = 0

    def mostrar(self):
        print(
            "P{} | {:12s} | Estado: {:12s} | "
            "Prioridad: {} | Ejecuciones: {}".format(
                self.pid,
                self.nombre,
                self.estado,
                self.prioridad,
                self.activaciones
            )
        )


def proceso_muestreo():
    for i in range(3):
        print("P1: muestra simulada", i)
        yield


def proceso_rasgos():
    for i in range(3):
        print("P2: calculando rasgos", i)
        yield


def proceso_modelo():
    for i in range(3):
        print("P3: clasificacion simulada", i)
        yield


def proceso_registro():
    for i in range(3):
        print("P4: registro simulado", i)
        yield


def proceso_salida():
    for i in range(3):
        print("P5: mostrando resultado", i)
        yield


def proceso_monitor():
    for i in range(3):
        print("P6: monitor activo", i)
        yield


def main():
    procesos = [
        (PCB(1, "Muestreo", 1), proceso_muestreo()),
        (PCB(2, "Rasgos", 2), proceso_rasgos()),
        (PCB(3, "Modelo", 2), proceso_modelo()),
        (PCB(4, "Registro", 3), proceso_registro()),
        (PCB(5, "Salida", 3), proceso_salida()),
        (PCB(6, "Monitor", 4), proceso_monitor())
    ]

    print("=== SensorOS-Lite: M1 ===")

    for pcb, generador in procesos:
        pcb.estado = "LISTO"

    activos = True

    while activos:
        activos = False

        for pcb, generador in procesos:
            if pcb.estado == "TERMINADO":
                continue

            activos = True
            pcb.estado = "EJECUCION"

            try:
                next(generador)
                pcb.activaciones += 1
                pcb.unidades_trabajo += 1
                pcb.estado = "LISTO"

            except StopIteration:
                pcb.estado = "TERMINADO"

        print("\n--- Estado de los procesos ---")
        for pcb, generador in procesos:
            pcb.mostrar()

        time.sleep(0.2)

    print("\nLos seis procesos terminaron.")
    print("Fin de la simulacion M1.")


if __name__ == "__main__":
    main()
