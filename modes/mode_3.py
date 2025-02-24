import cv2
import numpy as np
import time
#import RPi.GPIO as GPIO
import lgpio
import os
import sys
#from hablar import hablar
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from hablar import hablar

#descalificado_antiguo=0

# Configuración del pin GPIO
SERVO_PIN = 18
PWM_FREQ = 50
CHIP = 0

# Configuración de la biblioteca RPi.GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(SERVO_PIN, GPIO.OUT)


# Configuración de PWM
# pwm = GPIO.PWM(SERVO_PIN, 50)  # Frecuencia de 50 Hz (estándar para servos)
# pwm.start(0)  # Iniciar PWM con un duty cycle de 0%
h = lgpio.gpiochip_open(CHIP)
lgpio.gpio_claim_output(h, SERVO_PIN)
lgpio.tx_pwm(h, SERVO_PIN, PWM_FREQ, 50)

def mover_servo(angulo):
#    """Convierte un ángulo (0° a 180°) a ciclo de trabajo para el servo."""
    duty_cycle = 2.5 + (angulo / 180.0) * 10.0  # Mapear ángulo a duty cycle
    #pwm.ChangeDutyCycle(duty_cycle)
    lgpio.tx_pwm(h, SERVO_PIN, PWM_FREQ, duty_cycle)
    time.sleep(0.5)  # Esperar para que el servo se mueva a la posición

def capture_background(cap):
    print("Capturando el fondo")
    #time.sleep(1)  # Esperar 1 segundo
    ret, background = cap.read()
    if ret:
        print("Imagen de fondo capturada.")
        #cv2.imshow("Fondo Capturado", background)  # Mostrar la imagen del fondo
        #cv2.waitKey(500)  # Esperar 500 ms para que se pueda ver
        return background
    else:
        raise RuntimeError("No se pudo capturar la imagen de fondo.")

def detect_changes(background, frame, threshold=50):
    # Convertir imágenes a escala de grises
    gray_background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calcular la diferencia absoluta
    diff = cv2.absdiff(gray_background, gray_frame)

    # Aplicar umbral para destacar los cambios significativos
    _, diff_threshold = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    return diff_threshold

def process_movement(diff_threshold, frame):
    # Encontrar contornos del movimiento
    contours, _ = cv2.findContours(diff_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    height, width = frame.shape[:2]
    area1_rect = (0, 0, width // 2, height)  # Rectángulo de la primera área
    area2_rect = (width // 2, 0, width, height)  # Rectángulo de la segunda área

    movement_area1 = 0
    movement_area2 = 0
    #descalificado_antiguo= 0
    descalificado= 0
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Umbral de área mínima para contornos
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Dibujar rectángulo

            # Verificar si el contorno está en la primera o segunda área
            if x + w // 2 < area1_rect[2]:
                movement_area1 += 1
            elif x + w // 2 >= area2_rect[0]:
                movement_area2 += 1

    # Dibujar las áreas en el cuadro
    cv2.rectangle(frame, (area1_rect[0], area1_rect[1]), (area1_rect[2], area1_rect[3]), (255, 0, 0), 2)
    cv2.rectangle(frame, (area2_rect[0], area2_rect[1]), (area2_rect[2], area2_rect[3]), (0, 0, 255), 2)

    # Determinar si hay movimiento significativo en alguna área
    if movement_area1 > 0 and movement_area2 > 0:
        #print("Descalificados los dos")
        descalificado= 3
        return descalificado
        
    elif movement_area1 > 0:
        #print("Descalificado persona 1")
        descalificado= 1
        return descalificado
        
    elif movement_area2 > 0:
        #print("Descalificado persona 2")
        descalificado= 2
        return descalificado
        

    #return descalificado
      

def main(cap):
        descalificado_antiguo=0
        #posicion inicial (mirando a la pared)
        print("Moviendo servo a 0°...")
        mover_servo(0)
        hablar("Un, dos, tres pollito inglés a la pared")
        time.sleep(1)  # Esperar 3 segundo

        #posicion vigilancia
        print("Moviendo servo a 180°...")
        mover_servo(180)
        time.sleep(1)

        # Capturar el fondo cuando currito este en la posicion
        background = capture_background(cap)

        print("Iniciando detección de cambios durante 3 segundos...")
        start_time = time.time()
        while time.time() - start_time < 2:  # Detectar durante 5 segundos
            # Leer el cuadro actual de la cámara
            ret, frame = cap.read()
            if not ret:
                print("No se pudo leer el cuadro de la cámara.")
                break

            # Detectar cambios
            diff_threshold = detect_changes(background, frame)

            # Procesar movimiento en las áreas
            jugador_descalificado= process_movement(diff_threshold, frame)
            if  jugador_descalificado!= descalificado_antiguo:
                descalificado_antiguo=jugador_descalificado
                if jugador_descalificado==1 :
                    print("Descalificados jugador 1")
                    hablar("Descalificado el jugador 1")
                else : 
                    if jugador_descalificado==2 :
                        print("Descalificados jugador 2")
                        hablar("Descalificado el jugador 2")
                    else: 
                        if jugador_descalificado==3 :
                            print("Descalificados los dos")
                            hablar("Descalificados los dos")
            
                
            # Mostrar la imagen con movimiento detectado
            cv2.imshow("Movimiento Detectado", frame)
            
            # Presionar 'q' para salir anticipadamente
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return

       

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        main(cap)
        time.sleep(7)