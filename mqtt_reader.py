import paho.mqtt.client as mqtt
import json

class MQTTReader:
    def __init__(self, broker, port=1883, topic="#", client_id=None, serial= None):
        """
        Initialize the MQTTReader.

        :param broker: MQTT broker address
        :param port: MQTT broker port (default is 1883)
        :param topic: Topic to subscribe to (default is all topics)
        :param client_id: Unique client ID (default is None for auto-generated)
        """
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = client_id or f"mqtt_client_{id(self)}"
        self.client = mqtt.Client(self.client_id)
        self.serial = serial

        # Bind event handlers
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback when the client connects to the broker.
        """
        if rc == 0:
            print(f"Connected to broker at {self.broker}:{self.port}")
            self.client.subscribe(self.topic)
            print(f"Subscribed to topic: {self.topic}")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        """
        Callback when a message is received from the broker.
        """
        print(f"Received message on {msg.topic}: {msg.payload.decode('utf-8')}")
        json_file = json.loads(msg.payload.decode('utf-8'))
        modo = json_file["Modo"]
        l = json_file["leftPower"]
        r = json_file["rightPower"]
        f = json_file["forward"]
        msg = str(l)+","+str(r)+","+str(int(f))+"\n"
        print(msg)
        self.serial.send_msg(msg.encode('utf-8'))
        

    def start(self):
        """
        Start the MQTT client and listen for messages.
        """
        try:
            print("Starting MQTT client...")
            self.client.connect(self.broker, self.port)
            self.client.loop_forever()
        except Exception as e:
            print(f"An error occurred: {e}")

    def stop(self):
        """
        Stop the MQTT client.
        """
        print("Stopping MQTT client...")
        self.client.disconnect()
        self.client.loop_stop()
