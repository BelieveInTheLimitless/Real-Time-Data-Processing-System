import time
import logging
from database import init_db, get_db
from models import WeatherData
from weather_service import WeatherService
from alert_service import AlertService
from visualization import Visualization
from config import CITIES, UPDATE_INTERVAL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    init_db()
    logger.info("Database initialized.")
    
    while True:
        db = next(get_db())
        try:
            for city in CITIES:
                logger.info(f"Fetching weather data for {city}...")
                weather_data = WeatherService.get_weather_data(city)
                if weather_data:
                    logger.info(f"Weather data for {city}: {weather_data}")
                    
                    db_weather = WeatherData(**weather_data)
                    db.add(db_weather)
                    db.commit()
                    logger.info(f"Weather data for {city} saved to database.")
                    
                    alert = AlertService.check_temperature_threshold(db, city)
                    if alert:
                        logger.warning(alert)
                    
                    daily_summary = WeatherService.calculate_daily_summary(
                        db, city, weather_data['timestamp']
                    )
                    db.add(daily_summary)
                    db.commit()
                    logger.info(f"Daily summary updated for {city}.")
                    
                    Visualization.plot_daily_summary(db, city)
                    logger.info(f"Visualization generated for {city}.")
                
        except Exception as e:
            logger.error(f"Error processing weather data: {e}")
            db.rollback()
        finally:
            db.close()
            
        logger.info(f"Sleeping for {UPDATE_INTERVAL} seconds...")
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
