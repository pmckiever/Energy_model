
from random import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# from energy_model.agents import Sheep, Wolf, GrassPatch
from pandas import np


from energy_model.agents import Residential, Commercial
from energy_model.schedule import RandomActivationByBreed

import random
import numpy as np

# Setting up Initial Values from netlogo
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





#Model Starts here
class Energy(Model):
    height = 20
    width = 20
    #(4000000*.87 and *.13 /4000)
    initial_residential = 870
    initial_commercial = 130

    wind_investment = 3
    clean_incentive = 1
    producer_strategy = "min_cost"


    money_setting_r = np.random.lognormal(75000, 25000)
    money_setting_c = np.random.lognormal(30000, 150000)
    energy_consuming_c = np.random.normal(6300,1000)
    energy_consuming_r = np.random.normal(696, 100)


    verbose = False  # Print-monitoring

    def __init__(
        self,
        height=20,
        width=20,
        initial_residential= 870,
        initial_commercial=130,
        money_setting_r = np.random.lognormal(75000, 25000),
        money_setting_c =  np.random.lognormal(30000, 150000),
        wtp_setting_r = random.normalvariate(16, 16),
        wtp_setting_c = random.normalvariate(200, 200),
        savings_setting_r = np.random.lognormal(70000, 70000),
        savings_setting_c=np.random.lognormal(3000000, 1000000),
        costs_setting_r= energy_consuming_r * residential_kWh_cost,
        costs_setting_c=energy_consuming_c * commercial_kWh_cost,
        energy_consuming_c=np.random.normal(6300, 1000),
        energy_consuming_r=np.random.normal(696, 100),
        wind_investment = 3,
        clean_incentive = 1,
        producer_strategy = "min_cost"


    ):

        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_residential = initial_residential
        self.initial_commercial = initial_commercial
        self.money_setting_c = money_setting_c
        self.money_setting_r = money_setting_r
        self.energy_consuming_r = energy_consuming_r
        self.energy_consuming_c = energy_consuming_c
        self.initial_commercial = initial_commercial
        self.wtp_setting_r = wtp_setting_r
        self.wtp_setting_c = wtp_setting_c
        self.savings_setting_r =savings_setting_r
        self.savings_setting_c =savings_setting_c
        self.costs_setting_r = costs_setting_r
        self.costs_setting_c = costs_setting_c
        self.wind_investment = wind_investment
        self.clean_incentive = clean_incentive
        self.producer_strategy = producer_strategy


        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Residents": lambda m: m.schedule.get_breed_count(Residential),
                #"Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )

        # Create sheep:
        for i in range(self.initial_commercial):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            money_c = self.money_setting_c
            energy_consuming_c = self.energy_consuming_c
            wtp_setting_c =self.wtp_setting_c
            savings_setting_c =self.savings_setting_c
            costs_setting_c = self.costs_setting_c
            commercials = Commercial(self.next_id(), (x, y), self, True, money_c,energy_consuming_c,wtp_setting_c,savings_setting_c,costs_setting_c)
            self.grid.place_agent(commercials, (x, y))
            self.schedule.add(commercials)

        for i in range(self.initial_residential):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy_consuming_r = self.energy_consuming_r
            wtp_setting_r = self.wtp_setting_r
            savings_setting_r = self.savings_setting_r
            costs_setting_r = self.costs_setting_r
            money_r = self.money_setting_r
            residents = Residential(self.next_id(), (x, y), self, True, money_r,energy_consuming_r,wtp_setting_r,savings_setting_r,costs_setting_r)
            self.grid.place_agent(residents, (x, y))
            self.schedule.add(residents)

        self.datacollector = DataCollector(
            {
                "Residential Energy Consumed": lambda m: m.schedule.get_energy_usage_r(Residential),
                "Commercial Energy Consumed": lambda m: m.schedule.get_energy_usage_c(Commercial),
            }
        )

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_breed_count(Residential),
                    self.schedule.get_breed_count(Commercial),
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number commercial agents: ", self.schedule.get_breed_count(Residential))
            #print("Initial number resdidential agents: ", self.schedule.get_breed_count(Sheep))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number wolves: ", self.schedule.get_breed_count(Residential))
            #print("Final number sheep: ", self.schedule.get_breed_count(Sheep))


