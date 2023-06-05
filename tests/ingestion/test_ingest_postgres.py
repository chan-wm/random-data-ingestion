from src.ingestion import ingest_postgres
from typing import List, Dict, Any, Tuple
import pytest


@pytest.mark.parametrize(
    ["data", "expected_output"],
    [
        [
            [
                {"uid": "aer234",
                 "first_name": "John",
                 "last_name": "Doe",
                 "gender": "Male",
                 "address": {"country": "UK"}
                 },
                {"uid": "aep123",
                 "id": "7098",
                 "first_name": "Jane",
                 "last_name": "Doe",
                 "gender": "Female",
                 "address": {"country": "US"}
                 }
            ],
            [("aer234", "John", "Doe", "Male", "UK"), ("aep123", "Jane", "Doe", "Female", "US")]
        ]
    ]
)
def test_extract_relevant_fields(data: List[Dict[str, Any]], expected_output: List[Tuple[str, str, str, str, str]]):
    assert ingest_postgres.extract_relevant_fields(data=data) == expected_output
