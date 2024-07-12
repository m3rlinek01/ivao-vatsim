import requests
from shapely.geometry import Point, Polygon

# Przybliżone współrzędne granic Polski
POLAND_COORDINATES = [
    (14.123, 52.844), (14.074, 53.918), (16.364, 54.513),
    (18.196, 54.862), (19.661, 54.454), (20.979, 54.361),
    (22.731, 54.355), (23.484, 54.096), (23.527, 52.636),
    (23.706, 52.389), (23.598, 52.286), (23.587, 52.046),
    (23.803, 51.910), (24.029, 51.578), (24.145, 50.853),
    (22.776, 49.019), (22.558, 49.085), (21.607, 49.470),
    (18.853, 49.496), (18.392, 49.988), (17.649, 50.049),
    (16.942, 50.457), (16.202, 50.396), (15.491, 50.777),
    (15.017, 51.026), (14.706, 51.099), (14.593, 51.745),
    (14.119, 52.087), (14.123, 52.844)
]

POLAND_POLYGON = Polygon(POLAND_COORDINATES)

def is_over_poland(lat, lon):
    try:
        point = Point(float(lon), float(lat))
        return POLAND_POLYGON.contains(point)
    except ValueError:
        return False

def fetch_ivao_data():
    url = "https://api.ivao.aero/v2/tracker/whazzup"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        pilots = data.get('pilots', [])

        polish_pilots = []
        for pilot in pilots:
            last_track = pilot.get('lastTrack', {})
            lat = last_track.get('latitude')
            lon = last_track.get('longitude')
            if lat is not None and lon is not None and is_over_poland(lat, lon):
                try:
                    polish_pilots.append(parse_ivao_pilot(pilot))
                except Exception as e:
                    print(f"Błąd podczas parsowania danych pilota IVAO: {e}")

        return polish_pilots
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania danych IVAO: {e}")
        return []

def fetch_vatsim_data():
    url = "https://data.vatsim.net/v3/vatsim-data.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        pilots = data.get('pilots', [])

        polish_pilots = []
        for pilot in pilots:
            lat = pilot.get('latitude')
            lon = pilot.get('longitude')
            if lat is not None and lon is not None and is_over_poland(lat, lon):
                try:
                    polish_pilots.append(parse_vatsim_pilot(pilot))
                except Exception as e:
                    print(f"Błąd podczas parsowania danych pilota VATSIM: {e}")

        return polish_pilots
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania danych VATSIM: {e}")
        return []

def parse_ivao_pilot(pilot):
    last_track = pilot.get('lastTrack', {})
    flight_plan = pilot.get('flightPlan', {})
    aircraft = flight_plan.get('aircraft', {})

    return {
        'callsign': pilot.get('callsign', 'N/A'),
        'aircraft': aircraft.get('icaoCode', 'N/A'),
        'aircraft_model': aircraft.get('model', 'N/A'),
        'departure': flight_plan.get('departureId', 'N/A'),
        'arrival': flight_plan.get('arrivalId', 'N/A'),
        'latitude': last_track.get('latitude'),
        'longitude': last_track.get('longitude'),
        'altitude': last_track.get('altitude', 'N/A'),
        'groundspeed': last_track.get('groundSpeed', 'N/A'),
        'heading': last_track.get('heading', 'N/A'),
        'transponder': last_track.get('transponder', 'N/A'),
        'transponder_mode': last_track.get('transponderMode', 'N/A'),
        'flight_rules': flight_plan.get('flightRules', 'N/A'),
        'route': flight_plan.get('route', 'N/A'),
        'network': 'IVAO',
        'user_id': pilot.get('userId', 'N/A'),
        'rating': pilot.get('rating', 'N/A'),
        'simulator': pilot.get('pilotSession', {}).get('simulatorId', 'N/A'),
        'state': last_track.get('state', 'N/A'),
        'arrival_distance': last_track.get('arrivalDistance', 'N/A'),
        'departure_distance': last_track.get('departureDistance', 'N/A'),
        'flight_plan_id': flight_plan.get('id', 'N/A'),
        'speed': flight_plan.get('speed', 'N/A'),
        'level': flight_plan.get('level', 'N/A'),
        'people_on_board': flight_plan.get('peopleOnBoard', 'N/A'),
        'last_updated': last_track.get('timestamp', 'N/A')
    }

def parse_vatsim_pilot(pilot):
    flight_plan = pilot.get('flight_plan', {})
    return {
        'callsign': pilot.get('callsign', 'N/A'),
        'aircraft': flight_plan.get('aircraft_short', 'N/A'),
        'departure': flight_plan.get('departure', 'N/A'),
        'arrival': flight_plan.get('arrival', 'N/A'),
        'latitude': pilot.get('latitude'),
        'longitude': pilot.get('longitude'),
        'altitude': pilot.get('altitude', 'N/A'),
        'groundspeed': pilot.get('groundspeed', 'N/A'),
        'heading': pilot.get('heading', 'N/A'),
        'transponder': pilot.get('transponder', 'N/A'),
        'flight_rules': flight_plan.get('flight_rules', 'N/A'),
        'route': flight_plan.get('route', 'N/A'),
        'network': 'VATSIM'
    }

def update_flight_data():
    ivao_pilots = fetch_ivao_data()
    vatsim_pilots = fetch_vatsim_data()
    all_pilots = ivao_pilots + vatsim_pilots
    return all_pilots