# simulation_by_plant.py

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plants = [
    {"name": "Charlotte, NC", "region": "Southeast", "base_demand": 9500},
    {"name": "Birmingham, AL", "region": "South", "base_demand": 8700},
    {"name": "Los Angeles, CA", "region": "West", "base_demand": 11000},
    {"name": "Chicago, IL", "region": "Midwest", "base_demand": 10200},
    {"name": "Bedford, NH", "region": "Northeast", "base_demand": 8000}
]

days = 180
iterations = 500
lead_time_dist = lambda: np.random.triangular(2, 4, 7)

transport_delay_prob = 0.1
labor_shortage_prob = 0.05
raw_material_delay_prob = 0.07

plant_results = []

for plant in plants:
    results = []
    for sim in range(iterations):
        inventory = 50000
        on_order = 0
        orders = []
        stockouts = 0
        fulfilled_demand = 0
        total_demand = 0
        total_cost = 0
        holding_cost_per_unit = 0.02
        stockout_cost_per_unit = 1.00
        order_cost = 100
        reorder_point = 30000
        order_qty = 50000

        for day in range(days):
            demand = max(0, int(np.random.normal(plant["base_demand"], 2000)))
            total_demand += demand

            if inventory >= demand:
                inventory -= demand
                fulfilled_demand += demand
            else:
                fulfilled_demand += inventory
                total_cost += (demand - inventory) * stockout_cost_per_unit
                inventory = 0
                stockouts += 1

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
        results.append((stockouts, service_level, total_cost))

    stockouts_array, service_levels, total_costs = zip(*results)
    plant_results.append({
        "Plant": plant["name"],
        "Region": plant["region"],
        "Average Service Level": np.mean(service_levels),
        "Average Stockout Days": np.mean(stockouts_array),
        "Average Total Cost": np.mean(total_costs)
    })

plant_results_df = pd.DataFrame(plant_results)
print(plant_results_df)

plant_results_df.plot(kind='bar', x='Plant', y='Average Service Level', legend=False,
                      title='Average Service Level by Plant', color='skyblue')
plt.ylabel('Service Level')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("images/plant_performance_bar.png")
plt.show()