# class Energy(Model):
#     height = 20
#     width = 20
#     initial_residential = 3480000
#     initial_commercial = 520000
#     wind_investment = 3
#     clean_incentive = 1
#     verbose = False
#     residential_reproduce = .14
#     commercial_reproduce = .13
#
#     def __init__(
#             self,
#             height=20,
#             width=20,
#             initial_residential=1740,
#             initial_commercial=260,
#             wind_investment=3,
#             clean_incentive=1,
#             residential_reproduce = .14,
#             commercial_reproduce = .13,
#             producer_strategy="min_cost",
#     ):
#
#         super().__init__()
#         self.height = height
#         self.width = width
#         self.initial_residential = initial_residential
#         self.initial_commercial = initial_commercial
#         self.wind_investment = wind_investment
#         self.clean_incentive = clean_incentive
#         self.producer_strategy = producer_strategy
#         self.residential_reproduce = residential_reproduce
#         self.commercial_reproduce = commercial_reproduce
#         self.schedule = RandomActivationByBreed(self)
#         self.grid = MultiGrid(self.height, self.width, torus=True)
#         self.datacollector = DataCollector(
#             {
#                 "Residential": lambda m: m.schedule.get_breed_count(Residential),
#                 "Commercial": lambda m: m.schedule.get_breed_count(Commercial),
#                 #"Power Plants": lambda m: m.schedule.get_breed_count(Poweplants)
#             }
#         )
#
#         # Create sheep:
#         for i in range(self.initial_residential):
#             x = self.random.randrange(self.width)
#             y = self.random.randrange(self.height)
#             r_money = np.random.lognormal(75000, 25000)
#             r_wtp = random.normalvariate(16, 16)
#             r_energy_usage = random.normalvariate(696, 100)
#             r_savings = np.random.lognormal(70000, 70000)
#             r_costs = r_energy_usage * residential_kWh_cost
#             residential = Residential(self.next_id(), (x, y), self, True)
#             self.grid.place_agent(residential, (x, y))
#             self.schedule.add(residential)
#
#         # Create wolves
#         for i in range(self.initial_commercial):
#             x = self.random.randrange(self.width)
#             y = self.random.randrange(self.height)
#             c_money = np.random.lognormal(300000, 150000)
#             c_wtp = random.normalvariate(200, 200)
#             c_energy_usage = random.normalvariate(6300, 1000)
#             c_savings = np.random.lognormal(3000000, 1000000)
#             c_costs = c_energy_usage * commercial_kWh_cost
#             commercial = Commercial(self.next_id(), (x, y), self, True)
#             self.grid.place_agent(commercial, (x, y))
#             self.schedule.add(commercial)
#
#         self.running = True
#         self.datacollector.collect(self)
#
#     def step(self):
#         self.schedule.step()
#         # collect data
#         self.datacollector.collect(self)
#         if self.verbose:
#             print(
#                 [
#                     self.schedule.time,
#                     self.schedule.get_breed_count(Residential),
#                     self.schedule.get_breed_count(Commercial)
#                 ]
#             )
#
#     def run_model(self, step_count=480):
#
#         if self.verbose:
#             print("Initial number commercial agents: ", self.schedule.get_breed_count(Commercial))
#             print("Initial number residential agents: ", self.schedule.get_breed_count(Residential))
#
#         for i in range(step_count):
#             self.step()
#
#         if self.verbose:
#             print("")
#             print("Final number Commercial: ", self.schedule.get_breed_count(Commercial))
#             print("Final number Residential: ", self.schedule.get_breed_count(Residential))

