import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, PropertyMock
import uuid

def test_delete_transaction_success(authenticated_client: TestClient, mock_supabase_db, USER_ID):
    mock_execute = MagicMock()
    # Return a list with one item to simulate successful deletion
    type(mock_execute).data = PropertyMock(return_value=[{"id": str(uuid.uuid4())}])
    
    mock_supabase_db.return_value.delete.return_value.match.return_value.execute.return_value = mock_execute
    
    transaction_id = uuid.uuid4()
    response = authenticated_client.delete(
        f"/api/v1/transactions/{transaction_id}",
    )
    
    assert response.status_code == 200
    assert response.json() == {"detail": "Transaction deleted successfully"}
    
    # Verify the correct calls were made
    mock_supabase_db.assert_called_with('transactions')
    mock_supabase_db.return_value.delete.assert_called_once()
    mock_supabase_db.return_value.delete.return_value.match.assert_called_with({
        'id': str(transaction_id),
        'user_id': str(USER_ID)
    })

def test_delete_transaction_not_found(authenticated_client: TestClient, mock_supabase_db, USER_ID):
    mock_execute = MagicMock()
    # Return empty list to simulate not found or not owned by user
    type(mock_execute).data = PropertyMock(return_value=[])
    
    mock_supabase_db.return_value.delete.return_value.match.return_value.execute.return_value = mock_execute
    
    transaction_id = uuid.uuid4()
    response = authenticated_client.delete(
        f"/api/v1/transactions/{transaction_id}",
    )
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Transaction not found or user does not have permission."}
