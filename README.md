# Symmetries-GD: Dynamical Symmetry Breaking in Galaxies

This project investigates a novel mathematical framework for tracking orbital structures in migrating stars: **Parameterized Lie Algebra Deformations**.

## 1. The Idea

Traditional galactic dynamics relies on action-angle variables $(J_R, J_\phi, J_z)$, which often fail during radial migration. When a star is scattered (e.g., by a galactic bar) from the inner regions to the outer bulge, the underlying gravitational symmetry changes.

The core hypothesis was that by modeling the galaxy as a continuous deformation between two Lie algebras, we could derive a **Deformed Casimir Invariant ($C_2$)** that remains conserved even when traditional actions exhibit chaotic variance.

## 2. Theoretical Motivation

Galactic potentials possess exact symmetries at their radial extremes:

- **Inner Limit (SMBH):** A Keplerian $1/r$ potential with $SO(4)$ symmetry (conserved Laplace-Runge-Lenz vector).
- **Outer Limit (Bulge):** A Harmonic $r^2$ potential with $SU(3)$ symmetry (conserved Fradkin tensor).

We constructed a parameterized symmetry operator:
$$Q_{ij}(\lambda) = \frac{p_i p_j}{2m} + \Psi(r, \lambda) x_i x_j + \Phi(r, \lambda) \delta_{ij}$$
where $\Psi(r)$ and $\Phi(r)$ are structural functions that interpolate the force-gradient and potential-shift across the transition region.

## 3. Experimental Suite

We built a CLI-driven pipeline to test the stability of $C_2$ against traditional radial actions ($J_R$):

- **Limit Tests:** Verified $C_2$ conservation in pure Keplerian and Harmonic potentials.
- **Stress Tests:** Evaluated performance in chaotic regimes by sweeping the strength of a rotating Dehnen bar.
- **Convergence Tests:** Checked for adiabatic invariance by varying the formation time of the galactic bar.

## 4. Why It Fails

Despite the mathematical elegance, the empirical data forced a **NO-GO** recommendation:

1. **The Transition Floor:** In the composite potential, $C_2$ exhibits a variance floor of $\sim 10^{-8}$. This is 4--5 orders of magnitude less stable than traditional actions ($\sim 10^{-12}$).
2. **Lack of Adiabaticity:** Slower migration (more adiabatic transitions) did not improve $C_2$ stability, indicating it is not a robust invariant during the radial "jump" between symmetries.
3. **Non-Integrability:** The intermediate region between $1/r$ and $r^2$ does not possess a closed-form symmetry group. Simple parameterized structural functions are insufficient to capture the broken integrability of a real galactic potential.

## 5. Takeaways

- **Limits are Easy, Transitions are Hard:** Proving conservation in pure $SO(4)$ or $SU(3)$ cases is trivial; the project failed because the deformation path does not preserve the symplectic structure of the orbits.
- **Traditional Actions are Resilient:** Even in migrating systems, traditional $J_R$ (calculated via Staeckel approximation) is remarkably stable compared to experimental "algebraic" alternatives.
- **Future Directions:** A viable alternative would likely require non-linear Lie algebras or numerical basis functions rather than the analytical "parameterized" approach explored here.

---

### Project Structure

- `packages/symmetries`: Core tensor algebra and invariant logic.
- `packages/experiments`: CLI tools for simulation and variance analysis.
- `notebooks/notes/logs`: Detailed research logs and evaluation history.
