
from machine import Pin, I2C
import time

# Configuracion I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
MPU = 0x68

print("Buscando MPU6050...")

if MPU not in i2c.scan():
    raise Exception("MPU6050 no detectado")

# Despertar sensor
i2c.writeto_mem(MPU, 0x6B, b'\x00')
time.sleep_ms(100)

# Configurar giroscopio: +/- 250 grados/s
i2c.writeto_mem(MPU, 0x1B, b'\x00')
time.sleep_ms(100)

# Comprobar configuracion
config = i2c.readfrom_mem(MPU, 0x1B, 1)
print("Registro de configuracion:", config[0])

# Convertir dato de 16 bits a entero con signo
def convertir(datos):
    valor = int.from_bytes(datos, 'big')
    if valor >= 32768:
        valor -= 65536
    return valor

# Leer giroscopio
def leer_giroscopio():
    datos = i2c.readfrom_mem(MPU, 0x43, 6)

    gx = convertir(datos[0:2]) / 131
    gy = convertir(datos[2:4]) / 131
    gz = convertir(datos[4:6]) / 131

    return gx, gy, gz

# Calibracion
print("Calibrando...")
print("NO MUEVAS EL SENSOR")

sx = 0
sy = 0
sz = 0

MUESTRAS = 500

for i in range(MUESTRAS):
    gx, gy, gz = leer_giroscopio()

    sx += gx
    sy += gy
    sz += gz

    time.sleep_ms(5)

offset_x = sx / MUESTRAS
offset_y = sy / MUESTRAS
offset_z = sz / MUESTRAS

print("Calibracion terminada")
print("Offsets:", offset_x, offset_y, offset_z)

# Lectura corregida
print("Lectura en tiempo real")

while True:
    gx, gy, gz = leer_giroscopio()

    gx -= offset_x
    gy -= offset_y
    gz -= offset_z

    print("Giroscopio:", round(gx, 2),
          round(gy, 2), round(gz, 2))

    time.sleep_ms(500)
