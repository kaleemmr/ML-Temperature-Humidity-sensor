import time # imports the time library for the flashing and time delay for the sensor readings.

OFFLINE_TEMP_MIN = 21.32
OFFLINE_TEMP_MAX = 22.48 # temp values from model for the usual temp boundaries.
OFFLINE_HUM_MIN = 56.56
OFFLINE_HUM_MAX = 65.02 # humidity values from model for the usual humidity boundaries.

# These two lines calclate the models exact variance in temperature and humidity and how it varys over time.
TEMP_HALF_WIDTH = round((OFFLINE_TEMP_MAX - OFFLINE_TEMP_MIN) / 2.0, 2)  # 0.58°C
HUM_HALF_WIDTH = round((OFFLINE_HUM_MAX - OFFLINE_HUM_MIN) / 2.0, 2)    # 4.23%

# Absolute boundaries for temperature in a room, if the room is warmer or colder, these are extreme conditions and calibration will not happen.
ABSOLUTE_TEMP_MIN, ABSOLUTE_TEMP_MAX = 15.0, 32.0

# Active decision boundaries for temp and humidity from when the sensor is first on.
TEMP_MIN = OFFLINE_TEMP_MIN
TEMP_MAX = OFFLINE_TEMP_MAX
HUM_MIN = OFFLINE_HUM_MIN
HUM_MAX = OFFLINE_HUM_MAX

def calibrate(sensor, green_led, red_led, samples=5): 
    
    global TEMP_MIN, TEMP_MAX, HUM_MIN, HUM_MAX
    
    temps = []
    hums = [] # arrays for the data needed for calibration.
    print(" Calibrating trained ML envelope to local room baseline.")
    
    for i in range(samples): # flashing at 3Hz for as long the calibration is.
        # Visual calibration feedback: alternating LED flash
        green_led.value(1); red_led.value(0); time.sleep(0.3) 
        green_led.value(0); red_led.value(1); time.sleep(0.3)
        
        try:
            sensor.measure() # measures humidity and temp.
            temps.append(float(sensor.temperature())) # appends the temperature value from sensor to the empty temp array
            hums.append(float(sensor.humidity())) # appends the humidity value from sensor to empty humidity array
        except OSError: # ignores weird errors with the sensor readings.
            pass

    if temps and hums: # needed so the sensor and pico doesnt crash, only lets the program continue if theres atleast 1 reading in each array.
        avg_t = sum(temps) / len(temps) # finds averages in temp and humidity
        avg_h = sum(hums) / len(hums)
    
        if ABSOLUTE_TEMP_MIN <= avg_t <= ABSOLUTE_TEMP_MAX: # checks if the conditions fall within the general room temperature high and low.
            # uuses the model variance with the new calibrated values to make new boundaries for the sensor to follow, upto 2 decimal places.
            TEMP_MIN = round(avg_t - TEMP_HALF_WIDTH, 2)
            TEMP_MAX = round(avg_t + TEMP_HALF_WIDTH, 2)
            HUM_MIN  = round(max(0.0, avg_h - HUM_HALF_WIDTH), 2)
            HUM_MAX  = round(min(100.0, avg_h + HUM_HALF_WIDTH), 2)
            
            print(f' calibration is done')
            print(f"    Local Center Point: {avg_t:.2f}°C, {avg_h:.2f}%") # prints the average values for humidity and temperature 
            print(f"    Active Temp Bounds: {TEMP_MIN}°C to {TEMP_MAX}°C (Span: ±{TEMP_HALF_WIDTH}°C)") # prints temp boundaries 
            print(f"    Active Hum Bounds:  {HUM_MIN}% to {HUM_MAX}% (Span: ±{HUM_HALF_WIDTH}%)\n") # prints humidity boundaries
            return # return to main program

    print("[!] Environmental check failed. back to default offline boundaries since the calibration failed.\n")

def predict(temp, hum): # checks what the values temp and humidity are from sensor.
    
    t = float(hum)
    h = float(temp)
    if (TEMP_MIN <= t <= TEMP_MAX) and (HUM_MIN <= h <= HUM_MAX): # if the temperature and humidity are BOTH in between their boundaries return 1 if not return -1 to main program.
        return 1   # NORMAL
    return -1      # ANOMALY
