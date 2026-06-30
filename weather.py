import requests
import config


def get_weather():
    """
    Fetches current weather for the configured city.
    Returns a dict on success, or None if it fails
    (bad key, no internet, key not active yet, etc.)
    """
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": config.WEATHER_CITY,
            "appid": config.WEATHER_API_KEY,
            "units": config.WEATHER_UNITS
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if response.status_code != 200:
            print(f"Weather API error: {data.get('message', 'unknown error')}")
            return None

        return {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "condition": data["weather"][0]["description"].title(),
            "city": data["name"]
        }
    except Exception as e:
        print(f"Weather fetch failed: {e}")
        return None