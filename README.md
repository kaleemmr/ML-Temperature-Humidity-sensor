# ML-Temperature-Humidity-sensor
Real-time temperature and humidity monitoring using a Raspberry Pi Pico (RP2040) and a 4-pin DHT22 sensor with MicroPython and a custom pull up resistor.

Hardware Requirements:
- Raspberry Pi Pico H ((MicroPython RP2040 firmware) Get with headers on or else you have to solder it to the board)
- DHT22 (AM2302) Temperature and Humidity sensor 
- 4.7K Ohm pull up resistor (signal line to the VCC 3.3V power line of the dht22 sensor so between both)
- Status LED's (Green for normal, Red for anomaly), With 220 Ohm resistors.
- Micro-USB data cable (access data to and from the raspberry pico)

Wiring Pinout:
| Component | Pin Type | Pico Pin |

| DHT22 VCC (Pin 1 on DHT22) | Power (3.3V) | Pin 36 (`3V3_OUT`) |
| DHT22 Data (Pin 2 on DHT22) | GPIO Pin | Pin 20 (`GPIO15`) |
| DHT22 GND (Pin 4 on DHT22) | Ground | Pin 18 (`GND`) |
| Green LED | Status | Pin 21 (`GPIO16`) |
| Red LED | Alert | Pin 22 (`GPIO17`) |

Note: A 4.7kΩ resistor is wired between the DHT22 Data pin and DHT22 VCC (3.3V) to ensure stable signal readings.

Setup & Configuration:
1. Thonny IDE Environment

* Initial Interface: Standard Mode (enables the Files panel for managing CSV data).
* Interpreter: `MicroPython (Raspberry Pi Pico)`
* Family / Variant: RP2 Family -> Raspberry Pi Pico H

2. Autonomous Data Collection (`main.py`)
Upload the data-logging script to the Pico filesystem and save it as `main.py`. 

* Autonomous Boot: Saving the script as `main.py` allows the Pico to automatically execute code upon receiving USB power without needing Thonny connected. (you can use a phone charger or anything you can plug a USB into that has a battery to power this and its very efficient.
* Sampling Rate: 5-second intervals per sample (prevents sensor self-heating and conserves storage over 2 days, 192KB should be used from the 2MB of flash memory in the pico).
* Storage Format: Appends raw values to `dht22_data.csv` on internal flash memory.


3. Testing & Validation

* Validation Test: Performed a manual breath test on the DHT22. Captured immediate, real-time spikes in humidity and temperature within a 1 or 2 sampless, confirming hardware responsiveness and data logging accuracy.
  
- 5 results before:
[64] Saved -> Temp: 21.8°C | Hum: 65.1%
[65] Saved -> Temp: 21.8°C | Hum: 65.0%
[66] Saved -> Temp: 21.8°C | Hum: 64.5%
[67] Saved -> Temp: 21.8°C | Hum: 64.6%
[68] Saved -> Temp: 21.8°C | Hum: 65.2%
- 9 Results after I did the manual breath test which show the spike:
[69] Saved -> Temp: 21.9°C | Hum: 66.9%
[70] Saved -> Temp: 22.0°C | Hum: 68.7%
[71] Saved -> Temp: 22.3°C | Hum: 70.7%
[72] Saved -> Temp: 22.6°C | Hum: 75.0%
[73] Saved -> Temp: 22.7°C | Hum: 76.8%
[74] Saved -> Temp: 23.0°C | Hum: 78.7%
[75] Saved -> Temp: 23.3°C | Hum: 78.4%
[76] Saved -> Temp: 23.4°C | Hum: 76.4%
[77] Saved -> Temp: 23.5°C | Hum: 73.8%
[78] Saved -> Temp: 23.5°C | Hum: 71.5%


* Dataset Collection: Logged baseline ambient room conditions over a extended period to capture day/night environmental shifts. (1-3 days)
* Now leave the Pico logging data to collect a solid baseline! 
* Save src/pico_logger.py onto the Raspberry Pi Pico root directory as main.py so MicroPython auto-executes it on boot."


delete after done..
Project Structure

```text
├── data/
│   ├── dht22_raw_data.csv         # Raw logs extracted from Pico flash storage
│   └── dht22_cleaned_data.csv     # Preprocessed data (pandas)
├── models/
│   └── anomaly_model.joblib       # Trained Isolation Forest model binary
├── src/
│   ├── pico_logger.py             # Autonomous data logger (renamed to main.py on Pico)
│   ├── clean_data.py              # Script 2: Data cleaning & dropped packet removal
│   └── train_model.py             # Script 3: Unsupervised ML model training
└── README.md



