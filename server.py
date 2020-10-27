from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

# from energy_model.agents import Wolf, Sheep, GrassPatch
# from energy_model.model import Wolf-Sheep

from energy_model.agents import Residential, Commercial, Poweplants
from energy_model.model import Energy


def energy_portrayal(agent):
    if agent is None:
        return
    portrayal = {}

    if type(agent) is Residential:
        portrayal["Shape"] = "energy_model/house.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Commercial:
        portrayal["Shape"] = "energy_model/building.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)

    return portrayal


canvas_element = CanvasGrid(energy_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Residential", "Color": "#AA0000"}, {"Label": "Commercial", "Color": "#666666"}]
)
Wealth = ChartModule([{"Label": "Wealth($10k)", "Color": "Black", "canvas_height": 100, "canvas_width": 200}])

Average_Consumption = ChartModule(
    [{"Label": "Average Consumption", "Color": "Black", "canvas_height": 100, "canvas_width": 200}])

Average_cost = ChartModule(
    [{"Label": "Average cost per kwh", "Color": "Black", "canvas_height": 100, "canvas_width": 200}])

Power_mix = ChartModule([{"Label": "Power mix", "Color": "Black", "canvas_height": 100, "canvas_width": 200}])

CO2e = ChartModule([{"Label": "CO2e Released", "Color": "Black", "canvas_height": 100, "canvas_width": 200}])

Supply_and_demand = ChartModule(
    [{"Label": "Supply and demand", "Color": "Black", "canvas_height": 100, "canvas_width": 200}])

Average_bill = ChartModule([{"Label": "Average bill", "Color": "Black", "canvas_height": 100, "canvas_width": 200}])

Cost_by_source = ChartModule([{"Label": "Cost by source", "Color": "Black", "canvas_height": 100, "canvas_width": 200}])

model_params = {
    "wind_investment": UserSettableParameter("slider", "wind_investment", .8, 0, 100, 1),
    "clean_incentive": UserSettableParameter("slider", "clean_incentive", .3, 0, 10, 1),
    "producer_strategy": UserSettableParameter("choice", "producer_strategy", "min_cost",
                                               choices=['min_cost', 'wind_only', 'solar_only', 'renewable_only',
                                                        'on_demand_only']),
    "initial_residential": UserSettableParameter(
        "slider", "Initial Residential Agents", 10, 1740, 0
    ),
    "initial_commercial": UserSettableParameter(
        "slider", "Initial Commercial Agents", 10, 260, 0
    ),
}

server = ModularServer(
    WolfSheep,
    [canvas_element, Wealth, Average_Consumption, Average_cost, Power_mix, CO2e, Supply_and_demand, Average_bill,
     Cost_by_source], "Wolf Sheep Predation", model_params,
)
server.port = 8521

# Need to add in how we want to show the producer agents
#
# def wolf_sheep_portrayal(agent):
#     if agent is None:
#         return
#
#     portrayal = {}
#
#     if type(agent) is Sheep:
#         portrayal["Shape"] = "energy_model/house.png"
#         portrayal["scale"] = 0.9
#         portrayal["Layer"] = 1
#
#     elif type(agent) is Wolf:
#         portrayal["Shape"] = "energy_model/building.png"
#         portrayal["scale"] = 0.9
#         portrayal["Layer"] = 2
#         portrayal["text"] = round(agent.energy, 1)
#
#     elif type(agent) is GrassPatch:
#         if agent.fully_grown:
#             portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
#         else:
#             portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
#         portrayal["Shape"] = "rect"
#         portrayal["Filled"] = "true"
#         portrayal["Layer"] = 0
#         portrayal["w"] = 1
#         portrayal["h"] = 1
#
#     return portrayal

