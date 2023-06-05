## Random Data Ingestion
This is a repository for ingesting data generated from [random-data-api](https://random-data-api.com/).
The data is first ingested into a MongoDB database (staging layer) before relevant fields are extracted
and loaded into a PostgreSQL relational database.

## Quick Start
Start the MongoDB and PostgreSQL servers (data will be mounted at `./data` directory) by running
```
docker-compose up
```
In a separate terminal, run the bash script `run.sh` to build the required Docker 
image for the ingestion and run the ingestion code in the container
```
bash run.sh
```

## Structuring the solution in AWS environment
Using AWS, we can massively increase the scalability of this pipeline through
1. Use of Amazon S3 as a data lake for the staging layer. 
This allows large amount of data to be stored and allow for more flexibility in terms of the file formats. 
We are no longer tied to JSON format.
2. Use of Amazon Redshift for the relational database. Redshift has many optimisations that allow for big data analytics
such as columnar storage, query optimisation and data compression
3. Use of distributed processing framework such as Spark to perform the data processing.
4. Use of Airflow to orchestrate the pipeline.