import json
import math
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

GROUP_ID = "group07"
PROJECT = "vibration"
MACHINE_ID = "motor_01"

DATA_TOPIC = f"sensors/{GROUP_ID}/{PROJECT}/data"
ALERT_TOPIC = f"alerts/{GROUP_ID}/{PROJECT}/status"

PUBLISH_INTERVAL_SECONDS = 2


def detect_fault(vibration_rms, temperature):
    if vibration_rms > 6.0:
        return True, "FAULT", "High vibration detected"
    if vibration_rms > 4.0:
        return True, "WARNING", "Vibration above normal level"
    if temperature > 60.0:
        return True, "WARNING", "High temperature detected"
    return False, "NORMAL", "Machine operating normally"


def simulate_machine_sample(t):
    base_vibration = 2.0 + 0.5 * math.sin(t / 10)
    vibration_noise = random.uniform(-0.3, 0.3)
    vibration_rms = base_vibration + vibration_noise

    temperature = 35.0 + random.uniform(-2.0, 2.0)
    fault_type = "normal"

    if random.random() < 0.05:
        vibration_rms += random.uniform(3.0, 6.0)
        fault_type = "bearing_fault"

    if random.random() < 0.03:
        temperature += random.uniform(25.0, 35.0)
        fault_type = "overheating"

    return round(vibration_rms, 2), round(temperature, 2), fault_type


def build_sensor_payload(vibration_rms, temperature, fault_detected, status, fault_type):
    return {
        "machine_id": MACHINE_ID,
        "vibration_rms": vibration_rms,
        "temperature": temperature,
        "fault_detected": fault_detected,
        "fault_type": fault_type,
        "status": status,
        "timestamp": time.time(),
    }


def build_alert_payload(status, message, fault_type):
    return {
        "machine_id": MACHINE_ID,
        "status": status,
        "message": message,
        "fault_type": fault_type,
        "timestamp": time.time(),
    }


def main():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    print(f"Publishing sensor data to: {DATA_TOPIC}")
    print(f"Publishing alerts to: {ALERT_TOPIC}")

    t = 0
    while True:
        vibration_rms, temperature, fault_type = simulate_machine_sample(t)
        fault_detected, status, message = detect_fault(vibration_rms, temperature)

        sensor_payload = build_sensor_payload(
            vibration_rms,
            temperature,
            fault_detected,
            status,
            fault_type,
        )

        client.publish(DATA_TOPIC, json.dumps(sensor_payload))

        if fault_detected:
            alert_payload = build_alert_payload(status, message, fault_type)
            client.publish(ALERT_TOPIC, json.dumps(alert_payload))

        print(sensor_payload)

        t += 1
        time.sleep(PUBLISH_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
