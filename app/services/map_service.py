import folium
from folium.plugins import MarkerCluster, LocateControl
from app.models import get_pilots
from app.services.weather_service import get_weather_layer
from app.services.flight_service import create_flight_markers

def create_map():
    m = folium.Map(
        location=[52.0, 19.0],
        zoom_start=6,
        tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openweathermap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    )

    LocateControl().add_to(m)

    # Dodaj miasta
    add_cities(m)

    # Dodaj pilotów
    pilots = get_pilots()
    marker_cluster = MarkerCluster().add_to(m)
    flight_markers = create_flight_markers(pilots)
    for marker in flight_markers:
        marker.add_to(marker_cluster)

    # Dodaj warstwy pogodowe
    weather_layers = get_weather_layer()
    for layer in weather_layers.values():
        layer.add_to(m)

    # Dodaj kontrolkę warstw
    folium.LayerControl().add_to(m)

    return m

def add_cities(m):
    cities = [
        ("Warsaw", 52.2297, 21.0122),
        ("Krakow", 50.0647, 19.9450),
        ("Gdansk", 54.3520, 18.6466),
        ("Poznan", 52.4064, 16.9252),
        ("Wroclaw", 51.1079, 17.0385),
        ("Lodz", 51.7592, 19.4560),
        ("Szczecin", 53.4285, 14.5528),
        ("Bydgoszcz", 53.1235, 18.0084),
        ("Lublin", 51.2465, 22.5684),
    ]

    for city, lat, lon in cities:
        folium.Marker(
            [lat, lon],
            icon=folium.DivIcon(html=f'<div style="font-size: 10pt; color: gray;">{city}</div>')
        ).add_to(m)