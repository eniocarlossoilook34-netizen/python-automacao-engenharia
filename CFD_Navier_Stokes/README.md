# 2D Incompressible Navier-Stokes Solver

## Description
Implementation of a numerical solver for the unsteady Navier-Stokes equations to simulate laminar flow past a square cylinder. The project demonstrates the application of Computational Fluid Dynamics (CFD) fundamentals without reliance on commercial black-box software.

## Methodology
* **Governing Equations:** 2D Incompressible Navier-Stokes + Continuity Equation.
* **Numerical Scheme:** Finite Difference Method (FDM) on a staggered grid (Collocated arrangement adapted).
* **Algorithm:** Chorin’s Projection Method (Pressure-Correction scheme).
    1.  **Predictor Step:** Computes tentative velocity field ($u^*$) using advection-diffusion terms.
    2.  **Pressure Poisson Equation (PPE):** Solved via iterative Jacobi method to enforce $\nabla \cdot u = 0$.
    3.  **Corrector Step:** Projects velocity onto a divergence-free space using the pressure gradient.

## Key Results
The simulation successfully captures flow separation features, including the stagnation zone upstream and flow acceleration around the obstacle corners, validating the mass conservation constraint.

## Tech Stack
* Python 3.14
* NumPy (Vectorized operations)
* Matplotlib (Visualization & Animation)

## Author
Enio Oliveira - Engineering Student
