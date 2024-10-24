from datetime import datetime, timezone, timedelta
from models import WeatherData
from sqlalchemy.orm import Session
from config import TEMPERATURE_THRESHOLD, CONSECUTIVE_ALERTS

class AlertService:
    @staticmethod
    def check_temperature_threshold(db: Session, city: str):
        recent_readings = db.query(WeatherData).filter(
            WeatherData.city == city,
            WeatherData.timestamp >= datetime.now(timezone.utc) - timedelta(minutes=10)
        ).order_by(WeatherData.timestamp.desc()).limit(CONSECUTIVE_ALERTS).all()

        if len(recent_readings) >= CONSECUTIVE_ALERTS:
            if all(reading.temperature > TEMPERATURE_THRESHOLD for reading in recent_readings):
                return f"ALERT: Temperature in {city} has exceeded {TEMPERATURE_THRESHOLD}°C for {CONSECUTIVE_ALERTS} consecutive readings!"
        return None