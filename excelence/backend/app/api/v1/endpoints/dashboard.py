from typing import Any

from fastapi import APIRouter, Depends

from app import crud, models
from app.api import deps
from app.schemas import Summary, ChartDataResponse

router = APIRouter()


@router.get("/summary", response_model=Summary)
def read_summary(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve financial summary.
    """
    summary = crud.transactions.get_summary(user_id=current_user.id)
    return summary


@router.get("/chart-data", response_model=ChartDataResponse)
def get_chart_data(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve chart data (expenses by category).
    """
    data = crud.transactions.get_expenses_by_category(user_id=current_user.id)
    return {"status": "success", "data": data}
