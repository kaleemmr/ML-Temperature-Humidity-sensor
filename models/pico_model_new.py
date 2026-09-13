import time

# Feature boundaries extracted directly from your trained Isolation Forest model
OFFLINE_TEMP_MIN = 21.32
OFFLINE_TEMP_MAX = 22.48
OFFLINE_HUM_MIN = 56.56
OFFLINE_HUM_MAX = 65.02

# Calculate exact model variance half-widths from your 2-day baseline data
TEMP_HALF_WIDTH = round((OFFLINE_TEMP_MAX - OFFLINE_TEMP_MIN) / 2.0, 2)  # ~0.58°C
HUM_HALF_WIDTH = round((OFFLINE_HUM_MAX - OFFLINE_HUM_MIN) / 2.0, 2)    # ~4.23%

# Absolute physical safety rails for realistic room environments
ABSOLUTE_TEMP_MIN, ABSOLUTE_TEMP_MAX = 15.0, 32.0

# Active decision boundaries (initialized to your offline trained values)
TEMP_MIN = OFFLINE_TEMP_MIN
TEMP_MAX = OFFLINE_TEMP_MAX
HUM_MIN = OFFLINE_HUM_MIN
HUM_MAX = OFFLINE_HUM_MAX

def calibrate(sensor, green_led, red_led, samples=5):
    """
    Samples initial ambient conditions on boot and shifts your trained 
    Isolation Forest variance envelope over the local room baseline.
    """
    global TEMP_MIN, TEMP_MAX, HUM_MIN, HUM_MAX
    
    temps, hums = [], []
    print("[+] Calibrating trained ML envelope to local room baseline...")
    
    for _ in range(samples):
        # Visual calibration feedback: alternating LED flash
        green_led.value(1); red_led.value(0); time.sleep(0.3)
        green_led.value(0); red_led.value(1); time.sleep(0.3)
        
        try:
            sensor.measure()
            temps.append(float(sensor.temperature()))
            hums.append(float(sensor.humidity()))
        except OSError:
            pass

    if temps and hums:
        avg_t = sum(temps) / len(temps)
        avg_h = sum(hums) / len(hums)
        
        # Verify ambient conditions fall within safe physical limits
        if ABSOLUTE_TEMP_MIN <= avg_t <= ABSOLUTE_TEMP_MAX:
            # Shift the learned ML variance envelope to center on local ambient conditions
            TEMP_MIN = round(avg_t - TEMP_HALF_WIDTH, 2)
            TEMP_MAX = round(avg_t + TEMP_HALF_WIDTH, 2)
            HUM_MIN  = round(max(0.0, avg_h - HUM_HALF_WIDTH), 2)
            HUM_MAX  = round(min(100.0, avg_h + HUM_HALF_WIDTH), 2)
            
            print(f"[+] Dynamic Calibration Complete!")
            print(f"    Local Center Point: {avg_t:.2f}°C, {avg_h:.2f}%")
            print(f"    Active Temp Bounds: {TEMP_MIN}°C to {TEMP_MAX}°C (Span: ±{TEMP_HALF_WIDTH}°C)")
            print(f"    Active Hum Bounds:  {HUM_MIN}% to {HUM_MAX}% (Span: ±{HUM_HALF_WIDTH}%)\n")
            return

    print("[!] Environmental check failed. Falling back to default offline ML bounds.\n")

def predict(temp, hum):
    """
    Executes real-time inference using the active ML decision boundaries.
    Returns 1 for NORMAL, -1 for ANOMALY.
    """
    t, h = float(temp), float(hum)
    if (TEMP_MIN <= t <= TEMP_MAX) and (HUM_MIN <= h <= HUM_MAX):
        return 1   # NORMAL
    return -1      # ANOMALY
