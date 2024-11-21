import aiohttp
import asyncio
from datetime import datetime
import sys
import time


# Установка политики для Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def fetch_open_meteo(session, city, lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    async with session.get(url) as response:
        data = await response.json()
        temperature = data["current_weather"]["temperature"]
        return f"{city} (open-meteo.com): {temperature}°C"

async def fetch_wttr(session, city):
    url = f"https://wttr.in/{city}?format=%t"
    async with session.get(url) as response:
        temperature = await response.text()
        return f"{city} (wttr.in): {temperature.strip()}°C"

async def main(cities_coords):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for city, (lat, lon) in cities_coords.items():
            tasks.append(fetch_open_meteo(session, city, lat, lon))
            tasks.append(fetch_wttr(session, city))

        results = await asyncio.gather(*tasks)

        print(f"Результаты на {datetime.now()}:\n")
        for result in results:
            print(result)

if __name__ == "__main__":
    
    start_time = time.time()
    
    cities_coords = {
        "Moscow": (55.7558, 37.6173),
        "London": (51.5074, -0.1278),
        "New York": (40.7128, -74.0060)
    }
    asyncio.run(main(cities_coords))
    
    end_time = time.time()  
    execution_time = end_time - start_time  
    print(f"\nВремя выполнения программы: {execution_time:.2f} секунд")
