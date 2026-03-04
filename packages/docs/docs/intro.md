---
slug: /
sidebar_position: 1
---

# Introduction

This project investigates a simple but provocative question: **is orbital chaos in galaxies an illusion of the wrong coordinate system?**

## The problem

Stars in disk galaxies migrate radially. A rotating galactic bar scatters stars outward from the dense inner bulge into the extended disk, crossing regions where the gravitational potential changes character -- from Keplerian ($V \propto -1/r$) near the central black hole to harmonic ($V \propto r^2$) in the bulge to flattened disk dynamics further out.

Traditional galactic dynamics tracks orbits with **action-angle variables** $(J_R, J_\phi, J_z)$. These are powerful in integrable systems, but when a star migrates between gravitational regimes, the actions exhibit large, seemingly chaotic variance. The standard conclusion: integrability breaks down and the orbit becomes chaotic.

## The hypothesis

We propose an alternative: the integrability is never truly broken -- it undergoes a **continuous algebraic transformation**. What looks like chaos is an artifact of using a fixed coordinate framework to describe a system whose underlying symmetry is deforming.

The mathematical backbone is the transition between two Lie algebras:

- $\mathfrak{so}(4)$: the symmetry of the Kepler problem (conserves the Laplace-Runge-Lenz vector)
- $\mathfrak{su}(3)$: the symmetry of the isotropic harmonic oscillator (conserves the Fradkin tensor)

By constructing an invariant $C_2$ that tracks this deformation, we aim to find a quantity that remains stable even as $J_R$ fluctuates wildly.

## What we found

The algebraic approach -- interpolating directly between the two Casimir operators -- [failed in the transition region](results/staeckel-potential). But the failure pointed toward a deeper geometric insight: the deformation parameter of the Lie algebra is exactly the **focal distance of ellipsoidal coordinates**.

This led to the **Osculating Casimir**:

$$
C_2(r) = L^2 + \Delta(r)^2\, p_z^2
$$

where $\Delta(r)$ is a [dynamic focal distance](results/variable-delta) that adapts to the local symmetry of the potential. In disk migration experiments, $C_2$ is [87 times more stable](results/measuring-results) than the traditional radial action $J_R$.

## How this site is organized

- **[Concepts](concepts/lie-groups)** -- The mathematical framework: Lie group symmetries, action-angle variables, and how they connect through the interpolation tensor.
- **[Results](results/staeckel-potential)** -- What happened: the algebraic failure, the geometric breakthrough, and the experimental evidence.
