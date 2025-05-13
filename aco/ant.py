import random
import numpy as np
from utils.geo import haversine_distance

class Ant:
    def __init__(self, num_cities, num_servers):
        self.num_cities = num_cities
        self.num_servers = num_servers
        self.assignment = [-1 for _ in range(num_cities)]
        self.server_loads = [0 for _ in range(num_servers)]  # Track current server loads
        self.activated_servers = []  # Track which servers were activated

    def construct_solution(self, pheromones, cities, servers, alpha, beta, gamma, q0=1):
        """
        Construct solution with dynamic CPU health consideration

        Args:
            pheromones: Pheromone matrix object with get_pheromone(city_idx, server_idx)
            cities: List of city dicts with keys ['lat', 'long', 'UsagePerHour']
            servers: List of server dicts with keys ['lat', 'long', 'Capacity', 'CPU_Health', 'Threshold', 'Status']
            alpha: Weight for pheromone importance
            beta: Weight for CPU health objective
            gamma: Weight for server utilization objective (currently unused, reserved for future use)
            q0: Greediness parameter (probability to choose best option)
        """
        self.server_loads = [0 for _ in range(self.num_servers)]
        self.assignment = [-1 for _ in range(self.num_cities)]
        self.activated_servers = []

        for city_idx in range(self.num_cities):
            city = cities[city_idx]
            possible_servers = []

            for server_idx in range(self.num_servers):
                server = servers[server_idx]

                # Skip servers that are down (unless all are down)
                if server['Status'] == 'Down':
                    continue

                # Distance calculation
                distance = haversine_distance(
                    city['lat'], city['long'],
                    server['lat'], server['long']
                )

                # Projected server load
                current_load = self.server_loads[server_idx] + city['UsagePerHour']
                projected_load_percent = (current_load / server['Capacity']) * 100
                projected_stress = server['CPU_Health'] + projected_load_percent

                # CPU penalty if stress goes beyond threshold
                cpu_penalty = max(0, (projected_stress - server['Threshold'])) * beta

                # Pheromone and attractiveness calculation
                pheromone = pheromones.get_pheromone(city_idx, server_idx)
                attractiveness = (
                    (pheromone ** alpha) *
                    (1 / (distance + 1e-6)) *
                    (1 / (1 + cpu_penalty))
                )

                possible_servers.append((server_idx, attractiveness))

            if not possible_servers:
                # No running server was suitable, activate the nearest down server
                server_idx = self._activate_nearest_server(city, servers)
                pheromone = pheromones.get_pheromone(city_idx, server_idx)
                attractiveness = 1.0  # Assign max attractiveness
                possible_servers.append((server_idx, attractiveness))

            # Normalize probabilities
            total_attractiveness = sum(att for _, att in possible_servers)
            if total_attractiveness == 0:
                probabilities = [(s_idx, 1 / len(possible_servers)) for s_idx, _ in possible_servers]
            else:
                probabilities = [(s_idx, att / total_attractiveness) for s_idx, att in possible_servers]

            # Greedy or probabilistic choice
            if random.random() < q0:
                selected_server = max(possible_servers, key=lambda x: x[1])[0]
            else:
                selected_server = random.choices(
                    [s[0] for s in probabilities],
                    weights=[s[1] for s in probabilities]
                )[0]

            self.assignment[city_idx] = selected_server
            self.server_loads[selected_server] += city['UsagePerHour']

    def _activate_nearest_server(self, city, servers):
        """Activate the nearest down server when none are available"""
        min_dist = float('inf')
        best_server = None

        for server_idx, server in enumerate(servers):
            if server['Status'] == 'Down':
                dist = haversine_distance(
                    city['lat'], city['long'],
                    server['lat'], server['long']
                )
                if dist < min_dist:
                    min_dist = dist
                    best_server = server_idx

        if best_server is not None:
            servers[best_server]['Status'] = 'Running'
            servers[best_server]['CPU_Health'] = 30  # Assumed safe initial load
            self.activated_servers.append(best_server)
            return best_server
        else:
            raise RuntimeError("No server available to activate")

    def evaluate_fitness(self, cities, servers, alpha=1.0, beta=1.0):
        """
        Compute a fitness score for the solution. Lower is better.
        Combines total distance and CPU penalties.
        """
        total_distance = 0
        total_cpu_penalty = 0

        for city_idx, server_idx in enumerate(self.assignment):
            city = cities[city_idx]
            server = servers[server_idx]

            distance = haversine_distance(
                city['lat'], city['long'],
                server['lat'], server['long']
            )
            total_distance += distance

            load = self.server_loads[server_idx]
            projected_load_percent = (load / server['Capacity']) * 100
            stress = server['CPU_Health'] + projected_load_percent
            penalty = max(0, (stress - server['Threshold']))
            total_cpu_penalty += penalty

        return alpha * total_distance + beta * total_cpu_penalty
