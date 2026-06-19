from gpiozero import MCP3208, PWMLED
from time import sleep

adc0 = MCP3208(0)
adc1 = MCP3208(1)
adc2 = MCP3208(2)
led0 = PWMLED(26)
led1 = PWMLED(19)
led2 = PWMLED(3)

try:
    while True:
        inputVal0 = adc0.value
        inputVal1 = adc1.value
        inputVal2 = adc2.value
        
        led0.value = inputVal0
        led1.value = inputVal1
        led2.value = inputVal2
        
        sleep(0.2)
except KeyboardInterrupt:
    pass

adc0.close()
adc1.close()
adc2.close()

led0.close()
led1.close()
led2.close()