import smbus
import time

# ----- I2C Addresses -----
ICM_ADDR = 0x68        # ICM-20948
AK_ADDR = 0x0C         # AK09916

# ----- ICM-20948 Registers (User Bank 0) -----
PWR_MGMT_1 = 0x06
USER_CTRL = 0x03
INT_PIN_CFG = 0x0F

# ----- AK09916 Registers -----
WHO_AM_I = 0x01
ST1 = 0x10
HXL = 0x11
ST2 = 0x18
CNTL2 = 0x31

# ----- Initialize I2C bus -----
bus = smbus.SMBus(1)  # Pi Zero 2 W uses I2C1 (GPIO2=SDA, GPIO3=SCL)

# ----- Helper functions -----
def write_reg(addr, reg, value):
    bus.write_byte_data(addr, reg, value)

def read_reg(addr, reg):
    return bus.read_byte_data(addr, reg)

def read_regs(addr, reg, length):
    return bus.read_i2c_block_data(addr, reg, length)

# ----- Wake up ICM-20948 -----
write_reg(ICM_ADDR, PWR_MGMT_1, 0x01)

# ----- Enable passthrough to magnetometer -----
write_reg(ICM_ADDR, USER_CTRL, 0x00)      # Disable I2C master
write_reg(ICM_ADDR, INT_PIN_CFG, 0x02)    # Enable bypass (passthrough)

# ----- Check AK09916 identity -----
whoami = read_reg(AK_ADDR, WHO_AM_I)
print(f"AK09916 WHO_AM_I: 0x{whoami:02X}")  # Should print 0x09

# ----- Continuous measurement mode -----
write_reg(AK_ADDR, CNTL2, 0x08)

# ----- Read magnetometer data -----
def read_magnetometer():
    # Wait for data ready
    while not (read_reg(AK_ADDR, ST1) & 0x01):
        time.sleep(0.001)

    data = read_regs(AK_ADDR, HXL, 6)
    x = (data[1] << 8) | data[0]
    y = (data[3] << 8) | data[2]
    z = (data[5] << 8) | data[4]

    # Convert 2's complement
    x = x - 65536 if x > 32767 else x
    y = y - 65536 if y > 32767 else y
    z = z - 65536 if z > 32767 else z

    # Read ST2 to complete transaction
    read_reg(AK_ADDR, ST2)
    return x, y, z

# ----- Loop and print -----
try:
    while True:
        mx, my, mz = read_magnetometer()
        print(f"Magnetometer: X={mx}, Y={my}, Z={mz}")
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Stopped")




