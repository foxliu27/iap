from datetime import datetime

from fastapi import Depends, FastAPI, Query
from model.cost import VesselFuelCost
from model.fuel import FuelList
from model.response import ResponseModel
from service.calculate import CalculateService, get_calculate_service

api = FastAPI()


@api.post("/fuel/cost", summary="计算燃料总成本")
async def get_fuel_cost(
        fuel_list: FuelList,
        year: int = Query(default=datetime.now().year,
                          ge=1700, le=5000, description='年份'),
        carbon_unit_price: float = Query(default=500, description='碳单价'),
        capacity_unit_price: float = Query(default=2000, description='运力单价'),
        fee_bate_cost_gap: float = Query(default=None, description=''),
        lca_levy: int = Query(default=None, description=''),
        lca_reward_cost_gap: float = Query(default=None, description=''),
        service: CalculateService = Depends(get_calculate_service),
) -> ResponseModel[VesselFuelCost]:
    fuel_cost = service.get_vessel_fuel_cost(year, carbon_unit_price, capacity_unit_price, fuel_list, fee_bate_cost_gap,
                                             lca_levy, lca_reward_cost_gap)
    return {"code": 200, "data": fuel_cost, "message": "查询成功"}


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=9089)
