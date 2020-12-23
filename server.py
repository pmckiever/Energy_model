import math

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import TextElement
from .model import Change_Res_Network, State, number_has_clean


def network_portrayal(G):
    # The model ensures there is always 1 agent per node

    def node_color(agent):
        return {State.has_clean: "#FF0000", State.not_clean: "#008000"}.get(
            agent.state, "#808080"
        )

    def edge_color(agent1, agent2):
        if State.refuses_clean in (agent1.state, agent2.state):
            return "#000000"
        return "#e8e8e8"

    def edge_width(agent1, agent2):
        if State.refuses_clean in (agent1.state, agent2.state):
            return 3
        return 2

    def get_agents(source, target):
        return G.nodes[source]["agent"][0], G.nodes[target]["agent"][0]

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": node_color(agents[0]),
            "tooltip": "id: {}<br>state: {}".format(
                agents[0].unique_id, agents[0].state.name
            ),
        }
        for (_, agents) in G.nodes.data("agent")
    ]

    portrayal["edges"] = [
        {
            "source": source,
            "target": target,
            "color": edge_color(*get_agents(source, target)),
            "width": edge_width(*get_agents(source, target)),
        }
        for (source, target) in G.edges
    ]

    return portrayal


network = NetworkModule(network_portrayal, 500, 500, library="d3")
chart = ChartModule(
    [
        {"Label": "has_clean", "Color": "#FF0000"},
        {"Label": "not_clean", "Color": "#008000"},
        {"Label": "refuses_clean", "Color": "#808080"},
    ]
)


class MyTextElement(TextElement):
    def render(self, model):
        ratio = model.refuses_clean_not_clean_ratio()
        ratio_text = "&infin;" if ratio is math.inf else "{0:.2f}".format(ratio)
        has_clean_text = str(number_has_clean(model))

        return "refuses_clean/not_clean Ratio: {}<br>has_clean Remaining: {}".format(
            ratio_text, has_clean_text
        )


model_params = {
    "num_nodes": UserSettableParameter(
        "slider",
        "Number of agents",
        260,
        10,
        2000,
        1,
        description="Choose how many agents to include in the model",
    ),
    "avg_node_degree": UserSettableParameter(
        "slider", "Avg Node Degree", 3, 3, 8, 1, description="Avg Node Degree"
    ),
    "initial_with_clean": UserSettableParameter(
        "slider",
        "initial_with_clean",
        3,
        1,
        100,
        1,
        description="initial_with_clean",
    ),
    "change_clean_chance": UserSettableParameter(
        "slider",
        "Change Clean Chance",
        0.03,
        0.0,
        1.0,
        0.01,
        description="Probability that not_clean neighbor will be has_clean",
    ),
    "check_frequency": UserSettableParameter(
        "slider",
        "Check Frequency",
        1.0,
        0.0,
        1.0,
        0.1,
        description="Frequency the nodes check whether they are has_clean by " "a virus",
    ),
    "switch_back_chance": UserSettableParameter(
        "slider",
        "switch_back_chance",
        0.02,
        0.0,
        0.15,
        0.01,
        description="Probability that the virus will be removed",
    ),
    "gain_resistance_chance": UserSettableParameter(
        "slider",
        "Gain Resistance Chance",
        0.0,
        0.0,
        1.0,
        0.01,
        description="Probability that a switch_back agent will become "
        "refuses_clean to this virus in the future",
    ),
}

server = ModularServer(
    Change_Res_Network, [network, MyTextElement(), chart], "Change Res Model", model_params
)
server.port = 8521
