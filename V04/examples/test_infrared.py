# Bibliotheken
import RPi.GPIO as GPIO
import time

# GPIO definieren (Modus, Pins, Output)
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def entfernung():
    # Trig High setzen
    GPIO.output(GPIO_TRIGGER, True)

    # Trig Low setzen (nach 0.01ms)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    Startzeit = time.time()
    Endzeit = time.time()

    # Start/Stop Zeit ermitteln
    while GPIO.input(GPIO_ECHO) == 0:
        Startzeit = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        Endzeit = time.time()

    # Vergangene Zeit
    Zeitdifferenz = Endzeit - Startzeit

    # Schallgeschwindigkeit (34300 cm/s) einbeziehen
    entfernung = (Zeitdifferenz * 34300) / 2

    return entfernung


if __name__ == '__main__':
    try:
        while True:
            distanz = entfernung()
            print ("Distanz = %.1f cm" % distanz)
            time.sleep(1)

        # Programm beenden
    except KeyboardInterrupt:
        print("Programm abgebrochen")
        GPIO.cleanup()