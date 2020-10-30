from mesa import Agent
from energy_model.random_walk import RandomWalker
import random
import numpy as np

# Set Nuclear Cost
d = .07
nuclear_plantlife = int(np.random.normal(loc=60, scale=4))
nuclear_CRF = ((d * (1 + d) ** nuclear_plantlife) / ((1 + d) ** (nuclear_plantlife) - 1))
nuclear_capitalcost = 5530
#  set nuclear-efficiency ((85 + random 10) / 100)
nuclear_efficiency = ((85 + (random.randint(0, 10)) / 100))
nuclear_operationscost = 93.28
nuclear_variablecost = 2.14
nuclear_fuelcost = .76
nuclear_heatrate = 10450

# Calculating Nuclear CRF
nuclear_CRF = ((d * (1 + d) ** nuclear_plantlife) / ((1 + d) ** (nuclear_plantlife) - 1))


def nuclear_cost(nuclear_plantlife, nuclear_efficiency, nuclear_capitalcost, nuclear_operationscost,
                 nuclear_varible_cost, nuclear_fuelcost, nuclear_heatrate):
    return ((nuclear_capitalcost * nuclear_CRF) / (8760 * nuclear_efficiency) +
            (nuclear_operationscost) / (8760 * nuclear_efficiency) +
            (nuclear_variablecost) / (1000) +
            (nuclear_fuelcost * nuclear_heatrate) / (1000000))


nuclear_result = nuclear_cost(nuclear_plantlife, nuclear_efficiency, nuclear_capitalcost, nuclear_operationscost,
                              nuclear_variablecost, nuclear_fuelcost, nuclear_heatrate)

print("The nuclear cost is", nuclear_result)

# Calculating Nuclear_Cost
nuclear_cost = ((nuclear_capitalcost * nuclear_CRF) / (8760 * nuclear_efficiency) +
                (nuclear_operationscost) / (8760 * nuclear_efficiency) + (nuclear_variablecost) / (1000)
                + (nuclear_fuelcost * nuclear_heatrate) / (1000000))

# Set_coal_cost
coal_plantlife = int(np.random.normal(loc=60, scale=4))
coal_efficiency = ((50 + (random.randint(0, 5)) / 100))
coal_capitalcost = 5227
coal_operationscost = 80.53
coal_variablecost = 9.51
coal_fuelcost = 2.34
coal_heatrate = (np.random.normal(loc=10557, scale=1050))

coal_CRF = ((d * (1 + d) ** (coal_plantlife)) / ((1 + d) ** (coal_plantlife) - 1))


def coal_cost(coal_plantlife, coal_efficiency, coal_capitalcost, coal_operationscost, coal_variablecost, coal_fuelcost,
              coal_heatrate):
    return ((coal_capitalcost * coal_CRF) / (8760 * coal_efficiency) +
            (coal_operationscost) / (8760 * coal_efficiency) +
            (coal_variablecost) / (1000) +
            (coal_fuelcost * coal_heatrate) / (1000000))


coal_result = coal_cost(coal_plantlife, coal_efficiency, coal_capitalcost, coal_operationscost, coal_variablecost,
                        coal_fuelcost, coal_heatrate)

print("The coal cost is", coal_result)
# set gas_cost
gas_plantlife = int(np.random.normal(loc=45, scale=4))
gas_efficiency = ((43 + (random.randint(0, 5)) / 100))
gas_capitalcost = 1200
gas_operationscost = 10.17
gas_variablecost = 2.60
gas_fuelcost = 4.40
gas_heatrate = (np.random.normal(loc=6989, scale=478))

gas_CRF = ((d * (1 + d) ** (gas_plantlife)) / ((1 + d) ** (gas_plantlife) - 1))


def gas_cost(gas_plantlife, gas_efficiency, gas_capitalcost, gas_operationscost, gas_variablecost, gas_fuelcost,
             gas_heatrate):
    return ((gas_capitalcost * gas_CRF) / (8760 * gas_efficiency) +
            (gas_operationscost) / (8760 * gas_efficiency) +
            (gas_variablecost) / (1000) +
            (gas_fuelcost * gas_heatrate) / (1000000))


gas_result = gas_cost(gas_plantlife, gas_efficiency, gas_capitalcost, gas_operationscost, gas_variablecost,
                      gas_fuelcost, gas_heatrate)

