import time
import board
import busio
import adafruit_icm20x

# I2C setup on GPIO 2 (SDA) and GPIO 3 (SCL)
i2c = busio.I2C(scl=board.SCL, sda=board.SDA)
icm = adafruit_icm20x.ICM20948(i2c, address=0x68)

print("Adafruit ICM20948 test!")

# Print accelerometer range
accel_range = icm.accel_range
print(f"Accelerometer range set to: {accel_range} G")

# Print gyro range
gyro_range = icm.gyro_range
print(f"Gyro range set to: {gyro_range} dps")

# Print accelerometer data rate
accel_rate = 1125 / (1.0 + icm.accel_rate_divisor)
print(f"Accelerometer data rate (Hz) is approximately: {accel_rate:.2f}")

# Print gyro data rate
gyro_rate = 1100 / (1.0 + icm.gyro_rate_divisor)
print(f"Gyro data rate (Hz) is approximately: {gyro_rate:.2f}")

# Print magnetometer data rate
mag_rate = icm.mag_data_rate
print(f"Magnetometer data rate: {mag_rate}")

print("\nStarting sensor readings...\n")

while True:
    accel = icm.acceleration    # tuple: (x, y, z) in m/s^2
    gyro = icm.gyro             # tuple: (x, y, z) in rad/s
    mag = icm.magnetometer      # tuple: (x, y, z) in microtesla
    temp = icm.temperature      # in °C

    print(f"\tTemperature: {temp:.2f} °C")

    print(f"\tAccel X: {accel[0]:.3f} \tY: {accel[1]:.3f} \tZ: {accel[2]:.3f} m/s²")
    print(f"\tMag X: {mag[0]:.3f} \tY: {mag[1]:.3f} \tZ: {mag[2]:.3f} µT")
    print(f"\tGyro X: {gyro[0]:.3f} \tY: {gyro[1]:.3f} \tZ: {gyro[2]:.3f} rad/s\n")

    time.sleep(0.1)  # 100ms delay like the Arduino sketch
