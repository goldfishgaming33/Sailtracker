import serial
import pynmea2

port = "/dev/serial0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)

while True:
    newdata = ser.readline().decode('ascii', errors='replace')
    if newdata.startswith("$GPRMC"):
        newmsg = pynmea2.parse(newdata)
        print(f"Latitude={newmsg.latitude} and Longitude={newmsg.longitude}")


