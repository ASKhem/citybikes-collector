import requests
import time
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['citybikes']
collection = db['stations']

def fetch_data(network_id='bicicorunha'):
    try:
        network_response = requests.get(f'http://api.citybik.es/v2/networks/{network_id}')
        stations = network_response.json().get('network', {}).get('stations', [])
        
        for station in stations:
            collection.update_one({'id': station['id']}, {'$set': station}, upsert=True)
            print(f"Actualizada estación: {station.get('name', 'Sin nombre')}")
            
    except requests.RequestException as e:
        print(f"Error al obtener datos: {e}")

if __name__ == "__main__":
    while True:
        fetch_data()
        time.sleep(60)