print("The gas cost is", gas_result)

##solar cost
d_solar = 0.1
solar_plantlife = (18 + random.randint(0, 5))
solar_efficiency = ((14 + random.randint(0, 4)) / 100)
solar_capitalcost = 2524
solar_operationscost = 27.75
solar_CRF = ((d_solar * (1 + d_solar) ** (solar_plantlife)) / ((1 + d_solar) ** (solar_plantlife) - 1))


def solar_cost(olar_plantlife, solar_efficiency, solar_capitalcost, solar_operationscost):
    return ((solar_capitalcost * solar_CRF) / (8760 * solar_efficiency) +
            (solar_operationscost) / (8760 * solar_efficiency))


solar_cost_result = solar_cost(solar_plantlife, solar_efficiency, solar_capitalcost, solar_operationscost)

print("The solar cost is", solar_cost_result)

##solar cost
d_wind = 0.057
wind_plantlife = (18 + random.randint(0, 5))
wind_efficiency = ((35 + random.randint(0, 46)) / 100)
wind_capitalcost = 1686
wind_operationscost = 46.71

wind_CRF = ((d_wind * (1 + d_wind) ** (wind_plantlife)) / ((1 + d_wind) ** (wind_plantlife) - 1))


def wind_cost(wind_capitalcost, wind_CRF, wind_efficiency, wind_operationscost):
    return ((wind_capitalcost * wind_CRF) / (8760 * wind_efficiency) + (wind_operationscost) / (8760 * wind_efficiency))


wind_cost_result = wind_cost(wind_capitalcost, wind_CRF, wind_efficiency, wind_operationscost)

print("The wind cost is", wind_cost_result)

# ADDED THIS IN TO INCREASE THE INITIAL COST OF RENEWABLES DUE TO STORAGE/RELIABILITY NEEDS:
solar_cost = solar_cost_result * 1.5
wind_cost = wind_cost_result * 1.5

# setting up the capacities
# setting the plant sizes ub MW
nuclear_plantsize = 1100
coal_plantsize = 400
gas_plantsize = 800
wind_plantsize = 1.5
solar_plantsize = 14

power = ["nuclear", "gas", "coal"]

nuclear_capacities = [1268, 636, 1174, 1130]
nuclear_total_capacity = sum(nuclear_capacities)
nuclear_monthsrunning = [372, 570, 479, 434]


def nuclear_generation(nuclear_total_capacity, nuclear_efficiency):
    return float((nuclear_total_capacity * 24 * 30.416 * nuclear_efficiency))


print(nuclear_generation(nuclear_total_capacity, nuclear_efficiency))
coal_capacities = [(random.normalvariate(397, 7)), (random.normalvariate(397, 7)), (random.normalvariate(397, 7)),
                   (random.normalvariate(397, 7)), ]
coal_total_capacity = sum(coal_capacities)
coal_monthsrunning = [(random.normalvariate(480, 60)), (random.normalvariate(480, 60)), (random.normalvariate(480, 60)),
                      (random.normalvariate(480, 60))]


def coal_generation(coal_total_capacity, coal_efficiency):
    return (coal_total_capacity * 24 * 30.416 * coal_efficiency)


print(coal_generation(coal_total_capacity, coal_efficiency))

gas_capacities = [(random.normalvariate(578, 426)), (random.normalvariate(578, 426)), (random.normalvariate(578, 426)),
                  (random.normalvariate(578, 426)), (random.normalvariate(578, 426)), (random.normalvariate(578, 426)),
                  (random.normalvariate(578, 426)), (random.normalvariate(578, 426)), (random.normalvariate(578, 426)),
                  (random.normalvariate(578, 426)), (random.normalvariate(578, 426)), (random.normalvariate(578, 426)),
                  (random.normalvariate(1397, 168.5)), (random.normalvariate(1397, 168.5)),
                  (random.normalvariate(1397, 168.5)), (random.normalvariate(1397, 168.5))]
