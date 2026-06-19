from gpiozero import MCP3208, RGBLED
from time import sleep

adc0 = MCP3208(channel=0)
led = RGBLED(red=26, green=19, blue=13)

#den ngu thong minh (red, green, blue)

try:
    while True:
        inputVal0 = adc0.value
        if inputVal0 > 0.7:     
            led.color = (0,1,0)   #den blue = troi sang                                                                      
            
        elif 0.55 <= inputVal0 <= 0.7: 
            led.color = (0,0,1)  #den green = troi hoi toi
            
        else:
            led.color = (1,0,0) #den red = troi toi
            
    
        print(inputVal0,0.7,0.55)
        sleep(0.2)
        
except KeyboardInterrupt:
    pass

led.close()
adc0.close()

    