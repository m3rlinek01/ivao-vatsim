import sqlite3
from datetime import datetime

def init_database():
    conn = sqlite3.connect('pilots.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS current_pilots
                 (callsign TEXT PRIMARY KEY, aircraft TEXT, aircraft_model TEXT,
                 departure TEXT, arrival TEXT, latitude REAL, longitude REAL,
                 altitude INTEGER, groundspeed INTEGER, heading INTEGER,
                 transponder TEXT, transponder_mode TEXT, flight_rules TEXT,
                 route TEXT, network TEXT, user_id INTEGER, rating INTEGER,
                 simulator TEXT, state TEXT, arrival_distance REAL,
                 departure_distance REAL, flight_plan_id INTEGER,
                 speed TEXT, level TEXT, people_on_board INTEGER,
                 last_updated TEXT)''')
    conn.commit()
    conn.close()

def get_pilots():
    conn = sqlite3.connect('pilots.db')
    c = conn.cursor()
    c.execute('SELECT * FROM current_pilots')
    pilots = c.fetchall()
    conn.close()
    return pilots

def update_database(pilots):
    conn = sqlite3.connect('pilots.db')
    c = conn.cursor()

    try:
        c.execute('DELETE FROM current_pilots')

        for pilot in pilots:
            try:
                c.execute('''INSERT OR REPLACE INTO current_pilots VALUES 
                             (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (pilot['callsign'], pilot['aircraft'], pilot['departure'], pilot['arrival'],
                           pilot['latitude'], pilot['longitude'], pilot['altitude'], pilot['groundspeed'],
                           pilot['heading'], pilot['transponder'], pilot['flight_rules'],
                           pilot['route'], pilot['network'], pilot.get('cid', 'N/A'),
                           pilot.get('name', 'N/A'), pilot.get('server', 'N/A'),
                           pilot.get('qnh_mb', 'N/A'), pilot.get('logon_time', 'N/A'),
                           pilot.get('last_updated', 'N/A')))
            except sqlite3.Error as e:
                print(f"Błąd podczas wstawiania danych pilota do bazy: {e}")

        conn.commit()
    except sqlite3.Error as e:
        print(f"Błąd bazy danych: {e}")
        conn.rollback()
    finally:
        conn.close()