import numpy as np
from utils.geo import haversine_distance

def total_fitness(assignment, cities, servers, alpha=1.0, beta=1.0, gamma=1.0):
    """
    Multi-objective fitness function for evaluating a city's server assignment.
    
    Objectives:
    - Minimize total distance between cities and assigned servers
    - Minimize CPU health stress (penalty when server load exceeds threshold)
    - Balance load across all active (running) servers
    - Penalize overuse of servers (activation cost)

    Args:
        assignment (List[int]): Mapping from each city index to a server index.
        cities (List[dict]): Each dict must include 'lat', 'long', 'UsagePerHour'.
        servers (List[dict]): Each dict must include 'lat', 'long', 'Capacity',
                              'CPU_Health', 'Threshold', 'Status'.
        alpha (float): Weight for distance component.
        beta (float): Weight for CPU health penalty.
        gamma (float): Weight for server utilization balancing.

    Returns:
        float: Total fitness cost (lower is better).
    """
    total_cost = 0.0
    num_servers = len(servers)
    server_loads = [0.0] * num_servers
    running_servers = [i for i, s in enumerate(servers) if s['Status'] == 'Running']

    # 1. Distance + CPU health penalty
    for city_idx, server_idx in enumerate(assignment):
        city = cities[city_idx]
        server = servers[server_idx]

        # Haversine distance (in kilometers)
        distance = haversine_distance(
            city['lat'], city['long'],
            server['lat'], server['long']
        )

        # Accumulate server load
        server_loads[server_idx] += city['UsagePerHour']

        # Projected CPU load (as percentage)
        projected_cpu = server['CPU_Health'] + (server_loads[server_idx] / server['Capacity']) * 100

        # Penalize overloads beyond threshold (e.g. using a power penalty)
        cpu_penalty = max(0, projected_cpu - server['Threshold'])

        if distance != 0:
            total_cost += (alpha * distance) + (beta * (cpu_penalty))

    # 2. Utilization penalty (load imbalance among running servers)
    if running_servers:
        avg_load = np.mean([server_loads[i] for i in running_servers])
        imbalance = sum(
            (server_loads[i] - avg_load) ** 2 for i in running_servers
        )
        total_cost += gamma * imbalance

    # 3. Activation cost (number of active servers)
    total_cost += 0.01 * len(running_servers)

    return total_cost
