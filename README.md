# Real-Time-Data-Processing-System
A real-time data processing system to monitor weather conditions and provide summarized insights using rollups and aggregates. The system utilizes data from the OpenWeatherMap API.


## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Screenshots](#screenshots)

## Features
- The system continuously calls the OpenWeatherMap API at a configurable interval(e.g., every 5 minutes) to retrieve real-time weather data for the metros in India. (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad)
- Rolls up the weather data for each day
- Provides daily aggregates for Average temperature, Maximum temperature, Minimum temperature, Dominant weather condition
- Defines user-configurable thresholds for temperature or specific weather conditions (e.g., alert if temperature exceeds 35 degrees Celsius for two consecutive updates)
- Displays daily weather summaries, historical trends, triggered alerts along with temperature conversion between scales 
- Defined test cases over System Setup, Data Retrieval, Temperature Conversion, Daily Weather Summary and Alerting Thresholds
  
## Technologies Used
- OpenWeatherMap API
- Python3
- HTML-CSS
- Flask + Gunicorn
- MySQL (SQLAlchemy + PyMySQL client + Cryptography)
- Pytest
- Docker (v27.3.1)
- DockerCompose (v2.29.7)
- Linux (Ubuntu 24.04)

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/BelieveInTheLimitless/Real-Time-Data-Processing-System
cd Real-Time-Data-Processing-System
```

### 2. Database Configuration
```bash
# Making sure MySQL is not interacting already
sudo systemctl stop mysql
```

### 3.Building and running the docker container
```bash
docker compose up --build
# This step may take a while to complete the database setup, have some snacks handy with you :)
```

### 4.Running the Test cases
```bash
docker compose run test
# Note: The test does not cover app.py, app_frontend.py and database.py while being exhaustive for all scenarios
```


### 5. Running the front-end application
```bash
#open
http://127.0.0.1:5000/
```

### 6. Exiting the application
```bash
# CTRL + C to stop the running container
docker compose down
```

## Screenshots
![Screenshot from 2024-10-25 19-32-47](https://github.com/user-attachments/assets/49d68e69-b7fb-41ff-88b9-5b1f9281ac41)
