---
sidebar_position: 4
---

# Reinterpreting the Staeckel connection

The [algebraic framework](lie-groups) identifies the vertical action $J_z$ as the **deformed Casimir** of the galactic symmetry breaking. This page reinterprets the Staeckel focal distance $\Delta(R)$ not just as a fitting parameter, but as a **connection** on a fiber bundle that governs the transport of actions across the disk.

## The Galactic Fiber Bundle

Consider the phase space of a star as a fiber bundle $\pi: P \to \mathcal{M}$, where the base manifold $\mathcal{M}$ is the radial coordinate $R$ of the disk. Each fiber $\pi^{-1}(R)$ is the local phase space available to a star at that radius.

As a star migrates from $R_1$ to $R_2$, it must transition between fibers. However, the symmetry of the fibers changes with radius:

- **Inner fibers** are nearly spherical (Casimir $L^2$).
- **Outer fibers** are highly flattened (Casimir $J_z$).

## $\Delta(R)$ as a Connection

To compare actions between fibers, we need a **connection** -- a rule for how the action's coordinate system deforms during transport. The Staeckel focal distance $\Delta(R)$ provides exactly this rule.

When a star migrates to $R + dR$, the connection $\Delta(R)$ determines how the confocal coordinates $(\lambda, \nu)$ and their momenta transform. $J_z$ is the quantity that is **parallel-transported** by this connection.

The statement that $J_z$ is conserved during migration is equivalent to saying that $J_z$ is the **gauge-invariant observable** of this bundle: it is the quantity that does not depend on the local choice of coordinates (the specific confocal system at each $R$) and is preserved under transport.

## Physical Breakdown vs. Coordinate Breakdown

This geometric picture clarifies why $J_z$ is conserved while $J_R$ is not:

1. **$J_R$ Breakdown:** The bar breaks the axial symmetry of the potential. This is a **physical breakdown**: the torques exert work on the radial degree of freedom, changing the action value directly.
2. **$J_z$ Conservation:** The bar is planar and respect the disk's midplane. The vertical motion remains an **adiabatic invariant**. The algebraic framework ensures that we are measuring the _same_ invariant even as its coordinate representation deforms through $\Delta(R)$.

The "Fundamental Problem" addressed by this project is not how the bar avoids torquing $J_z$ (which is adiabaticity), but how $J_z$ maintains its identity as a conserved quantity across a disk where the underlying potential symmetry is non-uniform.

## Comparison of Frameworks

| Concept      | Standard Interpretation            | Fiber-Bundle Interpretation               |
| :----------- | :--------------------------------- | :---------------------------------------- |
| $\Delta$     | Fitting parameter for the fudge    | Connection on the galactic bundle         |
| $J_z$        | Adiabatic invariant of 1D osc.     | Deformed Casimir parallel-transported     |
| Migration    | Resonant scattering in phase space | Transport across fibers of the bundle     |
| Conservation | Separation of timescales           | Geometric invariance under the connection |

The fiber-bundle picture also clarifies _when_ this protection should fail:

1. **Non-planar perturbations.** GMC scattering or satellite impacts act "outside the bundle," exerting direct vertical torques that break the adiabaticity.
2. **Singular Connections.** If $\Delta(R)$ had a discontinuity, the parallel transport would fail, and $J_z$ would jump even under a planar perturbation.
