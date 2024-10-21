import gpiod  # Importa la biblioteca gpiod para interactuar con los pines GPIO del sistema
import time  # Importa la biblioteca time para gestionar retardos

# Definición de la propiedad que representa el pin donde está conectado el botón
BUTTON_PIN = 17  # El pin GPIO 17 se utilizará para detectar el estado del botón

# Crea un objeto `chip` que representa el chip de control GPIO
# En términos de POO, este objeto es la instancia de la clase `Chip`, que interactúa con el hardware
chip = gpiod.Chip('gpiochip4')  # Inicializa el chip GPIO 4, que controla el botón

# Crea un objeto `button_line` que representa la línea GPIO correspondiente al pin del botón
# Este objeto se comporta como una abstracción de la línea GPIO para el botón
button_line = chip.get_line(BUTTON_PIN)  # Obtiene la línea GPIO del pin 17

# Solicita acceso a la línea GPIO configurándola como entrada
# El método `request()` actúa como un constructor que establece la dirección de la línea (entrada)
button_line.request(consumer='Button', type=gpiod.LINE_REQ_DIR_IN)  # Configura el pin 17 como entrada

# Define una propiedad `pressed` que actúa como un estado booleano para saber si el botón ha sido presionado
pressed = False  # Inicializa el estado del botón como no presionado

# Bucle que verifica el estado del botón continuamente
try:
    while True:
        # Método `get_value()` que actúa como un método de acceso para verificar el valor de la línea GPIO
        if button_line.get_value():  # Si el valor del pin es 1 (botón presionado)
            if not pressed:  # Verifica si el botón no ha sido registrado como presionado aún
                print(f"Botón presionado")  # Imprime un mensaje indicando que el botón fue presionado
                pressed = True  # Actualiza el estado de `pressed` a verdadero
        else:  # Si el valor del pin es 0 (botón no presionado)
            print("Botón liberado")  # Imprime un mensaje indicando que el botón fue liberado
            pressed = False  # Actualiza el estado de `pressed` a falso
        time.sleep(0.1)  # Pausa de 100 milisegundos para reducir la frecuencia de lectura
except KeyboardInterrupt:
    # Captura la interrupción por teclado (CTRL + C) para finalizar el programa
    print("Programa terminado")
finally:
    # Libera los recursos de la línea GPIO y cierra el chip, como si fueran destructores en POO
    button_line.release()  # Libera la línea GPIO del botón
    chip.close()  # Cierra el chip GPIO, liberando los recursos
