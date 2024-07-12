from app import app
from app.models import init_database
from app.services.data_service import update_flight_data
import threading
import time

def update_data_periodically():
    while True:
        update_flight_data()
        time.sleep(60)  # Aktualizuj co minutę

if __name__ == '__main__':
    init_database()
    data_thread = threading.Thread(target=update_data_periodically)
    data_thread.daemon = True
    data_thread.start()
    app.run(debug=True)