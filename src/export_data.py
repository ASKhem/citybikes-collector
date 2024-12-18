import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import sys
import os
from dotenv import load_dotenv

def export_data():
    try:
        # Cargar configuración de MongoDB desde .env
        load_dotenv()
        mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
        
        client = MongoClient(mongodb_url)
        db = client['citybikes']
        collection = db['stations']
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Asegurar que existe el directorio data
        os.makedirs('data', exist_ok=True)
        
        # Exportar datos con los mismos campos que fetch_data.py guarda
        data = list(collection.find({}, {
            '_id': 0,
            'station_id': 1,
            'timestamp': 1,
            'empty_slots': 1,
            'free_bikes': 1,
            'name': 1,
            'last_updated': 1,
            'slots': 1,
            'normal_bikes': 1,
            'ebikes': 1
        }))
        
        df = pd.DataFrame(data)
        
        if not df.empty:
            df.to_csv(f'data/citybikes_data{timestamp}.csv', index=False)
            df.to_parquet(f'data/citybikes_data{timestamp}.parquet', index=False)
            print(f"Exportado {len(df)} registros desde {mongodb_url}")
        else:
            print("No se encontraron datos para exportar.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    export_data()