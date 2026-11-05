from machine import Pin, I2C
import time

# =====================================
# 1. CONFIGURACION DEL ESP32
# =====================================

i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=400000
)

MPU = 0x68

print("Iniciando SensorOS-Lite...")
print("Buscando MPU6050...")

dispositivos = i2c.scan()

if MPU not in dispositivos:
    print("ERROR: MPU6050 no detectado")
    raise Exception("Revisar conexiones I2C")

print("MPU6050 conectado correctamente")

# =====================================
# 2. CONFIGURACION DEL MPU6050
# =====================================

# Despertar sensor
i2c.writeto_mem(MPU, 0x6B, b'\x00')

# Acelerometro: rango +/- 2g
i2c.writeto_mem(MPU, 0x1C, b'\x00')

# Giroscopio: rango +/- 250 grados/s
i2c.writeto_mem(MPU, 0x1B, b'\x00')

time.sleep_ms(100)

# =====================================
# 3. FUNCION PARA LEER DATOS
# =====================================

def convertir(datos, posicion):
    return int.from_bytes(
        datos[posicion:posicion + 2],
        'big',
        True
    )

def leer_sensor():
    datos = i2c.readfrom_mem(MPU, 0x3B, 14)

    ax = convertir(datos, 0) / 16384
    ay = convertir(datos, 2) / 16384
    az = convertir(datos, 4) / 16384

    gx = convertir(datos, 8) / 131
    gy = convertir(datos, 10) / 131
    gz = convertir(datos, 12) / 131

    return ax, ay, az, gx, gy, gz

# =====================================
# 4. CALIBRACION DEL GIROSCOPIO
# =====================================

print("Calibrando giroscopio...")
print("Mantenga el sensor quieto")

sx = 0
sy = 0
sz = 0

for i in range(200):
    ax, ay, az, gx, gy, gz = leer_sensor()

    sx += gx
    sy += gy
    sz += gz

    time.sleep_ms(5)

offset_x = sx / 200
offset_y = sy / 200
offset_z = sz / 200

print("Calibracion terminada")
print("Offsets:", offset_x, offset_y, offset_z)

# =====================================
# 5. LECTURA INTEGRADA
# =====================================

print("Iniciando lectura de los seis ejes")

while True:

    ax, ay, az, gx, gy, gz = leer_sensor()

    # Correccion del giroscopio
    gx -= offset_x
    gy -= offset_y
    gz -= offset_z

    print("-----------------------------")

    print(
        "Aceleracion (g):",
        round(ax, 3),
        round(ay, 3),
        round(az, 3)
    )

    print(
        "Giroscopio (grados/s):",
        round(gx, 2),
        round(gy, 2),
        round(gz, 2)
    )

    time.sleep_ms(200)