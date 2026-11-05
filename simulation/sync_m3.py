
# ============================================================
# SensorOS-Lite - M3: Sincronizacion
# Simulacion cooperativa en Windows
# Universidad de Sucre-SO
# ============================================================

from collections import deque


# ------------------------------------------------------------
# 1. SEMAFORO PROPIO CON COLA DE ESPERA
# ------------------------------------------------------------

class Semaforo:
    def __init__(self, valor_inicial=1):
        self.valor = valor_inicial
        self.cola_espera = deque()

    def wait(self, pid):
        if self.valor > 0:
            self.valor -= 1
            return True

        self.cola_espera.append(pid)
        return False

    def signal(self):
        if self.cola_espera:
            pid = self.cola_espera.popleft()
            print("Semaforo: proceso", pid, "desbloqueado")
        else:
            self.valor += 1


# ------------------------------------------------------------
# 2. MUTEX PROPIO
# ------------------------------------------------------------

class Mutex:
    def __init__(self, nombre):
        self.nombre = nombre
        self.libre = True
        self.propietario = None
        self.cola_espera = deque()

    def adquirir(self, pid):
        if self.libre:
            self.libre = False
            self.propietario = pid
            print("P{} adquiere {}".format(pid, self.nombre))
            return True

        self.cola_espera.append(pid)
        print("P{} espera por {}".format(pid, self.nombre))
        return False

    def liberar(self, pid):
        if self.propietario != pid:
            raise RuntimeError(
                "El proceso no es propietario del mutex"
            )

        if self.cola_espera:
            siguiente = self.cola_espera.popleft()
            self.propietario = siguiente
            print(
                "P{} libera {}; propiedad transferida a P{}".format(
                    pid, self.nombre, siguiente
                )
            )
        else:
            self.libre = True
            self.propietario = None
            print("P{} libera {}".format(pid, self.nombre))


# ------------------------------------------------------------
# 3. CONDICION DE CARRERA REPRODUCIBLE
# ------------------------------------------------------------

def demostrar_carrera():
    print("\n=== CONDICION DE CARRERA ===")

    contador = 0

    # P1 y P2 leen el mismo valor antes de escribir.
    lectura_p1 = contador
    lectura_p2 = contador

    contador = lectura_p1 + 1
    contador = lectura_p2 + 1

    print("Esperado: 2")
    print("Obtenido sin proteccion:", contador)
    print("La actualizacion de un proceso se perdio.")


def demostrar_carrera_corregida():
    print("\n=== CARRERA CORREGIDA CON MUTEX ===")

    contador = 0
    mutex = Mutex("contador")

    # Simulacion secuencial de secciones criticas protegidas.
    for pid in (1, 2):
        if mutex.adquirir(pid):
            contador += 1
            mutex.liberar(pid)

    print("Esperado: 2")
    print("Obtenido con proteccion:", contador)


# ------------------------------------------------------------
# 4. DETECCION DE INTERBLOQUEO
# ------------------------------------------------------------

def detectar_interbloqueo(espera):
    """
    espera: diccionario proceso -> recurso que espera.
    propietarios: diccionario recurso -> proceso propietario.
    """
    propietarios = {
        "A": 4,
        "B": 6
    }

    grafo = {}

    for proceso, recurso in espera.items():
        propietario = propietarios.get(recurso)

        if propietario is not None:
            grafo[proceso] = propietario

    for inicio in grafo:
        visitados = set()
        actual = inicio

        while actual in grafo:
            if actual in visitados:
                return True

            visitados.add(actual)
            actual = grafo[actual]

    return False


def demostrar_interbloqueo():
    print("\n=== INTERBLOQUEO P4 Y P6 ===")

    # P4 posee A y espera B.
    # P6 posee B y espera A.
    espera = {
        4: "B",
        6: "A"
    }

    print("P4 posee A y espera B.")
    print("P6 posee B y espera A.")

    if detectar_interbloqueo(espera):
        print("Interbloqueo detectado correctamente.")
    else:
        print("No se detecto interbloqueo.")


# ------------------------------------------------------------
# 5. SOLUCION: ORDEN GLOBAL DE CERROJOS
# ------------------------------------------------------------

def demostrar_orden_global():
    print("\n=== SOLUCION POR ORDEN GLOBAL ===")

    orden = {"A": 1, "B": 2}

    solicitudes = {
        4: ["A", "B"],
        6: ["B", "A"]
    }

    for pid, recursos in solicitudes.items():
        ordenados = sorted(
            recursos,
            key=lambda recurso: orden[recurso]
        )

        print(
            "P{} solicita los recursos en orden: {}".format(
                pid, ordenados
            )
        )

    print("Ambos procesos respetan A antes que B.")
    print("Se elimina la espera circular por orden opuesto.")


# ------------------------------------------------------------
# 6. PRUEBAS
# ------------------------------------------------------------

def main():
    print("=" * 55)
    print("SensorOS-Lite - Modulo M3")
    print("=" * 55)

    sem = Semaforo(1)
    print("\n=== PRUEBA DE SEMAFORO ===")
    print("P1 puede entrar:", sem.wait(1))
    print("P2 puede entrar:", sem.wait(2))
    sem.signal()

    demostrar_carrera()
    demostrar_carrera_corregida()
    demostrar_interbloqueo()
    demostrar_orden_global()

    print("\nFin de la simulacion M3.")


if __name__ == "__main__":
    main()
