# Ant Colony Optimization for Travelling Salesman Problem
## Homework 6 Report
**Course:** Artificial Intelligence  
**Professor:** Truong-Son Hy  
**Due Date:** October 30, 2025

---

## 1. Algorithm Overview

This report presents an implementation of Ant Colony Optimization (ACO) for solving the Travelling Salesman Problem (TSP). The implementation includes:

1. **Ant Colony Optimization (ACO)** - Main metaheuristic algorithm
2. **Stochastic Path Sampling** - Probabilistic city selection based on pheromone and heuristic information
3. **Brute-force Backtracking** - Verification for N ≤ 10
4. **Bit-mask Dynamic Programming** - Verification for N ≤ 20
5. **Visualization** - Graphical representation of solutions and convergence

---

## 2. Implementation Details

### 2.1 Core ACO Algorithm

The ACO algorithm simulates the foraging behavior of ants to find optimal paths. The key components are:

#### Pheromone Matrix (τ)
- Initialized with small positive values (0.1)
- Updated after each iteration based on ant solutions
- Evaporates over time according to evaporation rate ρ

#### Heuristic Information (η)
- Calculated as the inverse of distance: η_xy = 1 / d_xy
- Represents the desirability of moving from city x to city y
- Higher values indicate shorter distances (more desirable)

### 2.2 Stochastic Path Sampling

The probability of an ant moving from city x to city y is calculated using:

```
p_xy = (τ_xy^α × η_xy^β) / Σ(τ_xz^α × η_xz^β)
```

where:
- τ_xy: pheromone level on edge (x, y)
- η_xy: heuristic information (inverse distance)
- α: pheromone importance factor
- β: heuristic importance factor
- Sum is over all unvisited cities z

**Implementation approach:**
1. For each unvisited city, calculate the numerator: τ_xy^α × η_xy^β
2. Sum all numerators to get the denominator
3. Normalize to create a probability distribution
4. Use `np.random.choice()` to sample the next city based on these probabilities

This stochastic selection balances between:
- **Exploitation**: Following strong pheromone trails (high τ)
- **Exploration**: Trying shorter edges (high η)

### 2.3 Pheromone Update

After all ants construct their solutions:

1. **Evaporation**: τ_xy ← (1 - ρ) × τ_xy for all edges
2. **Deposit**: For each ant k with tour length L_k:
   - Δτ_xy^k = Q / L_k
   - τ_xy ← τ_xy + Δτ_xy^k for all edges in the ant's tour

Better solutions (shorter tours) deposit more pheromone, reinforcing good paths.

### 2.4 Verification Algorithms

#### Brute-force Backtracking (N ≤ 10)
- Generates all possible permutations of cities
- Calculates the total distance for each permutation
- Returns the permutation with minimum distance
- Time complexity: O(N!)
- Used for small problems to verify ACO finds optimal solutions

#### Bit-mask Dynamic Programming (N ≤ 20)
- State: `dp[mask][i]` = minimum cost to visit cities in mask ending at city i
- Mask: binary representation of visited cities
- Transitions: Try extending to unvisited cities
- Reconstructs path using parent pointers
- Time complexity: O(N² × 2^N)
- Space complexity: O(N × 2^N)
- Efficient for medium-sized problems

---

## 3. Hyperparameters

The following hyperparameters were chosen based on literature and empirical testing:

| Parameter | Symbol | Value | Description |
|-----------|--------|-------|-------------|
| Iterations | T | 100 | Number of ACO iterations |
| Evaporation Rate | ρ | 0.5 | Pheromone evaporation (0 < ρ < 1) |
| Number of Ants | m | 10 | Ants per iteration |
| Pheromone Deposit | Q | 100 | Scaling factor for pheromone deposit |
| Epsilon | ε | 1×10⁻¹⁰ | Small constant for numerical stability |
| Pheromone Importance | α | 1 | Weight of pheromone in probability |
| Heuristic Importance | β | 2 | Weight of distance in probability |

**Rationale:**
- **α = 1, β = 2**: Gives more weight to heuristic information (distance), helping early convergence
- **ρ = 0.5**: Moderate evaporation prevents premature convergence while allowing learning
- **m = 10**: Sufficient exploration with reasonable computational cost
- **T = 100**: Enough iterations for convergence on test problems

---

## 4. Experimental Results

### 4.1 Test Case 1: Small Problem (N = 8 cities)

**ACO Results:**
- Best Distance: 277.23
- Execution Time: 0.1286 seconds
- Path: [3, 5, 0, 4, 1, 6, 7, 2]

**Brute-force Verification:**
- Optimal Distance: 277.23
- Execution Time: 0.0112 seconds
- Path: [0, 5, 3, 2, 7, 6, 1, 4]

**Analysis:**
- ACO found the optimal solution (0.00% error)
- Different path representation (different starting city) but same tour
- ACO took longer but scales better for larger problems

### 4.2 Test Case 2: Medium Problem (N = 15 cities)

