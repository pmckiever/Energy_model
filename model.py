import math
from enum import Enum
import networkx as nx

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid


class State(Enum):
    not_clean = 0
    has_clean = 1
    refuses_clean = 2


def number_state(model, state):
    return sum([1 for a in model.grid.get_all_cell_contents() if a.state is state])


def number_has_clean(model):
    return number_state(model, State.has_clean)


def number_not_clean(model):
    return number_state(model, State.not_clean)


def number_refuses_clean(model):
    return number_state(model, State.refuses_clean)


class Change_Res_Network(Model):
    """A virus model with some number of agents"""

    def __init__(
        self,
        num_nodes=1740,
        avg_node_degree=3,
        initial_with_clean=174,
        change_clean_chance=0.03,
        check_frequency=1.0,
        switch_back_chance=0.02,
        gain_resistance_chance=0.0,
    ):

        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)
        self.initial_with_clean = (
            initial_with_clean if initial_with_clean <= num_nodes else num_nodes
        )
        self.change_clean_chance = change_clean_chance
        self.check_frequency = check_frequency
        self.switch_back_chance = switch_back_chance
        self.gain_resistance_chance = gain_resistance_chance

        self.datacollector = DataCollector(
            {
                "has_clean": number_has_clean,
                "not_clean": number_not_clean,
                "refuses_clean": number_refuses_clean,
            }
        )

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            a = VirusAgent(
                i,
                self,
                State.not_clean,
                self.change_clean_chance,
                self.check_frequency,
                self.switch_back_chance,
                self.gain_resistance_chance,
            )
            self.schedule.add(a)
            # Add the agent to the node
            self.grid.place_agent(a, node)

        # Infect some nodes
        has_clean_nodes = self.random.sample(self.G.nodes(), self.initial_with_clean)
        for a in self.grid.get_cell_list_contents(has_clean_nodes):
            a.state = State.has_clean

        self.running = True
        self.datacollector.collect(self)

    def refuses_clean_not_clean_ratio(self):
        try:
            return number_state(self, State.refuses_clean) / number_state(
                self, State.not_clean
            )
        except ZeroDivisionError:
            return math.inf

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()


class VirusAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        initial_state,
        change_clean_chance,
        check_frequency,
        switch_back_chance,
        gain_resistance_chance,
    ):
        super().__init__(unique_id, model)

        self.state = initial_state

        self.change_clean_chance = change_clean_chance
        self.check_frequency = check_frequency
        self.switch_back_chance = switch_back_chance
        self.gain_resistance_chance = gain_resistance_chance

    def try_to_infect_neighbors(self):
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        not_clean_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.not_clean
        ]
        for a in not_clean_neighbors:
            if self.random.random() < self.change_clean_chance:
                a.state = State.has_clean

    def try_gain_resistance(self):
        if self.random.random() < self.gain_resistance_chance:
            self.state = State.refuses_clean

    def try_remove_infection(self):
        # Try to remove
        if self.random.random() < self.switch_back_chance:
            # Success
            self.state = State.not_clean
            self.try_gain_resistance()
        else:
            # Failed
            self.state = State.has_clean

    def try_check_situation(self):
        if self.random.random() < self.check_frequency:
            # Checking...
            if self.state is State.has_clean:
                self.try_remove_infection()

    def step(self):
        if self.state is State.has_clean:
            self.try_to_infect_neighbors()
        self.try_check_situation()

