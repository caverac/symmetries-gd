---
slug: /
sidebar_position: 1
---

# Introduction

## The observation

Stars in disk galaxies migrate radially. A rotating galactic bar exerts torques at corotation resonance, scattering stars inward and outward across the disk ([Sellwood & Binney 2002](https://doi.org/10.1046/j.1365-8711.2002.05806.x)). This process breaks the axial symmetry of the potential, causing large changes in the radial action $J_R$ and angular momentum $L_z$.

Yet the **vertical action** $J_z$ -- the amplitude of a star's oscillation above and below the disk plane -- remains nearly unchanged. This has been demonstrated repeatedly in $N$-body simulations: [Solway, Sellwood & Schoenrich (2012)](https://doi.org/10.1111/j.1365-2966.2012.21608.x) showed that churning preserves vertical action; [Minchev et al. (2012)](https://doi.org/10.1051/0004-6361/201220189) distinguished churning (which conserves $J_z$) from blurring (which heats vertically); and [Vera-Ciro, D'Onghia & Navarro (2016)](https://arxiv.org/abs/1605.03575) showed that migrated stars retain the vertical structure of their birth radius.

The numerical evidence is robust. But **why** is $J_z$ conserved, and how should we define it as a star migrates through a changing potential?

## The argument

This project provides a geometric and algebraic framework for understanding $J_z$ conservation.

The standard explanation for $J_z$ conservation is **adiabatic invariance**: the vertical oscillation frequency $\nu_z$ is much higher than the frequencies associated with the bar perturbation ($\nu_z \gg \Omega$). This separation of timescales protects the action as long as the potential changes slowly.

However, a migrating star moves from the inner galaxy (nearly spherical) to the outer disk (highly flattened). To compare $J_z$ across these regimes, we need a coordinate-independent definition. Using the theory of **Lie algebra deformations**, we show that:

1. The transition from a spherical bulge to a flattened disk corresponds to a symmetry breaking **$\mathfrak{so}(3) \to \mathfrak{so}(2)$**.
2. The Staeckel third integral $I_3$ is the **deformed Casimir** of this transition.
3. The vertical action $J_z$, computed in confocal ellipsoidal coordinates, is the gauge-invariant quantity that "parallel transports" correctly during migration.

The key point: $J_z$ is conserved because it is an adiabatic invariant of a planar perturbation that respects the disk plane, and the algebraic framework provides the **geometric connection** to measure it accurately across the entire disk.

## The evidence

In a Milky-Way-like potential, we integrated 2000 stellar orbits over a Hubble time while a bar drives radial migration.

$$
\frac{\sigma(J_z)}{|L_{z,0}|} \sim 10^{-3}, \qquad \frac{\sigma(J_R)}{|L_{z,0}|} \sim 10^{-1}
$$

Across the full ensemble, $J_z$ varies **$\sim$50 times less** than $J_R$. The conservation is radially dependent: in the outer disk, where the vertical frequency is highest and the Staeckel approximation is most accurate, $J_z$ is conserved more than **2000 times** better than $J_R$.

## How this site is organized

- **[Concepts](concepts/lie-groups)** -- The mathematical framework: Lie group symmetries, algebraic deformations, and the [fiber-bundle reinterpretation](concepts/reinterpreting-delta) of $\Delta(R)$.
- **[Results](results/staeckel-potential)** -- Experimental evidence: potential profiles, migration diagnostics, and action stability measurements.
