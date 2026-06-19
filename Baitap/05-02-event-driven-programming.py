from gpiozero import LED, Button
from time import sleep
from signal import pause

def pressed(button):
    if button.pin.number == 27:
        led.toggle()
        
#         global ledState
#         ledState = not ledState # togger, lenh not de lat nguoc gia tri
#         if ledState == 1:
#             led.on()
#         else:
#             led.off()

            
led = LED(25)
btn = Button(27, pull_up=False, bounce_time=0.05) #loai bo su kien thua -> chong doi phim bouce time

btn.when_pressed = pressed  #gan su kien (event blinding)
ledState = led.value

try:
    pause()
except KeyboardInterrupt:
    pass


led.close()
btn.close()

