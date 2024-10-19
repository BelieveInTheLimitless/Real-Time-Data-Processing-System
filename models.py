from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    
    id = Column(Integer, primary_key=True)
    city = Column(String(50))
    main_condition = Column(String(50))
    temperature = Column(Float)
    feels_like = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DailySummary(Base):
    __tablename__ = 'daily_summaries'
    
    id = Column(Integer, primary_key=True)
    city = Column(String(50))
    date = Column(DateTime)
    avg_temp = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)
    dominant_condition = Column(String(50))