#!/usr/bin/env python3

import gpiod  # Biblioteca para interactuar con los pines GPIO
import signal  # Biblioteca para manejar señales del sistema, como CTRL+C
import sys  # Biblioteca para manejar la terminación del programa
import time  # Biblioteca para manejar el tiempo y retardos

# Definición de los pines y el tiempo de debounce
BUTTON_PIN = 17  # El pin GPIO 17 se utiliza para detectar eventos en el botón
LED_PIN = 18  # El pin GPIO 18 se utiliza para controlar el LED
DEBOUNCE_TIME = 0.2  # Tiempo de debounce para evitar múltiples detecciones de pulsación
should_blink = False  # Variable para determinar si el LED debe parpadear

# Crea el objeto `chip` para interactuar con el GPIO
chip = gpiod.Chip('gpiochip4')  # Inicializa el chip GPIO correspondiente

# Crea objetos `button_line` y `led_line` que representan los pines del botón y del LED
button_line = chip.get_line(BUTTON_PIN)  # Línea GPIO para el botón
led_line = chip.get_line(LED_PIN)  # Línea GPIO para el LED

# Solicita acceso a la línea del botón con detección de eventos en ambos flancos (subida y bajada)
button_line.request(consumer='Button', type=gpiod.LINE_REQ_EV_BOTH_EDGES)

# Solicita acceso a la línea del LED y la configura como salida
led_line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)

# Variables para controlar el tiempo de la última pulsación y el estado del botón
last_press_time = 0  # Tiempo de la última vez que el botón fue presionado
button_pressed = False  # Estado actual del botón (presionado o no)

# Función para manejar señales (como CTRL+C) y liberar recursos de forma segura
# Actúa como un destructor en POO para garantizar que los recursos se limpien al finalizar
def signal_handler(sig, frame):
    button_line.release()  # Libera la línea GPIO del botón
    led_line.release()  # Libera la línea GPIO del LED
    chip.close()  # Cierra el chip GPIO, liberando recursos
    sys.exit(0)  # Finaliza el programa de manera controlada

# Función callback que se llama cada vez que se detecta un cambio en el estado del botón
def button_callback():
    global should_blink, last_press_time, button_pressed
    current_time = time.time()  # Obtiene el tiempo actual
    
    # Detecta si el botón ha sido presionado (flanco de subida) y si no está presionado actualmente
    if button_line.get_value() == 1 and not button_pressed:
        # Verifica si ha pasado suficiente tiempo desde la última pulsación (debounce)
        if current_time - last_press_time > DEBOUNCE_TIME:
            # Alterna el estado de `should_blink` para habilitar/deshabilitar el parpadeo del LED
            should_blink = not should_blink
            print(f"Blinking {'enabled' if should_blink else 'disabled'}")  # Muestra el estado actual
            last_press_time = current_time  # Actualiza el tiempo de la última pulsación
            button_pressed = True  # Marca el botón como presionado
    # Detecta si el botón ha sido liberado (flanco de bajada)
    elif button_line.get_value() == 0 and button_pressed:
        button_pressed = False  # Marca el botón como no presionado

# Asocia el manejador de señales SIGINT (CTRL+C) con la función `signal_handler`
signal.signal(signal.SIGINT, signal_handler)

# Bucle principal que espera eventos de presión del botón y controla el parpadeo del LED
try:
    while True:
        # Espera un evento en el botón
        event = button_line.event_wait()
        
        if event:  # Si se detecta un evento (cambio en el estado del botón)
            button_callback()  # Llama a la función callback para manejar la pulsación del botón

        # Si el parpadeo está habilitado, alterna el estado del LED
        if should_bblink:
            led_line.set_value(1)  # Enciende el LED
            time.sleep(0.5)  # Espera 500 ms
            led_line.set_value(0)  # Apaga el LED
            time.sleep(0.5)  # Espera otros 500 ms
        else:
            time.sleep(0.1)  # Espera 100 ms cuando no hay parpadeo activo

# Captura la excepción KeyboardInterrupt (cuando se presiona CTRL+C) y llama al manejador de señales
except KeyboardInterrupt:
    signal_handler(None, None)  # Invoca el manejador de la señal para liberar los recursos
