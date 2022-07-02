from time import sleep
from smbus2 import SMBus

bus = SMBus(1)  # 1 indicates /dev/i2c-1

address_SRF_v = 0x70  # Adresse vorderer Ultraschallsensor
address_SRF_h = 0x71  # Adresse hinterer Ultraschallsensor

# Messung starten und Messwert in cm
bus.write_byte_data(address_SRF_v, 0x00, 0x51)
bus.write_byte_data(address_SRF_h, 0x00, 0x51)

# Wartezeit von 70 ms
sleep(0.07)

# Messwert abholen (vorderer Ultraschallsensor)
range_High_Byte = bus.read_byte_data(address_SRF_v, 0x02)  # höherwertiges Byte
range_Low_Byte = bus.read_byte_data(address_SRF_v, 0x03)  # niederwertiges Byte

# Lichtwert abholen (vorderer Ultraschallsensor)
light_v = bus.read_byte_data(address_SRF_v, 0x01)

# Address Infrarot
address_IR = 0x4f
# Messwert Abholen
distance_IR = bus.read_byte(address_IR)

# Address Kompass
address_COM = 0x60
# Messwert abholen
bear_High_Byte = bus.read_byte_data(address_COM, 2)  # höherwertiges Byte
bear_Low_Byte = bus.read_byte_data(address_COM, 3)  # niederwertiges Byte
