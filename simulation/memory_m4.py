
# SensorOS-Lite - M4
# Administracion de memoria: simulacion inicial
# Universidad de Sucre-SO

import gc
import sys


class GestorMemoria:
    def __init__(self):
        self.cuotas = {
            1: 8 * 1024,
            2: 4 * 1024,
            3: 16 * 1024,
            4: 8 * 1024,
            5: 2 * 1024,
            6: 4 * 1024,
        }

        self.activos = {pid: True for pid in self.cuotas}
        self.usos = {pid: 0 for pid in self.cuotas}

    def reservar(self, pid, cantidad):
        if not self.activos.get(pid, False):
            print("P{} ya esta detenido.".format(pid))
            return False

        nuevo_uso = self.usos[pid] + cantidad
        cuota = self.cuotas[pid]

        if nuevo_uso > cuota:
            self.activos[pid] = False
            print(
                "OOM: P{} excedio su cuota de {} bytes.".format(
                    pid, cuota
                )
            )
            print("P{} detenido por el gestor.".format(pid))
            return False

        self.usos[pid] = nuevo_uso

        print(
            "P{}: uso simulado = {} / {} bytes".format(
                pid, nuevo_uso, cuota
            )
        )

        return True

    def mostrar_estado(self):
        print("\n=== Estado de memoria por proceso ===")

        for pid in sorted(self.cuotas):
            estado = "ACTIVO" if self.activos[pid] else "DETENIDO"

            print(
                "P{} | cuota={} B | uso_contabilizado={} B | {}".format(
                    pid,
                    self.cuotas[pid],
                    self.usos[pid],
                    estado
                )
            )


def main():
    print("=" * 50)
    print("SensorOS-Lite - M4")
    print("Simulacion de cuotas de memoria")
    print("=" * 50)

    gc.collect()

    memoria_inicial = (
        getattr(gc, "mem_alloc", lambda: 0)()
    )
    memoria_final = None

    gestor = GestorMemoria()

    # Reservas contabilizadas por el gestor.
    gestor.reservar(1, 2048)
    gestor.reservar(2, 1024)
    gestor.reservar(3, 4096)

    # Provocar exceso de cuota en P5:
    # su cuota es de 2048 bytes.
    gestor.reservar(5, 1536)
    gestor.reservar(5, 1024)

    # El sistema continua atendiendo otros procesos.
    gestor.reservar(1, 1024)
    gestor.reservar(6, 1024)

    gestor.mostrar_estado()

    # Medicion aproximada del objeto en Python de escritorio.
    ejemplo = bytearray(1024)
    print("\nTamanio del objeto de prueba:", sys.getsizeof(ejemplo))
    print("Memoria asignada por Python:", memoria_inicial, "bytes")

    del ejemplo
    gc.collect()

    memoria_final = (
        getattr(gc, "mem_alloc", lambda: 0)()
    )

    print("Memoria despues de limpieza:", memoria_final, "bytes")
    print("Fin de la simulacion M4.")
    print("Las cuotas son contabilidad simulada, no RAM real por proceso.")


if __name__ == "__main__":
    main()
