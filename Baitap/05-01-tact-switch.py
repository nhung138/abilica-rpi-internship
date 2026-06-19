from gpiozero import LED, Button
from time import sleep

led = LED(25)
btn = Button(27, pull_up=False)

try:
    while True:
        if btn.value ==1:  #khi nhan nut
            led.on()
        else:
            led.off()      #khi nha nut
        sleep(0.01)
        
except KeyboardInterrupt:
    pass

led.close()