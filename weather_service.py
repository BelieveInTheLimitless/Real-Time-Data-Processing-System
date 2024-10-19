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
        daily_data = db.query(
            func.avg(WeatherData.temperature).label('avg_temp'),
            func.max(WeatherData.temperature).label('max_temp'),
            func.min(WeatherData.temperature).label('min_temp'),
            WeatherData.main_condition
        ).filter(
            WeatherData.city == city,
            func.date(WeatherData.timestamp) == date.date()
        ).group_by(WeatherData.main_condition).order_by(func.count(WeatherData.main_condition).desc()).limit(1).first()

        return DailySummary(
            city=city,
            date=date,
            avg_temp=daily_data.avg_temp,
            max_temp=daily_data.max_temp,
            min_temp=daily_data.min_temp,
            dominant_condition=daily_data.main_condition 
        )
