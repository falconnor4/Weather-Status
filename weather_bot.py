import requests
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Vancouver"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if "weather" not in response:
        print(f"API Error Response: {response}")
        return "Unknown Risk"
    
    condition = response['weather'][0]['main'].lower()
    
    mapping = {
        "rain": "Slight Risk of Rain",
        "drizzle": "Minor Risk of Rain",
        "thunderstorm": "High Risk of Rain",
        "clear": "No Risk!",
        "clouds": "Slight Risk of Clouds",
        "snow": "Slight Risk of Snow"
    }
    return mapping.get(condition, f"Risk of {condition.capitalize()}")

def update_discord(text):
    header = {"Authorization": DISCORD_TOKEN, "Content-Type": "application/json"}
    data = {"custom_status": {"text": text}}
    r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=header, json=data)
    return r.status_code

if __name__ == "__main__":
    weather_text = get_weather()
    status = update_discord(weather_text)
    print(f"Status: {status} - Updated to: {weather_text}")
