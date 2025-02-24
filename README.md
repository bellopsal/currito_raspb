# Currito RASP

En este repositorio estan disponibles toda la configuración y código necesario para el correcto funcionamiento de Currito para el proyecto de la asignatura "Proyectos de Robótica" en el curso 2024/2025 por Ana Calvo, Iñaki Caballero, Juan TTT y Belén López.

En el proyecto se diseña una aplicación que se comunica con Currito para poder jugar a 4 modos diferentes de juegos. La aplicación se puede descargar en cualquier dispositivo Android con el fichero app.apk. En los siguientes pasos veremos como configurar a Currito para si correcto funcionamiento.

# Configuración 
En primer lugar clona este repositorio en una Raspberry con el Sistema Operativo ya instalado.

## Configuración del Servidor MQTT
Para ello solo tiene que realizar los siguientes comandos:
```
chmod +x configure_mqtt.sh
./configure_mqtt.sh
```

para asegurarse de que el servidor está levantado puede realizar el siguiente comando asegurandose de que el resultado sea "active"
```
systemctl status mosquitto.service
```

## Configuración del Python
```
chmod +x configure_python.sh
./configure_python.sh
```

## Configuración de la app
Conecte la Raspberry al WIFI que vaya a usar generalmente y obtenga la IP. Esa IP debe ser introducida en la App y generar la APK con esa configuración.
Posible mejora: la app solicite en la primera pantalla la IP de la Raspberry Pi para configurar la dirección del servidor MQTT.

# Uso
Para su correcto funcionamiento, se debe conectar lo siguiente:
- Raspberry Pi y Arduino Uno por puerto serie.
- Conectar Web Cam por USB
- Conectar Altavoz (Bluetooth o USB es indiferente)
- La señal del servo de la cabeza al PIN 18.

Una vez todo conectado. Solo debe lanzar el main.py (en el environment currito) de la forma que prefiera. Desde la terminal sería
```
source /home/pi/currito/bin/activate
python /home/pi/currito_raspb/main.py
```
Ya puede hacer uso de la aplicación para jugar con su currito :)

