
import time
import math
import csv
import os

FRECUENCIA = 100
PERIODO = 1.0 / FRECUENCIA
NUM_MUESTRAS = 20


def leer_sensor_simulado(indice):
    t = indice * PERIODO

    ax = 0.05 * math.sin(2 * math.pi * 2 * t)
    ay = 0.04 * math.cos(2 * math.pi * 2 * t)
    az = 1.0 + 0.03 * math.sin(2 * math.pi * t)

    return ax, ay, az


def main():
    print("=" * 45)
    print("SENSOROS-LITE - H0")
    print("Simulacion del sensor MPU6050")
    print("=" * 45)

    nombre_csv = "h0_simulation.csv"

    with open(nombre_csv, "w", newline="") as archivo:
        escritor = csv.writer(archivo)

        escritor.writerow([
            "indice", "tiempo_s",
            "ax_g", "ay_g", "az_g", "modo"
        ])

        inicio = time.perf_counter()

        for i in range(NUM_MUESTRAS):
            ax, ay, az = leer_sensor_simulado(i)

            escritor.writerow([
                i,
                round(i * PERIODO, 4),
                round(ax, 6),
                round(ay, 6),
                round(az, 6),
                "SINTETICO"
            ])

            print(
                "Muestra:", i,
                "| Ax:", round(ax, 3),
                "| Ay:", round(ay, 3),
                "| Az:", round(az, 3)
            )

            objetivo = inicio + (i + 1) * PERIODO
            espera = objetivo - time.perf_counter()

            if espera > 0:
                time.sleep(espera)

    print("\nSimulacion terminada correctamente.")
    print("Archivo generado:", nombre_csv)
    print("Son datos sinteticos, no reales.")


if __name__ == "__main__":
    main()
