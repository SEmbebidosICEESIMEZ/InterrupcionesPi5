import gpiod  # Importa la biblioteca para interactuar con los pines GPIO del sistema
import signal  # Importa la biblioteca para manejar señales del sistema, como CTRL+C
import sys  # Importa la biblioteca sys para manejar la terminación del programa
import time  # Importa la biblioteca time para manejar el tiempo y retardos

# Definición de propiedades que representan los pines GPIO y el tiempo de debounce
BUTTON_PIN = 17  # El pin GPIO 17 se utilizará para detectar eventos en el botón
LED_PIN = 18  # El pin GPIO 18 se utilizará para controlar el LED
DEBOUNCE_TIME = 0.2  # Tiempo de debounce para evitar múltiples detecciones rápidas de la pulsación

# Crea un objeto `chip` que representa el chip de control GPIO
# En POO, este objeto es una instancia de la clase `Chip`, que interactúa con el hardware GPIO
chip = gpiod.Chip('gpiochip4')  # Inicializa el chip GPIO 4, que controla tanto el botón como el LED

# Crea un objeto `button_line` que representa la línea GPIO correspondiente al pin del botón
# Este objeto encapsula la lógica de la línea GPIO para el botón
button_line = chip.get_line(BUTTON_PIN)  # Obtiene la línea GPIO del pin 17

# Crea un objeto `led_line` que representa la línea GPIO correspondiente al pin del LED
# En POO, este objeto encapsula la lógica para controlar el LED a través de GPIO
led_line = chip.get_line(LED_PIN)  # Obtiene la línea GPIO del pin 18

# Solicita acceso a la línea GPIO del botón para manejar interrupciones por flanco de subida
button_line.request(consumer='Button', type=gpiod.LINE_REQ_EV_RISING_EDGE)

# Solicita acceso a la línea GPIO del LED y lo configura como salida
led_line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)

# Variables para almacenar el último estado del LED y el tiempo de la última pulsación del botón
last_LED_state = 0  # Estado inicial del LED (apagado)
last_press_time = 0  # Almacena el tiempo de la última pulsación del botón

# Función de manejo de señales (como CTRL+C) para liberar recursos de forma segura
# En POO, esta función actúa como un destructor que asegura la limpieza de recursos antes de terminar el programa
def signal_handler(sig, frame):
    button_line.release()  # Libera la línea GPIO asociada al botón
    led_line.release()  # Libera la línea GPIO asociada al LED
    chip.close()  # Cierra el chip GPIO, liberando los recursos asociados
    sys.exit(0)  # Finaliza el programa de manera controlada

# Función para alternar el estado del LED (encender o apagar)
# En POO, esta función actúa como un método que controla el comportamiento del LED
def toggle_led():
    global last_LED_state  # Utiliza la variable global para almacenar el último estado del LED
    new_state = not last_LED_state  # Invierte el estado actual del LED
    led_line.set_value(new_state)  # Cambia el valor del LED en el pin GPIO (ON/OFF)
    last_LED_state = new_state  # Actualiza el estado del LED
    print(f"LED state changed to: {'ON' if new_state else 'OFF'}")  # Imprime el estado del LED

# Configura el manejador de señales SIGINT (CTRL+C) con la función `signal_handler`
signal.signal(signal.SIGINT, signal_handler)

# Bucle principal que espera eventos de presión del botón con lógica de debounce
try:
    while True:
        # Espera un evento en el botón
        event = button_line.event_wait()
        
        if event:  # Si se detecta un evento (presión del botón)
            current_time = time.time()  # Obtiene el tiempo actual
            # Comprueba si ha pasado más tiempo que el definido por DEBOUNCE_TIME desde la última pulsación
            if current_time - last_press_time > DEBOUNCE_TIME:
                time.sleep(0.05)  # Introduce una pequeña espera para mayor estabilidad en la lectura
                if button_line.get_value() == 1:  # Verifica si el botón está presionado
                    toggle_led()  # Cambia el estado del LED
                    last_press_time = current_time  # Actualiza el tiempo de la última pulsación

# Captura la excepción KeyboardInterrupt (cuando se presiona CTRL+C) y llama al manejador de señales
except KeyboardInterrupt:
    signal_handler(None, None)  # Invoca el manejador de la señal para liberar los recursos
