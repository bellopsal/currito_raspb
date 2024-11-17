from mqtt_reader import MQTTReader
from arduino_serial import SerialArduino
import serial
import time

##########################################################################
##      Serial Port
##########################################################################
# Serial Settings
arduino_port = '/dev/ttyUSB0'  # Puede variar; intenta con /dev/ttyUSB0 si es necesario
baud_rate = 9600
timeout=1
### test
arduino_serial = SerialArduino(arduino_port, baud_rate, timeout)


##########################################################################
##      MQTT
##########################################################################
# MQTT broker settings
BROKER = "localhost"  
PORT = 1883
TOPIC = "currito"


mqtt_reader = MQTTReader(broker=BROKER, port=PORT, topic=TOPIC, serial = arduino_serial)





###########################
############################

# Start listening for messages
try:
    mqtt_reader.start()
except KeyboardInterrupt:
    print("Exiting...")
    mqtt_reader.stop()
