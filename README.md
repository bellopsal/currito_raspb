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
