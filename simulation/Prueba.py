
from machine import Pin, I2C
from time import sleep

# Configurar comunicacion I2C
i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=400000
)

print("Buscando sensor MPU6050...")

while True:
    dispositivos = i2c.scan()
    print("Dispositivos encontrados:", dispositivos)

    if 0x68 in dispositivos or 0x69 in dispositivos:
        direccion = 0x68 if 0x68 in dispositivos else 0x69

        identidad = i2c.readfrom_mem(
            direccion, 0x75, 1
        )

        print("Sensor detectado!")
        print("Direccion:", hex(direccion))
        print("WHO_AM_I:", hex(identidad[0]))
        break

    print("Sensor no encontrado. Revisar conexiones.")
    sleep(2)
