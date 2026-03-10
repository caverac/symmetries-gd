---
sidebar_position: 2
---

# Action-angle variables

Action-angle variables are the standard tool for describing orbits in integrable gravitational potentials ([Binney & Tremaine 2008, Ch. 3](https://press.princeton.edu/books/paperback/9780691130279/galactic-dynamics)). They reduce the full 6D phase space to three conserved actions and three linearly evolving angles.

## The three actions

For an axisymmetric galactic potential, the three action variables are:

| Action         | Description                                                                |
| -------------- | -------------------------------------------------------------------------- |
| $J_R$          | **Radial action** -- amplitude of radial oscillation                       |
| $J_\phi = L_z$ | **Azimuthal action** -- angular momentum about the symmetry axis           |
| $J_z$          | **Vertical action** -- amplitude of oscillation above/below the disk plane |

Each action is defined as a phase-space integral over one complete oscillation cycle:

$$
J_i = \frac{1}{2\pi} \oint p_i\, dq_i
$$

In an integrable system, the actions are exact constants of motion: a star's orbit is fully determined by its three action values, and these values never change. This makes them the natural coordinates for galactic dynamics -- the entire structure of the Milky Way's disk can be described as a distribution function $f(J_R, J_\phi, J_z)$ ([Binney 2010](https://doi.org/10.1111/j.1365-2966.2010.16734.x)).

## Why actions break down

Actions work beautifully in static, integrable potentials. The problem arises when the potential is perturbed -- for instance, by a rotating galactic bar.

A bar creates **resonances**: regions in phase space where the orbital frequencies are commensurate with the bar's pattern speed ([Sellwood & Binney 2002](https://doi.org/10.1046/j.1365-8711.2002.05806.x)). At these resonances, stars can be scattered radially -- pushed outward from the inner bulge into the disk, or vice versa. This is **radial migration**.

During migration, the radial action $J_R$ is no longer conserved. As a star crosses from one gravitational regime to another, $J_R(t)$ exhibits large fluctuations. The connection between resonance overlap and the breakdown of invariant tori was established rigorously by the KAM theorem ([Arnold 1963](https://doi.org/10.1070/RM1963v018n05ABEH004130)): when perturbations are strong enough that neighboring resonances overlap, the orbit is no longer confined to a torus in phase space and the motion becomes chaotic. In galactic dynamics, this manifests as the failure of action-based descriptions in the bar region ([Weinberg 1994](https://doi.org/10.1086/174036); [Minchev & Famaey 2010](https://doi.org/10.1088/0004-637X/722/1/112)). Recent Gaia-era work has mapped these resonances directly in action space ([Trick et al. 2021](https://doi.org/10.1093/mnras/staa2722)), and a decelerating bar sweeps its resonances outward over time, driving sustained radial migration ([Chiba & Schoenrich 2021](https://doi.org/10.1093/mnras/stab1094)).

## The alternative view

This project challenges that interpretation. Rather than concluding that all actions break down equally, we ask: **why does the bar destroy $J_R$ but leave $J_z$ untouched?**

The answer lies in the [symmetry algebra](lie-groups). The disk potential breaks the spherical $SO(3)$ symmetry down to axial $SO(2)$, and the bar perturbation acts entirely within the surviving $SO(2)$ subalgebra -- it generates planar torques that reshuffle radial orbits. The vertical action $J_z$, as the [deformed Casimir](lie-groups#the-deformed-casimir-is-j_z) of the $\mathfrak{so}(3) \to \mathfrak{so}(2)$ breaking, commutes with all such planar perturbations. It is algebraically protected.

## References

- Arnold, V. I. (1963). Small denominators and problems of stability of motion in classical and celestial mechanics. _Russian Mathematical Surveys_, 18(6), 85-191. [doi:10.1070/RM1963v018n05ABEH004130](https://doi.org/10.1070/RM1963v018n05ABEH004130)
- Chiba, R. & Schoenrich, R. (2021). Tree-ring structure of Galactic bar resonance. _Monthly Notices of the Royal Astronomical Society_, 505(2), 2412-2426. [doi:10.1093/mnras/stab1094](https://doi.org/10.1093/mnras/stab1094)
- Binney, J. (2010). Distribution functions for the Milky Way. _Monthly Notices of the Royal Astronomical Society_, 401(4), 2318-2330. [doi:10.1111/j.1365-2966.2010.16734.x](https://doi.org/10.1111/j.1365-2966.2010.16734.x)
- Binney, J. & Tremaine, S. (2008). _Galactic Dynamics_ (2nd ed.). Princeton University Press.
- Minchev, I. & Famaey, B. (2010). A New Mechanism for Radial Migration in Galactic Disks. _The Astrophysical Journal_, 722(1), 112-121. [doi:10.1088/0004-637X/722/1/112](https://doi.org/10.1088/0004-637X/722/1/112)
- Trick, W. H., Fragkoudi, F., Hunt, J. A. S., Mackereth, J. T. & White, S. D. M. (2021). Identifying resonances of the Galactic bar in Gaia DR2: I. Clues from action space. _Monthly Notices of the Royal Astronomical Society_, 500(2), 2645-2665. [doi:10.1093/mnras/staa2722](https://doi.org/10.1093/mnras/staa2722)
- Sellwood, J. A. & Binney, J. J. (2002). Radial mixing in galactic discs. _Monthly Notices of the Royal Astronomical Society_, 336(3), 785-796. [doi:10.1046/j.1365-8711.2002.05806.x](https://doi.org/10.1046/j.1365-8711.2002.05806.x)
- Weinberg, M. D. (1994). Kinematic Signatures of Bar Dissolution. _The Astrophysical Journal_, 420, 597. [doi:10.1086/174036](https://doi.org/10.1086/174036)