#
# class WolfSheep(Model):
#     """
#     Wolf-Sheep Predation Model
#     """
#
#     height = 20
#     width = 20
#
#     initial_residential = 4000000*.87
#     initial_wolves = 50
#
#     sheep_reproduce = 0.04
#     wolf_reproduce = 0.05
#
#     wolf_gain_from_food = 20
#
#     grass = False
#     grass_regrowth_time = 30
#     sheep_gain_from_food = 4
#
#     verbose = False  # Print-monitoring
#
#     description = (
#         "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
#     )
#
# def __init__(
#     self,
#     height=20,
#     width=20,
#     initial_residential=1740,
#     initial_commercial=260,
#     wind_investment =3,
#     clean_incentive= 1,
#     producer_strategy = "min_cost",
#     sheep_reproduce=0.04,
#     wolf_reproduce=0.05,
#     wolf_gain_from_food=20,
#     grass=False,
#     grass_regrowth_time=30,
#     sheep_gain_from_food=4,
# ):
#     """
#     Create a new Wolf-Sheep model with the given parameters.
#
#     Args:
#         initial_residential: Number of sheep to start with
#         initial_commercial: Number of wolves to start with
#         sheep_reproduce: Probability of each sheep reproducing each step
#         wolf_reproduce: Probability of each wolf reproducing each step
#         wolf_gain_from_food: Energy a wolf gains from eating a sheep
#         grass: Whether to have the sheep eat grass for energy
#         grass_regrowth_time: How long it takes for a grass patch to regrow
#                              once it is eaten
#         sheep_gain_from_food: Energy sheep gain from grass, if enabled.
#     """
#     super().__init__()
#     # Set parameters
#     self.height = height
#     self.width = width
#     self.initial_residential = initial_residential
#     self.initial_commercial = initial_commercial
#     self.wind_investment = wind_investment
#     self.clean_incentive = clean_incentive
#     self.producer_strategy = producer_strategy
#     self.sheep_reproduce = sheep_reproduce
#     self.wolf_reproduce = wolf_reproduce
#     self.wolf_gain_from_food = wolf_gain_from_food
#     self.grass = grass
#     self.grass_regrowth_time = grass_regrowth_time
#     self.sheep_gain_from_food = sheep_gain_from_food
#
#     self.schedule = RandomActivationByBreed(self)
#     self.grid = MultiGrid(self.height, self.width, torus=True)
#     self.datacollector = DataCollector(
#         {
#             "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
#             "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
#         }
#     )
#
#     # Create sheep:
#     for i in range(self.initial_residential):
#         x = self.random.randrange(self.width)
#         y = self.random.randrange(self.height)
#         energy = self.random.randrange(2 * self.sheep_gain_from_food)
#         sheep = Sheep(self.next_id(), (x, y), self, True, energy)
#         self.grid.place_agent(sheep, (x, y))
#         self.schedule.add(sheep)
#
#     # Create wolves
#     for i in range(self.initial_commercial):
#         x = self.random.randrange(self.width)
#         y = self.random.randrange(self.height)
#         energy = self.random.randrange(2 * self.wolf_gain_from_food)
#         wolf = Wolf(self.next_id(), (x, y), self, True, energy)
#         self.grid.place_agent(wolf, (x, y))
#         self.schedule.add(wolf)
#
#     # Create grass patches
#     if self.grass:
#         for agent, x, y in self.grid.coord_iter():
#
#             fully_grown = self.random.choice([True, False])
#
#             if fully_grown:
#                 countdown = self.grass_regrowth_time
#             else:
#                 countdown = self.random.randrange(self.grass_regrowth_time)
#
#             patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
#             self.grid.place_agent(patch, (x, y))
#             self.schedule.add(patch)
#
#     self.running = True
#     self.datacollector.collect(self)
#
# def step(self):
#     self.schedule.step()
#     # collect data
#     self.datacollector.collect(self)
#     if self.verbose:
#         print(
#             [
#                 self.schedule.time,
#                 self.schedule.get_breed_count(Wolf),
#                 self.schedule.get_breed_count(Sheep),
#             ]
#         )
#
# def run_model(self, step_count=200):
#
#     if self.verbose:
#         print("Initial number commercial agents: ", self.schedule.get_breed_count(Wolf))
#         print("Initial number resdidential agents: ", self.schedule.get_breed_count(Sheep))
#
#     for i in range(step_count):
#         self.step()
#
#     if self.verbose:
#         print("")
#         print("Final number wolves: ", self.schedule.get_breed_count(Wolf))
#         print("Final number sheep: ", self.schedule.get_breed_count(Sheep))
