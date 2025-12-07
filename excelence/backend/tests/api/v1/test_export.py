import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, PropertyMock
import uuid
from datetime import date

def test_export_csv(authenticated_client: TestClient, mock_supabase_db, USER_ID):
    mock_execute = MagicMock()
    today = date.today()
    category_id = uuid.uuid4()
    transaction_id = uuid.uuid4()

    # Mock response data with joined category
    type(mock_execute).data = PropertyMock(return_value=[
        {
            "id": str(uuid.uuid4()),
            "amount": 1000.0,
            "type": "income",
            "date": str(today),
            "description": "Salary",
            "user_id": str(USER_ID),
            "category_id": str(uuid.uuid4()),
            "categories": {"name": "Work"}
        },
        {
            "id": str(transaction_id),
            "amount": 50.0,
            "type": "expense",
            "date": str(today),
            "description": "Groceries",
            "user_id": str(USER_ID),
            "category_id": str(category_id),
            "categories": {"name": "Food"}
        }
    ])
    
    # Mock the chain: table().select().eq().order().execute()
    # Note: The order of calls must match the implementation: table -> select -> eq -> order -> execute
    mock_supabase_db.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_execute

    response = authenticated_client.get("/api/v1/export/csv")
    
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment; filename=export.csv" in response.headers["content-disposition"]
    
    content = response.text
    assert "Date,Description,Category,Amount,Type" in content
    assert f"{today},Groceries,Food,50.0,expense" in content
    assert f"{today},Salary,Work,1000.0,income" in content

def test_export_csv_empty(authenticated_client: TestClient, mock_supabase_db, USER_ID):
    mock_execute = MagicMock()
    type(mock_execute).data = PropertyMock(return_value=[])
    
    mock_supabase_db.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_execute

    response = authenticated_client.get("/api/v1/export/csv")
    
    assert response.status_code == 200
    content = response.text
    assert "Date,Description,Category,Amount,Type" in content
    # Should only contain header
    lines = content.strip().split('\n')
    assert len(lines) == 1
    assert lines[0] == "Date,Description,Category,Amount,Type"

def test_export_csv_unauthenticated(client: TestClient):
    response = client.get("/api/v1/export/csv")
    # Assuming global auth middleware or dependency handles 401
    assert response.status_code == 401
