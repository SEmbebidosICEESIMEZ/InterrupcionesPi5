import gpiod  # Importa la biblioteca para interactuar con los pines GPIO del sistema

# Definición de la propiedad que representa el pin donde está conectado el botón
BUTTON_PIN = 17  # El pin GPIO 17 se utilizará para detectar eventos en el botón

# Crea un objeto `chip` que representa el chip de control GPIO
# En términos de POO, este objeto es la instancia de la clase `Chip`, que interactúa con el hardware GPIO
chip = gpiod.Chip('gpiochip4')  # Inicializa el chip GPIO correspondiente (gpiochip4)

# Crea un objeto `button_line` que representa la línea GPIO correspondiente al pin del botón
# Este objeto encapsula la lógica de interacción con el pin GPIO 17
button_line = chip.get_line(BUTTON_PIN)  # Obtiene la línea GPIO del pin 17

# Solicita acceso a la línea GPIO y configura el manejo de interrupciones por flanco de subida
# Este método se comporta como un constructor que define que el pin reaccione ante eventos de subida
button_line.request(consumer='Button', type=gpiod.LINE_REQ_EV_RISING_EDGE)

# Bucle que espera y detecta eventos de flanco de subida en el botón
try:
    while True:
        # Método `event_read()` actúa como un observador que espera una interrupción de flanco de subida
        if button_line.event_read():  # Detecta un evento de flanco de subida en el pin GPIO
            print("Button pressed")  # Imprime un mensaje cuando se detecta que el botón ha sido presionado
        
except KeyboardInterrupt:
    # Maneja la interrupción por teclado (CTRL + C) para finalizar el programa de manera segura
    print("Programa terminado")
finally:
    # Libera los recursos de la línea GPIO y cierra el chip, comportándose como un destructor en POO
    button_line.release()  # Libera la línea GPIO asociada al botón
    chip.close()  # Cierra el chip GPIO, liberando los recursos asociados
