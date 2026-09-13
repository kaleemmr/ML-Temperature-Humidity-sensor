import machine
import dht
import time
import pico_model # imports the libraries machine, dht, time and the pico_model module we just made.

# Hardware Pin Setup
sensor = dht.DHT22(machine.Pin(15)) # the dht22 sensor is connected to gp15 on the pico
green_led = machine.Pin(16, machine.Pin.OUT) # the green led is connected to gp16 on the pico
red_led = machine.Pin(14, machine.Pin.OUT) # the red led is connected to gp14 on the pico 

print("Starting to detect. ")

try:
    pico_model.calibrate(sensor, green_led, red_led, samples=5) # starts to calibrate

    print("Decision Boundariess:") # prints just to show the calibration has worked.
    print("Temp Bounds:", pico_model.TEMP_MIN, "to", pico_model.TEMP_MAX) # prints final temp boundaries
    print("Hum Bounds:", pico_model.HUM_MIN, "to", pico_model.HUM_MAX) # prints final humidity boundaries
    print("System active. Monitoring live environment.") # tells us its working now.

    while True: # infinite loop
        try: # used this just in case crashing occurs, this stops the program and pico from continuing if it cant.
            time.sleep(3) # time delay of 3 seconds 
            sensor.measure() # tells the sensor to measure both temperature and humidity values.
            temp = float(sensor.temperature()) 
            hum = float(sensor.humidity())  
        
            result = pico_model.predict(temp, hum) # passes values from sensor directly to the model to compare.
            
            if result == 1:
                green_led.value(1)
                red_led.value(0)
                print(f"[OK] Temp: {temp:.1f}°C | Hum: {hum:.1f}% | NORMAL") # if result is 1 which is in boundaries, then green led is on and is normal.
            else:
                green_led.value(0)
                red_led.value(1)
                print(f"[ALERT] Temp: {temp:.1f}°C | Hum: {hum:.1f}% | ANOMALY") # if result is -1 which is NOT in boundaries, then red led is on and is not normal.
                
        except OSError: 
            time.sleep(1) # delays for one second between each check so errors dont occur and crash the pico.

except KeyboardInterrupt:
    print("\nProgram stopped by user.") # used for when i was testing to stop the sensor running from the IDE.

finally:
    # Safety to ensure LEDs turn off when execution stops
    green_led.value(0)
    red_led.value(0)
    print(" safety is done , LEDs turned OFF.")
