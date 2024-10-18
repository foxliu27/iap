from typing import List

from pydantic import BaseModel


class FuelDetail(BaseModel):
    fuel_name: str
    fuel_cost: float
    fuel_consumption: float


class FuelList(BaseModel):
    fuel_detail: List[FuelDetail]
