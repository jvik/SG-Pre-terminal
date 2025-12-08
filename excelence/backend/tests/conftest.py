import pytest
from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path
import uuid
from unittest.mock import MagicMock, patch

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Set test environment variables before importing app
os.environ["TESTING"] = "true"
os.environ.setdefault("SECRET_KEY", "test_secret_key_for_testing_only")
os.environ.setdefault("SUPABASE_URL", "http://localhost:54321")
os.environ.setdefault("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdNz54uxxlswPOe5IOOI1s")


from main import app

USER_DELETED_MESSAGE = "Transaction deleted successfully"
@pytest.fixture
def USER_ID():
    """Yields the mock user's ID."""
    return USER_ID_VALUE

USER_ID_VALUE = uuid.uuid4()

class MockSupabaseUser:
    def __init__(self, id, email="test@example.com"):
        self.id = id
        self.email = email

class MockGotrueResponse:
    def __init__(self, user):
        self.user = user

@pytest.fixture
def mock_supabase_auth_user(mocker, USER_ID):
    """Mocks supabase.auth.get_user to return a mock user."""
    mock_user = MockSupabaseUser(id=USER_ID)
    return mocker.patch(
        "app.db.session.supabase.auth.get_user",
        return_value=MockGotrueResponse(user=mock_user),
    )
    
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def authenticated_client(client, mock_supabase_auth_user):
    """Yields a test client with authenticated headers."""
    client.headers["Authorization"] = "Bearer fake-token"
    yield client
    del client.headers["Authorization"]

@pytest.fixture
def mock_supabase_db(mocker):
    return mocker.patch('app.db.session.supabase.table')
