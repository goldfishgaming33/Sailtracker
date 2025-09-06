import time
import csv
from datetime import datetime
import math
import board
import busio
from adafruit_icm20x import ICM20948

# I2C setup
i2c = busio.I2C(board.D3, board.D2)
sensor = ICM20948(i2c, address=0x68)

# CSV file name
csv_file = "icm20948_log.csv"

# Create CSV header if file does not exist
try:
    with open(csv_file, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Roll (deg)", "Pitch (deg)", "Heading (deg)"])
except FileExistsError:
    pass  # File already exists, skip header

def get_roll(accel):
    """
    Compute roll angle (degrees) from accelerometer data
    accel: (ax, ay, az) in m/s²
    """
    ax, ay, az = accel
    roll_rad = math.atan2(ay, az)
    return math.degrees(roll_rad)

def get_pitch(accel):
    """
    Compute pitch angle (degrees) from accelerometer data
    accel: (ax, ay, az)
    """
    ax, ay, az = accel
    pitch_rad = math.atan2(-ax, math.sqrt(ay**2 + az**2))
    return math.degrees(pitch_rad)

def get_tilt_compensated_heading(mag, accel):
    """
    Compute tilt-compensated heading (degrees)
    mag: (mx, my, mz)
    accel: (ax, ay, az)
    """
    mx, my, mz = mag
    ax, ay, az = accel

    # Calculate roll and pitch in radians
    roll = math.atan2(ay, az)
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2))

    # Tilt-compensated magnetic values
    mx_comp = mx * math.cos(pitch) + mz * math.sin(pitch)
    my_comp = mx * math.sin(roll) * math.sin(pitch) + my * math.cos(roll) - mz * math.sin(roll) * math.cos(pitch)

    # Heading
    heading_rad = math.atan2(my_comp, mx_comp)
    heading_deg = math.degrees(heading_rad)
    if heading_deg < 0:
        heading_deg += 360
    return heading_deg

while True:
    # Read sensor data
    accel = sensor.acceleration  # (ax, ay, az)
    mag = sensor.magnetic  # (mx, my, mz)

    # Calculate roll and tilt-compensated heading
    roll = get_roll(accel)
    pitch = get_pitch(accel)
    heading = get_tilt_compensated_heading(mag, accel)

    # Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Print
    print(f"[{timestamp}] Roll: {roll:.2f}°, Pitch: {pitch:.2f}°, Heading: {heading:.2f}°")

    # Log to CSV
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, f"{roll:.2f}", f"{heading:.2f}"])

    # Wait 20 seconds
    time.sleep(5)
