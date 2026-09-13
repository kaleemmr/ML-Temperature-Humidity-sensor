import machine
import dht
import time
import pico_model

# Hardware Pin Setup
sensor = dht.DHT22(machine.Pin(15))
green_led = machine.Pin(16, machine.Pin.OUT)
red_led = machine.Pin(14, machine.Pin.OUT)

print("Starting Autonomous Edge-AI Anomaly Detector...")

try:
    # 1. On-boot dynamic calibration using trained ML variance envelope
    pico_model.calibrate(sensor, green_led, red_led, samples=5)

    print("Active ML Decision Bounds:")
    print("Temp Bounds:", pico_model.TEMP_MIN, "to", pico_model.TEMP_MAX)
    print("Hum Bounds:", pico_model.HUM_MIN, "to", pico_model.HUM_MAX)
    print("System active. Monitoring live environment...\n")

    # 2. Main Micro-ML Inference Loop
    while True:
        try:
            time.sleep(3)
            sensor.measure()
            temp = float(sensor.temperature())
            hum = float(sensor.humidity())
            
            # Execute Micro-ML prediction
            result = pico_model.predict(temp, hum)
            
            if result == 1:
                green_led.value(1)
                red_led.value(0)
                print(f"[OK] Temp: {temp:.1f}°C | Hum: {hum:.1f}% | NORMAL")
            else:
                green_led.value(0)
                red_led.value(1)
                print(f"[ALERT] Temp: {temp:.1f}°C | Hum: {hum:.1f}% | ANOMALY")
                
        except OSError:
            time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    # Safety cleanup: ensure status LEDs turn off when execution stops
    green_led.value(0)
    red_led.value(0)
    print("Cleanup complete: Status LEDs turned OFF.")
