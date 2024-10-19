

import pandas as pd
from db import get_db_session
from fastapi import Depends
from model.cost import VesselFuelCost
from sqlmodel import Session


def get_calculate_service(session: Session = Depends(get_db_session)):
    return CalculateService()


class CalculateService:
    def create_dataframe(self, year=2030):
        # 根据年份设置 fuel_gfi 的值
        fuel_gfi1 = (
            0 if year <= 2034 else
            18.8 if year <= 2039 else
            28.2
        )
        fuel_gfi2 = (
            0 if year <= 2039 else
            9.4
        )
        fuel_gfi3 = (
            76.2 if year < 2030 else
            94
        )
        fuel_detail = pd.DataFrame(columns=['fuel_name', 'fuel_gfi', 'emission_factor', 'hfo_conversion',
                                            'mdo_conversion', 'lfo_conversion'])
        # 创建数据   emission_factor == Baseline   ***_conversion  == 折算系数
        data = [
            {'fuel_name': 'bio-LNG', 'fuel_gfi': fuel_gfi1, 'emission_factor': 0.6170,
                'hfo_conversion': 0.88, 'mdo_conversion': 0.86, 'lfo_conversion': 0.88},
            {'fuel_name': 'bio-methanol', 'fuel_gfi': 0, 'emission_factor': 0.9022,
                'hfo_conversion': 2.15, 'mdo_conversion': 2.11, 'lfo_conversion': 2.15},
            {'fuel_name': 'e-LNG', 'fuel_gfi': fuel_gfi2, 'emission_factor': 0.8043,
                'hfo_conversion': 0.88, 'mdo_conversion': 0.86, 'lfo_conversion': 0.88},
            {'fuel_name': 'e-methanol', 'fuel_gfi': 0, 'emission_factor': 0.9674,
                'hfo_conversion': 2.15, 'mdo_conversion': 2.11, 'lfo_conversion': 2.15},
            {'fuel_name': 'e-ammonia', 'fuel_gfi': fuel_gfi2, 'emission_factor': 0.7935,
                'hfo_conversion': 2.3, 'mdo_conversion': 2.26, 'lfo_conversion': 2.3},
            {'fuel_name': 'biodiesel', 'fuel_gfi': fuel_gfi2, 'emission_factor': 0.65,
                'hfo_conversion': 1.03, 'mdo_conversion': 1, 'lfo_conversion': 1.03},
            {'fuel_name': 'LNG', 'fuel_gfi': fuel_gfi2, 'emission_factor': 0.8043,
                'hfo_conversion': 0.88, 'mdo_conversion': 0.86, 'lfo_conversion': 0.88},
            {'fuel_name': 'methanol', 'fuel_gfi': 0, 'emission_factor': 0.9674,
                'hfo_conversion': 2.15, 'mdo_conversion': 2.11, 'lfo_conversion': 2.15},
            {'fuel_name': 'b-ammonia', 'fuel_gfi': fuel_gfi2, 'emission_factor': 0.7935,
                'hfo_conversion': 2.3, 'mdo_conversion': 2.26, 'lfo_conversion': 2.3},
            {'fuel_name': 'HFO', 'fuel_gfi': fuel_gfi3, 'emission_factor': 0,
                'hfo_conversion': 1, 'mdo_conversion': 1, 'lfo_conversion': 1},
            {'fuel_name': 'MDO', 'fuel_gfi': fuel_gfi1, 'emission_factor': 0,
                'hfo_conversion': 1, 'mdo_conversion': 1, 'lfo_conversion': 1},
            {'fuel_name': 'LFO', 'fuel_gfi': fuel_gfi1, 'emission_factor': 0,
                'hfo_conversion': 1, 'mdo_conversion': 1, 'lfo_conversion': 1},
        ]
        fuel_detail = pd.DataFrame(data)
        return fuel_detail

    def form_annual_consumption(self, fuel_df):
        fuel_cf_dict = {'HFO': 3.114, 'MDO': 3.206, 'LFO': 3.151}
        clean_fuel_df = fuel_df.loc[fuel_df['fuel_name'].isin(
            ['HFO', 'MDO', 'LFO'])].copy()
        clean_fuel_name = list(clean_fuel_df['fuel_name'])
        clean_fuel_df[['consumption_cost',
                       'consumption_cf', 'annual_consumption']] = 0
        for clean_name in clean_fuel_name:
            clean_fuel_df.loc[fuel_df['fuel_name'] == clean_name, 'consumption_cf'] = (
                clean_fuel_df['fuel_consumption'] * fuel_cf_dict[clean_name])
            clean_fuel_df.loc[fuel_df['fuel_name'] == clean_name, 'annual_consumption'] = (
                clean_fuel_df)['fuel_consumption']
        # 提取各燃料（HFO、MDO、LFO）的价格（fuel_cost），如果价格为空，则设置为0。
        hfo_price = clean_fuel_df.loc[fuel_df['fuel_name'] == 'HFO', 'fuel_cost'] if not clean_fuel_df.loc[
            clean_fuel_df['fuel_name'] == 'HFO'].empty else 0
        mdo_price = clean_fuel_df.loc[fuel_df['fuel_name'] == 'MDO', 'fuel_cost'] if not clean_fuel_df.loc[
            clean_fuel_df['fuel_name'] == 'MDO'].empty else 0
        lfo_price = clean_fuel_df.loc[fuel_df['fuel_name'] == 'LFO', 'fuel_cost'] if not clean_fuel_df.loc[
            clean_fuel_df['fuel_name'] == 'LFO'].empty else 0
        hfo_price, mdo_price, lfo_price = float(
            hfo_price), float(mdo_price), float(lfo_price)
        form_fuel_df = fuel_df.loc[~fuel_df['fuel_name'].isin(
            ['HFO', 'MDO', 'LFO'])].copy()
        form_fuel_df['annual_consumption'] = form_fuel_df['fuel_consumption'] / \
            len(clean_fuel_name)
        if 'HFO' in clean_fuel_name:
            form_fuel_df['annual_hfo'] = form_fuel_df['annual_consumption'] / \
                form_fuel_df['hfo_conversion']
        else:
            form_fuel_df['annual_hfo'] = 0
        if 'MDO' in clean_fuel_name:
            form_fuel_df['annual_mdo'] = form_fuel_df['annual_consumption'] / \
                form_fuel_df['mdo_conversion']
        else:
            form_fuel_df['annual_mdo'] = 0
        if 'LFO' in clean_fuel_name:
            form_fuel_df['annual_lfo'] = form_fuel_df['annual_consumption'] / \
                form_fuel_df['lfo_conversion']
        else:
            form_fuel_df['annual_lfo'] = 0
        form_fuel_df['consumption_cf'] = 0
        for fuel in fuel_cf_dict.keys():
            form_fuel_df['consumption_cf'] += form_fuel_df['annual_' +
                                                           fuel.lower()] * fuel_cf_dict[fuel]
        form_fuel_df['consumption_cost'] = (form_fuel_df['annual_hfo'] * hfo_price + form_fuel_df['annual_lfo']
                                            * lfo_price + form_fuel_df['annual_mdo'] * mdo_price)
        form_fuel_df['annual_consumption'] = form_fuel_df['annual_mdo'] + form_fuel_df['annual_lfo'] + form_fuel_df[
            'annual_hfo']
        form_fuel_df.drop(
            columns=['annual_hfo', 'annual_mdo', 'annual_lfo'], inplace=True)
        """fuel_df = pd.merge(fuel_df, form_fuel_df[['consumption_cf', 'consumption_cost', 'annual_consumption',
                                                      'fuel_name']], on='fuel_name', how='left')"""
        fuel_df = pd.concat([form_fuel_df, clean_fuel_df],
                            axis=0).reset_index(drop=True)
        return fuel_df, clean_fuel_df

    # 计算燃料总成本
    def get_vessel_fuel_cost(self, year, carbon_unit_price, capacity_unit_price, fuel_list, fee_bate_cost_gap,
                             lca_levy, lca_reward_cost_gap):
        # 各燃料gfi给定值，去数据库表查询？
        fuel_df = pd.DataFrame(list(vars(i) for i in fuel_list.fuel_detail))
        fuel_detail = self.create_dataframe(year=year)
        fuel_df = pd.merge(fuel_df, fuel_detail, on='fuel_name', how='left')

        fuel_df, clean_fuel_df = self.form_annual_consumption(fuel_df)
        # fuel_df['annual_consumption'] = fuel_df['fuel_consumption'] / fuel_df['conversion_factor']

        # gfi_target计算
        if year >= 2050:
            gfi_target = 11.43
        elif year >= 2045:
            gfi_target = 26.67
        elif year >= 2040:
            gfi_target = 49.53
        elif year >= 2035:
            gfi_target = 64.77
        elif year >= 2030:
            gfi_target = 72.39
        else:
            gfi_target = 74.676

        # gfi_attained计算
        gfi_attained = (fuel_df['fuel_gfi'] * fuel_df['fuel_consumption']
                        ).sum() / fuel_df['fuel_consumption'].sum()

        # 碳排放总量    ***_年平均消耗量 * 1 * ***_CF值 * (1 - emission_factor)
        fuel_substitution_rate = 1
        # cf_hfo = 3.114
        # cf_mdo = 3.206
        # cf_lfo = 3.151
        # carbon_emission_total = ((fuel_df['annual_consumption'] * cf_hfo) * (1 - fuel_substitution_rate * fuel_df['emission_factor'])).sum()
        carbon_emission_total = ((1 - fuel_df['emission_factor']) * (
            fuel_df['consumption_cf']) * fuel_substitution_rate).sum()

        # 碳排放费
        carbon_emission_cost = carbon_emission_total * carbon_unit_price

        # 碳排放差价  31.836为固定能量消耗系数   ??
        hfo_gfi = 94
        carbon_emission_difference = (
            hfo_gfi - fuel_df['fuel_gfi']).sum() * carbon_unit_price * 31.836

        # gfi奖励单元
        gfi_reward_unit = max(gfi_target - gfi_attained, 0)

        # 欧盟燃料罚款
        fuel_eu_penalty = max(gfi_attained - gfi_target,
                              0) * gfi_target * 41000 * 2400

        # 燃料费
        fuel_cost_total = (fuel_df['fuel_consumption']
                           * fuel_df['fuel_cost']).sum()

        # 燃料差价
        # hfo_cost = 450
        # fuel_cost_difference = (fuel_df['annual_consumption'] * hfo_cost).sum() - fuel_cost_total
        fuel_cost_difference = (fuel_df['consumption_cost'].sum() - fuel_cost_total +
                                (clean_fuel_df['fuel_consumption'] * clean_fuel_df['fuel_cost']).sum())

        # 运力差价
        capacity_loss = (fuel_df['annual_consumption'] -
                         fuel_df['fuel_consumption']).sum() * capacity_unit_price

        # 合规收益
        compliance_benefit = fuel_cost_difference + \
            carbon_emission_difference + capacity_loss

        # 合规成本
        compliance_cost = carbon_emission_cost + fuel_cost_total

        # 合规利益
        compliance_profit = compliance_benefit - compliance_cost

        # CII评级

        # LCA导则征税
        if gfi_attained > 0:
            lca_tax = max(max(gfi_attained - gfi_target, 0) *
                          lca_levy * carbon_emission_total / gfi_attained, 0)
        else:
            lca_tax = 0  # 或者其他默认值

        # LCA导则奖励
        if gfi_attained > 0:
            lca_reward = gfi_reward_unit * lca_reward_cost_gap * \
                carbon_emission_total * carbon_unit_price / gfi_attained
        else:
            lca_reward = 0  # 或者其他默认值

        # 费率
        if gfi_attained > 0:
            fee_bate = gfi_reward_unit * fee_bate_cost_gap * \
                carbon_emission_total * carbon_unit_price / gfi_attained
        else:
            fee_bate = 0  # 或者其他默认值

        return VesselFuelCost(gfi_attained=gfi_attained, carbon_emission_total=carbon_emission_total,
                              carbon_emission_cost=carbon_emission_cost,
                              carbon_emission_difference=carbon_emission_difference,
                              gfi_reward_unit=gfi_reward_unit,
                              fuel_eu_penalty=fuel_eu_penalty, fuel_cost_total=fuel_cost_total,
                              fuel_cost_difference=fuel_cost_difference, capacity_loss=capacity_loss,
                              compliance_benefit=compliance_benefit, compliance_cost=compliance_cost,
                              compliance_profit=compliance_profit, lca_tax=lca_tax, lca_reward=lca_reward,
                              fee_bate=fee_bate)
