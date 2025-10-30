# Ant Colony Optimization for Travelling Salesman Problem

This repository contains a complete implementation of Ant Colony Optimization (ACO) for solving the Travelling Salesman Problem (TSP), developed as part of Homework 6 for the Artificial Intelligence course.

## Overview

The implementation includes:
- **Ant Colony Optimization** algorithm with pheromone trail management
- **Stochastic path sampling** based on probabilistic selection
- **Verification algorithms**: Brute-force (N ≤ 10) and Dynamic Programming (N ≤ 20)
- **Visualization**: Solution paths and convergence plots
- **Comprehensive testing**: Test suite with multiple test cases

## Files

- `ant_colony_optimization_tsp.py` - Main ACO implementation
- `test_aco_tsp.py` - Test suite
- `REPORT.md` - Detailed report with algorithm explanation and results
- `requirements.txt` - Python dependencies
- `aco_solution_*.png` - Generated solution visualizations
- `aco_convergence_*.png` - Generated convergence plots

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yash777AI/AI-in-healthcare.git
cd AI-in-healthcare
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the main demonstration:
```bash
python ant_colony_optimization_tsp.py
```

This will:
- Run ACO on three problem sizes (N=8, 15, 20)
- Verify solutions using brute-force/DP
- Generate visualizations
- Display results and statistics

### Run tests:
```bash
python test_aco_tsp.py
```

### Use in your own code:

```python
from ant_colony_optimization_tsp import AntColonyOptimization, generate_random_cities

# Generate a random TSP instance with 10 cities
cities, distances = generate_random_cities(n=10, max_coord=100)

# Create ACO solver with custom hyperparameters
aco = AntColonyOptimization(
    distances,
    T=100,      # iterations
    rho=0.5,    # evaporation rate
    m=10,       # number of ants
    Q=100,      # pheromone deposit factor
    alpha=1,    # pheromone importance
    beta=2      # heuristic importance
)

# Run optimization
best_path, best_distance, history = aco.optimize(verbose=True)

print(f"Best path: {best_path}")
print(f"Best distance: {best_distance:.2f}")
```

## Algorithm Details

### Ant Colony Optimization

The ACO algorithm simulates ant foraging behavior:

1. **Initialize** pheromone trails
2. **For each iteration**:
   - Each ant constructs a solution using stochastic sampling
   - Update pheromone trails based on solution quality
3. **Return** best solution found

### Stochastic Path Sampling

Probability of moving from city x to city y:

```
p_xy = (τ_xy^α × η_xy^β) / Σ(τ_xz^α × η_xz^β)
```

Where:
- τ_xy = pheromone level on edge (x,y)
- η_xy = heuristic information (1/distance)
- α = pheromone importance factor
- β = heuristic importance factor

### Verification Algorithms

1. **Brute-force Backtracking** (N ≤ 10):
   - Tries all permutations
   - Guarantees optimal solution
   - Time: O(N!)

2. **Bit-mask Dynamic Programming** (N ≤ 20):
   - Uses bitmask to represent visited cities
   - State: dp[mask][city] = min cost to reach state
   - Time: O(N² × 2^N)

## Hyperparameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| T | 100 | Number of iterations |
| ρ (rho) | 0.5 | Pheromone evaporation rate |
| m | 10 | Number of ants per iteration |
| Q | 100 | Pheromone deposit scaling factor |
| α (alpha) | 1 | Pheromone importance weight |
| β (beta) | 2 | Heuristic importance weight |

## Results

Tested on random TSP instances:

| Problem Size | ACO Time | Optimal Time | ACO Error |
|--------------|----------|--------------|-----------|
| N = 8        | 0.13s    | 0.01s        | 0.00%     |
| N = 15       | 0.30s    | 0.47s        | 0.00%     |
| N = 20       | 0.44s    | 28.22s       | 3.09%     |

Key findings:
- ACO finds optimal solutions for small-medium problems
- Excellent scalability compared to exact methods
- Near-optimal solutions with significant speedup for larger problems

## Visualizations

The implementation generates:
1. **Solution plots**: Shows cities and optimal tour
2. **Convergence plots**: Shows best distance over iterations

Example visualizations are included in the repository.

## Testing

The test suite (`test_aco_tsp.py`) includes:
- Basic ACO functionality
- Brute-force solver correctness
- DP solver correctness
- ACO vs optimal solution comparison
- Probability calculation validation
- Pheromone update mechanism
- Random city generation

Run tests with:
```bash
python test_aco_tsp.py
```

## References

1. Dorigo, M., & Stützle, T. (2004). *Ant Colony Optimization*. MIT Press.
2. Dorigo, M., & Gambardella, L. M. (1997). Ant colony system: a cooperative learning approach to the traveling salesman problem. *IEEE Transactions on Evolutionary Computation*.

## License

This is an academic project for educational purposes.

## Author

Homework 6 - Artificial Intelligence Course  
Prof. Truong-Son Hy  
Due: October 30, 2025
