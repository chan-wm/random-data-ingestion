from src.ingestion import ingest_mongodb
import pytest
from typing import List, Any, Dict


@pytest.mark.parametrize(
    ["resource_type", "size", "mock_content", "expected_output"],
    [
        ["users", 2,
         b'[{"id": 2, "name": "John"}, {"id": 5, "name": "Jane"}]',
         [{"id": 2, "name": "John"}, {"id": 5, "name": "Jane"}]
         ],
        ["users", 1,
         b'{"id": 2, "name": "John"}',
         [{"id": 2, "name": "John"}]
         ],
    ]
)
def test_get_resources(requests_mock,
                       resource_type: str,
                       size: int,
                       mock_content: bytes,
                       expected_output: List[Dict[str, Any]]):
    requests_mock.get(f"https://random-data-api.com/api/v2/{resource_type}?size={size}&response_type=json",
                      content=mock_content)

    assert ingest_mongodb.get_resources(resource_type=resource_type, size=size) == expected_output
