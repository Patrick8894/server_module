from mongomock_motor import AsyncMongoMockClient
import pytest

@pytest.fixture
def mock_motor_collection():
    client = AsyncMongoMockClient()
    db = client["test_db"]
    
    return db