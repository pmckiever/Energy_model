"""
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

#from energy_model.agents import Sheep, Wolf, GrassPatch

from energy_model.agents import Residential, Commercial, Poweplants
from energy_model.schedule import RandomActivationByBreed

class Energy(Model):
    height = 20
    width = 20
    initial_residential = 3480000
    initial_commercial = 520000
    verbose = False

    def __init__(
        self,
        height=20,
        width=20,
        initial_residential=1740,
        initial_commercial=260,
        wind_investment = 3,
        clean_incentive= 1,
        producer_strategy = "min_cost",
    ):

        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_residential = initial_residential
        self.initial_commercial = initial_commercial
        self.wind_investment = wind_investment
        self.clean_incentive = clean_incentive
        self.producer_strategy = producer_strategy

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Residential": lambda m: m.schedule.get_breed_count(Residential),
                "Commercial": lambda m: m.schedule.get_breed_count(Commercial),
                "Power Plants": lambda m: m.schedule.get_breed_count(Poweplants)
            }
        )

        # Create sheep:
        for i in range(self.initial_residential):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.sheep_gain_from_food)
            sheep = Sheep(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves
        for i in range(self.initial_commercial):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_breed_count(Wolf),
                    self.schedule.get_breed_count(Sheep),
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number commercial agents: ", self.schedule.get_breed_count(Wolf))
            print("Initial number resdidential agents: ", self.schedule.get_breed_count(Sheep))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number wolves: ", self.schedule.get_breed_count(Wolf))
            print("Final number sheep: ", self.schedule.get_breed_count(Sheep))


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
