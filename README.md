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

## 🚀 Deploy en OpenStack (CESGA)

### 1. Conexión a la instancia

```bash
# Conectarse a la instancia usando la llave privada
ssh -i /ruta/a/tu/llave/privada cesgaxuser@10.133.27.7
```

### 2. Verificar el funcionamiento

```bash
# Ver contenedores en ejecución
docker ps

# Ver logs de la aplicación
docker-compose -f docker-compose.prod.yml logs -f citybikes

# Verificar datos en MongoDB
docker exec -it $(docker ps -q -f name=mongodb) mongosh
# Una vez dentro de MongoDB:
use citybikes
db.stations.countDocuments({})
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

4. Exportar datos:

#### Opción A: Exportar desde MongoDB local
```bash
python src/export_data.py
```

#### Opción B: Exportar desde MongoDB Atlas

1. Configura a conexión con MongoDB Atlas:
```env
MONGODB_URL=mongodb+srv://tu_usuario:tu_password@tu_cluster.mongodb.net/
```

2. Executa o script de exportación:
```bash
python src/export_data.py
```

📁 Os ficheiros exportados gardaranse no directorio `data/` co formato:
- `citybikes_data_AAAAMMDD_HHMMSS.csv`
- `citybikes_data_AAAAMMDD_HHMMSS.parquet`

> ℹ️ O script de exportación detectará automaticamente a fonte dos datos (MongoDB local ou Atlas) baseándose na variable de contorno MONGODB_URL.

### 3. Opcións de execución do script contra MongoDB Atlas:

#### Opción A: Usando a variable de contorno desde liña de comandos:

```bash
docker build -t citybikes .
docker run -e MONGODB_URL="mongodb+srv://tu_usuario:tu_password@tu_cluster.mongodb.net/" citybikes
```

#### Opción B: Usando un arquivo .env:

```bash
docker build -t citybikes .
docker run --env-file .env citybikes
```

Para que isto funcione, necesitas:

1. Crear un arquivo `.env` coa túa URL de MongoDB Atlas:

```env
MONGODB_URL=mongodb+srv://tu_usuario:tu_password@tu_cluster.mongodb.net/
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

## 🐳 Docker Hub

A imaxe do proxecto está dispoñible en Docker Hub:

```bash
docker pull askhem/citybikes:latest
```

### Execución con Docker Hub

1. Execución simple:

```bash
docker run -d askhem/citybikes:latest
```

2. Execución con MongoDB usando docker-compose:

```bash
# Descarga o arquivo docker-compose.prod.yml
wget https://raw.githubusercontent.com/ASKhem/citybikes-collector/main/docker-compose.prod.yml

# Executa os servizos
docker compose -f docker-compose.prod.yml up -d
```

### Actualización automática

O proxecto está configurado con GitHub Actions para actualizar automaticamente a imaxe en Docker Hub cando se fan cambios no repositorio.

Podes ver a imaxe en: [Docker Hub - askhem/citybikes](https://hub.docker.com/r/askhem/citybikes)

## 🔄 Integración Continua e Despliegue

### GitHub Actions

O proxecto utiliza GitHub Actions para a integración continua. Cada vez que se fai un push á rama `main`, automaticamente:

1. Constrúese unha nova imaxe Docker
2. Súbese a imaxe a Docker Hub
3. Actualízase a tag `latest`

Para configurar GitHub Actions no teu fork:

1. Configura os seguintes secrets no teu repositorio:
   - `DOCKERHUB_USERNAME`: O teu nome de usuario en Docker Hub
   - `DOCKERHUB_TOKEN`: O teu token de acceso de Docker Hub

2. Asegúrate de que as GitHub Actions teñen permisos de escritura:
   - Settings → Actions → General
   - En "Workflow permissions" selecciona "Read and write permissions"

### Monitorización

Os datos recóllense cada 5 minutos (300 segundos). Estimación de documentos:

- Por hora: 588 documentos (49 estacións × 12 actualizacións)
- Por día: 14,112 documentos
- Por mes: ~423,360 documentos

> ℹ️ Estes cálculos están baseados nas 49 estacións de Bicicoruña

### Mantemento

Para manter o servizo actualizado en producción:

```bash
# Actualizar a última versión
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

Para automatizar as actualizacións:
```bash
# Crear script de actualización
cat > update.sh << 'EOF'
#!/bin/bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
EOF

chmod +x update.sh

# Configurar actualización diaria ás 4 AM
(crontab -l 2>/dev/null; echo "0 4 * * * $PWD/update.sh") | crontab -
```
