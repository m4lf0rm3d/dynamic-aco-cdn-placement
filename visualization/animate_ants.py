import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import Normalize
import numpy as np

def init_map(ax):
    """Initialize the map with beautiful styling"""
    ax.set_global()
    
    # Add natural earth features with custom styling
    ax.add_feature(cfeature.OCEAN, facecolor='#a6cee3', alpha=0.8)
    ax.add_feature(cfeature.LAND, facecolor='#f2f2f2', edgecolor='none')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='#7f7f7f')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8, edgecolor='#4d4d4d')
    
    # Add gridlines
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    
    # Set background color for the figure
    fig.patch.set_facecolor('#f9f9f9')

def calculate_line_width(usage, min_usage=100, max_usage=10000):
    """Calculate line width proportional to usage"""
    min_width = 0.1
    max_width = 2.0
    # Logarithmic scaling works better for wide value ranges
    log_usage = np.log10(usage)
    log_min = np.log10(min_usage)
    log_max = np.log10(max_usage)
    normalized = (log_usage - log_min) / (log_max - log_min)
    return min_width + normalized * (max_width - min_width)

def calculate_marker_size(cpu_health):
    """Calculate marker size proportional to CPU health
    Args:
        cpu_health: CPU health percentage (30-100)
    Returns:
        Marker size between min_size and max_size
    """
    # min_size = 120
    # max_size = 120
    # min_cpu = 30
    # max_cpu = 100
    
    # # Direct scaling (higher CPU = larger marker)
    # # Normalize between actual min/max CPU range
    # normalized = (cpu_health - min_cpu) / (max_cpu - min_cpu)
    # normalized = np.clip(normalized, 0, 1)  # Ensure within bounds
    
    return 60

def update_map(cities, servers, ants_paths):
    """Update the map with current data"""
    ax.clear()
    init_map(ax)
    
    # Create a color map for CPU health
    cmap = plt.get_cmap('RdYlGn_r')  # Red-Yellow-Green (reversed)
    cpu_norm = Normalize(vmin=0, vmax=100)
    
    # Plot edge servers with size based on CPU health and color based on status
    for server in servers:
        lat = float(server['lat'])
        lon = float(server['long'])
        status = server['Status']
        cpu_health = float(server['CPU_Health'])
        
        # Determine color and edge properties
        if status == 'Running':
            color = cmap(cpu_norm(cpu_health))
            edgecolor = 'darkgreen'
            edgewidth = 0.5
        else:
            color = 'black'
            edgecolor = 'darkred'
            edgewidth = 1.0
        
        size = calculate_marker_size(cpu_health)
        
        ax.scatter(lon, lat, s=size, 
                   c=[color], 
                   edgecolors=edgecolor,
                   linewidths=edgewidth,
                   marker='o',
                   transform=ccrs.PlateCarree(),
                   zorder=4)
        
        # Add server label
        ax.text(lon, lat+1, server['CDN_ID'], 
                fontsize=8, ha='center', va='bottom',
                transform=ccrs.PlateCarree())
    
    # Plot connections with width based on city usage
    for path in ants_paths:
        for c_idx, s_idx in enumerate(path):
            city = cities[c_idx]
            server = servers[s_idx]
            
            city_lat, city_lon = float(city['lat']), float(city['long'])
            server_lat, server_lon = float(server['lat']), float(server['long'])
            
            usage = float(city['UsagePerHour'])
            linewidth = calculate_line_width(usage)
            
            ax.plot([city_lon, server_lon], [city_lat, server_lat],
                    color='#6a3d9a',  # Purple color for connections
                    linewidth=linewidth,
                    alpha=0.7,
                    transform=ccrs.PlateCarree(),
                    zorder=2,
                    solid_capstyle='round')
    
    # Add city markers with size based on usage
    for city in cities:
        lat, lon = float(city['lat']), float(city['long'])
        usage = float(city['UsagePerHour'])
        size = calculate_line_width(usage) * 3  # Scale for marker size
        
        ax.scatter(lon, lat, s=size,
                   c='#ff7f00',  # Orange color for cities
                   alpha=0.8,
                   edgecolors='#984ea3',
                   linewidths=0.5,
                   marker='s',  # Square marker
                   transform=ccrs.PlateCarree(),
                   zorder=3)
        
        # Add city label
        ax.text(lon, lat-1, city['City'], 
                fontsize=8, ha='center', va='top',
                transform=ccrs.PlateCarree())
    
    # Add title and legend
    ax.set_title("ACO Ants on CDN Network - Real-time Optimization", 
                fontsize=14, pad=20, weight='bold')
    
    # Add custom legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Edge Server',
                  markerfacecolor='green', markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='City',
                  markerfacecolor='orange', markersize=10),
        plt.Line2D([0], [0], color='purple', lw=2, label='Network Connection'),
    ]
    
    ax.legend(handles=legend_elements, loc='lower left',
             frameon=True, facecolor='white', framealpha=0.8)
    
    # Add colorbar for CPU health
    # sm = plt.cm.ScalarMappable(cmap=cmap, norm=cpu_norm)
    # sm.set_array([])
    # cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.05, aspect=40)
    # cbar.set_label('CPU Health (%)')
    
    plt.tight_layout()

def plot_map(cities, servers, ants_paths):
    """
    Public function to initialize and render the ants animation on map.
    """
    global fig, ax
    fig, ax = plt.subplots(figsize=(16, 9), 
                         subplot_kw={'projection': ccrs.PlateCarree()})
    
    update_map(cities, servers, ants_paths)
    plt.show()

def plot_best_assignment_progress(best_assignment_each_iteration):
    """
    Plots the progress of the best assignment value over iterations.

    Args:
        best_assignment_each_iteration: List of best cost or objective values per iteration
    """
    iterations = list(range(1, len(best_assignment_each_iteration) + 1))
    values = best_assignment_each_iteration

    print(iterations)
    print(values)

    plt.figure(figsize=(10, 6))
    plt.plot(iterations, values, marker='o', linestyle='-', color='blue', label='Best Assignment Cost')
    plt.title('ACO Optimization Convergence')
    plt.xlabel('Iteration')
    plt.ylabel('Best Assignment Value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
