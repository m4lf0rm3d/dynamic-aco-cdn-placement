import numpy as np

class PheromoneMatrix:
    def __init__(
        self,
        num_cities: int,
        num_servers: int,
        min_val: float = 0.1,
        max_val: float = 10.0,
        initial_val: float = 1.0
    ):
        """
        Initializes the pheromone matrix with specified bounds and initial value.

        Args:
            num_cities (int): Number of cities.
            num_servers (int): Number of servers.
            min_val (float): Minimum allowed pheromone value.
            max_val (float): Maximum allowed pheromone value.
            initial_val (float): Initial pheromone value for all paths.
        """
        self.min_val = min_val
        self.max_val = max_val
        self.matrix = np.full((num_cities, num_servers), initial_val, dtype=np.float32)

    def update(self, city_idx: int, server_idx: int, delta: float):
        """
        Updates the pheromone level for a specific city-server pair with bounds checking.

        Args:
            city_idx (int): Index of the city.
            server_idx (int): Index of the server.
            delta (float): Amount to change the pheromone by.
        """
        new_value = self.matrix[city_idx, server_idx] + delta
        self.matrix[city_idx, server_idx] = np.clip(new_value, self.min_val, self.max_val)

    def get_pheromone(self, city_idx: int, server_idx: int) -> float:
        """
        Returns the current pheromone level for a city-server pair.
        """
        return self.matrix[city_idx, server_idx]

    def evaporate(self, evaporation_rate: float):
        """
        Globally evaporates pheromones by reducing each value.

        Args:
            evaporation_rate (float): Fraction by which pheromones are reduced.
        """
        self.matrix = np.clip(self.matrix * (1 - evaporation_rate), self.min_val, self.max_val)

    def reinforce(self, city_idx: int, server_idx: int, delta: float):
        """
        Increases pheromone level for a specific path (same as `update`).

        Args:
            city_idx (int): Index of the city.
            server_idx (int): Index of the server.
            delta (float): Amount to increase pheromone by.
        """
        self.update(city_idx, server_idx, delta)

    def enforce_bounds(self):
        """
        Ensures all pheromone values stay within [min_val, max_val].
        """
        self.matrix = np.clip(self.matrix, self.min_val, self.max_val)

    def get_matrix(self) -> np.ndarray:
        """
        Returns a copy of the full pheromone matrix.
        """
        return self.matrix.copy()

    def normalize(self):
        """
        Normalizes pheromone values row-wise (per city), so each city's pheromones sum to 1.
        """
        row_sums = self.matrix.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        self.matrix = self.matrix / row_sums
        self.enforce_bounds()
