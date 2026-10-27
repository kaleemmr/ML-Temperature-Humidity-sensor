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

Problem:
I noticed in my home i didnt have a temperature or humidity sensor, and even if i got a device to do so, most will just display the temperature, some more clearer then others. Most don't have the intelligence to tell you if its too cold or too warm, nevermind adapt to different rooms and homes, and then have the hardware to clearly make clear to the user and other people if the temperature or humidity isn't normal. My little brother is very sensitive to environment changes, and it can cause him to fall ill. So i decided to build one myself using my current knowledge.

Setup & Configuration:
1. Thonny IDE Environment

* Initial Interface: Standard Mode (enables the Files panel for managing CSV data).
* Interpreter: `MicroPython (Raspberry Pi Pico)`
* Family / Variant: RP2 Family -> Raspberry Pi Pico H

2. Autonomous Data Collection (`main.py`)
Upload the data-logging script to the Pico filesystem and save it as `main.py`. 

* Autonomous Boot: Saving the script as `main.py` allows the Pico to automatically execute code upon receiving USB power without needing Thonny connected. (you can use a phone charger or anything you can plug a USB into that has a battery to power this and its very efficient.
* Sampling Rate: 5-second intervals per sample (prevents sensor self-heating and conserves storage over 2 days, (192KB should be used from the 2MB of flash memory in the pico, i collected data for 1 and a half days).
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
│   ├── clean_data.py              # Script 2: Data cleaning & dropped packet removal
│   └── train_model.py             # Script 3: Unsupervised ML model training
└── README.md

4. Cleaning Up the Raw Data...
When you leave a sensor running for over a day, you're bound to pick up some junk data—dropped packets, missing values, or weird electrical spikes where the DHT22 glitches out. The cleaning script handles this by:
- Dropping any blank or broken rows.
- Forcing everything into proper numeric types (and turning text errors into NaN(Not a Number) so they can be thrown away as they get found).
- Running a sanity check to delete physically impossible readings (like a temperature of -999°C or 200% humidity which could happen due to weird electrical faults and more).
- Plotting the cleaned data into a dual-panel graph (baseline_plot.png) so you can visually verify the room's temperature and humidity trends before sending it to the model to use.
  
5. Training the Isolation Forest...

- Instead of manually guessing what counts as "too hot" or "too humid", I used an unsupervised machine learning model to learn the normal baseline.
- The Algorithm: An Isolation Forest from Scikit-Learn. It's great for this because it works by randomly slicing data to see how easily points can be isolated (outliers get isolated fast; normal points take a lot of cuts).
- Settings: Set n_estimators=100 so it builds 100 independent trees to cancel out noise, and contamination=0.01 to assume roughly 1% of the baseline data might have minor anomalies.
- Reproducibility: Used random_state=42 so the random tree generation is completely deterministic—anyone cloning the repo will get the exact same model.
- Export: Saves the trained model as models/isolation_forest.joblib


6. Shrinking the Model for the Pico...

You obviously can't install Scikit-Learn, Pandas, or NumPy on a Raspberry Pi Pico because it only has 264 KB of RAM and 2 MB of flash memory.To bridge that gap, I wrote an export script that extracts the model's core logic without needing the heavy libraries that would nott be able to run in the pico:
- It loads up the trained .joblib model.
- It looks inside all 100 decision trees and pulls out every threshold split used for temperature and humidity.
- it runs a statistical check (5th and 95th percentiles) to find the core variance envelope—the actual width of normal fluctuation, Temperature and Humidity overr time.
- It writes those numbers directly into a tiny, standalone MicroPython file (models/pico_model.py) that the Pico can run instantly with zero dependencies.


7. Making It Adapt to New Environments...

If you hardcode static temperature limits based on the room you trained it in (e.g., 21°C), the moment you take the Pico to a warmer room (like 26°C), it'll immediately trigger a false alarm and flash red forever. To fix this, I added an on-boot calibration routine:When the Pico powers up, it takes 5 quick sensor readings over 3 seconds.It calculates the average baseline of whatever room it's currently sitting in. It takes the pre-trained ML variance envelope, so in my case +- 0.58C and +- 4.23% Humidity and shifts that box right over the new room's center point. 
- Safety Rails: If the room is freezing (<15°C) or scorching (>32°C), it refuses to calibrate to a bad reading and safely falls back to default limits.

And thats it, thats how i made a temperature and humidity sensor from scratch, which helps me keep an eye on the temperature and humidity in my home as my brother gets ill quite easily. 

