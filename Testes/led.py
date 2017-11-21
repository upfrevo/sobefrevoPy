import RPi.GPIO as GPIO ## Import GPIO library
GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(16, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(16,True) ## Turn on GPIO pin 7
GPIO.cleanup()

