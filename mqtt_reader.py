import paho.mqtt.client as mqtt
import json
from loguru import logger
import threading
import time  # Missing import for time module

import modes.mode_1 as mode_1


class MQTTReader:
    def __init__(self, broker, port=1883, topic="#", client_id=None, serial=None):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.serial = serial

        self.exit_some_function = False
        self.some_function_active = False
        self.before_mode = None

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
        else:
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
                if self.before_mode != 1:
                    self.exit_some_function = True

            elif modo == 1:
                self.before_mode = 1
                self.exit_some_function = False  # Reset flag
                mode_1.send_control_message(json_file=json_file, mqtt_class=self)

            elif modo == 2:
                command = json_file.get("Command")
                if command == "Take picture":
                    logger.info("Executing 'Take picture' command.")
                    # Add actual logic for taking a picture here.
                else:
                    logger.warning("Incorrect Command")
            else:
                logger.warning(f"Unknown mode: {modo}")

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON message: {msg.payload}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def wait_to_detect(self):
        self.some_function_active = True
        try:
            logger.info("Starting mode 2: Detect and Talk")
            for i in range(10):  # Simulate some work
                if self.exit_some_function:
                    logger.info("Exiting wait_to_detect() early due to 'Modo == 0'")
                    break
                logger.info(f"wait_to_detect running: step {i}")
                time.sleep(1)  # Simulate a time-consuming task
            else:
                logger.info("Completed wait_to_detect()")
        finally:
            self.some_function_active = False

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




