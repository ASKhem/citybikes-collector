# 🚲 CityBikes Data Collector

## 📝 Descrición

Este proxecto é unha ferramenta para recoller e exportar datos das estacións de bicicletas públicas. Permite obter información en tempo real sobre a dispoñibilidade de bicicletas e gardar os datos en diferentes formatos para a súa posterior análise.

## ⭐ Características principais

- 🔄 Recollida de datos en tempo real das estacións de bicicletas
- 💾 Almacenamento en MongoDB
- 📊 Exportación de datos en formatos CSV e Parquet
- 📡 Monitorización do estado das estacións
- 🔋 Seguimento de bicicletas normais e eléctricas

## 📚 Guía rápida de inicio

### 1. Clonar o repositorio:

```bash
git clone https://github.com/ASKhem/data-fetching-scripts.git
cd citybikes-collector
```

### 2. Escolle unha opción para executar:

#### Opción A: Con Docker e MongoDB local (Recomendado para probas)

1. Construír e executar con Docker Compose:

```bash
docker compose up -d
```

#### Opción B: Con Docker e MongoDB Atlas

1. Configura o arquivo .env:

```env
MONGODB_URL=mongodb+srv://user:password@cluster.mongodb.net/
```

2. Comenta o servizo mongodb no docker-compose.yml e executa:

```bash
docker compose up -d citybikes
```

#### Opción C: Execución local

1. Crear contorno virtual:

```bash
conda create -n citybikes python=3.12
pip install -r requirements.txt
```

2. Instalar Contenedor con MongoDB:

⚠️ O contenedor non persiste os datos. Unha vez que se para o contendor eliminarase.

```bash
docker run --rm --name mongo-container -d -p 27017:27017 mongo
```

3. Executar a aplicación:

```bash
python src/fetch_data.py
```

4. Exportar datos (opcional):

```bash
python src/export_data.py
```

📁 Os ficheiros exportados gardaranse no directorio `data/` co formato:

- `citybikes_data_AAAAMMDD_HHMMSS.csv`
- `citybikes_data_AAAAMMDD_HHMMSS.parquet`

## ⚙️ Configuración

O proxecto utiliza unha base de datos MongoDB local por defecto:

- 🔗 URL: `mongodb://localhost:27017/`
- 💾 Base de datos: `citybikes`
- 📁 Colección: `stations`

## 📂 Estructura do proxecto

```bash
citybikes-collector/
├── src/
│   ├── fetch_data.py     # Script para obter datos das estacións
│   └── export_data.py    # Script para exportar datos a CSV/Parquet
├── data/                 # Directorio para os ficheiros exportados
├── .env                  # Variables de contorno (tes que crear o teu)
├── docker-compose.yml    # Configuración de servizos Docker
├── Dockerfile
├── requirements.txt      # Dependencias do proxecto
└── README.md
```

## 📚 Dependencias principais

- `pandas`: Manipulación e análise de datos
- `pymongo`: Conexión con MongoDB
- `pyarrow`: Soporte para formato Parquet
- `requests`: Para realizar solicitudes HTTP
- `time`: Para introducir retardos
- `datetime`: Para obter a data e hora actual

## 🌐 CityBikes API

Este proxecto utiliza a API de CityBikes para recoller datos sobre a dispoñibilidade de bicicletas.

URL: [URL](https://api.citybik.es/v2/)

### Endpoints Principais

1. **Listar Redes de Bicicletas**
   - **URL**: `http://api.citybik.es/v2/networks`
   - **Resposta**:

    ```json
    {
    "networks": [
        {
        "id": "bicicorunha",
        "name": "Bicicoruña",
        "location": {
            "latitude": 43.3623,
            "longitude": -8.4115,
            "city": "A Coruña",
            "country": "ES"
        },
        "href": "/v2/networks/bicicorunha",
        "company": [
            "PBSC Urban Solutions"
        ],
        "gbfs_href": "https://acoruna.publicbikesystem.net/customer/gbfs/v2/gbfs.json"
        }
    ]
    }
    ```

2. **Obter Información sobre unha Rede**
   - **URL**: `http://api.citybik.es/v2/networks/{network_id}`
   - **Resposta**:

     ```json
     {
       "network": {
         "id": "bicicorunha",
         "name": "Bicicoruña",
         "location": {...},
         "href": "/v2/networks/bicicorunha",
         "company": [
           "PBSC Urban Solutions"
         ],
         "gbfs_href": "https://acoruna.publicbikesystem.net/customer/gbfs/v2/gbfs.json",
         "stations": [
           {
             "id": "023efce1bbb332a1b918d56aeb671890",
             "name": "Avenida de Arteixo",
             "latitude": 43.360755,
             "longitude": -8.410942,
             "timestamp": "2024-12-10T13:23:47.619019Z",
             "free_bikes": 5,
             "empty_slots": 10,
             "extra": {...}
             ...
           }
         ]
       }
     }
     ```

### Filtrado de Campos

Engade `?fields=list,of,fields` á URL para filtrar os campos na resposta. Por exemplo:

```bash
http://api.citybik.es/v2/networks?fields=id,name
```

### Formato

A API devolve datos en formato JSON.
