import requests
import json
import tap
import logging
import pymongo
from typing import Dict, Any, List
from src.ingestion import constants

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO
)
logging.getLogger(__name__).info("Configured logging with level=INFO")


class RandomDataMongoDbIngestionTap(tap.Tap):
    resource_type: str
    size: int
    collection: str
    response_type: str = "json"
    timeout: int = 60


def get_resources(resource_type: str,
                  size: int,
                  response_type: str = "json",
                  timeout: int = 60) -> List[Dict[str, Any]]:
    base_uri = "https://random-data-api.com/api/v2"

    r = requests.get(f"{base_uri}/{resource_type}?size={size}&response_type={response_type}", timeout=timeout)
    r.raise_for_status()
    users = json.loads(r.content)
    # Always return a list of dictionary even if it is just one dictionary
    users = users if isinstance(users, list) else [users]
    return users


def insert_data(client: pymongo.MongoClient,
                database: str,
                collection: str,
                data: List[Dict[str, Any]]) -> None:
    client[database][collection].insert_many(data)


def run(resource_type: str,
        size: int,
        collection: str,
        response_type: str = "json",
        timeout: int = 60
        ):
    logging.info(f"Getting {size} {resource_type}")
    users = get_resources(resource_type=resource_type,
                          size=size,
                          response_type=response_type,
                          timeout=timeout)

    logging.info(f"Connecting to MongoDB at {constants.MONGODB_HOST}")
    mongo_client = pymongo.MongoClient(constants.MONGODB_HOST,
                                       username=constants.MONGODB_USER,
                                       password=constants.MONGODB_PASSWORD)

    logging.info(f"Writing to database {resource_type} with collection {collection}")
    insert_data(client=mongo_client,
                database=resource_type,
                collection=collection,
                data=users)


def main():
    args = RandomDataMongoDbIngestionTap().parse_args()

    logging.info(f"Resource Type: {args.resource_type}")
    logging.info(f"Size: {args.size}")
    logging.info(f"Collection: {args.collection}")
    logging.info(f"Response Type: {args.response_type}")
    logging.info(f"Timeout: {args.timeout}")

    run(resource_type=args.resource_type,
        collection=args.collection,
        size=args.size,
        response_type=args.response_type,
        timeout=args.timeout)


if __name__ == "__main__":
    main()
