import machine
import dht
import time

sensor = dht.DHT22(machine.Pin(15))
FILENAME = "dht22_data.csv"

# Check if CSV exists; if not, tis creates it with a header
try:
    with open(FILENAME, "r") as f:
        pass
except OSError:
    with open(FILENAME, "w") as f:
        f.write("temperature_c,humidity_percent\n")

print("=== Pico Data Logger Active ===")

read_count = 0

while True:
    try:
        # Logs every 5 seconds (saves space & prevents sensor self-heating)
        time.sleep(5)
        
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        # Append data row to the CSV file on Pico's memory
        with open(FILENAME, "a") as f:
            f.write(f"{temp:.1f},{hum:.1f}\n")
            
        read_count += 1
        print(f"[{read_count}] Saved -> Temp: {temp:.1f}°C | Hum: {hum:.1f}%")
        
    except OSError as e:
        print("Sensor read error, retrying...", e)

