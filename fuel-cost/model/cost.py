from pydantic import BaseModel


class VesselFuelCost(BaseModel):
    gfi_attained: float
    carbon_emission_total: float          # 碳排放总量
    carbon_emission_cost: float           # 碳排放费
    carbon_emission_difference: float     # 碳排放差价
    gfi_reward_unit: float                # GFI奖励单元
    fuel_eu_penalty: float                # 燃料欧盟罚款
    fuel_cost_total: float                # 燃料费
    fuel_cost_difference: float           # 燃料差价
    capacity_loss: float                  # 运力损失
    compliance_benefit: float    # 合规收益
    compliance_cost: float   # 合规成本
    compliance_profit: float   # 合规利润
    lca_tax: float      # LCA导则征税
    lca_reward: float   # LCA导则奖励
    fee_bate: float     # Fee_bate
