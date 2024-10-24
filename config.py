from os import getenv
from dotenv import load_dotenv

load_dotenv()

TESTING = getenv('TESTING', 'false').lower() == 'true'

CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
API_KEY = getenv('OPENWEATHERMAP_API_KEY')
UPDATE_INTERVAL = 300
TEMPERATURE_THRESHOLD = 35
CONSECUTIVE_ALERTS = 2

DB_CONFIG = {
    'host': getenv('MYSQL_HOST', 'localhost'),
    'user': getenv('MYSQL_USER', 'weather_user'),
    'password': getenv('MYSQL_PASSWORD', 'weather_pass'),
    'database': getenv('MYSQL_DATABASE', 'weather_db')
}

if TESTING:
    DB_CONFIG = {
        'host': getenv('MYSQL_HOST', 'test-db'),
        'user': getenv('MYSQL_USER', 'test_user'),
        'password': getenv('MYSQL_PASSWORD', 'test_pass'),
        'database': getenv('MYSQL_DATABASE', 'test_db')
    }