
from loguru import logger
def send_control_message(json_file, mqtt_class):
    """
    Sends a control message based on the values provided in a JSON file.

    The method extracts "leftPower", "rightPower", and "forward" values from the
    given JSON object, constructs a formatted message, and sends it through the
    serial interface if available. Logs the operation or warnings as appropriate.

    Args:
        json_file (dict): A dictionary containing control parameters:
                          - "leftPower" (int/float, optional): Power for the left motor. Defaults to 0.
                          - "rightPower" (int/float, optional): Power for the right motor. Defaults to 0.
                          - "forward" (int/float, optional): Forward motion value. Defaults to 0.
    """
    left_power = json_file.get("leftPower", 0)
    right_power = json_file.get("rightPower", 0)
    forward = json_file.get("forward", 0)
    message = f"{left_power},{right_power},{int(forward)}\n"

    logger.info(f"Sending message: {message}")

    if mqtt_class.serial:
        mqtt_class.serial.send_msg(message.encode('utf-8'))
    else:
        mqtt_class.warning("Serial interface not set")
