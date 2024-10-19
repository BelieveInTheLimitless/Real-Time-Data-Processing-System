import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
from models import DailySummary
from sqlalchemy.orm import Session

class Visualization:
    @staticmethod
    def plot_daily_summary(db: Session, city: str, days: int = 7):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        data = db.query(DailySummary).filter(
            DailySummary.city == city,
            DailySummary.date >= start_date,
            DailySummary.date <= end_date
        ).all()
        
        df = pd.DataFrame([{
            'date': summary.date,
            'avg_temp': summary.avg_temp,
            'max_temp': summary.max_temp,
            'min_temp': summary.min_temp
        } for summary in data])
        
        plt.figure(figsize=(12, 6))
        plt.plot(df['date'], df['avg_temp'], label='Average Temperature')
        plt.plot(df['date'], df['max_temp'], label='Maximum Temperature')
        plt.plot(df['date'], df['min_temp'], label='Minimum Temperature')
        plt.title(f'Temperature Trends for {city}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'weather_trends_{city}.png')
        plt.close()