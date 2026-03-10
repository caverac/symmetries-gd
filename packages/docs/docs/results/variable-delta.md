---
sidebar_position: 2
---

# Migration traces

The [action scatter plot](staeckel-potential) showed that $J_z$ is conserved across the entire particle ensemble. This page follows **individual stars** through time, making the conservation visible as a direct time series.

## Three representative orbits

<figure className="scientific scientific--narrow">
  <img
    src="/img/migration-traces.png"
    alt="Time traces of guiding radius, vertical action, and radial action for three particles"
  />
  <figcaption>
    <strong>Figure 1.</strong> Time evolution of $R_g$, $J_z$, and $J_R$ for three
    representative particles: a non-migrating star (black), an outward migrator (red),
    and an inward migrator (blue). The bar grows to full strength over the first
    $\sim$1 Gyr and drives migration through corotation resonance.
  </figcaption>
</figure>

The three panels tell the story of bar-driven migration at the level of a single orbit:

- **Top panel ($R_g$).** The guiding radius tracks how far each star migrates. The outward migrator gains several kpc; the inward migrator loses a comparable amount. The non-migrating star stays near its birth radius throughout.

- **Middle panel ($J_z$).** The vertical action remains flat for all three particles, regardless of whether and how far they migrate. This is the signature of a conserved quantity -- the deformed Casimir of the $\mathfrak{so}(3) \to \mathfrak{so}(2)$ symmetry breaking.

- **Bottom panel ($J_R$).** The radial action fluctuates strongly once the bar reaches full strength. The bar perturbation pumps energy into the radial degree of freedom, and $J_R$ tracks this pumping in real time.

The contrast between the middle and bottom panels is the central result: the bar acts within $SO(2)$ and drives large changes in $J_R$, but the Casimir $J_z$ is algebraically immune to planar perturbations. This holds not just on average (as shown in the [ensemble scatter](staeckel-potential)), but snapshot by snapshot for each individual orbit.

## The role of $\Delta(R)$

A migrating star crosses regions with different local geometry. In the [concepts section](../concepts/connection#why-deltar-and-not-a-constant) we showed that the Staeckel focal distance $\Delta(R)$ -- the deformation parameter -- varies smoothly from $\sim$3 kpc in the inner galaxy to $\sim$8 kpc at $R \sim 10$ kpc. Yet $J_z$ remains constant throughout.

This is not a coincidence. The continuity of $\Delta(R)$ ensures that the deformed Casimir adapts smoothly to the local symmetry as the star moves outward or inward. If $\Delta(R)$ had a discontinuity -- a sudden jump in the local coordinate geometry -- $J_z$ would not be preserved across it. The smooth variation of $\Delta(R)$ is what makes global $J_z$ conservation possible even when the local symmetry changes from nearly spherical ($SO(3)$) to strongly flattened ($SO(2)$). This smooth adaptation also explains why the Staeckel fudge converges reliably for $J_z$ across all particles and snapshots ([Sanders & Binney 2016](https://doi.org/10.1093/mnras/stw075)).
