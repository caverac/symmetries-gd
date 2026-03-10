---
sidebar_position: 1
---

# Action stability during migration

The vertical action $J_z$ is robustly conserved during radial migration, even as the radial action $J_R$ and angular momentum $L_z$ change dramatically. This page presents the numerical evidence for this conservation and explains its radial dependence.

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

**Across the full ensemble, $J_z$ is conserved $\sim$50 times better than $J_R$.**

## Radial Dependence of Conservation

The protection of $J_z$ is strongly radially dependent. For outer-disk particles ($R_g > 7$ kpc), the ratio drops to $4.6 \times 10^{-4}$, meaning $J_z$ is conserved **$\sim$2200 times** better than $J_R$. In the inner disk ($R_g < 3$ kpc), where the potential is nearly spherical and the bar is most non-axisymmetric, the conservation is much weaker ($\sim$2x).

This radial dependence confirms the **adiabatic** nature of the conservation:

1. **Outer Disk:** The vertical oscillation frequency $\nu_z$ is much higher than the orbital frequencies. According to **adiabatic theory**, $J_z$ should be highly conserved in this regime.
2. **Inner Disk:** The potential is more spherical, frequencies are comparable, and the separation of timescales breaks down. Here, $J_z$ (which reduces to the $L^2$ Casimir) is less protected from the bar's torques.

The algebraic framework provides the **geometric context** for this result. By adapting the action definition to the local potential (via $\Delta(R)$), we ensure that the measured "vertical" action is the true adiabatic invariant of the system as the star migrates.

## Staeckel convergence

galpy's `actionAngleStaeckel` returns a sentinel value (9999.99) when the Staeckel fudge fails to converge. In our simulation, **zero convergence failures** occurred for either $J_z$ or $J_R$ across all 2000 particles and 50 snapshots. The action computation uses the median of the analytically-derived $\Delta(R)$ from the Miyamoto-Nagai separability condition, which provides a well-matched focal distance for the entire disk.

## Limitations

The simulation uses a smooth, collisionless potential. In realistic galaxies, giant molecular clouds and other dense gas structures provide a non-planar perturbation channel that operates on shorter timescales than the bar. This mechanism can drive vertical heating that bypasses the adiabatic protection. [Arora et al. (2025)](https://doi.org/10.1093/mnras/stae2707) found that in MHD simulations with gas dynamics, vertical actions evolve through GMC encounters even when planar migration is weak.
