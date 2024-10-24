import time
from database import init_db, get_db
from models import WeatherData
from weather_service import WeatherService
from config import CITIES, UPDATE_INTERVAL

def main():
    init_db()
    
    while True:
        db = next(get_db())
        try:
            for city in CITIES:
                weather_data = WeatherService.get_weather_data(city)
                if weather_data:
                    
                    db_weather = WeatherData(**weather_data)
                    db.add(db_weather)
                    db.commit()
                    
                    daily_summary = WeatherService.calculate_daily_summary(
                        db, city, weather_data['timestamp']
                    )
                    db.add(daily_summary)
                    db.commit()
                
        except Exception as e:
            db.rollback()
        finally:
            db.close()
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
