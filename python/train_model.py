import json
import math
import random
from pathlib import Path

from edge_ai_model import GaussianAnomalyDetector

MODEL_PATH = Path(__file__).with_name("model.json")
TRAINING_SAMPLE_COUNT = 1000


def generate_normal_training_data():
    samples = []

    for t in range(TRAINING_SAMPLE_COUNT):
        base_vibration = 2.0 + 0.5 * math.sin(t / 10)
        samples.append(
            {
                "vibration_rms": base_vibration + random.uniform(-0.3, 0.3),
                "temperature": 35.0 + random.uniform(-2.0, 2.0),
            }
        )

    return samples


def main():
    training_data = generate_normal_training_data()
    model = GaussianAnomalyDetector.train(training_data, threshold=3.0)

    with MODEL_PATH.open("w", encoding="utf-8") as model_file:
        json.dump(model.to_dict(), model_file, indent=2)

    print(f"Model trained using {len(training_data)} normal samples")
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