**ACO Results:**
- Best Distance: 320.53
- Execution Time: 0.2959 seconds
- Path: [6, 10, 14, 9, 2, 7, 11, 8, 13, 3, 5, 0, 12, 4, 1]

**DP Verification:**
- Optimal Distance: 320.53
- Execution Time: 0.4733 seconds
- Path: [0, 5, 3, 13, 8, 11, 7, 2, 9, 14, 10, 6, 1, 4, 12]

**Analysis:**
- ACO found the optimal solution (0.00% error)
- ACO was faster than DP
- Shows ACO's effectiveness for medium-sized problems

### 4.3 Test Case 3: Large Problem (N = 20 cities)

**ACO Results:**
- Best Distance: 398.38
- Execution Time: 0.4429 seconds
- Path: [17, 4, 12, 0, 5, 16, 3, 13, 8, 11, 9, 18, 2, 7, 14, 10, 15, 6, 19, 1]

**DP Verification:**
- Optimal Distance: 386.43
- Execution Time: 28.2181 seconds
- Path: [0, 16, 5, 3, 13, 8, 11, 7, 2, 18, 9, 15, 10, 14, 6, 19, 1, 17, 4, 12]

**Analysis:**
- ACO found a near-optimal solution with 3.09% error
- ACO was 63× faster than DP (0.44s vs 28.2s)
- Trade-off: Slight optimality loss for significant speed gain
- As problem size increases, the speed advantage becomes more pronounced

---

## 5. Convergence Analysis

The convergence plots show:

1. **N = 8**: Fast convergence within first 20 iterations, then plateaus
2. **N = 15**: Gradual improvement over 80 iterations before stabilizing
3. **N = 20**: Multiple improvements throughout execution, showing continued exploration

Key observations:
- Larger problems require more iterations for convergence
- Pheromone trails effectively guide search toward good solutions
- Balance between exploration and exploitation is maintained

---

## 6. Visualization

The implementation generates two types of visualizations for each test case:

1. **Solution Path**: Shows cities and the tour found by ACO
   - Red dots: Cities with labels
   - Blue lines: Path edges
   - Total distance displayed

2. **Convergence Plot**: Shows best distance over iterations
   - X-axis: Iteration number
   - Y-axis: Best distance found so far
   - Demonstrates algorithm improvement over time

See generated images:
- `aco_solution_8_cities.png`, `aco_convergence_8_cities.png`
- `aco_solution_15_cities.png`, `aco_convergence_15_cities.png`
- `aco_solution_20_cities.png`, `aco_convergence_20_cities.png`

---

## 7. Comparison: ACO vs. Exact Methods

| Problem Size | ACO Time | Exact Time | ACO Error | Speed-up |
|--------------|----------|------------|-----------|----------|
| N = 8        | 0.13s    | 0.01s      | 0.00%     | 0.09×    |
| N = 15       | 0.30s    | 0.47s      | 0.00%     | 1.59×    |
| N = 20       | 0.44s    | 28.22s     | 3.09%     | 63.78×   |

**Conclusions:**
- ACO is slower for very small problems (overhead of iterations)
- ACO becomes competitive at N = 15
- ACO shows dramatic speed advantages for N = 20
- ACO provides good approximations when exact methods become impractical

---

## 8. Strengths and Limitations

### Strengths:
1. ✓ Finds optimal or near-optimal solutions efficiently
2. ✓ Scales well to larger problem sizes
3. ✓ Naturally parallelizable (multiple ants)
4. ✓ Balance between exploration and exploitation
5. ✓ Verified against exact algorithms for correctness

### Limitations:
1. ✗ Requires hyperparameter tuning
2. ✗ Stochastic nature means results vary between runs
3. ✗ May converge to local optima for very large problems
4. ✗ More complex than simple heuristics (e.g., nearest neighbor)

---

## 9. Conclusion

This implementation successfully demonstrates Ant Colony Optimization for TSP with:

- Complete ACO algorithm with proper pheromone management
- Detailed implementation of stochastic path sampling based on p_xy
- Verification using both brute-force (N ≤ 10) and DP (N ≤ 20)
- Comprehensive visualization of solutions and convergence
- Empirical validation showing ACO effectiveness

The results show that ACO is a powerful metaheuristic for TSP:
- Finds optimal solutions for small to medium problems
- Provides high-quality approximations for larger problems
- Offers excellent scalability compared to exact methods
- Demonstrates the effectiveness of bio-inspired algorithms

---

## 10. Files Included

1. `ant_colony_optimization_tsp.py` - Main implementation
2. `requirements.txt` - Python dependencies
3. `REPORT.md` - This report
4. `aco_solution_*.png` - Solution visualizations (3 files)
5. `aco_convergence_*.png` - Convergence plots (3 files)

---

## References

1. Dorigo, M., & Stützle, T. (2004). *Ant Colony Optimization*. MIT Press.
2. Dorigo, M., & Gambardella, L. M. (1997). Ant colony system: a cooperative learning approach to the traveling salesman problem. *IEEE Transactions on Evolutionary Computation*.
3. Course lecture notes by Prof. Truong-Son Hy
