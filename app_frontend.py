from flask import Flask, render_template, jsonify
from database import get_db
from models import WeatherData, DailySummary
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/current-weather')
def current_weather():
    db = next(get_db())
    try:
        current_data = {}
        for city in ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']:
            latest = db.query(WeatherData).filter(
                WeatherData.city == city
            ).order_by(WeatherData.timestamp.desc()).first()
            
            if latest:
                current_data[city] = {
                    'temperature': round(latest.temperature, 1),
                    'feels_like': round(latest.feels_like, 1),
                    'condition': latest.main_condition,
                    'timestamp': latest.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                }
        return jsonify(current_data)
    finally:
        db.close()

@app.route('/api/daily-summary/<city>')
def daily_summary(city):
    db = next(get_db())
    try:
        summaries = db.query(DailySummary).filter(
            DailySummary.city == city,
            DailySummary.date >= datetime.now() - timedelta(days=7)
        ).order_by(DailySummary.date.desc()).all()
        
        return jsonify([{
            'date': s.date.strftime('%Y-%m-%d'),
            'avg_temp': round(s.avg_temp, 1),
            'max_temp': round(s.max_temp, 1),
            'min_temp': round(s.min_temp, 1),
            'condition': s.dominant_condition
        } for s in summaries])
    finally:
        db.close()

@app.route('/api/alerts')
def get_alerts():
    db = next(get_db())
    try:
        alerts = []
        for city in ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']:
            recent_readings = db.query(WeatherData).filter(
                WeatherData.city == city,
                WeatherData.timestamp >= datetime.now() - timedelta(minutes=10)
            ).order_by(WeatherData.timestamp.desc()).limit(2).all()
            
            if len(recent_readings) >= 2 and all(r.temperature > 35 for r in recent_readings):
                alerts.append({
                    'city': city,
                    'message': f'Temperature exceeded 35°C in {city}',
                    'temperature': round(recent_readings[0].temperature, 1),
                    'timestamp': recent_readings[0].timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
        return jsonify(alerts)
    finally:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)