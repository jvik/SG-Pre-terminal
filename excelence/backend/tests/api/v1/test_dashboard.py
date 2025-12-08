from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, PropertyMock

from app.core.config import settings

def test_get_financial_summary_integration(
    authenticated_client: TestClient,
    USER_ID,
) -> None:
    """
    Test the financial summary endpoint, mocking the database RPC call.
    This verifies the integration from the API endpoint to the CRUD layer.
    """
    # 1. Define the mock summary data that the RPC call should return
    mock_summary_data = {
        "total_income": 1250.75,
        "total_expenses": 300.50,
        "net_balance": 950.25
    }

    # 2. Mock the supabase.rpc call
    with patch('app.db.session.supabase.rpc') as mock_rpc:
        # Configure the mock to return the desired data structure
        mock_execute = MagicMock()
        type(mock_execute).data = PropertyMock(return_value=[mock_summary_data])
        mock_rpc.return_value.execute.return_value = mock_execute

        # 3. Call the API endpoint
        response = authenticated_client.get(
            f"{settings.API_V1_STR}/dashboard/summary"
        )
        
        # 4. Assert the response
        assert response.status_code == 200
        content = response.json()
        assert content["total_income"] == mock_summary_data["total_income"]
        assert content["total_expenses"] == mock_summary_data["total_expenses"]
        assert content["net_balance"] == mock_summary_data["net_balance"]
        
        # 5. Verify that the RPC was called correctly
        mock_rpc.assert_called_once_with(
            'get_user_financial_summary',
            {'p_user_id': str(USER_ID)}
        )

def test_get_chart_data_integration(
    authenticated_client: TestClient,
    USER_ID,
) -> None:
    """
    Test the chart data endpoint, mocking the database RPC call.
    """
    mock_chart_data = [
        {"category_name": "Food", "total_amount": 100.0},
        {"category_name": "Transport", "total_amount": 50.0}
    ]

    with patch('app.db.session.supabase.rpc') as mock_rpc:
        mock_execute = MagicMock()
        type(mock_execute).data = PropertyMock(return_value=mock_chart_data)
        mock_rpc.return_value.execute.return_value = mock_execute

        response = authenticated_client.get(
            f"{settings.API_V1_STR}/dashboard/chart-data"
        )
        
        assert response.status_code == 200
        content = response.json()
        assert content["status"] == "success"
        assert len(content["data"]) == 2
        assert content["data"][0]["category_name"] == "Food"
        assert content["data"][0]["total_amount"] == 100.0
        
        mock_rpc.assert_called_once_with(
            'get_expenses_by_category',
            {'p_user_id': str(USER_ID)}
        )

def test_get_chart_data_empty(
    authenticated_client: TestClient,
    USER_ID,
) -> None:
    """
    Test chart data with no expenses.
    """
    with patch('app.db.session.supabase.rpc') as mock_rpc:
        mock_execute = MagicMock()
        type(mock_execute).data = PropertyMock(return_value=[])
        mock_rpc.return_value.execute.return_value = mock_execute

        response = authenticated_client.get(
            f"{settings.API_V1_STR}/dashboard/chart-data"
        )
        
        assert response.status_code == 200
        content = response.json()
        assert content["status"] == "success"
        assert content["data"] == []

def test_get_financial_summary_no_transactions(
    authenticated_client: TestClient,
    USER_ID,
) -> None:
    """
    Test the financial summary endpoint when the user has no transactions.
    """
    with patch('app.db.session.supabase.rpc') as mock_rpc:
        # Configure the mock to return an empty list, simulating no data
        mock_execute = MagicMock()
        type(mock_execute).data = PropertyMock(return_value=[])
        mock_rpc.return_value.execute.return_value = mock_execute

        response = authenticated_client.get(
            f"{settings.API_V1_STR}/dashboard/summary"
        )
        
        assert response.status_code == 200
        content = response.json()
        assert content["total_income"] == 0
        assert content["total_expenses"] == 0
        assert content["net_balance"] == 0
        
        mock_rpc.assert_called_once_with(
            'get_user_financial_summary',
            {'p_user_id': str(USER_ID)}
        )