gas_total_capacity = sum(nuclear_capacities)
gas_monthsrunning = [(random.normalvariate(186, 54)), (random.normalvariate(186, 54)), (random.normalvariate(186, 54)),
                     (random.normalvariate(186, 54)), (random.normalvariate(186, 54)), (random.normalvariate(186, 54)),
                     (random.normalvariate(186, 54)), (random.normalvariate(186, 54)), (random.normalvariate(186, 54)),
                     (random.normalvariate(186, 54)), (random.normalvariate(186, 54)), (random.normalvariate(186, 54)),
                     (random.normalvariate(186, 54)), (random.normalvariate(186, 54)), (random.normalvariate(186, 54)),
                     (random.normalvariate(186, 54))]


def gas_generation(gas_total_capacity, gas_efficiency):
    return float(
        (gas_total_capacity * 24 * 30.416 * gas_efficiency * .8) + (gas_total_capacity * 24 * 30.416 * .12 * .12))


print(gas_generation(gas_total_capacity, gas_efficiency))


# Wind Capacity
def create_powerplants_5():
    create_powerplants_5_wind = [1.5, 127]
    return create_powerplants_5_wind


# ssolar capacity
def create_powerplants_106():
    create_powerplants_106_solar = [(random.normalvariate(14, 4)), (random.normalvariate(3, 1))]
    return create_powerplants_106_solar


# Hydro Capacity
hydrocreate_efficiency = .5


def create_powerplants_1():
    create_powerplants_1_hydro = [0, 0]
    return create_powerplants_1_hydro


wind_total_capacity = create_powerplants_5()[0] * 5
solar_total_capacity = create_powerplants_106()[0] * 106
hydrocreate_total_capacity = create_powerplants_1()[0] * 1


def wind_generation(wind_total_capacity, wind_efficiency):
    return float((wind_total_capacity * 24 * 30.416 * wind_efficiency))


print(wind_generation(wind_total_capacity, wind_efficiency))


def solar_generation(solar_total_capacity, solar_efficiency):
    return float((solar_total_capacity * 24 * 30.416 * solar_efficiency))


print(solar_generation(solar_total_capacity, solar_efficiency))


def hydrocreate_generation(hydrocreate_total_capacity, hydrocreate_efficiency):
    return float((hydrocreate_total_capacity * 24 * 30.416 * hydrocreate_efficiency))


print(hydrocreate_generation(hydrocreate_total_capacity, hydrocreate_efficiency))

total_clean_gen = ((wind_generation(wind_total_capacity, wind_efficiency)) + (
    solar_generation(solar_total_capacity, solar_efficiency)) + (
                       hydrocreate_generation(hydrocreate_total_capacity, hydrocreate_efficiency)))
print(total_clean_gen)

# Setting CO2 Values ub kg per MWh
wind_CO2 = 12
solar_CO2 = 54
nuclear_CO2 = 12
gas_CO2 = 477
coal_CO2 = 1001
hydro_CO2 = 8

# To kWh Costs
residential_kWh_cost = 1.8 * ((nuclear_total_capacity * nuclear_cost) + (coal_total_capacity * coal_result) + (
            gas_total_capacity * gas_result) + (wind_total_capacity * wind_cost) + (solar_total_capacity * wind_cost))
commercial_kWh_cost = 1.5 * ((nuclear_total_capacity * nuclear_cost) + (coal_total_capacity * coal_result) + (
            gas_total_capacity * gas_result) + (wind_total_capacity * wind_cost) + (solar_total_capacity * wind_cost))
total_KWh_cost = residential_kWh_cost + commercial_kWh_cost
print(residential_kWh_cost)
print(commercial_kWh_cost)
print(total_KWh_cost)

# To Change Prices NEED TO COME BACK TO THIS SECTION AND DECIDE WHERE TO PUT IT
# change-prices
nuclear_plantlife = nuclear_plantlife + random.uniform(0, 0.1)
solar_plantlife = solar_plantlife + random.uniform(0, .16)
wind_plantlife = wind_plantlife + random.uniform(0, .033)
gas_plantlife = gas_plantlife + random.uniform(0, .016)
coal_plantlife = coal_plantlife + random.uniform(0, .016)

nuclear_capitalcost = nuclear_capitalcost + random.uniform(0, 10.52)
wind_capitalcost = wind_capitalcost + random.uniform(0, 8.33)
solar_capitalcost = solar_capitalcost - random.uniform(0, 3)
gas_capitalcost = gas_capitalcost + random.uniform(0, 1.69)
coal_capitalcost = coal_capitalcost + random.uniform(0, 5.5)

