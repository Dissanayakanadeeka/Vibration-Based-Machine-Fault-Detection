# Vibration-Based Machine Fault Detection Using Edge AI and MQTT

## Group Members

- E/20/078
- E/20/286
- E/20/318
- E/20/397

## Project Description

This project implements a simulation-based Edge AI and Industrial IoT system for vibration-based machine fault detection. A Python script simulates vibration and temperature readings from an industrial motor, trains a simple local ML anomaly detector, publishes sensor data and alerts through MQTT, and displays the results on a Node-RED dashboard.

The system is designed for the CO326 Edge AI + Industrial IoT mini project.

## System Architecture

```text
Simulated Vibration Sensor -> Python Edge AI -> MQTT Broker -> Node-RED -> Dashboard
```

Main components:

- Python simulation and edge AI processing
- Local MQTT broker using Eclipse Mosquitto
- Node-RED for MQTT subscription and dashboard visualization
- Docker Compose for running Node-RED and Mosquitto

## Repository Structure

```text
project-root/
+-- python/
|   +-- requirements.txt
|   +-- edge_ai_model.py
|   +-- train_model.py
|   +-- model.json
|   +-- vibration_publisher.py
+-- node-red/
|   +-- flows.json
+-- mosquitto/
|   +-- config/
|       +-- mosquitto.conf
+-- docs/
|   +-- report.md
+-- docker-compose.yml
+-- README.md
```

## How to Run

### 1. Start Docker Services

From the project root folder, run:

```bash
docker compose up --build
```

This starts:

- Node-RED at `http://localhost:1880`
- Local MQTT broker on port `1883`

### 2. Install Python Dependencies

Open another terminal in the project root folder and run:

```bash
python -m pip install -r python/requirements.txt
```

### 3. Train the Simple ML Model

```bash
python python/train_model.py
```

This creates:

```text
python/model.json
```

The model file stores the learned normal vibration and temperature values.

### 4. Run the Vibration Publisher

```bash
python python/vibration_publisher.py
```

The Python script publishes simulated machine data every 2 seconds.

### 5. Open the Node-RED Dashboard

Open:

```text
http://localhost:1880/ui
```

## MQTT Configuration

For Python running on the host machine:

```python
BROKER = "localhost"
PORT = 1883
GROUP_ID = "group07"
```

For Node-RED running inside Docker, the MQTT broker server should be:

```text
Server: mqtt
Port: 1883
```

## MQTT Topics Used

Sensor data topic:

```text
sensors/group07/vibration/data
```

Alert topic:

```text
alerts/group07/vibration/status
```

## Sensor Data Format

Example sensor payload:

```json
{
  "machine_id": "motor_01",
  "vibration_rms": 2.34,
  "temperature": 36.5,
  "anomaly_score": 1.42,
  "fault_detected": false,
  "fault_type": "normal",
  "status": "NORMAL",
  "timestamp": 1710000000.0
}
```

Example alert payload:

```json
{
  "machine_id": "motor_01",
  "status": "FAULT",
  "message": "High vibration detected",
  "fault_type": "bearing_fault",
  "timestamp": 1710000000.0
}
```

## Edge AI Logic

The edge AI logic runs locally in Python before data is published to the dashboard. This is the edge computing part of the system because raw sensor values are processed on the local device before MQTT publishing.

The project uses a simple ML anomaly detection model implemented in `python/edge_ai_model.py`.

Model approach:

- `python/train_model.py` generates normal machine samples.
- The model learns the normal mean and standard deviation for vibration and temperature.
- The trained model parameters are saved in `python/model.json`.
- `python/vibration_publisher.py` loads the trained model at runtime.
- For each live sample, the model calculates an anomaly score using z-score distance.
- If the anomaly score is greater than the model threshold, the edge script marks the sample as warning or fault.
- The result is published to MQTT with the sensor payload.

Final decision rules:

- Normal anomaly score: `NORMAL`
- High anomaly score with moderate change: `WARNING`
- High anomaly score with `vibration_rms > 6.0`: `FAULT`
- High anomaly score with `temperature > 60.0`: `FAULT`

Simulated fault types:

- Normal machine operation
- Bearing fault using sudden vibration spikes
- Overheating using sudden temperature increase

## Node-RED Dashboard

The dashboard displays:

- Vibration RMS gauge
- Vibration trend chart
- Temperature gauge
- Machine status text
- Fault alert text

Node-RED subscribes to the MQTT topics and visualizes real-time machine condition data.

## Results

Add dashboard screenshots here after testing the system.

Suggested screenshots:

- Node-RED flow
- Live dashboard during normal operation
- Dashboard during warning or fault condition
- Python publisher terminal output

## Challenges

- Configuring the MQTT broker correctly for both Python and Node-RED
- Understanding the difference between `localhost` on the host machine and `mqtt` inside Docker
- Designing realistic simulated vibration data with normal and abnormal behavior
- Tuning vibration thresholds for warning and fault detection

## Future Improvements

- Train the anomaly detection model using real vibration sensor data
- Add more fault types such as imbalance and misalignment
- Use a real vibration sensor with ESP32 or Raspberry Pi
- Store MQTT data in a database for historical analysis
- Improve the dashboard with status colors and fault history
