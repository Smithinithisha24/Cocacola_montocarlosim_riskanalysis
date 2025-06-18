# simulation_baseline.py

import numpy as np
import matplotlib.pyplot as plt

# Parameters
mean_demand = 10000
std_demand = 2000
reorder_point = 30000
order_qty = 50000
initial_inventory = 50000
lead_time_dist = lambda: np.random.triangular(2, 4, 7)
disruption_prob = 0.1
days = 180
iterations = 1000

results = []

for sim in range(iterations):
    inventory = initial_inventory
    on_order = 0
    orders = []
    stockouts = 0
    total_demand = 0
    fulfilled_demand = 0

    for day in range(days):
        demand = max(0, int(np.random.normal(mean_demand, std_demand)))
        total_demand += demand

        if inventory >= demand:
            inventory -= demand
            fulfilled_demand += demand
        else:
            fulfilled_demand += inventory
            inventory = 0
            stockouts += 1

        arrivals_today = [o for o in orders if o["arrival_day"] == day]
        for order in arrivals_today:
            inventory += order["qty"]
        orders = [o for o in orders if o["arrival_day"] > day]

        disrupted = np.random.rand() < disruption_prob if day % 7 == 0 else False

        if inventory <= reorder_point and on_order == 0:
            if not disrupted:
                arrival = day + int(lead_time_dist())
                orders.append({"qty": order_qty, "arrival_day": arrival})
                on_order = 1

        if on_order and inventory > reorder_point:
            on_order = 0

    service_level = fulfilled_demand / total_demand
    results.append((stockouts, service_level))

# Analysis
stockouts_array, service_levels = zip(*results)

plt.hist(service_levels, bins=30, edgecolor='black')
plt.title("Distribution of Service Levels - Coca-Cola U.S. Supply Chain")
plt.xlabel("Service Level")
plt.ylabel("Frequency")
plt.grid(True)
plt.savefig("images/service_level_histogram.png")
plt.show()

print(f"Avg Service Level: {np.mean(service_levels):.2f}")
print(f"95% CI: ({np.percentile(service_levels, 2.5):.2f}, {np.percentile(service_levels, 97.5):.2f})")
print(f"Avg Stockout Days: {np.mean(stockouts_array):.2f}")
