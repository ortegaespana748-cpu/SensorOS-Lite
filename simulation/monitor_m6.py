
# SensorOS-Lite - M6
# Monitor y registro CSV
# Simulacion para Windows

import csv
import gc
import os
import time
from datetime import datetime

INTERVALO_SEGUNDOS = 5
DURACION_SEGUNDOS = 15

PROCESOS = [
    {"pid": 1, "nombre": "Muestreo", "estado": "LISTO"},
    {"pid": 2, "nombre": "Rasgos", "estado": "LISTO"},
    {"pid": 3, "nombre": "Modelo", "estado": "LISTO"},
    {"pid": 4, "nombre": "Registro", "estado": "LISTO"},
    {"pid": 5, "nombre": "Salida", "estado": "LISTO"},
    {"pid": 6, "nombre": "Monitor", "estado": "EJECUCION"},
]


def memoria_disponible():
    # gc.mem_free existe en MicroPython, no en Python de escritorio.
    if hasattr(gc, "mem_free"):
        return gc.mem_free()

    # En Windows no se puede obtener la RAM libre con gc.
    return -1


def main():
    os.makedirs("results/csv", exist_ok=True)
    archivo_csv = "results/csv/monitor_m6.csv"

    inicio = time.perf_counter()
    siguiente = inicio
    muestras = 0

    with open(archivo_csv, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        escritor.writerow([
            "fecha_hora",
            "tiempo_s",
            "cpu_util_aprox_pct",
            "ram_libre_bytes",
            "plazos_incumplidos",
            "pid",
            "proceso",
            "estado"
        ])

        print("SensorOS-Lite - Monitor M6")
        print("Duracion:", DURACION_SEGUNDOS, "segundos")
        print("Intervalo:", INTERVALO_SEGUNDOS, "segundos")

        while True:
            ahora = time.perf_counter()
            tiempo_transcurrido = ahora - inicio

            if tiempo_transcurrido >= DURACION_SEGUNDOS:
                break

            gc.collect()

            # Solo es una estimacion de actividad del bucle,
            # no una medicion real de CPU del sistema operativo.
            cpu_aprox = 0.0
            ram_libre = memoria_disponible()

            fecha = datetime.now().isoformat(timespec="seconds")

            for proceso in PROCESOS:
                escritor.writerow([
                    fecha,
                    round(tiempo_transcurrido, 3),
                    cpu_aprox,
                    ram_libre,
                    0,
                    proceso["pid"],
                    proceso["nombre"],
                    proceso["estado"]
                ])

            archivo.flush()
            muestras += 1

            print(
                "Registro", muestras,
                "| tiempo:", round(tiempo_transcurrido, 2), "s",
                "| procesos:", len(PROCESOS)
            )

            siguiente += INTERVALO_SEGUNDOS
            espera = siguiente - time.perf_counter()

            if espera > 0:
                time.sleep(espera)

    print("\nMonitor finalizado.")
    print("CSV generado:", archivo_csv)
    print("Registros temporales:", muestras)
    print("CPU y RAM real por proceso: pendientes de integrar al kernel.")


if __name__ == "__main__":
    main()
