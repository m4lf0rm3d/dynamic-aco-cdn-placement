import time
from utils.generator import generate_city_data, generate_fake_data, generate_server_data
from aco.aco_runner import run_aco
from utils.geo import adjust_usage_based_on_time
from utils.loader import load_csv
from visualization.animate_ants import plot_best_assignment_progress, plot_map
from config import ALPHA, BETA, GAMMA, NUM_ITERATIONS, NUM_ANTS, Q0
import numpy as np

def run_aco_and_visualize(cities, servers, num_iterations=NUM_ITERATIONS, num_ants=NUM_ANTS):
    """
    Run the ACO algorithm and visualize the movement of ants on the 2D map.
    
    Args:
        cities: List of city dictionaries
        servers: List of server dictionaries
        num_iterations: Number of ACO iterations
        num_ants: Number of ants per iteration
        
    Returns:
        Dictionary containing optimization results and metrics
    """
    # Initialize logging structures
    results = {
        'latency_log': [],
        'cpu_health_history': [],
        'server_utilization': [],
        'active_servers_history': []
    }

    # Convert data types
    for city in cities:
        city['lat'] = float(city['lat'])
        city['long'] = float(city['long'])
        city['UsagePerHour'] = int(city['UsagePerHour'])

    for server in servers:
        server['lat'] = float(server['lat'])
        server['long'] = float(server['long'])
        server['CPU_Health'] = float(server['CPU_Health'])
        server['Threshold'] = float(server['Threshold'])
        server['Capacity'] = float(server.get('Capacity', 15000))  # Default capacity

    print(f"[INFO] Starting ACO optimization with {num_iterations} iterations...")
    
    # Run ACO optimization
    aco_results = run_aco(
        cities=cities,
        servers=servers,
        alpha=ALPHA,
        beta=BETA,
        gamma=GAMMA,
        q0=Q0,
        iterations=num_iterations,
        num_ants=num_ants
    )

    best_assignment = aco_results['best_assignment']
    best_assignment_each_iteration = aco_results['best_assignment_each_iteration']
    # ant_paths = aco_results['last_iteration_paths']

    # Update server statuses based on final assignment
    server_loads = {server['CDN_ID']: 0 for server in servers}
    # server_indices = {server['CDN_ID']: i for i, server in enumerate(servers)}

    # Calculate server loads and update CPU health
    for city_idx, server_idx in enumerate(best_assignment):
        server = servers[server_idx]
        city = cities[city_idx]
        server_loads[server['CDN_ID']] += city['UsagePerHour']
        
        # Update CPU health based on load
        utilization = server_loads[server['CDN_ID']] / server['Capacity']
        server['CPU_Health'] = min(100, utilization * 100)  # Cap at 100%

    # Update server statuses
    for server in servers:
        cdn_id = server['CDN_ID']
        if server_loads[cdn_id] < server['Capacity'] * 0.2:  # 30% threshold
            server['Status'] = 'Down'
            server['CPU_Health'] = 0  # Reset CPU health when down
        else:
            server['Status'] = 'Running'

    # Visualize final result
    print("[INFO] Visualizing final optimization result...")
    plot_map(cities, servers, [best_assignment])

    # Visual best assignment graph using matplotlib
    print("[INFO] Visualizing best assignment graph...")
    plot_best_assignment_progress(best_assignment_each_iteration)




    # Compile results
    results.update({
        'best_assignment': best_assignment,
        'final_server_loads': server_loads,
        'convergence_data': aco_results['convergence'],
        'utilization_history': aco_results['server_utilization'],
        'active_servers_history': aco_results['active_servers'],
        'best_cost': aco_results['best_cost'],
    })

    return results

if __name__ == '__main__':
    print("[INFO] Initializing simulation...")

    # Generate and load data
    generate_city_data()
    generate_server_data()

    cities = load_csv('data/cities.csv')
    servers = load_csv('data/edge_servers.csv')

    # Uncomment the following line to generate realistic hemisphere usage data
    # cities = adjust_usage_based_on_time(cities)

    try:
        print("[INFO] Running the simulation...")
        results = run_aco_and_visualize(cities, servers)
        
        print("\n[INFO] Simulation completed successfully!")
        print(f"Best solution found with fitness: {results['best_cost']}")
        print(f"Final active servers: {sum(1 for s in servers if s['Status'] == 'Running')}/{len(servers)}")
        
    except KeyboardInterrupt:
        print("\n[STOPPED] Simulation stopped by user.")
    except Exception as e:
        print(f"\n[ERROR] Simulation failed: {str(e)}")