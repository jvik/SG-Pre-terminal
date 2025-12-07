from typing import List
from pydantic import BaseModel

class ChartDataPoint(BaseModel):
    category_name: str
    total_amount: float

class ChartDataResponse(BaseModel):
    status: str
    data: List[ChartDataPoint]
