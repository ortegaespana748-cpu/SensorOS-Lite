# SensorOS-Lite

## Sistema operativo cooperativo para ESP32 con MicroPython y TinyML

**Proyecto académico – Sistema Operativo Avanzado**  
**Universidad de Sucre – Programa de Ingeniería Electrónica**

## 1. Descripción del proyecto

SensorOS-Lite es un proyecto académico orientado al desarrollo de un sistema operativo ligero para ESP32 utilizando MicroPython.

El sistema busca implementar un kernel cooperativo con planificación de tareas, mecanismos de sincronización, gestión de memoria y monitorización. Además, incorpora el sensor MPU6050 para obtener información de movimiento y desarrollar un sistema de clasificación mediante técnicas de TinyML.

## 2. Objetivo general

Desarrollar e implementar un sistema operativo cooperativo ligero en un ESP32 que permita administrar procesos, recursos de memoria y datos provenientes del sensor MPU6050, integrando un modelo de aprendizaje automático para reconocer diferentes patrones de movimiento.

## 3. Hardware y herramientas

### Hardware
- ESP32 ESP-WROOM-32.
- Sensor MPU6050.
- Conexión I2C.
- Computador para desarrollo y entrenamiento del modelo.

### Software
- MicroPython.
- Thonny IDE.
- Python.
- Git y GitHub.
- Herramientas de análisis y entrenamiento TinyML.

## 4. Arquitectura del proyecto

El proyecto contempla seis procesos principales:

| Proceso | Función |
|---|---|
| P1 – Muestreo | Captura de datos del MPU6050 a 100 Hz. |
| P2 – Rasgos | Extracción de características de las señales. |
| P3 – Modelo | Clasificación de patrones de movimiento. |
| P4 – Registro | Almacenamiento de datos y resultados. |
| P5 – Salida | Presentación de resultados de clasificación. |
| P6 – Monitor | Supervisión de CPU, memoria y plazos. |

## 5. Módulos de desarrollo

- **H0:** configuración inicial y comprobación del hardware.
- **M1:** kernel cooperativo y administración de procesos.
- **M2:** planificación de tareas y métricas.
- **M3:** sincronización mediante semáforos y mutex.
- **M4:** gestión de memoria y control de recursos.
- **M5:** extracción de características e integración de TinyML.
- **M6:** monitorización y registro de métricas en CSV.

## 6. Estructura actual del repositorio

```text
SensorOS-Lite/
└── simulation/
    ├── h0_simulation.py
    ├── h0_simulation.csv
    ├── kernel_m1.py
    ├── scheduler_m2.py
    ├── sync_m3.py
    ├── memory_m4.py
    ├── tinyml_m5.py
    ├── monitor_m6.py
    ├── diagnostico_mpu6050.py
    ├── sensor_integrado.py
    ├── sensor_prueba.py
    ├── prueba_acelerometro.py
    ├── prueba_giroscopio.py
    ├── Prueba.py
    └── results/
        └── csv/
            └── monitor_m6.csv
```

## 7. Estado actual del desarrollo

El repositorio contiene una primera versión de los módulos de simulación H0, M1, M2, M3, M4 y M6, además de programas de prueba del sensor MPU6050.

El módulo M5 se encuentra pendiente de implementación. También están pendientes la integración completa de los módulos en el ESP32 y la validación experimental del sistema.

## 8. Objetivo final

Implementar un sistema funcional en el ESP32 que permita adquirir señales del MPU6050, ejecutar tareas cooperativas, administrar recursos, clasificar patrones de movimiento y registrar métricas de funcionamiento.

## 9. Repositorio

[SensorOS-Lite – GitHub](https://github.com/ortegaespana748-cpu/SensorOS-Lite)

---

**Proyecto académico – Ingeniería Electrónica**  
**Universidad de Sucre**
