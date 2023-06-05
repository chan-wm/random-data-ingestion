# Build the docker image
docker build -t random-data-ingestor:1.0.0 .

# Get the time. This will be used as the `collection` key in MongoDB
TIME=$(date +"%Y-%m-%dT%H:%M:%S%z")
RESOURCE_TYPE=users
SIZE=100
PG_TABLE=user_info

# Call the API and ingest into MongoDB
docker run --network container:random-data-ingestion-mongodb random-data-ingestor:1.0.0 \
python src/ingestion/ingest_mongodb.py --resource_type $RESOURCE_TYPE --size $SIZE --collection $TIME

# Read from MongoDB, extract relevant fields and load into PostgreSQL
docker run --network container:random-data-ingestion-postgres random-data-ingestor:1.0.0 \
python src/ingestion/ingest_postgres.py --mongo_database $RESOURCE_TYPE --mongo_collection $TIME --pg_table $PG_TABLE