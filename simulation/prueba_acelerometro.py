from machine import Pin, I2C
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
MPU = 0x68

# Despertar MPU6050
i2c.writeto_mem(MPU, 0x6B, b'\x00')
time.sleep_ms(100)

# Configurar acelerometro en +/- 2g
i2c.writeto_mem(MPU, 0x1C, b'\x00')

def convertir(datos):
    valor = int.from_bytes(datos, 'big')
    if valor >= 32768:
        valor -= 65536
    return valor

while True:
    datos = i2c.readfrom_mem(MPU, 0x3B, 6)

    ax = convertir(datos[0:2]) / 16384
    ay = convertir(datos[2:4]) / 16384
    az = convertir(datos[4:6]) / 16384

    print("Aceleracion (g):",
          round(ax, 2),
          round(ay, 2),
          round(az, 2))

    time.sleep_ms(500)