# Symmetries-GD: Algebraic Protection of Vertical Action in Disk Galaxies

Why is the vertical action $J_z$ conserved during bar-driven radial migration, even as the radial action $J_R$ changes dramatically? This project proposes and tests an algebraic answer based on Lie algebra deformations.

## The argument

A galaxy's gravitational potential has layered symmetry. The spherical bulge has $SO(3)$ symmetry (conserved $L^2$); the flattened disk breaks this to $SO(2)$ (only $L_z$ survives). In the theory of Lie algebra deformations, the Casimir invariant of the original algebra does not vanish under symmetry breaking -- it **deforms** into a new invariant of the reduced algebra.

For the $\mathfrak{so}(3) \to \mathfrak{so}(2)$ breaking, the deformation parameter is the **Staeckel focal distance** $\Delta(R)$, which measures the potential's departure from spherical symmetry. The third integral $I_3$ in Staeckel potentials is identified as the deformed Casimir, and the vertical action $J_z$ -- computed in confocal coordinates parameterized by $\Delta$ -- inherits its conservation. A bar perturbation acts within $SO(2)$ and cannot change the deformed Casimir.

## The evidence

In a Milky-Way-like potential (Hernquist bulge + Miyamoto-Nagai disk + NFW halo + Dehnen bar), we integrated 2000 stellar orbits over a Hubble time:

$$
\frac{\sigma(J_z)}{|L_{z,0}|} \sim 10^{-3}, \qquad \frac{\sigma(J_R)}{|L_{z,0}|} \sim 10^{-1}
$$

Across the full ensemble, $J_z$ varies **~50 times less** than $J_R$. In the outer disk ($R_g > 7$ kpc), where the Staeckel deformation is largest, $J_z$ is conserved **~2000 times** better than $J_R$. Even stars that migrate by $\Delta R_g \sim 4$--$9$ kpc show $\sigma(J_z) \approx 0$.

## Documentation

Full writeup with derivations, figures, and references: [symmetries-gd.vercel.app](https://symmetries-gd.vercel.app)

## Project structure

- `packages/symmetries`: Core physics library (galpy-based orbit integration, action computation, Staeckel analysis).
- `packages/experiments`: CLI tools for simulation, plotting, and analysis.
- `packages/docs`: Docusaurus site with the full writeup.
- `packages/infrastructure`: Deployment configuration.

## Quick start

```bash
# Install dependencies
uv sync

# Run a simulation
uv run experiments simulate --name mw --n-particles 1000

# Generate figures
uv run experiments action-scatter --name mw
uv run experiments migration-scatter --name mw
uv run experiments potential-plot
uv run experiments delta-plot
```
