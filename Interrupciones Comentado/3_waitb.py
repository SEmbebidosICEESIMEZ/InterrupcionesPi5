import gpiod  # Importa la biblioteca gpiod para interactuar con los pines GPIO del sistema

# Define la propiedad que representa el pin donde está conectado el botón
BUTTON_PIN = 17  # El pin GPIO 17 se utilizará para detectar eventos de botón

# Crea un objeto `chip` que representa el chip de control GPIO
# En términos de POO, este objeto es una instancia de la clase `Chip`, que interactúa con el hardware GPIO
chip = gpiod.Chip('gpiochip4')  # Inicializa el chip GPIO 4, que controla el botón

# Crea un objeto `button_line` que representa la línea GPIO correspondiente al pin del botón
# Este objeto encapsula la lógica de la línea GPIO para el botón
button_line = chip.get_line(BUTTON_PIN)  # Obtiene la línea GPIO del pin 17

# Solicita acceso a la línea GPIO para manejar interrupciones por flanco de subida
# Este método actúa como un constructor que inicializa el pin para reaccionar a eventos
button_line.request(consumer='Button', type=gpiod.LINE_REQ_EV_RISING_EDGE)

# Bucle principal para esperar y detectar eventos de botón
try:
    while True:
        # Método `event_read()` que actúa como un observador que espera un evento en el pin
        # Aquí `event` guarda el resultado del evento (presión del botón)
        event = button_line.event_read()
        
        # Si se detecta un evento (presión del botón)
        if event:
            print("Button pressed")  # Imprime un mensaje cuando el botón se presiona
        else:
            print("released!!")  # Imprime un mensaje cuando no hay presión del botón (liberado)
        
except KeyboardInterrupt:
    # Maneja la interrupción por teclado (CTRL + C) para finalizar el programa de manera segura
    print("Programa terminado")
finally:
    # Libera los recursos de la línea GPIO y cierra el chip, comportándose como un destructor en POO
    button_line.release()  # Libera la línea GPIO del botón
    chip.close()  # Cierra el chip GPIO, liberando los recursos asociados
