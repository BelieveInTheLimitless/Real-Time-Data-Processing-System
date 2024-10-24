import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, WeatherData, DailySummary
from weather_service import WeatherService
from alert_service import AlertService
from config import TEMPERATURE_THRESHOLD, CONSECUTIVE_ALERTS

class TestWeatherMonitoringSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    def setUp(self):
        self.session.query(WeatherData).delete()
        self.session.query(DailySummary).delete()
        self.session.commit()

    def tearDown(self):
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        Base.metadata.drop_all(cls.engine)

    def test_system_setup_and_api_connection(self):
        """Test 1: System Setup - Verify API connection"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'weather': [{'main': 'Clear'}],
            'main': {'temp': 298.15, 'feels_like': 300.15},
            'dt': datetime.now().timestamp()
        }

        with patch('requests.get', return_value=mock_response):
            result = WeatherService.get_weather_data('Delhi')
            self.assertIsNotNone(result)
            self.assertEqual(result['city'], 'Delhi')
            self.assertIn('temperature', result)
            self.assertIn('main_condition', result)

    @patch('requests.get')
    def test_data_retrieval_and_parsing(self, mock_get):
        """Test 2: Data Retrieval - Test API calls and response parsing"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'weather': [{'main': 'Cloudy'}],
            'main': {'temp': 293.15, 'feels_like': 294.15},
            'dt': datetime.now().timestamp()
        }

        weather_data = WeatherService.get_weather_data('Mumbai')
        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data['city'], 'Mumbai')
        self.assertEqual(weather_data['main_condition'], 'Cloudy')
        
        mock_get.return_value.status_code = 404
        weather_data = WeatherService.get_weather_data('InvalidCity')
        self.assertIsNone(weather_data)

    def test_temperature_conversion(self):
        """Test 3: Temperature Conversion - Test Kelvin to Celsius conversion"""
        test_cases = [
            (273.15, 0),    
            (373.15, 100),
            (298.15, 25),  
            (310.15, 37),     
        ]

        for kelvin, expected_celsius in test_cases:
            celsius = WeatherService.kelvin_to_celsius(kelvin)
            self.assertAlmostEqual(celsius, expected_celsius, places=2)

    def test_daily_summary_calculation(self):
        """Test 4: Daily Weather Summary - Test summary statistics calculation"""
        test_date = datetime(2024, 1, 1, 12, 0)
        test_data = [
            WeatherData(city='Chennai', temperature=25.0, main_condition='Sunny', timestamp=test_date),
            WeatherData(city='Chennai', temperature=30.0, main_condition='Sunny', timestamp=test_date + timedelta(hours=3)),
            WeatherData(city='Chennai', temperature=28.0, main_condition='Cloudy', timestamp=test_date + timedelta(hours=6)),
            WeatherData(city='Chennai', temperature=23.0, main_condition='Sunny', timestamp=test_date + timedelta(hours=9))
        ]

        expected_avg = sum(data.temperature for data in test_data) / len(test_data)
        expected_avg = round(expected_avg, 1) 

        for data in test_data:
            self.session.add(data)
        self.session.commit()

        summary = WeatherService.calculate_daily_summary(self.session, 'Chennai', test_date)
        
        self.assertEqual(summary.city, 'Chennai')
        self.assertEqual(summary.date.date(), test_date.date())
        self.assertAlmostEqual(summary.avg_temp, expected_avg)
        self.assertEqual(summary.max_temp, 30.0)
        self.assertEqual(summary.min_temp, 23.0)
        self.assertEqual(summary.dominant_condition, 'Sunny')

    def test_temperature_alerts(self):
        """Test 5: Alerting Thresholds - Test temperature threshold alerts"""
        city = 'Bangalore'
        current_time = datetime.utcnow()

        high_temp_readings = [
            WeatherData(
                city=city,
                temperature=TEMPERATURE_THRESHOLD + 1,
                timestamp=current_time - timedelta(minutes=i)
            )
            for i in range(CONSECUTIVE_ALERTS)
        ]

        for reading in high_temp_readings:
            self.session.add(reading)
        self.session.commit()

        alert = AlertService.check_temperature_threshold(self.session, city)
        self.assertIsNotNone(alert)
        self.assertIn(f"exceeded {TEMPERATURE_THRESHOLD}°C", alert)

        self.session.query(WeatherData).delete()
        normal_temp_readings = [
            WeatherData(
                city=city,
                temperature=TEMPERATURE_THRESHOLD - 1,
                timestamp=current_time - timedelta(minutes=i)
            )
            for i in range(CONSECUTIVE_ALERTS)
        ]

        for reading in normal_temp_readings:
            self.session.add(reading)
        self.session.commit()

        alert = AlertService.check_temperature_threshold(self.session, city)
        self.assertIsNone(alert)

if __name__ == '__main__':
    unittest.main()