
import machine # Gives access to the Pico's hardware pins (GPIO)
import dht # gives the DHT sensor library built into MicroPython
import time # Used for creating delays and timing intervals in micropythonn

sensor = dht.DHT22(machine.Pin(15)) # Initialize the DHT22 sensor connected to GPIO pin 15 (pin 20 on the pico)
FILENAME = "dht22_data.csv"  # Defines the file name where sensor logs will be stored in the Pico's flash memory


# CSV initialisation
# Check if CSV exists; if not, tis creates it with a header
try: 
    with open(FILENAME, "r") as f:  # Trys to open the CSV file in read mode ("r") to check if it already exists.
        pass # the file already exists so do nothing and move on.
except OSError: # if an OSError happens that means the file does not exist so we have to create one.
    with open(FILENAME, "w") as f: # creates a file using 'w'  
        f.write("temperature_c,humidity_percent\n") # writes the temperature and humidity.

print("=== Pico Data Logger Active ===") # when the program has done all the csv initialisation then this is printed and it shows its all ready to go.

read_count = 0  # Counter to track total successful readings taken during this session


# STEP 2: Infinite Data Collection Loop

while True: # creates the infinite loop
    try: 
        # Logs every 5 seconds (saves space & prevents sensor self-heating)
        time.sleep(5) # Wait 5 seconds between each read or sample.
        # This prevents sensor self-heating and keeps the log file size smaller so flash memory isnt overloaded.
        
        sensor.measure() # triggers the physical DHT22 sensor to take a new reading
        temp = sensor.temperature() # extracts the temeperature reading into the variable temp
        hum = sensor.humidity() # extracts the relative humidity reading to the variable hum
        
        # Appends the data row to the CSV file on Pico's  flash memory using 'a' mode which is append and adding them into the csv file one after another
        with open(FILENAME, "a") as f: 
            f.write(f"{temp:.1f},{hum:.1f}\n")
            
        read_count += 1 # increments the variable read_count by 1 for every reading 
        print(f"[{read_count}] Saved -> Temp: {temp:.1f}°C | Hum: {hum:.1f}%") # prints the read count and the current temp and humidity
        
    except OSError as e: # i learned that DHT sensors can sometimes drop packets due to precise signal timing.
        print("Sensor read error, retrying...", e) # so this catches the OSError and keeps the script from crashing when a read fails, so you dont randomly come back after a day with insufficient data.
