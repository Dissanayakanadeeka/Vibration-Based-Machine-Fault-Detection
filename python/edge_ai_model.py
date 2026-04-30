import math


class GaussianAnomalyDetector:
    """Small edge-friendly anomaly detector using normal baseline statistics."""

    def __init__(self, vibration_mean, vibration_std, temperature_mean, temperature_std, threshold=3.0):
        self.vibration_mean = vibration_mean
        self.vibration_std = max(vibration_std, 0.001)
        self.temperature_mean = temperature_mean
        self.temperature_std = max(temperature_std, 0.001)
        self.threshold = threshold

    @classmethod
    def train(cls, samples, threshold=3.0):
        vibration_values = [sample["vibration_rms"] for sample in samples]
        temperature_values = [sample["temperature"] for sample in samples]

        return cls(
            vibration_mean=_mean(vibration_values),
            vibration_std=_std(vibration_values),
            temperature_mean=_mean(temperature_values),
            temperature_std=_std(temperature_values),
            threshold=threshold,
        )

    def predict(self, vibration_rms, temperature):
        vibration_z = abs(vibration_rms - self.vibration_mean) / self.vibration_std
        temperature_z = abs(temperature - self.temperature_mean) / self.temperature_std
        anomaly_score = max(vibration_z, temperature_z)

        if anomaly_score >= self.threshold:
            return True, round(anomaly_score, 2)

        return False, round(anomaly_score, 2)

    def to_dict(self):
        return {
            "vibration_mean": self.vibration_mean,
            "vibration_std": self.vibration_std,
            "temperature_mean": self.temperature_mean,
            "temperature_std": self.temperature_std,
            "threshold": self.threshold,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            vibration_mean=data["vibration_mean"],
            vibration_std=data["vibration_std"],
            temperature_mean=data["temperature_mean"],
            temperature_std=data["temperature_std"],
            threshold=data["threshold"],
        )


def _mean(values):
    return sum(values) / len(values)


def _std(values):
    mean = _mean(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return math.sqrt(variance)