nuclear_operationscost = nuclear_operationscost + random.uniform(.2, .05)
gas_operationscost = gas_operationscost + random.uniform(.003, .002)
coal_operationscost = coal_operationscost + random.uniform(.1, .05)
wind_operationscost = wind_operationscost + random.uniform(.004, .002)
solar_operationscost = solar_operationscost - random.uniform(.08, .03)

nuclear_variablecost = nuclear_variablecost + random.uniform(0.002, .0044)
gas_variablecost = gas_variablecost + random.uniform(0.0015, .0028)
coal_variablecost = coal_variablecost + random.uniform(0.002, .0035)

coal_efficiency = coal_efficiency + random.uniform(0, .001)
# gas_efficiency = gas_efficiency + random.uniform(0,(.001*(1-wind_investment)/100))
# wind_efficiency = wind_efficiency + random.uniform(0,(.002*wind_investment/100))
nuclear_efficiency = nuclear_efficiency + random.uniform(0, .0005)

gas_fuelcost = gas_fuelcost + random.uniform(.007, .013)
coal_fuelcost = coal_fuelcost + random.uniform(.007, .013)

class Residential(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    money_r = None
    energy_consumption_r = None

    def __init__(self, unique_id, pos, model, moore, money_r=None, energy_consumption_r=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.money_r = money_r
        self.energy_consumption_r = energy_consumption_r

    def step(self):
        self.random_move()

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        resident = [obj for obj in this_cell if isinstance(obj, Residential)]
        if resident:
            self.money_r = self.model.money_setting_r
            self.energy_consumption_r =self.model.energy_consuming_r

class Commercial(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    money_c = None
    energy_consumption_c = None

    def __init__(self, unique_id, pos, model, moore, money_c=None, energy_consumption_c=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.money_c = money_c
        self.energy_consumption_c = energy_consumption_c

    def step(self):
        self.random_move()

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        commercial = [obj for obj in this_cell if isinstance(obj, Commercial)]
        if commercial:
            self.money_c = self.model_c.money_setting_c
            self.energy_consumption_c = self.model.energy_consuming_c
        #     # Kill the sheep
        #     #self.model.grid._remove_agent(self.pos, sheep_to_eat)
        #     self.model.schedule.remove(sheep_to_eat)
        #
        # # Death or reproduction
        # if self.energy < 0:
        #     self.model.grid._remove_agent(self.pos, self)
        #     self.model.schedule.remove(self)
        # else:
        #     if self.random.random() < self.model.wolf_reproduce:
        #         # Create a new wolf cub
        #         self.energy /= 2
        #         cub = Wolf(
        #             self.model.next_id(), self.pos, self.model, self.moore, self.energy
        #         )
        #         self.model.grid.place_agent(cub, cub.pos)
        #         self.model.schedule.add(cub)


# # This is where defining the class begins
#
# class Residential(RandomWalker):
#     r_money = np.random.lognormal(75000, 25000)
#     r_wtp = random.normalvariate(16, 16)
#     r_energy_usage = random.normalvariate(696, 100)
#     r_savings = np.random.lognormal(70000, 70000)
#     r_costs = r_energy_usage * residential_kWh_cost
#
#     # whats up with solar and clean.
#
#     def __init(self, unique_id, pos, model,moore, r_money=np.random.lognormal(75000, 25000), r_wtp=random.normalvariate(16, 16),
#                r_energy_usage=random.normalvariate(696, 100), r_savings=np.random.lognormal(70000, 70000),
#                r_costs=(r_energy_usage * residential_kWh_cost)):
#         super().__init__(unique_id, pos, model,moore =moore)
#         self.r_money = r_money
#         self.r_wtp = r_

#    def step(self):
#
# class nuclear_plant(Agent):
#     nuclear_power =
#     nuclear_capacity =
#     nuclear_months_running =
#
#     # whats up with solar and clean.
#
#     def __init(self, unique_id, pos, model,power =, capacity =,months_running=):
#         super().__init__(unique_id, pos, model)
#         self.power = power
#         self.capacity = capacity
#         self.months_running = months_running
#
#     def step(self):

#
# class Sheep(RandomWalker):
#     """
#
