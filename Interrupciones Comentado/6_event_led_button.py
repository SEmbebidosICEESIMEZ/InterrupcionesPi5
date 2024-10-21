import gpiod  # Importa la biblioteca para interactuar con los pines GPIO del sistema
import signal  # Importa la biblioteca para manejar señales del sistema, como CTRL+C
import sys  # Importa la biblioteca sys para manejar la terminación del programa

# Definición de propiedades que representan los pines GPIO para el botón y el LED
BUTTON_PIN = 17  # El pin GPIO 17 se utilizará para detectar eventos en el botón
LED_PIN = 18  # El pin GPIO 18 se utilizará para controlar el LED

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
# En POO, este método actúa como un constructor que inicializa la línea GPIO para reaccionar a eventos
button_line.request(consumer='Button', type=gpiod.LINE_REQ_EV_RISING_EDGE)

# Solicita acceso a la línea GPIO del LED y lo configura como salida
# Este método inicializa la línea GPIO del LED para controlar su estado (encendido/apagado)
led_line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)

# Función de manejo de señales (como CTRL+C) para liberar recursos de forma segura
# En POO, esta función actúa como un destructor que asegura la limpieza de recursos antes de terminar el programa
def signal_handler(sig, frame):
    button_line.release()  # Libera la línea GPIO asociada al botón
    led_line.release()  # Libera la línea GPIO asociada al LED
    chip.close()  # Cierra el chip GPIO, liberando los recursos asociados
    sys.exit(0)  # Finaliza el programa de manera controlada

# Callback que se llama cuando se detecta que el botón ha sido presionado
# Esta función es equivalente a un método que reacciona a eventos específicos (presión del botón)
def button_pressed_callback():
    state = button_line.get_value()  # Obtiene el valor actual de la línea GPIO (estado del botón)
    if state:  # Si el botón está presionado (estado alto)
        print("button pressed!")  # Imprime un mensaje indicando que el botón fue presionado
        led_line.set_value(1)  # Enciende el LED (estado alto)
    else:  # Si el botón está liberado (estado bajo)
        print("button released!")  # Imprime un mensaje indicando que el botón fue liberado
        led_line.set_value(0)  # Apaga el LED (estado bajo)

# Asocia el manejador de la señal SIGINT (CTRL+C) con la función `signal_handler`
signal.signal(signal.SIGINT, signal_handler)

# Bucle principal que espera eventos de presión del botón
try:
    while True:
        # Método `event_wait()` espera un evento (presión del botón) durante 1 segundo
        # Este método actúa como un observador, esperando que ocurra una interacción
        event = button_line.event_wait(sec=1)
        
        if event:  # Si se detecta un evento (presión del botón)
            button_pressed_callback()  # Llama al callback para manejar el evento
        else:
            print("Esperando")  # Imprime un mensaje indicando que sigue esperando eventos

# Captura la excepción KeyboardInterrupt (cuando se presiona CTRL+C) y llama al manejador de señales
except KeyboardInterrupt:
    signal_handler(None, None)  # Invoca el manejador de la señal para liberar los recursos
