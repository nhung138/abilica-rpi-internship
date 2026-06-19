from gpiozero import MCP3208, LED
from time import sleep

adc0 = MCP3208(0)
led = LED(12)
try:
    while True:
        inputVal0 = adc0.value
        if inputVal0 < 0.6:
            led.on()
        else:
            led.off()
        #print(inputVal0)
        sleep(0.2)
        
except KeyboardInterrupt:
    pass


adc0.close()
led.close() 