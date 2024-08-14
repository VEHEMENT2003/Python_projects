from flask import Flask, render_template, request
import requests
from datetime import datetime
from config import API_KEY, BASE_URL

app = Flask(__name__)

# Custom filter to convert Unix timestamp to readable time
@app.template_filter('timestamp_to_time')
def timestamp_to_time(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%H:%M %p')

@app.route('/', methods=['GET', 'POST'])
def index():
    city = request.form.get('city')  # Get city name from user input

    weather_data = None
    if city:
        city = city.strip()  # Remove leading/trailing spaces
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()  # Parse the JSON data from the API response
        else:
            weather_data = {'error': 'City not found. Please try again.'}

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
