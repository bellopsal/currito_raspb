import serial
import time

class SerialArduino:
    def __init__(self, arduino_port = '/dev/ttyUSB0', baud_rate = 9600, timeout=1):
        self.serial = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)
        print("Conexión establecida con Arduino")
    
    def send_msg(self, msg):
        self.serial.write(msg)
        


