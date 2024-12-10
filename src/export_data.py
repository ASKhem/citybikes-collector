import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import sys

def export_data():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['citybikes']
        collection = db['stations']
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') #Para nomear os ficheiros
        
        # Exportar datos
        data = list(collection.find({}, {
            '_id': 0,
            'id': 1,
            'name': 1,
            'timestamp': 1,
            'free_bikes': 1,
            'empty_slots': 1,
            'extra': 1   
        }))
        
        df = pd.DataFrame(data)

        # Normalizar columnas de 'extra'
        if not df.empty and 'extra' in df.columns:
            extra_columns = ['uid', 'last_updated', 'slots', 'normal_bikes', 'ebikes']
            extra_df = pd.json_normalize(df['extra'])[extra_columns]
            df = pd.concat([df.drop(columns=['extra']), extra_df], axis=1)
        
        if not df.empty:
            df.to_csv(f'data/citybikes_data{timestamp}.csv', index=False)
            df.to_parquet(f'data/citybikes_data{timestamp}.parquet', index=False)
            print(f"Exportado {len(df)} registros.")
        else:
            print("No se encontraron datos para exportar.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    export_data()