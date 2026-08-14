🐺 Wolf–Sheep Ecosystem Simulation
An interactive agent-based predator–prey simulation built with Python, Mesa, and Solara. It extends Mesa's classic Wolf–Sheep model with two protective agents—Farmers and Dogs—to explore how intervention changes an ecosystem over time.

Wolf–Sheep simulation interface

Why This Project Is Different
The original model focuses on wolves, sheep, and renewable grass. This extension adds two new forces:

Farmers restore grass, support sheep, and may remove nearby wolves.
Dogs temporarily scare wolves, causing them to avoid neighbouring cells containing sheep.
Interactive controls let users compare different starting populations, reproduction rates, food energy values, grass-regrowth times, and intervention levels.
Live population charts show how wolves, sheep, and grass change during a run.
Seeded randomness makes experiments reproducible.
Agent Behaviour
Agent	Behaviour
Sheep	Move, eat grass, gain or lose energy, reproduce, and die when their energy reaches zero.
Wolves	Move, hunt sheep, gain energy, reproduce, and die when their energy reaches zero.
Grass	Provides energy to sheep and regrows after a configurable delay.
Farmer	Moves randomly, has a 10% chance to restore grass, a 25% chance to give a sheep 2 energy, and a 20% chance to remove a wolf in the same cell.
Dog	Moves randomly and scares wolves in the same cell for 8 simulation steps.
Scared wolf	Avoids neighbouring cells containing sheep while the scared timer is active.
Interactive Parameters
The Solara interface exposes controls for:

Random seed
Initial sheep and wolf population
Sheep and wolf reproduction probabilities
Energy gained from food
Grass availability and regrowth time
Number of Farmers and Dogs
Technology
Python 3.12+
Mesa 3.5.1 for agent-based modelling and data collection
Solara for the interactive browser interface
Matplotlib for grid and population visualizations
The visualization and plotting dependencies are installed through Mesa's recommended dependency bundle.

Getting Started
1. Clone the repository
git clone https://github.com/iamprashik/wolf_sheep_simulation.git
cd wolf_sheep_simulation
2. Create a virtual environment
Windows

py -3.12 -m venv .venv
.venv\Scripts\activate
macOS or Linux

python3 -m venv .venv
source .venv/bin/activate
3. Install the dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
4. Run the simulation
solara run wolf_sheep.py
Open the address printed in the terminal, normally http://localhost:8765.

Reproducible Experiments
Choose a seed, keep the original ecosystem parameters fixed, and change only one intervention variable.

Experiment	Baseline	Comparison	Question
Farmer intervention	0 Farmers	2–10 Farmer	Does additional food support improve long-term sheep survival?
Dog intervention	0 Dogs	2–10 Dogs	Does wolf avoidance reduce the rate of sheep loss?
Combined intervention	0 Farmers, 0 Dogs	Farmers and Dogs together	Do the intervention reinforce each other?
Run each comparison with the same seed so difference are caused by the selected parameter rather than a different random sequence.

Project Structure
wolf_sheep_simulation/
├── wolf_sheep.py       # Agents, extended model, visualization, and controls
├── simulation.png      # Interface preview
├── requirements.txt    # Reproducible dependencies
├── .gitignore
└── README.md
Current Limitations
The project extends Mesa's bundled Wolf–Sheep example and depends on its internal example modules.
Farmer and Dog rules use fixed probabilities and durations.
Results are visualized interactively but are not yet exported for statistical analysis.
The model is intended for experimentation and education rather than real ecological forecasting.
Future Improvements
Export run data to CSV
Compare multiple seeds automatically
Add summary statistics for extinction and survival
Separate model, agent, and visualization code into modules
Add automated tests for Farmer and Dog behaviour
Credits
Built by Prashik Koirala using the Mesa agent-based modelling framework and its Wolf–Sheep example as the foundation.