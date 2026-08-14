from mesa.examples.advanced.wolf_sheep.agents import GrassPatch, Sheep, Wolf
from mesa.examples.advanced.wolf_sheep.model import WolfSheep
from mesa.experimental.devs import ABMSimulator
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
from mesa.discrete_space import CellAgent

##############################################################
# NEW AGENTS: Farmer and Dog
##############################################################

class Farmer(CellAgent):
    """Farmer agent that helps sheep and removes wolves."""

    def __init__(self, model):
        super().__init__(model)
        self.type = "Farmer"

    def step(self):
        # Move randomly to a neighboring cell
        neighborhood = list(self.cell.connections.values())
        if neighborhood:
            self.move_to(self.random.choice(neighborhood))

        cellmates = list(self.cell.agents)

        # 10% chance to sod grass (make fully grown)
        for obj in cellmates:
            if isinstance(obj, GrassPatch) and not obj.fully_grown:
                if self.random.random() < 0.10:
                    obj.fully_grown = True

        # 25% chance to give a sheep some energy
        for obj in cellmates:
            if isinstance(obj, Sheep):
                if self.random.random() < 0.25:
                    obj.energy += 2

        # 20% chance to remove a wolf
        for obj in list(cellmates):
            if isinstance(obj, Wolf):
                if self.random.random() < 0.20:
                    obj.remove()


class Dog(CellAgent):
    """Dog agent that scares wolves."""

    def __init__(self, model):
        super().__init__(model)
        self.type = "Dog"

    def step(self):
        # Move randomly to a neighboring cell
        neighborhood = list(self.cell.connections.values())
        if neighborhood:
            self.move_to(self.random.choice(neighborhood))

        # Scare any wolves in the same cell for 8 steps
        for obj in list(self.cell.agents):
            if isinstance(obj, Wolf):
                obj.scared_timer = 8


###############################################################
# PATCH WOLF BEHAVIOR TO AVOID SHEEP WHEN SCARED
###############################################################

def wolf_step_patched(self):
    """Patch wolf to avoid sheep when scared."""

    if hasattr(self, "scared_timer") and self.scared_timer > 0:
        self.scared_timer -= 1

        neighborhood = list(self.cell.connections.values())
        safe_cells = [
            cell for cell in neighborhood
            if not any(isinstance(a, Sheep) for a in cell.agents)
        ]

        move_to = self.random.choice(safe_cells) if safe_cells else self.random.choice(neighborhood)
        self.move_to(move_to)
        return

    self.original_step()


Wolf.original_step = Wolf.step
Wolf.step = wolf_step_patched


###############################################################
# EXTENDED MODEL WITH FARMERS & DOGS
###############################################################

class WolfSheepExtended(WolfSheep):
    def __init__(self, farmer_count=2, dog_count=2, **kwargs):
        super().__init__(**kwargs)

        self.farmers = []
        self.dogs = []

        for _ in range(farmer_count):
            farmer = Farmer(self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            farmer.move_to(self.grid[(x, y)])
            self.farmers.append(farmer)

        for _ in range(dog_count):
            dog = Dog(self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            dog.move_to(self.grid[(x, y)])
            self.dogs.append(dog)

    def step(self):
        super().step()

        # Step new agents
        for farmer in self.farmers:
            farmer.step()
        for dog in self.dogs:
            dog.step()

###############################################################
# CUSTOM SPACE COMPONENT
###############################################################

import solara
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure


def make_custom_space(model):
    grid = model.grid
    W, H = grid.width, grid.height

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    # Draw grass patches as background rectangles
    for cell in grid.all_cells:
        x, y = cell.coordinate
        for agent in cell.agents:
            if isinstance(agent, GrassPatch):
                color = "#2ca02c" if agent.fully_grown else "#8c564b"
                rect = mpatches.Rectangle((x, y), 1, 1, color=color, zorder=1)
                ax.add_patch(rect)

    # Draw animals on top
    for cell in grid.all_cells:
        x, y = cell.coordinate
        cx, cy = x + 0.5, y + 0.5
        for agent in cell.agents:
            if isinstance(agent, Wolf):
                ax.plot(cx, cy, "o", color="tab:red", markersize=9, zorder=4)
            elif isinstance(agent, Sheep):
                ax.plot(cx, cy, "o", color="tab:cyan", markersize=7, zorder=4)
            elif isinstance(agent, Farmer):
                ax.plot(cx, cy, "D", color="gold", markersize=11, zorder=5,
                        markeredgecolor="black", markeredgewidth=0.5)
            elif isinstance(agent, Dog):
                ax.plot(cx, cy, "^", color="black", markersize=10, zorder=5)

    plt.tight_layout()
    return fig


@solara.component
def CustomSpaceComponent(model):
    """Redraws the grid by polling model.steps every 50ms."""
    import threading

    actual_model = model.value if hasattr(model, "value") else model
    tick, set_tick = solara.use_state(0)

    def start_polling():
        stop_event = threading.Event()

        def poll():
            last = -1
            while not stop_event.is_set():
                current = getattr(actual_model, "steps", 0)
                if current != last:
                    last = current
                    set_tick(current)
                stop_event.wait(0.05)

        t = threading.Thread(target=poll, daemon=True)
        t.start()
        return lambda: stop_event.set()

    solara.use_effect(start_polling, dependencies=[actual_model])

    fig = make_custom_space(actual_model)
    solara.FigureMatplotlib(fig)
    plt.close(fig)


###############################################################
# MODEL PARAMS
###############################################################

model_params = {
    "seed": {"type": "InputText", "value": 42, "label": "Random Seed"},
    "grass": {"type": "Select", "value": True, "values": [True, False], "label": "Grass?"},
    "grass_regrowth_time": Slider("Grass Regrowth Time", 20, 1, 50),
    "initial_sheep": Slider("Initial Sheep", 100, 10, 300),
    "sheep_reproduce": Slider("Sheep Reproduction", 0.04, 0.01, 1.0, 0.01),
    "initial_wolves": Slider("Initial Wolves", 10, 5, 100),
    "wolf_reproduce": Slider("Wolf Reproduction", 0.05, 0.01, 1.0, 0.01),
    "wolf_gain_from_food": Slider("Wolf Gain From Food", 20, 1, 50),
    "sheep_gain_from_food": Slider("Sheep Gain From Food", 4, 1, 10),
    "farmer_count": Slider("Farmers", 2, 0, 10),
    "dog_count": Slider("Dogs", 2, 0, 10),
}


###############################################################
# RUN SIMULATION
###############################################################

def post_process_lines(ax):
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.9))


space_component = CustomSpaceComponent

lineplot_component = make_plot_component(
    {"Wolves": "tab:orange", "Sheep": "tab:cyan", "Grass": "tab:green"},
    post_process=post_process_lines,
)

simulator = ABMSimulator()
model = WolfSheepExtended(simulator=simulator, grass=True)

page = SolaraViz(
    model,
    components=[space_component, lineplot_component],
    model_params=model_params,
    name="Wolf Sheep Extended",
    simulator=simulator,
)

page