import uuid
from app.db.session import supabase

def delete_transaction(transaction_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """
    Deletes a transaction by its ID for a specific user.
    Returns True if deletion was successful (record found and deleted), False otherwise.
    """
    response = supabase.table('transactions').delete().match({
        'id': str(transaction_id),
        'user_id': str(user_id)
    }).execute()

    if response.data:
        return True
    return False

def get_summary(user_id: uuid.UUID) -> dict:
    """
    Retrieves the financial summary for a user by calling a database function.
    This performs the aggregation at the database level for better performance.
    """
    response = supabase.rpc(
        'get_user_financial_summary',
        {'p_user_id': str(user_id)}
    ).execute()

    if response.data:
        # RPC returns a list, we expect a single result object
        return response.data[0]
    
    # Return a zero-summary if there's no data
    return {
        "total_income": 0,
        "total_expenses": 0,
        "net_balance": 0
    }

