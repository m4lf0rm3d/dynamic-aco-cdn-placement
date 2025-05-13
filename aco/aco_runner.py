import numpy as np

from utils.geo import haversine_distance
from .pheromone import PheromoneMatrix
from .ant import Ant
from .fitness import total_fitness

def run_aco(cities, servers, alpha=1.0, beta=1.0, gamma=0.5, iterations=50, num_ants=10, 
            evaporation=0.1, q0=0.1, min_pheromone=0.1, max_pheromone=10.0):
    """
    Run ACO optimization for CDN server assignment with dynamic server management
    
    Args:
        cities: List of cities with usage data
        servers: List of servers with capacity and status
        alpha: Weight for distance objective
        beta: Weight for CPU health objective
        gamma: Weight for load balancing objective
        iterations: Number of ACO iterations
        num_ants: Number of ants per iteration
        evaporation: Pheromone evaporation rate
        q0: Exploration/exploitation parameter
        min_pheromone: Minimum pheromone value
        max_pheromone: Maximum pheromone value
        
    Returns:
        best_assignment: Best found city-server assignment
        last_iteration_ant_paths: Paths from last iteration for visualization
        convergence_data: Fitness values over iterations for analysis
    """
    pheromones = PheromoneMatrix(len(cities), len(servers), 
                 min_val=min_pheromone, max_val=max_pheromone)
    best_assignment = None
    best_assignment_each_iteration = []
    best_cost = float('inf')
    convergence_data = []
    
    # Track server states over iterations
    server_utilization_history = []
    active_servers_history = []

    for iteration in range(iterations):
        ants = [Ant(len(cities), len(servers)) for _ in range(num_ants)]
        iteration_costs = []
        
        # Construct solutions
        for ant in ants:
            # Dynamic q0 - more exploration early, more exploitation later
            current_q0 = q0 * (iteration / iterations)
            ant.construct_solution(pheromones, cities, servers, 
                                 alpha, beta, gamma, q0=current_q0)
            
            # Calculate fitness with dynamic weights
            cost = total_fitness(ant.assignment, cities, servers, alpha, beta, gamma)
            iteration_costs.append(cost)
            
            # Update best solution
            if cost < best_cost:
                best_cost = cost
                best_assignment = ant.assignment.copy()
                
                # Dynamic server management based on best solution
                update_server_states(best_assignment, cities, servers)

        best_assignment_each_iteration.append(best_cost)
        print(f"[INFO] Iteration {iteration+1}/{iterations}, Ant Cost: {cost:.2f}, Best Cost: {best_cost:.2f}")

        # Track convergence and server utilization
        avg_cost = np.mean(iteration_costs)
        convergence_data.append(avg_cost)
        
        # Record server utilization metrics
        util, active = calculate_utilization_metrics(best_assignment, cities, servers)
        server_utilization_history.append(util)
        active_servers_history.append(active)

        # Pheromone update
        pheromones.evaporate(evaporation)
        
        # Only reinforce top-performing solutions
        elite_ants = sorted(ants, key=lambda a: total_fitness(a.assignment, cities, servers, alpha, beta, gamma))[:int(num_ants*0.3)]
        
        for ant in elite_ants:
            cost = total_fitness(ant.assignment, cities, servers, alpha, beta, gamma)
            pheromone_deposit = 1.0 / (1 + cost)  # Normalized deposit
            
            for city_idx, server_idx in enumerate(ant.assignment):
                pheromones.reinforce(city_idx, server_idx, pheromone_deposit)
                
        # Apply pheromone bounds
        pheromones.enforce_bounds()

    # Get paths from last iteration
    last_iteration_ant_paths = [ant.assignment for ant in ants]
    
    # Final server state update
    update_server_states(best_assignment, cities, servers)
    
    return {
        'best_assignment': best_assignment,
        'last_iteration_paths': last_iteration_ant_paths,
        'convergence': convergence_data,
        'server_utilization': server_utilization_history,
        'active_servers': active_servers_history,
        'best_cost': best_cost,
        'best_assignment_each_iteration': best_assignment_each_iteration
    }

def update_server_states(assignment, cities, servers):
    """Dynamically turn servers on/off based on assignment"""
    server_loads = [0] * len(servers)
    
    # Calculate server loads
    for city_idx, server_idx in enumerate(assignment):
        server_loads[server_idx] += cities[city_idx]['UsagePerHour']
    
    # Update server states
    for server_idx, server in enumerate(servers):
        if server['Status'] == 'Down':
            # Consider turning on if nearby cities have sufficient demand
            nearby_demand = calculate_nearby_demand(server, cities, assignment)
            if nearby_demand > server['Capacity'] * 0.3:  # 30% threshold
                server['Status'] = 'Running'
                server['CPU_Health'] = 10  # Initial low CPU
        else:
            # Turn off if underutilized
            if server_loads[server_idx] < server['Capacity'] * 0.1:  # 10% threshold
                server['Status'] = 'Down'
                server['CPU_Health'] = 0

def calculate_nearby_demand(server, cities, assignment, radius_km=1000):
    """Calculate total demand from cities within radius of server"""
    total_demand = 0
    for city_idx, city in enumerate(cities):
        if assignment[city_idx] == -1:  # Unassigned cities
            distance = haversine_distance(
                server['lat'], server['long'],
                city['lat'], city['long']
            )
            if distance <= radius_km:
                total_demand += city['UsagePerHour']
    return total_demand

def calculate_utilization_metrics(assignment, cities, servers):
    """Calculate server utilization metrics"""
    server_loads = [0] * len(servers)
    for city_idx, server_idx in enumerate(assignment):
        if server_idx != -1:  # Skip unassigned
            server_loads[server_idx] += cities[city_idx]['UsagePerHour']
    
    active_servers = sum(1 for s in servers if s['Status'] == 'Running')
    avg_utilization = np.mean([load/servers[i]['Capacity'] 
                             for i, load in enumerate(server_loads) 
                             if servers[i]['Status'] == 'Running'] or [0])
    
    return avg_utilization, active_servers