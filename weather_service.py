import requests
from datetime import datetime
from models import WeatherData, DailySummary
from sqlalchemy.orm import Session
from sqlalchemy import func
from config import API_KEY

class WeatherService:
    @staticmethod
    def kelvin_to_celsius(kelvin):
        return kelvin - 273.15

    @staticmethod
    def get_weather_data(city: str):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                'city': city,
                'main_condition': data['weather'][0]['main'],
                'temperature': WeatherService.kelvin_to_celsius(data['main']['temp']),
                'feels_like': WeatherService.kelvin_to_celsius(data['main']['feels_like']),
                'timestamp': datetime.fromtimestamp(data['dt'])
            }
        return None
    
    @staticmethod
    def calculate_daily_summary(db: Session, city: str, date: datetime):
        conditions = db.query(
            WeatherData.main_condition,
            func.count(WeatherData.main_condition).label('count')
        ).filter(
            WeatherData.city == city,
            func.date(WeatherData.timestamp) == date.date()
        ).group_by(WeatherData.main_condition).order_by(func.count(WeatherData.main_condition).desc()).first()

        temp_stats = db.query(
            func.avg(WeatherData.temperature).label('avg_temp'),
            func.max(WeatherData.temperature).label('max_temp'),
            func.min(WeatherData.temperature).label('min_temp')
        ).filter(
            WeatherData.city == city,
            func.date(WeatherData.timestamp) == date.date()
        ).first()

        return DailySummary(
            city=city,
            date=date,
            avg_temp=round(temp_stats.avg_temp, 1) if temp_stats.avg_temp else None,
            max_temp=temp_stats.max_temp,
            min_temp=temp_stats.min_temp,
            dominant_condition=conditions.main_condition if conditions else None
        )