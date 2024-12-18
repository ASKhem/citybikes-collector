import requests
import time
from pymongo import MongoClient
import os
from datetime import datetime, timezone
import logging

# logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)

mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
if not mongodb_url:
    raise ValueError("MONGODB_URL environment variable is not set")

try:
    client = MongoClient(mongodb_url)
    client.server_info()
    logger.info("MongoDB conectado")
except Exception as e:
    logger.error(f"Error MongoDB: {e}")
    raise

db = client['citybikes']
collection = db['stations']

def fetch_data(network_id='bicicorunha'):
    try:
        network_response = requests.get(f'http://api.citybik.es/v2/networks/{network_id}')
        stations = network_response.json().get('network', {}).get('stations', [])
        
        timestamp = datetime.now(timezone.utc)
        stations_updated = 0
        
        for station in stations:
            station_data = {
                'station_id': station['id'],
                'timestamp': timestamp,
                'empty_slots': station.get('empty_slots'),
                'free_bikes': station.get('free_bikes'),
                'name': station.get('name'),
                'last_updated': station.get('extra', {}).get('last_updated'),
                'slots': station.get('extra', {}).get('slots'),
                'normal_bikes': station.get('extra', {}).get('normal_bikes', station.get('free_bikes')),
                'ebikes': station.get('extra', {}).get('ebikes', 0)
            }
            
            collection.insert_one(station_data)
            stations_updated += 1
            
        logger.info(f"Actualizadas {stations_updated} estaciones")
            
    except requests.RequestException as e:
        logger.error(f"Error API: {e}")

if __name__ == "__main__":
    logger.info("Servicio iniciado")
    while True:
        fetch_data()
        time.sleep(300)