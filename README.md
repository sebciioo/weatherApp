# WeatherApp - AuraAlert

**AuraAlert** is a web application that allows users to check current and forecasted weather data for selected locations. It is written in Python using the Flask framework, along with libraries such as SQLAlchemy, matplotlib, and the OpenWeatherMap API for retrieving weather data.

## Technologies Used

- **Python**: The main programming language used to build the application.
- **Flask**: A lightweight web framework for building the application.
- **SQLAlchemy**: An Object-Relational Mapping (ORM) tool for database management.
- **OpenWeatherMap API**: Used to fetch weather and air quality data.
- **Matplotlib**: A library for creating charts and data visualizations.

## Features

AuraAlert provides a range of features:

- **Weather Data**: View current and forecasted weather information for various locations.
- **Data Visualization**: Generate visual charts of weather trends for selected cities.
- **Database Integration**: Efficient management of weather data using SQLAlchemy.

### Recommended Test Cities

When testing chart generation, we recommend using one of the following cities, as the database contains the most entries for these locations:

- Toruń
- Katar
- Bydgoszcz

## Installation

To install and run AuraAlert, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd AuraAlert
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add your OpenWeatherMap API key:
   Open the ```config.py``` file and replace `API_KEY` with your actual OpenWeatherMap API key(https://openweathermap.org/):
   ```python
   WEATHER_API_KEY = 'API_KEY'
   ```
5. Run the Flask application:
   ```bash
   flask run
   ```

## Dependencies

The application relies on the following dependencies:

- Flask~=3.0.3
- requests~=2.32.3
- plotly
- pandas
- pytz~=2024.1
- numpy~=1.26.4
- matplotlib~=3.9.0
- SQLAlchemy==1.4.23
- Flask-SQLAlchemy>=3.0.0

## Documentation

There are two detailed documentation files available for the application:

1. **User Documentation (Polish)**: A comprehensive guide for end-users to understand and interact with the application.
2. **Code Documentation (Polish)**: Technical documentation aimed at developers, explaining the application's structure, functions, and implementation details.
