from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime, timedelta
import pytz
import json

app = Flask(__name__)

# Load the weather data from CSV
weather_data = pd.read_csv("weather.csv")
# Convert event_start column to datetime
weather_data['event_start'] = pd.to_datetime(weather_data['event_start'])

def get_forecasts(now, then):
    # Convert strings to datetime objects and localize to UTC
    now = parse_datetime_without_offset_and_convert_to_utc(now)
    then = parse_datetime_without_offset_and_convert_to_utc(then)

    # Filter data based on belief horizon and event start time
    filtered_data = weather_data[weather_data['event_start'] <= pd.Timestamp(then) - timedelta(hours=3)]
    filtered_data = filtered_data[filtered_data['event_start'] >= pd.Timestamp(now) - timedelta(hours=3)]
    
    # Group data by event type and get the latest forecasts
    latest_forecasts = filtered_data.groupby('sensor').apply(lambda x: x.nlargest(1, 'belief_horizon_in_sec'))
    
    return latest_forecasts[['event_start', 'event_value', 'sensor']].to_dict(orient='records')

def get_tomorrow_forecast(now):
    # Convert string to datetime object and localize to UTC
    now = parse_datetime_without_offset_and_convert_to_utc(now)
    
    # Convert now to the local timezone (you may need to change 'Europe/Berlin' to your local timezone)
    local_now = now.astimezone(pytz.timezone('Europe/Berlin'))
    
    # Calculate tomorrow's date in the local timezone
    tomorrow = local_now + timedelta(days=1)
    
    # Filter data for tomorrow in the local timezone
    tomorrow_data = weather_data[weather_data['event_start'].dt.date == tomorrow.date()]
    
    # Calculate boolean values for warm, sunny, and windy
    is_warm = tomorrow_data['event_value'].max() >= 25
    is_sunny = tomorrow_data[tomorrow_data['sensor'] == 'irradiance']['event_value'].max() >= 200
    is_windy = tomorrow_data[tomorrow_data['sensor'] == 'wind speed']['event_value'].max() >= 5
    
    return {
        "is_warm": str(is_warm),
        "is_sunny": str(is_sunny),
        "is_windy": str(is_windy)
    }


def parse_datetime_without_offset_and_convert_to_utc(datetime_str):
    naive_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    local_timezone = pytz.timezone('UTC')  # Specify your local timezone here
    localized_datetime = local_timezone.localize(naive_datetime)
    return localized_datetime.astimezone(pytz.utc)


@app.route('/forecasts', methods=['GET'])
def forecasts():
    data = request.json
    if data is None or 'now' not in data or 'then' not in data:
        return jsonify({"error": "Please provide 'now' and 'then' parameters in JSON body."}), 400

    now = data['now']
    then = data['then']
    
    forecasts = get_forecasts(now, then)
    return jsonify(forecasts)

@app.route('/tomorrow', methods=['GET'])
def tomorrow():
    data = request.json
    
    if data is None or 'now' not in data:
        return jsonify({"error": "Please provide 'now' parameter in JSON body."}), 400
    
    now = data['now']
    
    forecast = get_tomorrow_forecast(now)
    return jsonify(forecast)

if __name__ == '__main__':
    app.run(debug=True)
