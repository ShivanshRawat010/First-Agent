from langchain_core.tools import tool
from dotenv import load_dotenv

import os
import requests

load_dotenv()

@tool
def get_weather(city : str) -> str:
  """Returns the weather conditions of the place"""

  url = os.getenv("VISUAL_CROSSING_URL").replace("<LOCATION_INPUT>", city).replace("<API_KEY>", os.getenv("VISUAL_CROSSING_API_KEY"))
  response = requests.get(url=url)

  if response.status_code != 200:
    return "Couldn't fetch weather details."

  data = response.json()

  weather = {
    "location": data["resolvedAddress"],
    "temperature": data["currentConditions"]["temp"],
    "feels_like": data["currentConditions"]["feelslike"],
    "conditions": data["currentConditions"]["conditions"],
    "humidity": data["currentConditions"]["humidity"],
    "wind_speed": data["currentConditions"]["windspeed"],
    "visibility": data["currentConditions"]["visibility"]
  }

  return weather