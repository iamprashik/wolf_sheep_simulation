# 🐺 Wolf–Sheep Ecosystem Simulation

An interactive **agent-based predator–prey simulation** built with Python, Mesa, and Solara.

This project extends Mesa's classic Wolf–Sheep model with two protective agents — **Farmers** and **Dogs** — to explore how intervention changes an ecosystem over time.

## 📸 Simulation Preview

![Wolf–Sheep Simulation Interface](simulation.png)

---

## 🌱 Why This Project Is Different

The original model focuses on wolves, sheep, and renewable grass. This extension introduces two additional forces into the ecosystem:

- 👨‍🌾 **Farmers** restore grass, support sheep, and may remove nearby wolves.
- 🐕 **Dogs** temporarily scare wolves, causing them to avoid neighbouring cells containing sheep.

The simulation also provides interactive controls that allow users to experiment with different:

- Starting sheep and wolf populations
- Reproduction rates
- Food energy values
- Grass-regrowth times
- Farmer populations
- Dog populations
- Random seeds

Live population charts show how **wolves, sheep, and grass** change throughout the simulation.

Seeded randomness also makes experiments reproducible.

---

## 🧠 Agent Behaviour

| Agent | Behaviour |
|---|---|
| 🐑 **Sheep** | Move, eat grass, gain or lose energy, reproduce, and die when their energy reaches zero. |
| 🐺 **Wolf** | Move, hunt sheep, gain energy, reproduce, and die when their energy reaches zero. |
| 🌱 **Grass** | Provides energy to sheep and regrows after a configurable delay. |
| 👨‍🌾 **Farmer** | Moves randomly, has a 10% chance to restore grass, a 25% chance to give a sheep 2 energy, and a 20% chance to remove a wolf in the same cell. |
| 🐕 **Dog** | Moves randomly and scares wolves in the same cell for 8 simulation steps. |
| 😨 **Scared Wolf** | Avoids neighbouring cells containing sheep while the scared timer is active. |

---

## 🎛️ Interactive Parameters

The Solara interface exposes controls for:

- Random seed
- Initial sheep population
- Initial wolf population
- Sheep reproduction probability
- Wolf reproduction probability
- Energy gained from food
- Grass availability
- Grass regrowth time
- Number of Farmers
- Number of Dogs

These parameters make it possible to experiment with how different ecosystem conditions affect population dynamics.

---

## 🛠️ Technology

- **Python 3.12+**
- **Mesa 3.4.2** — agent-based modelling and data collection
- **Solara** — interactive browser interface
- **Matplotlib** — grid and population visualizations

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/iamprashik/wolf_sheep_simulation.git
cd wolf_sheep_simulation
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the simulation

```bash
solara run wolf_sheep.py
```

Open the address printed in the terminal, normally:

```text
http://localhost:8765
```

---

## 🧪 Reproducible Experiments

Choose a random seed, keep the original ecosystem parameters fixed, and change only one intervention variable.

| Experiment | Baseline | Comparison | Question |
|---|---|---|---|
| Farmer intervention | 0 Farmers | 2–10 Farmers | Does additional food support improve long-term sheep survival? |
| Dog intervention | 0 Dogs | 2–10 Dogs | Does wolf avoidance reduce the rate of sheep loss? |
| Combined intervention | 0 Farmers, 0 Dogs | Farmers and Dogs together | Do the interventions reinforce each other? |

Running each comparison with the same random seed helps ensure that observed differences are caused by the selected parameter rather than a different random sequence.

---

## 📁 Project Structure

```text
wolf_sheep_simulation/
│
├── wolf_sheep.py       # Agents, extended model, visualization, and controls
├── simulation.png      # Simulation interface preview
├── requirements.txt    # Project dependencies
├── .gitignore
└── README.md
```

---

## ⚠️ Current Limitations

- The project extends the Wolf–Sheep example bundled with Mesa 3.4.2 and depends on its example modules.
- Farmer and Dog rules use fixed probabilities and durations.
- Results are visualized interactively but are not currently exported for statistical analysis.
- The model is intended for experimentation and education rather than real ecological forecasting.

---

## 🔮 Future Improvements

Possible future improvements include:

- Export simulation data to CSV
- Compare multiple random seeds automatically
- Add summary statistics for extinction and survival
- Separate model, agent, and visualization code into modules
- Add automated tests for Farmer and Dog behaviour

---

## 🙏 Credits

Built by **Prashik Koirala** using the Mesa agent-based modelling framework and its Wolf–Sheep example as the foundation.
