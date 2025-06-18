# strategy_comparison.py

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

scenarios = {
    "Base Case": {
        "initial_inventory": 50000,
        "reorder_point": 30000,
        "lead_time_dist": lambda: np.random.triangular(2, 4, 7),
        "description": "Standard configuration"
    },
    "Higher Inventory Buffer": {
        "initial_inventory": 70000,
        "reorder_point": 50000,
        "lead_time_dist": lambda: np.random.triangular(2, 4, 7),
        "description": "Increased initial inventory and reorder point"
    },
    "Reduced Lead Time Variability": {
        "initial_inventory": 50000,
        "reorder_point": 30000,
        "lead_time_dist": lambda: np.random.triangular(3, 4, 5),
        "description": "Tighter lead time distribution"
    },
    "Diversified Sourcing (Lower Risk)": {
        "initial_inventory": 50000,
        "reorder_point": 30000,
        "lead_time_dist": lambda: np.random.triangular(2, 4, 7),
        "transport_delay_prob": 0.05,
        "labor_shortage_prob": 0.03,
        "raw_material_delay_prob": 0.04,
        "description": "Reduced disruption probabilities"
    }
}

days = 180
iterations = 300
order_qty = 50000
holding_cost_per_unit = 0.02
stockout_cost_per_unit = 1.00
order_cost = 100

scenario_results = []

for name, config in scenarios.items():
    service_levels = []
    stockout_days_list = []
    total_costs = []

    transport_delay_prob = config.get("transport_delay_prob", 0.1)
    labor_shortage_prob = config.get("labor_shortage_prob", 0.05)
    raw_material_delay_prob = config.get("raw_material_delay_prob", 0.07)

    for _ in range(iterations):
        inventory = config["initial_inventory"]
        reorder_point = config["reorder_point"]
        lead_time_dist = config["lead_time_dist"]
        on_order = 0
        orders = []
        total_cost = 0
        total_demand = 0
        fulfilled_demand = 0
        stockout_days = 0

        for day in range(days):
            demand = max(0, int(np.random.normal(10000, 2000)))
            total_demand += demand

            if inventory >= demand:
                inventory -= demand
                fulfilled_demand += demand
            else:
                fulfilled_demand += inventory
                total_cost += (demand - inventory) * stockout_cost_per_unit
                inventory = 0
                stockout_days += 1

            arrivals_today = [o for o in orders if o["arrival_day"] == day]
            for order in arrivals_today:
                inventory += order["qty"]
            orders = [o for o in orders if o["arrival_day"] > day]

            disrupted = (
                np.random.rand() < transport_delay_prob or
                np.random.rand() < labor_shortage_prob or
                np.random.rand() < raw_material_delay_prob
            ) if day % 7 == 0 else False

            if inventory <= reorder_point and on_order == 0:
                if not disrupted:
                    arrival = day + int(lead_time_dist())
                    orders.append({"qty": order_qty, "arrival_day": arrival})
                    total_cost += order_cost
                    on_order = 1

            if on_order and inventory > reorder_point:
                on_order = 0

            total_cost += inventory * holding_cost_per_unit

        service_level = fulfilled_demand / total_demand
        service_levels.append(service_level)
        stockout_days_list.append(stockout_days)
        total_costs.append(total_cost)

    scenario_results.append({
        "Strategy": name,
        "Description": config["description"],
        "Avg Service Level": np.mean(service_levels),
        "Avg Stockout Days": np.mean(stockout_days_list),
        "Avg Total Cost": np.mean(total_costs)
    })

results_df = pd.DataFrame(scenario_results)
print(results_df)

fig, axs = plt.subplots(3, 1, figsize=(12, 16))

axs[0].bar(results_df["Strategy"], results_df["Avg Service Level"], color="skyblue")
axs[0].set_title("Average Service Level by Strategy")
axs[0].set_ylabel("Service Level")
axs[0].grid(True)

axs[1].bar(results_df["Strategy"], results_df["Avg Stockout Days"], color="salmon")
axs[1].set_title("Average Stockout Days by Strategy")
axs[1].set_ylabel("Days")
axs[1].grid(True)

axs[2].bar(results_df["Strategy"], results_df["Avg Total Cost"], color="seagreen")
axs[2].set_title("Average Total Cost by Strategy")
axs[2].set_ylabel("Total Cost ($)")
axs[2].grid(True)

for ax in axs:
    ax.tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig("images/strategy_comparison_summary.png")
plt.show()
