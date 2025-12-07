import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, PropertyMock
import uuid
from datetime import date

def test_create_transaction(authenticated_client: TestClient, mock_supabase_db, USER_ID):
    mock_execute = MagicMock()
    today = date.today()
    category_id = uuid.uuid4()
    transaction_id = uuid.uuid4()
    
    type(mock_execute).data = PropertyMock(return_value=[{
        "id": transaction_id,
        "amount": 50.0,
        "type": "expense",
        "date": str(today),
        "description": "Groceries",
        "user_id": USER_ID,
        "category_id": category_id
    }])
    mock_supabase_db.return_value.insert.return_value.execute.return_value = mock_execute

    response = authenticated_client.post(
        "/api/v1/transactions/",
        json={
            "amount": 50.0,
            "type": "expense",
            "date": str(today),
            "description": "Groceries",
            "category_id": str(category_id)
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 50.0
    assert data["type"] == "expense"
    assert data["description"] == "Groceries"
    assert data["user_id"] == str(USER_ID)
    assert data["category_id"] == str(category_id)
    assert data["id"] == str(transaction_id)
