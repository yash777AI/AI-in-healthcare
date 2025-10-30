"""
Test suite for Ant Colony Optimization TSP implementation
"""

import numpy as np
from ant_colony_optimization_tsp import (
    AntColonyOptimization,
    brute_force_tsp,
    dp_tsp,
    generate_random_cities
)


def test_aco_basic():
    """Test basic ACO functionality."""
    print("Testing ACO basic functionality...")
    
    # Simple 4-city problem
    distances = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ])
    
    aco = AntColonyOptimization(distances, T=20, m=5)
    path, distance, history = aco.optimize(verbose=False)
    
    assert len(path) == 4, "Path should contain all 4 cities"
    assert len(set(path)) == 4, "Path should contain unique cities"
    assert distance > 0, "Distance should be positive"
    assert len(history) == 20, "History should contain 20 iterations"
    
    print(f"✓ ACO found solution with distance: {distance:.2f}")
    print(f"✓ Path: {path}")


def test_brute_force():
    """Test brute-force TSP solver."""
    print("\nTesting brute-force solver...")
    
    # Simple 5-city problem
    distances = np.array([
        [0, 2, 9, 10, 7],
        [2, 0, 6, 4, 3],
        [9, 6, 0, 8, 5],
        [10, 4, 8, 0, 6],
        [7, 3, 5, 6, 0]
    ])
    
    path, distance = brute_force_tsp(distances)
    
    assert path is not None, "Should find a path"
    assert len(path) == 5, "Path should contain all 5 cities"
    assert distance > 0, "Distance should be positive"
    
    print(f"✓ Brute-force found optimal solution: {distance:.2f}")
    print(f"✓ Path: {path}")


def test_dp():
    """Test dynamic programming TSP solver."""
    print("\nTesting DP solver...")
    
    # Simple 6-city problem
    np.random.seed(123)
    cities, distances = generate_random_cities(6, max_coord=50)
    
    path, distance = dp_tsp(distances)
    
    assert path is not None, "Should find a path"
    assert len(path) == 6, "Path should contain all 6 cities"
    assert distance > 0, "Distance should be positive"
    
    print(f"✓ DP found optimal solution: {distance:.2f}")
    print(f"✓ Path: {path}")


def test_aco_vs_optimal():
    """Test ACO against optimal solution for small problem."""
    print("\nTesting ACO vs optimal solution...")
    
    # Generate small problem
    np.random.seed(456)
    cities, distances = generate_random_cities(7, max_coord=100)
    
    # Run ACO
    aco = AntColonyOptimization(distances, T=50, m=10, rho=0.5, alpha=1, beta=2)
    aco_path, aco_distance, _ = aco.optimize(verbose=False)
    
    # Get optimal solution
    opt_path, opt_distance = brute_force_tsp(distances)
    
    error_percent = abs(aco_distance - opt_distance) / opt_distance * 100
    
    print(f"✓ ACO distance: {aco_distance:.2f}")
    print(f"✓ Optimal distance: {opt_distance:.2f}")
    print(f"✓ Error: {error_percent:.2f}%")
    
    # ACO should be within 10% of optimal for small problems
    assert error_percent <= 10, f"ACO error too high: {error_percent:.2f}%"


def test_probability_calculation():
    """Test probability calculation for path sampling."""
    print("\nTesting probability calculation...")
    
    distances = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ])
    
    aco = AntColonyOptimization(distances, T=10, m=5)
    
    # Calculate probabilities from city 0
    unvisited = {1, 2, 3}
    probs = aco.calculate_probabilities(0, unvisited)
    
    # Check that probabilities sum to 1
    prob_sum = sum(probs.values())
    assert abs(prob_sum - 1.0) < 1e-6, f"Probabilities should sum to 1, got {prob_sum}"
    
    # Check all unvisited cities have probabilities
    assert len(probs) == 3, "Should have probabilities for all unvisited cities"
    
    print(f"✓ Probabilities: {probs}")
    print(f"✓ Probability sum: {prob_sum:.6f}")


def test_pheromone_update():
    """Test pheromone update mechanism."""
    print("\nTesting pheromone update...")
    
    distances = np.array([
        [0, 10, 15],
        [10, 0, 20],
        [15, 20, 0]
    ])
    
    aco = AntColonyOptimization(distances, T=5, m=2, rho=0.5, Q=100)
    
    # Store initial pheromone
    initial_pheromone = aco.pheromones.copy()
    
    # Create some paths
    paths = [[0, 1, 2], [0, 2, 1]]
    distances_list = [aco.calculate_path_distance(p) for p in paths]
    
    # Update pheromones
    aco.update_pheromones(paths, distances_list)
    
    # Check that pheromones changed
    assert not np.allclose(aco.pheromones, initial_pheromone), "Pheromones should change"
    
    # Check evaporation occurred
    assert np.all(aco.pheromones >= 0), "Pheromones should be non-negative"
    
    print("✓ Pheromone update working correctly")


def test_random_cities_generation():
    """Test random city generation."""
    print("\nTesting random city generation...")
    
    n = 10
    cities, distances = generate_random_cities(n, max_coord=100)
    
    assert cities.shape == (n, 2), "Should generate n cities with 2D coordinates"
    assert distances.shape == (n, n), "Distance matrix should be n x n"
    assert np.allclose(distances, distances.T), "Distance matrix should be symmetric"
    assert np.allclose(np.diag(distances), 0), "Diagonal should be zero"
    
    print(f"✓ Generated {n} cities successfully")
    print(f"✓ Distance matrix is symmetric and valid")


def run_all_tests():
    """Run all test cases."""
    print("=" * 70)
    print("Running Test Suite for Ant Colony Optimization TSP")
    print("=" * 70)
    
    try:
        test_aco_basic()
        test_brute_force()
        test_dp()
        test_aco_vs_optimal()
        test_probability_calculation()
        test_pheromone_update()
        test_random_cities_generation()
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED")
        print("=" * 70)
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
