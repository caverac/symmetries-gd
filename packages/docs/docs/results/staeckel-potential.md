---
sidebar_position: 1
---

# Action stability during migration

The [algebraic framework](../concepts/lie-groups) predicts that the vertical action $J_z$ -- as the deformed Casimir of the $\mathfrak{so}(3) \to \mathfrak{so}(2)$ symmetry breaking -- should be conserved during bar-driven radial migration, even as the radial action $J_R$ changes dramatically. This page presents the numerical evidence.

## The key result

<figure className="scientific scientific--narrow">
  <img
    src="/img/action-scatter.png"
    alt="Action stability scatter plot"
  />
  <figcaption>
    <strong>Figure 1.</strong> Normalized action variability $\sigma(J) / |L_{z,0}|$
    for $J_z$ (vertical axis) versus $J_R$ (horizontal axis), for each particle
    in the simulation. Points are grouped by initial guiding radius $R_{{g,0}}$.
    Outer-disk particles cluster along the horizontal axis: $\sigma(J_R) / |L_{z,0}|$
    reaches $\sim$0.5, while $\sigma(J_z) / |L_{z,0}|$ remains near zero.
  </figcaption>
</figure>

The median values across the full ensemble (2000 particles):

| Quantity                    | Median value         |
| --------------------------- | -------------------- |
| $\sigma(J_z) / \|L_{z,0}\|$ | $1.7 \times 10^{-3}$ |
| $\sigma(J_R) / \|L_{z,0}\|$ | $8.6 \times 10^{-2}$ |
| Ratio                       | $2.0 \times 10^{-2}$ |

**Across the full ensemble, $J_z$ is conserved $\sim$50 times better than $J_R$.** The protection is strongly radially dependent: for outer-disk particles ($R_g > 7$ kpc), the ratio drops to $4.6 \times 10^{-4}$, meaning $J_z$ is conserved **$\sim$2200 times** better than $J_R$. In the inner disk ($R_g < 3$ kpc), where the bar dominates and the Staeckel deformation parameter $\Delta$ is small, the protection is weaker ($\sim$2x).

This radial dependence is consistent with the algebraic framework: the deformed Casimir $J_z$ is defined in coordinates set by $\Delta(R)$, and the protection is strongest where $\Delta$ is large -- i.e., in the outer disk where flattening dominates. The most strongly migrated particles ($|\Delta R_g| \sim 4\text{--}9$ kpc) still show $\sigma(J_z) \approx 0$, confirming that the bar perturbation acts within $SO(2)$ and cannot change the deformed Casimir in the regime where the deformation is significant.

## Migration driven by the bar

<figure className="scientific scientific--narrow">
  <img
    src="/img/migration-scatter.png"
    alt="Migration scatter plot"
  />
  <figcaption>
    <strong>Figure 2.</strong> Fractional change in guiding radius
    $\ln(R_g / R_{{g,0}})$ versus initial guiding radius. The dashed
    line marks the bar's corotation radius $R_{{\mathrm{{CR}}}} \approx 5.5$ kpc.
    Particles near corotation undergo the strongest migration, with
    $\ln(R_g / R_{{g,0}})$ reaching $-6$ for inward scattering. The bar
    drives substantial radial reshuffling across the entire disk.
  </figcaption>
</figure>

## Staeckel convergence

galpy's `actionAngleStaeckel` returns a sentinel value (9999.99) when the Staeckel fudge fails to converge. In our simulation, **zero convergence failures** occurred for either $J_z$ or $J_R$ across all 2000 particles and 50 snapshots. The action computation uses the median of the analytically-derived $\Delta(R)$ from the Miyamoto-Nagai separability condition, which provides a well-matched focal distance for the entire disk.

## Limitations

The simulation uses a smooth, collisionless potential. In realistic galaxies, giant molecular clouds and other dense gas structures provide an additional source of vertical scattering that operates outside the $SO(2)$ subalgebra. Recent work using MHD simulations with gas dynamics found that GMC scattering can drive vertical action evolution on timescales comparable to or shorter than radial action evolution ([Arora et al. 2025](https://doi.org/10.1093/mnras/stae2707)). The algebraic protection demonstrated here applies specifically to planar perturbations -- the bar being the primary example -- and does not preclude vertical heating from non-planar sources.

## Simulation details

- **Potential**: Hernquist bulge ($a_b = 0.5$ kpc) + Miyamoto-Nagai disk ($a_d = 3$ kpc, $b_d = 0.28$ kpc) + NFW halo ($a_h = 16$ kpc) + Dehnen bar ($r_b = 4$ kpc, $\Omega_b = 40$ km/s/kpc)
- **Bar growth**: 0 to full strength over $\sim$1 Gyr
- **Note on bar parameters**: Gaia-era measurements place the present-day MW bar pattern speed at $\sim$33--41 km/s/kpc ([see model details](../concepts/connection#the-galactic-model)). Our $\Omega_b = 40$ km/s/kpc is within this range.
- **Integration time**: $\sim$10 Gyr (approximately one Hubble time)
- **Particles**: 2000 (1000 center + 1000 disk population)
- **Snapshots**: 50 evenly spaced
- **Actions**: computed via `actionAngleStaeckel` with $\Delta$ set to the median of the analytically-derived $\Delta(R)$ from the Miyamoto-Nagai separability condition

## Reproducing the figures

```bash
# Run the simulation
uv run experiments simulate --name mw --n-particles 1000 --force

# Generate the figures
uv run experiments action-scatter --name mw
uv run experiments migration-scatter --name mw
```
