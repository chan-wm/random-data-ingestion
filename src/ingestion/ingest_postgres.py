import psycopg2
import pymongo
import logging
from src.ingestion import constants
import tap
from typing import List, Dict, Any, Tuple
from psycopg2 import sql

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO
)
logging.getLogger(__name__).info("Configured logging with level=INFO")


class RandomDataPostgresIngestionTap(tap.Tap):
    mongo_database: str
    mongo_collection: str
    pg_table: str


def get_data(client: pymongo.MongoClient,
             database: str,
             collection: str) -> List[Dict[str, Any]]:
    return list(client[database][collection].find())


def extract_relevant_fields(data: List[Dict[str, Any]]) -> List[Tuple[str, str, str, str, str]]:
    return [(ele["uid"], ele["first_name"], ele["last_name"], ele["gender"], ele["address"]["country"])
            for ele in data]


def run(mongo_database: str,
        mongo_collection: str,
        pg_table: str):

    logging.info("Connecting to MongoDB")
    mongo_client = pymongo.MongoClient(constants.MONGODB_HOST,
                                       username=constants.MONGODB_USER,
                                       password=constants.MONGODB_PASSWORD)

    logging.info("Querying data from MongoDB")
    data = get_data(client=mongo_client,
                    database=mongo_database,
                    collection=mongo_collection)

    logging.info("Extracting relevant fields")
    values = extract_relevant_fields(data=data)

    logging.info("Connecting to PostgreSQL")
    conn = psycopg2.connect(host=constants.POSTGRES_HOST,
                            user=constants.POSTGRES_USER,
                            password=constants.POSTGRES_PASSWORD,
                            port=constants.POSTGRES_PORT,
                            database="postgres")
    conn.autocommit = True

    try:
        cursor = conn.cursor()

        logging.info("Creating table in PostgreSQL")
        cursor.execute(
            sql.SQL("""
        CREATE TABLE IF NOT EXISTS {pg_table} (
        uid VARCHAR(50) PRIMARY KEY,
        first_name VARCHAR(50) NULL,
        last_name VARCHAR(50) NULL,
        gender VARCHAR(20) NULL,
        country VARCHAR(50) NULL
        )
        """).format(pg_table=sql.Identifier(pg_table)))

        args = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s)", value).decode("utf-8") for value in values)
        logging.info("Inserting data into PostgreSQL")
        cursor.execute(
            sql.SQL(
            """
            INSERT INTO {pg_table} (uid, first_name, last_name, gender, country) VALUES
            """
            + args +
            """
            ON CONFLICT DO NOTHING
            """
            ).format(pg_table=sql.Identifier(pg_table)))
    finally:
        cursor.close()
        conn.commit()
        conn.close()


def main():
    args = RandomDataPostgresIngestionTap().parse_args()

    logging.info(f"Mongo Database: {args.mongo_database}")
    logging.info(f"Mongo Collection: {args.mongo_collection}")
    logging.info(f"Postgres Table: {args.pg_table}")

    run(mongo_database=args.mongo_database,
        mongo_collection=args.mongo_collection,
        pg_table=args.pg_table)


if __name__ == "__main__":
    main()
