"""
Ant Colony Optimization for Travelling Salesman Problem
Homework 6 - Artificial Intelligence
Prof. Truong-Son Hy

This implementation includes:
1. Ant Colony Optimization (ACO) algorithm
2. Stochastic path sampling based on pheromone and heuristic information
3. Brute-force backtracking for verification (N ≤ 10)
4. Bit-mask dynamic programming for verification (N ≤ 20)
5. Visualization of the solution path
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import time


class AntColonyOptimization:
    """
    Ant Colony Optimization for solving the Travelling Salesman Problem.
    
    Hyperparameters:
    - T: Number of iterations
    - rho (ρ): Pheromone evaporation rate (0 < ρ < 1)
    - m: Number of ants
    - Q: Pheromone deposit factor
    - epsilon (ε): Small constant to avoid division by zero
    - alpha (α): Pheromone importance factor
    - beta (β): Heuristic information (distance) importance factor
    """
    
    def __init__(self, distances, T=100, rho=0.5, m=10, Q=100, epsilon=1e-10, alpha=1, beta=2):
        """
        Initialize ACO algorithm.
        
        Args:
            distances: Distance matrix between cities (N x N)
            T: Number of iterations
            rho: Pheromone evaporation rate
            m: Number of ants
            Q: Pheromone deposit factor
            epsilon: Small constant for numerical stability
            alpha: Pheromone importance
            beta: Heuristic importance
        """
        self.distances = np.array(distances)
        self.n_cities = len(distances)
        self.T = T
        self.rho = rho
        self.m = m
        self.Q = Q
        self.epsilon = epsilon
        self.alpha = alpha
        self.beta = beta
        
        # Initialize pheromone matrix with small positive values
        self.pheromones = np.ones((self.n_cities, self.n_cities)) * 0.1
        
        # Heuristic information (inverse of distance)
        self.eta = 1.0 / (self.distances + epsilon)
        np.fill_diagonal(self.eta, 0)
        
        # Track best solution
        self.best_path = None
        self.best_distance = float('inf')
        self.history = []
        
    def calculate_path_distance(self, path):
        """Calculate total distance of a given path."""
        distance = 0
        for i in range(len(path) - 1):
            distance += self.distances[path[i]][path[i+1]]
        # Return to starting city
        distance += self.distances[path[-1]][path[0]]
        return distance
    
    def calculate_probabilities(self, current_city, unvisited):
        """
        Calculate probability of moving to each unvisited city.
        
        Based on pxy = (τxy^α * ηxy^β) / Σ(τxz^α * ηxz^β) for z in unvisited
        
        Args:
            current_city: Current city index
            unvisited: Set of unvisited cities
            
        Returns:
            Dictionary mapping city to its selection probability
        """
        probabilities = {}
        denominator = 0
        
        # Calculate numerator for each unvisited city
        for city in unvisited:
            pheromone = self.pheromones[current_city][city] ** self.alpha
            heuristic = self.eta[current_city][city] ** self.beta
            probabilities[city] = pheromone * heuristic
            denominator += probabilities[city]
        
        # Normalize probabilities
        if denominator > 0:
            for city in probabilities:
                probabilities[city] /= denominator
        else:
            # Equal probability if denominator is zero
            prob = 1.0 / len(unvisited)
            for city in unvisited:
                probabilities[city] = prob
                
        return probabilities
    
    def construct_solution(self):
        """
        Construct a solution path for one ant using stochastic sampling.
        
        The ant starts from a random city and selects the next city based on
        probabilities calculated from pheromone trails and heuristic information.
        
        Returns:
            path: List of cities visited
        """
        # Start from a random city
        start_city = np.random.randint(0, self.n_cities)
        path = [start_city]
        unvisited = set(range(self.n_cities)) - {start_city}
        
        current_city = start_city
        
        # Visit all cities
        while unvisited:
            # Calculate probabilities for unvisited cities
            probabilities = self.calculate_probabilities(current_city, unvisited)
            
            # Stochastic selection based on probabilities
            cities = list(probabilities.keys())
            probs = list(probabilities.values())
            
            # Sample next city based on probability distribution
            next_city = np.random.choice(cities, p=probs)
            
            path.append(next_city)
            unvisited.remove(next_city)
            current_city = next_city
        
        return path
    
    def update_pheromones(self, all_paths, all_distances):
        """
        Update pheromone trails based on ant solutions.
        
        Args:
            all_paths: List of paths constructed by all ants
            all_distances: List of distances for each path
        """
        # Evaporation
        self.pheromones *= (1 - self.rho)
        
        # Add new pheromones
        for path, distance in zip(all_paths, all_distances):
            delta_pheromone = self.Q / distance
            
            # Update pheromones for each edge in the path
            for i in range(len(path) - 1):
                self.pheromones[path[i]][path[i+1]] += delta_pheromone
                self.pheromones[path[i+1]][path[i]] += delta_pheromone
            
            # Edge from last city back to first
            self.pheromones[path[-1]][path[0]] += delta_pheromone
            self.pheromones[path[0]][path[-1]] += delta_pheromone
    
    def optimize(self, verbose=True):
        """
        Run the ACO algorithm for T iterations.
        
        Args:
            verbose: Print progress information
            
        Returns:
            best_path: Best path found
            best_distance: Distance of best path
            history: History of best distances per iteration
        """
        for iteration in range(self.T):
            # Generate solutions for all ants
            all_paths = []
            all_distances = []
            
            for ant in range(self.m):
                path = self.construct_solution()
                distance = self.calculate_path_distance(path)
                
                all_paths.append(path)
                all_distances.append(distance)
                
                # Update best solution
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_path = path.copy()
            
            # Update pheromones
            self.update_pheromones(all_paths, all_distances)
            
            # Track history
            self.history.append(self.best_distance)
            
            if verbose and (iteration + 1) % 10 == 0:
                print(f"Iteration {iteration + 1}/{self.T}: Best distance = {self.best_distance:.2f}")
        
        return self.best_path, self.best_distance, self.history


def brute_force_tsp(distances):
    """
    Brute-force solution for TSP using backtracking.
    Suitable for N ≤ 10.
    
    Args:
        distances: Distance matrix
        
    Returns:
        best_path: Optimal path
        best_distance: Optimal distance
    """
    n = len(distances)
    
    if n > 10:
        print("Warning: Brute-force is too slow for N > 10")
        return None, float('inf')
    
    cities = list(range(n))
    best_path = None
    best_distance = float('inf')
    
    # Try all permutations starting from city 0
    for perm in permutations(cities[1:]):
        path = [0] + list(perm)
        
        # Calculate distance
        distance = 0
        for i in range(n - 1):
            distance += distances[path[i]][path[i+1]]
        distance += distances[path[-1]][path[0]]
        
        if distance < best_distance:
            best_distance = distance
            best_path = path
    
    return best_path, best_distance


def dp_tsp(distances):
    """
    Dynamic Programming solution for TSP using bit-mask DP.
    Suitable for N ≤ 20.
    
    The state is (current_city, visited_mask) where visited_mask is a bitmask
    representing which cities have been visited.
    
    Args:
        distances: Distance matrix
        
    Returns:
        best_path: Optimal path
        best_distance: Optimal distance
    """
    n = len(distances)
    
    if n > 20:
        print("Warning: DP solution is too memory intensive for N > 20")
        return None, float('inf')
    
    # dp[mask][i] = minimum cost to visit cities in mask ending at city i
    dp = [[float('inf')] * n for _ in range(1 << n)]
    parent = [[None] * n for _ in range(1 << n)]
    
    # Start from city 0
    dp[1][0] = 0
    
    # Iterate through all subsets
    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == float('inf'):
                continue
            
            # Try to extend to unvisited cities
            for next_city in range(n):
                if mask & (1 << next_city):
                    continue
                
                new_mask = mask | (1 << next_city)
                new_cost = dp[mask][last] + distances[last][next_city]
                
                if new_cost < dp[new_mask][next_city]:
                    dp[new_mask][next_city] = new_cost
                    parent[new_mask][next_city] = last
    
    # Find the minimum cost to visit all cities
    full_mask = (1 << n) - 1
    best_distance = float('inf')
    last_city = -1
    
    for i in range(n):
        cost = dp[full_mask][i] + distances[i][0]
        if cost < best_distance:
            best_distance = cost
            last_city = i
    
    # Reconstruct path
    path = []
    mask = full_mask
    current = last_city
    
    while current is not None:
        path.append(current)
        next_current = parent[mask][current]
        if next_current is not None:
            mask ^= (1 << current)
        current = next_current
    
    path.reverse()
    
    return path, best_distance


def generate_random_cities(n, max_coord=100):
    """
    Generate random city coordinates and compute distance matrix.
    
    Args:
        n: Number of cities
        max_coord: Maximum coordinate value
        
    Returns:
        cities: Array of city coordinates (n x 2)
        distances: Distance matrix (n x n)
    """
    cities = np.random.rand(n, 2) * max_coord
    
    # Calculate Euclidean distances
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                distances[i][j] = np.sqrt(np.sum((cities[i] - cities[j]) ** 2))
    
    return cities, distances


def visualize_solution(cities, path, distance, title="TSP Solution"):
    """
    Visualize the TSP solution.
    
    Args:
        cities: Array of city coordinates
        path: Solution path
        distance: Total distance
        title: Plot title
    """
    plt.figure(figsize=(10, 8))
    
    # Plot cities
    plt.scatter(cities[:, 0], cities[:, 1], c='red', s=200, zorder=2)
    
    # Label cities
    for i, (x, y) in enumerate(cities):
        plt.annotate(str(i), (x, y), fontsize=12, ha='center', va='center')
    
    # Plot path
    for i in range(len(path) - 1):
        x = [cities[path[i]][0], cities[path[i+1]][0]]
        y = [cities[path[i]][1], cities[path[i+1]][1]]
        plt.plot(x, y, 'b-', linewidth=2, alpha=0.7, zorder=1)
    
    # Connect last city back to first
    x = [cities[path[-1]][0], cities[path[0]][0]]
    y = [cities[path[-1]][1], cities[path[0]][1]]
    plt.plot(x, y, 'b-', linewidth=2, alpha=0.7, zorder=1)
    
    plt.title(f"{title}\nTotal Distance: {distance:.2f}")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return plt


def visualize_convergence(history, title="ACO Convergence"):
    """
    Visualize the convergence of ACO algorithm.
    
    Args:
        history: List of best distances per iteration
        title: Plot title
    """
    plt.figure(figsize=(10, 6))
    plt.plot(history, linewidth=2)
    plt.xlabel("Iteration")
    plt.ylabel("Best Distance")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return plt


def main():
    """
    Main function to demonstrate ACO for TSP with different problem sizes.
    """
    print("=" * 70)
    print("Ant Colony Optimization for Travelling Salesman Problem")
    print("=" * 70)
    
    # Hyperparameters
    T = 100          # Number of iterations
    rho = 0.5        # Evaporation rate
    m = 10           # Number of ants
    Q = 100          # Pheromone deposit factor
    epsilon = 1e-10  # Small constant
    alpha = 1        # Pheromone importance
    beta = 2         # Heuristic importance
    
    print("\nHyperparameters:")
    print(f"T (iterations): {T}")
    print(f"ρ (evaporation rate): {rho}")
    print(f"m (number of ants): {m}")
    print(f"Q (pheromone deposit): {Q}")
    print(f"ε (epsilon): {epsilon}")
    print(f"α (pheromone importance): {alpha}")
    print(f"β (heuristic importance): {beta}")
    
    # Test cases with different sizes
    test_cases = [
        {"name": "Small (N=8)", "n": 8, "verify": "brute-force"},
        {"name": "Medium (N=15)", "n": 15, "verify": "dp"},
        {"name": "Large (N=20)", "n": 20, "verify": "dp"},
    ]
    
    for test_case in test_cases:
        print("\n" + "=" * 70)
        print(f"Test Case: {test_case['name']}")
        print("=" * 70)
        
        n = test_case['n']
        
        # Generate random cities
        np.random.seed(42)  # For reproducibility
        cities, distances = generate_random_cities(n)
        
        # Run ACO
        print(f"\nRunning ACO for {n} cities...")
        start_time = time.time()
        aco = AntColonyOptimization(distances, T=T, rho=rho, m=m, Q=Q, 
                                     epsilon=epsilon, alpha=alpha, beta=beta)
        aco_path, aco_distance, history = aco.optimize(verbose=True)
        aco_time = time.time() - start_time
        
        print(f"\nACO Solution:")
        print(f"Path: {aco_path}")
        print(f"Distance: {aco_distance:.2f}")
        print(f"Time: {aco_time:.4f} seconds")
        
        # Verify with optimal solution
        if test_case['verify'] == 'brute-force' and n <= 10:
            print(f"\nVerifying with brute-force...")
            start_time = time.time()
            opt_path, opt_distance = brute_force_tsp(distances)
            opt_time = time.time() - start_time
            
            print(f"Optimal Solution (Brute-force):")
            print(f"Path: {opt_path}")
            print(f"Distance: {opt_distance:.2f}")
            print(f"Time: {opt_time:.4f} seconds")
            print(f"ACO Error: {abs(aco_distance - opt_distance) / opt_distance * 100:.2f}%")
            
        elif test_case['verify'] == 'dp' and n <= 20:
            print(f"\nVerifying with DP...")
            start_time = time.time()
            opt_path, opt_distance = dp_tsp(distances)
            opt_time = time.time() - start_time
            
            print(f"Optimal Solution (DP):")
            print(f"Path: {opt_path}")
            print(f"Distance: {opt_distance:.2f}")
            print(f"Time: {opt_time:.4f} seconds")
            print(f"ACO Error: {abs(aco_distance - opt_distance) / opt_distance * 100:.2f}%")
        
        # Visualize
        plt1 = visualize_solution(cities, aco_path, aco_distance, 
                                  f"ACO Solution - {test_case['name']}")
        plt1.savefig(f"aco_solution_{n}_cities.png", dpi=150, bbox_inches='tight')
        plt1.close()
        
        plt2 = visualize_convergence(history, f"ACO Convergence - {test_case['name']}")
        plt2.savefig(f"aco_convergence_{n}_cities.png", dpi=150, bbox_inches='tight')
        plt2.close()
        
        print(f"\nVisualization saved as 'aco_solution_{n}_cities.png' and 'aco_convergence_{n}_cities.png'")


if __name__ == "__main__":
    main()
