---
slug: /
sidebar_position: 1
---

# Introduction

## The observation

Stars in disk galaxies migrate radially. A rotating galactic bar exerts torques at corotation resonance, scattering stars inward and outward across the disk ([Sellwood & Binney 2002](https://doi.org/10.1046/j.1365-8711.2002.05806.x)). During this process, the radial action $J_R$ changes dramatically -- the radial orbit is reshuffled by the bar perturbation.

Yet the **vertical action** $J_z$ -- the amplitude of a star's oscillation above and below the disk plane -- remains nearly unchanged. This has been demonstrated repeatedly in $N$-body simulations: [Solway, Sellwood & Schoenrich (2012)](https://doi.org/10.1111/j.1365-2966.2012.21608.x) showed that churning preserves vertical action; [Minchev et al. (2012)](https://doi.org/10.1051/0004-6361/201220189) distinguished churning (which conserves $J_z$) from blurring (which heats vertically); and [Vera-Ciro, D'Onghia & Navarro (2016)](https://arxiv.org/abs/1605.03575) showed that migrated stars retain the vertical structure of their birth radius, creating a "provenance bias" in the disk. More recent $N$-body studies have refined the picture: [Mikkola, McMillan & Hobbs (2020)](https://doi.org/10.1093/mnras/staa364) confirmed that $J_z$ is conserved on average during churning, though individual particles show scatter; and [Frankel et al. (2020)](https://doi.org/10.3847/1538-4357/ab910c) showed observationally that the Milky Way disk undergoes substantial migration with remarkably little heating, consistent with approximate $J_z$ conservation.

The numerical evidence is robust. But **why** is $J_z$ conserved? The standard answer -- **adiabatic invariance**, the argument that the bar changes on timescales much longer than the vertical oscillation period ([Binney & Tremaine 2008](https://press.princeton.edu/books/paperback/9780691130279/galactic-dynamics)) -- is an approximation that breaks down for strong perturbations ([Vera-Ciro & D'Onghia 2016](https://doi.org/10.3847/0004-637X/824/1/39)). It doesn't explain _which_ property of $J_z$ protects it, or why the same protection doesn't extend to $J_R$.

## The argument

This project proposes an algebraic answer.

The gravitational potential of a galaxy has a layered symmetry. The spherical bulge is invariant under all rotations -- its symmetry group is $SO(3)$, and the conserved quantity is the total angular momentum $L^2$. The flattened disk breaks this to $SO(2)$: only the vertical component $L_z$ survives as an exact integral.

In the theory of Lie algebra deformations, when a symmetry is broken the Casimir invariant of the original algebra does not simply vanish -- it **deforms** into a new invariant of the reduced algebra. The deformation is governed by a parameter that encodes the geometry of the symmetry breaking.

For the $\mathfrak{so}(3) \to \mathfrak{so}(2)$ breaking by disk flattening, this parameter is the **Staeckel focal distance** $\Delta(R)$ -- a geometric property of the gravitational potential that measures its departure from spherical symmetry. In a Staeckel potential, the Hamilton-Jacobi equation separates in confocal ellipsoidal coordinates parameterized by $\Delta$, yielding a third integral $I_3$ that reduces to $L^2$ in the spherical limit. We [identify $I_3$](concepts/lie-groups#identifying-the-deformed-casimir) as the deformed Casimir of the broken algebra, and the **vertical action**

$$
J_z = \frac{1}{2\pi} \oint p_\nu\, d\nu
$$

computed in those confocal coordinates, inherits its conservation.

The key point: **if this identification holds, $J_z$ is conserved because it descends from a Casimir invariant of the deformed algebra, not merely from adiabatic invariance.** A bar perturbation acts within the disk plane -- it generates torques that change $L_z$ and reshuffle radial orbits, but these are operations _within_ $SO(2)$. The Casimir of the deformed algebra commutes with all generators, including planar perturbations. This is why the bar changes $J_R$ and $L_z$ freely but cannot touch $J_z$.

## The evidence

In a Milky-Way-like potential (Hernquist bulge + Miyamoto-Nagai disk + NFW halo + Dehnen bar), we integrated 2000 stellar orbits over a Hubble time while the bar grows and drives radial migration. Measuring temporal variability via the standard deviation normalized by the initial angular momentum $|L_{z,0}|$:

$$
\frac{\sigma(J_z)}{|L_{z,0}|} \sim 10^{-3}, \qquad \frac{\sigma(J_R)}{|L_{z,0}|} \sim 10^{-1}
$$

Across the full ensemble, the vertical action varies **$\sim$50 times less** than the radial action. The protection is radially dependent: in the outer disk ($R_g > 7$ kpc), where the Staeckel deformation is largest, $J_z$ is conserved more than **2000 times** better than $J_R$. Even for stars that migrate by $\Delta R_g \sim 4\text{--}9$ kpc, $J_z$ remains essentially constant. This is consistent with the $N$-body results cited above, and the algebraic framework explains why.

A caveat: this result holds for collisionless dynamics in a smooth potential. In simulations that include gas and giant molecular clouds, gravitational scattering off dense structures can drive vertical action evolution through a separate, non-planar channel ([Arora et al. 2025](https://doi.org/10.1093/mnras/stae2707)). The algebraic protection applies specifically to perturbations within $SO(2)$ -- the bar is one, but GMC scattering is not.

## How this site is organized

- **[Concepts](concepts/lie-groups)** -- The mathematical framework: Lie group symmetries, algebraic deformations, the Staeckel connection, and the [fiber-bundle reinterpretation](concepts/reinterpreting-delta) of $\Delta(R)$.
- **[Results](results/staeckel-potential)** -- Experimental evidence: potential profiles, migration diagnostics, and action stability measurements.
