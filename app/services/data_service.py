import requests
from app import app
from app.models import init_database, update_database

def fetch_ivao_data():
    url = "https://api.ivao.aero/v2/tracker/whazzup"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        pilots = data.get('clients', {}).get('pilots', [])

        parsed_pilots = []
        for pilot in pilots:
            try:
                parsed_pilots.append(parse_ivao_pilot(pilot))
            except Exception as e:
                print(f"Błąd podczas parsowania danych pilota IVAO: {e}")

        return parsed_pilots
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

        parsed_pilots = []
        for pilot in pilots:
            try:
                parsed_pilots.append(parse_vatsim_pilot(pilot))
            except Exception as e:
                print(f"Błąd podczas parsowania danych pilota VATSIM: {e}")

        return parsed_pilots
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania danych VATSIM: {e}")
        return []

def parse_ivao_pilot(pilot):
    last_track = pilot.get('lastTrack', {})
    flight_plan = pilot.get('flightPlan') or {}  # Użyj pustego słownika, jeśli flightPlan jest None
    return {
        'callsign': pilot.get('callsign', 'N/A'),
        'aircraft': flight_plan.get('aircraftId', 'N/A'),
        'departure': flight_plan.get('departureId', 'N/A'),
        'arrival': flight_plan.get('arrivalId', 'N/A'),
        'latitude': last_track.get('latitude'),
        'longitude': last_track.get('longitude'),
        'altitude': last_track.get('altitude', 'N/A'),
        'groundspeed': last_track.get('groundSpeed', 'N/A'),
        'heading': last_track.get('heading', 'N/A'),
        'transponder': last_track.get('transponder', 'N/A'),
        'flight_rules': flight_plan.get('flightRules', 'N/A'),
        'route': flight_plan.get('route', 'N/A'),
        'network': 'IVAO'
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
        'network': 'VATSIM',
        'cid': pilot.get('cid', 'N/A'),
        'name': pilot.get('name', 'N/A'),
        'server': pilot.get('server', 'N/A'),
        'qnh_mb': pilot.get('qnh_mb', 'N/A'),
        'logon_time': pilot.get('logon_time', 'N/A'),
        'last_updated': pilot.get('last_updated', 'N/A')
    }

def update_flight_data():
    ivao_pilots = fetch_ivao_data()
    vatsim_pilots = fetch_vatsim_data()
    all_pilots = ivao_pilots + vatsim_pilots
    update_database(all_pilots)