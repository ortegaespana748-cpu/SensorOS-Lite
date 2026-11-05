from machine import Pin, I2C
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
MPU = 0x68

i2c.writeto_mem(MPU, 0x6B, b'\x00')
i2c.writeto_mem(MPU, 0x1B, b'\x00')

time.sleep_ms(200)

def convertir(datos, posicion):
    valor = (datos[posicion] << 8) | datos[posicion + 1]
    if valor >= 32768:
        valor -= 65536
    return valor

def leer_giroscopio():
    datos = i2c.readfrom_mem(MPU, 0x43, 6)

    gx = convertir(datos, 0) / 131
    gy = convertir(datos, 2) / 131
    gz = convertir(datos, 4) / 131

    return gx, gy, gz

print("CALIBRANDO GIROSCOPIO")
print("No mueva el sensor")

sx = 0
sy = 0
sz = 0

for i in range(500):
    gx, gy, gz = leer_giroscopio()

    sx += gx
    sy += gy
    sz += gz

    time.sleep_ms(5)

offset_x = sx / 500
offset_y = sy / 500
offset_z = sz / 500

print("Offsets calculados:")
print(offset_x, offset_y, offset_z)

print("INICIANDO LECTURA CORREGIDA")

while True:
    gx, gy, gz = leer_giroscopio()

    gx -= offset_x
    gy -= offset_y
    gz -= offset_z

    print(
        "GX:", round(gx, 2),
        "GY:", round(gy, 2),
        "GZ:", round(gz, 2)
    )

    time.sleep_ms(500)