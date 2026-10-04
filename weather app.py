import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.parse
import json


# Get weather from Open-Meteo
def get_weather():

    city = city_entry.get().strip()

    if city == "":
        messagebox.showwarning("Error", "Please enter a city.")
        return

    try:
        # Find the city
        city_url = (
            "https://geocoding-api.open-meteo.com/v1/search?"
            + urllib.parse.urlencode({
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            })
        )

        with urllib.request.urlopen(city_url) as response:
            city_data = json.loads(response.read().decode())

        if "results" not in city_data:
            messagebox.showerror("Error", "City not found.")
            return

        location = city_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        city_name = location["name"]
        country = location.get("country", "")

        # Get weather
        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            + urllib.parse.urlencode({
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,"
                           "apparent_temperature,wind_speed_10m,"
                           "weather_code",
                "timezone": "auto"
            })
        )

        with urllib.request.urlopen(weather_url) as response:
            weather_data = json.loads(response.read().decode())

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        feels_like = current["apparent_temperature"]
        wind = current["wind_speed_10m"]
        weather_code = current["weather_code"]

        # Convert weather code into text
        condition = get_weather_condition(weather_code)

        # Show information
        city_label.config(text=f"{city_name}, {country}")

        temperature_label.config(
            text=f"{temperature}°C"
        )

        condition_label.config(
            text=condition
        )

        feels_label.config(
            text=f"Feels like: {feels_like}°C"
        )

        humidity_label.config(
            text=f"Humidity: {humidity}%"
        )

        wind_label.config(
            text=f"Wind speed: {wind} km/h"
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            "Could not get weather.\n\n"
            "Check your internet connection."
        )


# Weather descriptions
def get_weather_condition(code):

    if code == 0:
        return "☀️ Clear Sky"

    elif code in [1, 2, 3]:
        return "⛅ Partly Cloudy"

    elif code in [45, 48]:
        return "🌫️ Foggy"

    elif code in [51, 53, 55]:
        return "🌦️ Drizzle"

    elif code in [61, 63, 65]:
        return "🌧️ Rainy"

    elif code in [71, 73, 75]:
        return "❄️ Snowy"

    elif code in [80, 81, 82]:
        return "🌧️ Rain Showers"

    elif code in [95, 96, 99]:
        return "⛈️ Thunderstorm"

    else:
        return "🌤️ Unknown"


# --------------------------------
# CREATE WINDOW
# --------------------------------

window = tk.Tk()

window.title("Weather App")
window.geometry("450x550")
window.resizable(False, False)


# --------------------------------
# TITLE
# --------------------------------

title = tk.Label(
    window,
    text="Weather App",
    font=("Arial", 28, "bold")
)

title.pack(pady=25)


# --------------------------------
# SEARCH BOX
# --------------------------------

city_entry = tk.Entry(
    window,
    width=25,
    font=("Arial", 15)
)

city_entry.pack(pady=10)

city_entry.insert(0, "Enter city")


search_button = tk.Button(
    window,
    text="Search Weather",
    font=("Arial", 13, "bold"),
    command=get_weather
)

search_button.pack(pady=10)


# --------------------------------
# WEATHER INFORMATION
# --------------------------------

city_label = tk.Label(
    window,
    text="City",
    font=("Arial", 22, "bold")
)

city_label.pack(pady=25)


temperature_label = tk.Label(
    window,
    text="--°C",
    font=("Arial", 45, "bold")
)

temperature_label.pack()


condition_label = tk.Label(
    window,
    text="Weather",
    font=("Arial", 18)
)

condition_label.pack(pady=10)


feels_label = tk.Label(
    window,
    text="Feels like: --°C",
    font=("Arial", 13)
)

feels_label.pack(pady=5)


humidity_label = tk.Label(
    window,
    text="Humidity: --%",
    font=("Arial", 13)
)

humidity_label.pack(pady=5)


wind_label = tk.Label(
    window,
    text="Wind speed: -- km/h",
    font=("Arial", 13)
)

wind_label.pack(pady=5)


# --------------------------------
# RUN APP
# --------------------------------

window.mainloop()