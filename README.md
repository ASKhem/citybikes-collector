# 🚲 CityBikes Data Collector

## 📝 Descrición
Este proxecto é unha ferramenta para recoller e exportar datos das estacións de bicicletas públicas. Permite obter información en tempo real sobre a dispoñibilidade de bicicletas e gardar os datos en diferentes formatos para a súa posterior análise.

## ⭐ Características principais
- 🔄 Recollida de datos en tempo real das estacións de bicicletas
- 💾 Almacenamento en MongoDB
- 📊 Exportación de datos en formatos CSV e Parquet
- 📡 Monitorización do estado das estacións
- 🔋 Seguimento de bicicletas normais e eléctricas

## 📂 Requisitos previos
- Python 3.8 ou superior
- MongoDB instalado e en execución
- pip (xestor de paquetes de Python)

## 📚 Dependencias principais
- `pandas`: Manipulación e análise de datos
- `pymongo`: Conexión con MongoDB
- `pyarrow`: Soporte para formato Parquet
- `requests`: Para realizar solicitudes HTTP
- `time`: Para introducir retardos
- `datetime`: Para obter a data e hora actual

## 🚀 Instalación

### 1. Clonar o repositorio:
```bash
git clone https://github.com/ASKhem/data-fetching-scripts.git
cd citybikes-collector
```

### 2. Instalar Contenedor con MongoDB:
⚠️ O contenedor non persiste os datos. Unha vez que se para o contendor eliminarase.
```bash
docker run --rm --name mongo-container -d -p 27017:27017 mongo
```

## ⚙️ Configuración
O proxecto utiliza unha base de datos MongoDB local por defecto:
- 🔗 URL: `mongodb://localhost:27017/`
- 💾 Base de datos: `citybikes`
- 📁 Colección: `stations`

## 📂 Estructura do proxecto
```bash
citybikes-collector/
├── src/
│ ├── fetch_data.py  # Script para obter datos das estacións
│ └── export_data.py # Script para exportar datos a CSV/Parquet
├── data/            # Directorio para os ficheiros exportados
├── requirements.txt # Dependencias do proxecto
└── README.md        # Documentación
```

## 📋 Uso

### 1. Recollida de datos
Para iniciar a recollida de datos das estacións:
```bash
python src/fetch_data.py
```

### 2. Exportación de datos
Para exportar os datos recollidos a un ficheiro CSV ou Parquet:
```bash
python src/export_data.py
```

📁 Os ficheiros exportados gardaranse no directorio `data/` co formato:
- `citybikes_data_AAAAMMDD_HHMMSS.csv`
- `citybikes_data_AAAAMMDD_HHMMSS.parquet`

## 📊 Estrutura dos datos
Os datos recollidos inclúen:
- `id`: Identificador único da estación
- `name`: Nome da estación
- `timestamp`: Data e hora da recollida
- `free_bikes`: Número de bicicletas dispoñibles
- `empty_slots`: Número de ancoraxes libres
- `uid`: Identificador único universal
- `last_updated`: Última actualización dos datos
- `slots`: Número total de ancoraxes
- `normal_bikes`: Número de bicicletas convencionais
- `ebikes`: Número de bicicletas eléctricas

Exemplo de CSV:
```bash
id,empty_slots,free_bikes,name,timestamp,uid,last_updated,slots,normal_bikes,ebikes
023efce1bbb332a1b918d56aeb671890,13,2,Avenida de Arteixo,2024-12-10T08:32:47.715830Z,53,1733819412,15,2,0
02cecd02915c86d7ab8034b61b19da0e,15,0,Mercado de Monte Alto,2024-12-10T08:32:47.715734Z,43,1733819453,15,0,0
030c4027b0bea390e562645c7082db4c,15,10,Los Rosales,2024-12-10T08:32:47.714591Z,11,1733819469,25,10,0
0e3aa0134a2f3d07ae5bd093e6af9a33,0,19,Plaza de Portugal,2024-12-10T08:32:47.715870Z,55,1733819364,20,19,0
104e0797759d11ac22a61cfed357800b,19,0,Ventorrillo,2024-12-10T08:32:47.714938Z,27,1733819465,19,0,0
```
