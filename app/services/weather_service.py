import folium
from app import app

def get_weather_layer():
    return {
        'clouds': folium.TileLayer(
            tiles='https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=' + app.config['OPENWEATHERMAP_API_KEY'],
            attr='OpenWeatherMap',
            name='Clouds',
            overlay=True,
            control=True
        ),
        'wind': folium.TileLayer(
            tiles='https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=' + app.config['OPENWEATHERMAP_API_KEY'],
            attr='OpenWeatherMap',
            name='Wind',
            overlay=True,
            control=True
        )
    }