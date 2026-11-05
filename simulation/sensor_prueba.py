
from machine import Pin, I2C
import time

# ==================================
# 1. CONFIGURACION DEL ESP32
# ==================================

i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=100000
)

MPU = 0x68

# ==================================
# 2. VERIFICAR SENSOR
# ==================================

print("Buscando MPU6050...")

dispositivos = i2c.scan()
print("Dispositivos encontrados:", dispositivos)

if MPU not in dispositivos:
    print("ERROR: MPU6050 no detectado")
    raise Exception("Revisar conexiones I2C")

print("MPU6050 conectado correctamente")

# ==================================
# 3. CONFIGURAR MPU6050
# ==================================

# Despertar sensor
i2c.writeto_mem(MPU, 0x6B, b'\x00')
time.sleep_ms(100)

# Acelerometro: rango +/- 2g
i2c.writeto_mem(MPU, 0x1C, b'\x00')

# Giroscopio: rango +/- 250 grados/s
i2c.writeto_mem(MPU, 0x1B, b'\x00')

time.sleep_ms(100)

# ==================================
# 4. FUNCION PARA LEER DATOS
# ==================================

def leer_sensor():

    datos = i2c.readfrom_mem(MPU, 0x3B, 14)

    ax = int.from_bytes(datos[0:2], 'big', True) / 16384
    ay = int.from_bytes(datos[2:4], 'big', True) / 16384
    az = int.from_bytes(datos[4:6], 'big', True) / 16384

    gx = int.from_bytes(datos[8:10], 'big', True) / 131
    gy = int.from_bytes(datos[10:12], 'big', True) / 131
    gz = int.from_bytes(datos[12:14], 'big', True) / 131

    return ax, ay, az, gx, gy, gz

# ==================================
# 5. CALIBRAR GIROSCOPIO
# ==================================

print()
print("CALIBRANDO GIROSCOPIO")
print("No muevas el sensor...")

sx = 0
sy = 0
sz = 0

N = 500

for i in range(N):

    ax, ay, az, gx, gy, gz = leer_sensor()

    sx += gx
    sy += gy
    sz += gz

    time.sleep_ms(5)

offset_x = sx / N
offset_y = sy / N
offset_z = sz / N

print("Calibracion terminada")
print("Offsets:", offset_x, offset_y, offset_z)

# ==================================
# 6. LECTURA CONTINUA
# ==================================

print()
print("LEYENDO MPU6050...")
print("Presiona STOP para detener")

while True:

    ax, ay, az, gx, gy, gz = leer_sensor()

    # Corregir giroscopio
    gx = gx - offset_x
    gy = gy - offset_y
    gz = gz - offset_z

    print("Aceleracion (g):",
          round(ax, 2),
          round(ay, 2),
          round(az, 2))

    print("Giroscopio (grados/s):",
          round(gx, 2),
          round(gy, 2),
          round(gz, 2))

    print("-------------------------")

    time.sleep_ms(500)
