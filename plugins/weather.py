import os
import requests

# MCP metadata
DESCRIPTION = "Get current weather information for a location"
SCHEMA = {
    "type": "object",
    "properties": {
        "city": {
            "type": "string",
            "description": "The city name to get weather for"
        },
        "units": {
            "type": "string",
            "description": "Temperature units",
            "enum": ["metric", "imperial", "kelvin"],
            "default": "metric"
        }
    },
    "required": ["city"]
}

def run(params):
    city = params.get("city", "")
    if not city:
        return {
            "tool": "weather",
            "error": "Missing 'city' parameter"
        }
    
    # Get API key from environment
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        # Fallback to mock data if no API key
        return {
            "tool": "weather",
            "city": city,
            "result": f"Mock weather data: The weather in {city} is sunny with 25°C (no API key configured)"
        }
    
    units = params.get("units", "metric")
    
    try:
        # Call OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather"
        response = requests.get(url, params={
            "q": city,
            "appid": api_key,
            "units": units
        })
        
        if response.status_code == 200:
            data = response.json()
            return {
                "tool": "weather",
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "units": units,
                "result": f"Weather in {city}: {data['weather'][0]['description']}, {data['main']['temp']}°{'C' if units == 'metric' else 'F' if units == 'imperial' else 'K'}"
            }
        else:
            return {
                "tool": "weather",
                "error": f"Weather API error: {response.status_code} - {response.text}"
            }
    except Exception as e:
        return {
            "tool": "weather",
            "error": f"Weather service error: {str(e)}"
        }
