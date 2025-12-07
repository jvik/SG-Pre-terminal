from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.db.session import supabase
from app.api import deps
from app import models
import csv
import io

router = APIRouter()

@router.get("/csv")
def export_transactions_csv(user: models.User = Depends(deps.get_current_user)):
    """
    Export all transactions for the current user as a CSV file.
    """
    try:
        user_id = user.id
        
        # Fetch transactions with category names
        # Using Supabase foreign table join syntax: categories(name)
        # This assumes a foreign key relationship exists between transactions.category_id and categories.id
        response = supabase.table('transactions').select('*, categories(name)').eq('user_id', str(user_id)).order('date', desc=True).execute()

        output = io.StringIO()
        writer = csv.writer(output)

        # Write Header
        writer.writerow(['Date', 'Description', 'Category', 'Amount', 'Type'])

        if response.data:
            transactions = response.data
            for t in transactions:
                # Handle joined category data
                # Supabase returns joined data as a nested dictionary or list of dictionaries
                category_name = "Uncategorized"
                categories_data = t.get('categories')
                
                if categories_data:
                    # If it's a dict (single relation)
                    if isinstance(categories_data, dict):
                        category_name = categories_data.get('name', 'Uncategorized')
                    # If it's a list (shouldn't be for Many-to-One, but safe to check)
                    elif isinstance(categories_data, list) and len(categories_data) > 0:
                        category_name = categories_data[0].get('name', 'Uncategorized')
                
                writer.writerow([
                    t.get('date', ''),
                    t.get('description', ''),
                    category_name,
                    t.get('amount', 0.0),
                    t.get('type', '')
                ])

        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=export.csv"}
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
