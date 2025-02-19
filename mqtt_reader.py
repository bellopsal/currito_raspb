import paho.mqtt.client as mqtt
import json
from loguru import logger
import threading
import time  # Missing import for time module
from hablar import hablar
import modes.mode_1 as mode_1
import modes.mode_2 as mode_2
import modes.mode_3 as mode_3
import cv2

##########
# detector = mode_2.ObjectDetector('yolov5su.pt')
# video_source=0




class MQTTReader:
    def __init__(self, broker, port=1883, topic="#", client_id="test", serial=None):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.serial = serial

        self.exit_some_function = False
        self.some_function_active = False
        self.active_mode = None

        # Initialize the MQTT client
        self.client = mqtt.Client(client_id)

        # Bind event handlers
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):  # Corrected method signature
        if rc == 0:
            logger.info(f"Connected to broker at {self.broker}:{self.port}")
            self.client.subscribe(self.topic)
            logger.info(f"Subscribed to topic: {self.topic}")
            hablar("Conexión MQTT correcta")
        else:
            hablar("No me he logrado crear el servidor MQTT")
            logger.error(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):  # Corrected method signature
        try:
            logger.info(f"Received message on {msg.topic}: {msg.payload.decode('utf-8')}")
            json_file = json.loads(msg.payload.decode('utf-8'))
            modo = json_file.get("Modo")

            if modo is None:
                logger.warning("Missing 'Modo' in message")
                return

            if modo == 0:
                # This mode is only sent when a back button is clicked.
                logger.info("Exiting current operation...")
                if self.active_mode != 1:
                    self.exit_some_function = True
                    self.some_function_active = False

            elif modo == 1:
                self.active_mode = 1
                self.exit_some_function = False  # Reset flag
                mode_1.send_control_message(json_file=json_file, mqtt_class=self)

            elif modo == 2:
                self.active_mode = 1
                self.exit_some_function = False  # Reset flag
                if not self.some_function_active:
                    threading.Thread(target=self.fun_fact, daemon=True).start()
                    self.some_function_active = True

            elif modo == 3:
                self.active_mode = 1
                self.exit_some_function = False  # Reset flag
                if not self.some_function_active:
                    threading.Thread(target=self.pollito_ingles, daemon=True).start()
                    self.some_function_active = True

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON message: {msg.payload}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def fun_fact(self):
        self.some_function_active = True
        cap = cv2.VideoCapture(0)
        detector = mode_2.ObjectDetector('yolov5su.pt')
        
        while not self.exit_some_function:
            detector.detect_live(cap)

        cap.release()
        cv2.destroyAllWindows()
    
    def pollito_ingles(self):
        self.some_function_active = True
        cap = cv2.VideoCapture(0)
        
        descalificado_antiguo=0
        time.sleep(2)
        if not cap.isOpened():
            print("No se pudo abrir la cámara.")
            return
        while not self.exit_some_function:
            mode_3.main()

        cap.release()
        cv2.destroyAllWindows()
        

###### START AND STOP MQTT            

    def start(self):
        threading.Thread(target=self._start_client, daemon=True).start()

    def _start_client(self):
        while True:
            try:
                logger.info("Starting MQTT client...")
                self.client.connect(self.broker, self.port)
                self.client.loop_forever()
            except Exception as e:
                logger.error(f"Connection error: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    def stop(self):
        logger.info("Stopping MQTT client...")
        self.client.disconnect()
        self.client.loop_stop()




