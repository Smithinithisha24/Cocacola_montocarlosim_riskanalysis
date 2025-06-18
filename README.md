# cocacola_montocarlosim_riskanalysis
This repository presents a simulation-based study of Coca-Cola's U.S. supply chain network. The goal is to evaluate performance metrics like service levels, stockout frequency, and total operational cost under realistic conditions and strategic improvements.


# Coca-Cola Supply Chain Simulation and Risk Mitigation Analysis

This repository presents a simulation-based study of Coca-Cola's U.S. supply chain network. The goal is to evaluate performance metrics like service levels, stockout frequency, and total operational cost under realistic conditions and strategic improvements.

---

## 📌 Objectives

* Model baseline operations with demand uncertainty and supply disruptions.
* Analyze performance across regional plants.
* Evaluate strategic mitigation scenarios.
* Recommend optimal risk management actions.

---

## 📁 Repository Structure

```
coca-cola-supply-chain-simulation/
│
├── README.md                      # Project overview
├── LICENSE                        # MIT License
├── requirements.txt               # Python dependencies
├── simulation_baseline.py         # Base case simulation
├── simulation_by_plant.py         # Regional plant simulation
├── strategy_comparison.py         # Mitigation strategy comparison
├── notebooks/
│   └── analysis.ipynb             # Jupyter-based analysis (optional)
├── images/                        # Visual output
│   ├── service_level_histogram.png
│   ├── plant_performance_bar.png
│   ├── strategy_service_level.png
│   ├── strategy_stockout_days.png
│   ├── strategy_total_cost.png
│   └── combined_distributions.png
├── data/                          # Placeholder for raw/synthetic data
├── results/                       # Summary outputs
│   └── summary_tables.csv
```

---

## 📊 Key Results

* **Baseline Service Level**: \~78%
* **Average Stockout Days**: \~51
* **Best Performing Strategy**: Reduced Lead Time Variability (highest service, lowest cost)
* **Weakest Strategy**: Higher Inventory Buffer (low service, highest cost)
* **Most Resilient Plant**: Bedford, NH

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/coca-cola-supply-chain-simulation.git
cd coca-cola-supply-chain-simulation
```

### 2. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 3. Run Simulations

```bash
python simulation_baseline.py
python simulation_by_plant.py
python strategy_comparison.py
```

---

## 🚀 Technologies Used

* Python 3.8+
* NumPy
* Pandas
* Matplotlib

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 📃 Author

Smithi Nithisha Boda
Graduate Student, Industrial Engineering
California State University, East Bay

For questions, suggestions, or collaborations, feel free to reach out!
