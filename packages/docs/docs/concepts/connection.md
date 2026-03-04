---
sidebar_position: 3
---

# From algebra to experiment

The [previous pages](lie-groups) established two exact symmetry limits and the idea of a [deformation parameter](lie-groups#lie-algebra-deformation) $\lambda(r)$ connecting them. This page turns that abstract framework into a concrete, testable construction: an interpolation tensor, a candidate invariant, a simulation setup, and a metric for success or failure.

## The generalized tensor

We need a single tensor $Q_{ij}$ that reduces to the [LRL tensor](lie-groups#the-kepler-potential-so4) at small radii and the [Fradkin tensor](lie-groups#the-harmonic-potential-su3) at large radii. The most general rank-2 symmetric form built from position and momentum is ([Goldstein et al. 2002, S8.5](https://doi.org/10.1017/9781108679923)):

$$
Q_{ij}(\lambda) = \frac{p_i\, p_j}{2m} + \Psi(r,\lambda)\, x_i\, x_j + \Phi(r,\lambda)\, \delta_{ij}
$$

The **structural functions** $\Psi$ and $\Phi$ encode the local character of the potential and use a sigmoid transition centered at the core radius $r_{\text{core}}$:

$$
\sigma(\lambda) = \frac{1}{1 + e^{-4(\lambda - 1)}}
$$

- **$\Psi(r,\lambda)$** interpolates between the Kepler tidal field $\mu/r^3$ and the harmonic spring constant $\omega^2$
- **$\Phi(r,\lambda)$** provides a scalar potential offset that vanishes in the harmonic limit

At $\lambda \ll 1$ (deep Kepler), the tensor reduces to the LRL structure. At $\lambda \gg 1$ (deep harmonic), it becomes the Fradkin tensor.

An alternative construction interpolates directly on the normalized boundary tensors:

$$
Q_{ij}(\lambda) = (1 - \sigma)\,\frac{A_{ij}}{-2E_K} + \sigma\,\frac{T_{ij}}{\omega}
$$

This **path tensor** explicitly blends the LRL tensor (normalized by orbital energy) with the Fradkin tensor (normalized by frequency), weighted by the sigmoid.

## The candidate invariant

From either tensor construction, we extract a scalar -- the **deformed Casimir**:

$$
C_2(\lambda) = L^2 + \operatorname{Tr}(Q^2)
$$

By construction, $C_2$ is exactly conserved in both pure limits. The open question is whether it remains approximately conserved in the transition region, where the potential is a composite of the two.

## Simulation setup

To test $C_2$, we integrate orbits in an analytical potential that contains both gravitational regimes and a mechanism to force stars between them:

1. **Kepler component** -- a central point mass (SMBH) with gravitational parameter $\mu$
2. **Bulge component** -- a [Plummer sphere](https://doi.org/10.1093/mnras/71.5.460) with mass $M_b$ and scale radius $a_b$, providing the harmonic core
3. **Disk component** -- a [Miyamoto-Nagai](https://doi.org/10.1093/pasj/27.4.533) potential with mass $M_d$ and scale lengths $(a_d, b_d)$
4. **Bar perturbation** -- a rotating [Dehnen bar](https://doi.org/10.1086/321642) that grows over time, creating resonances that scatter stars radially

Figure 1 shows the equatorial potential profile $\Phi(R, z=0)$ for each component and the total. This is the potential in which all orbits are integrated.

<figure className="scientific">
  <img
    src="/img/potential-profile.png"
    alt="Radial profile of the composite galactic potential"
  />
  <figcaption>
    <strong>Figure 1.</strong> Equatorial potential profile $\Phi(R,\, z=0)$ of the composite galactic model.
    Dashed lines show the three axisymmetric components: Kepler SMBH ($\mu = 0.1$),
    Plummer bulge ($M_b = 0.4$, $a_b = 0.5$), and Miyamoto-Nagai disk
    ($M_d = 0.5$, $a_d = 3.0$, $b_d = 0.2$). The solid black curve is the total
    axisymmetric potential. At small radii the Kepler term dominates; near
    $R \sim a_b$ the bulge takes over; beyond $R \sim 1$ the disk contribution
    becomes significant. A migrating star driven outward by the bar crosses all
    three regimes.
  </figcaption>
</figure>

An ensemble of test particles is initialized on stable orbits in the inner potential well and integrated forward as the bar grows and rotates. At each time step, we record the full 6D phase space and compute both $C_2$ and $J_R$.

The orbit integration and action computation use [galpy](https://doi.org/10.3847/1538-4365/aabead) ([Bovy 2015](https://doi.org/10.3847/0067-0049/216/2/29)).

### How $J_R$ is computed: the Staeckel fudge

The composite potential in Figure 1 is not separable in any coordinate system -- there is no closed-form expression for the actions. To estimate $J_R$ numerically, galpy uses the **Staeckel fudge** ([Binney 2012](https://doi.org/10.1111/j.1365-2966.2012.21757.x); [Sanders 2012](https://doi.org/10.1111/j.1365-2966.2012.21964.x)).

The method works by evaluating the _real_ composite potential in confocal ellipsoidal coordinates parameterized by a focal distance $\Delta$, then assuming the potential separates in those coordinates to perform the action integral analytically. It does not replace the potential with a Staeckel one -- it uses the actual potential values but exploits the Staeckel form to make the integral tractable. For static, nearly axisymmetric potentials, this recovers actions to $\sim$1% accuracy.

The critical limitation is that the method uses a **single, fixed** $\Delta$ for the entire orbit. This works well when a star stays in one gravitational regime, but during radial migration the orbit crosses regions where the locally optimal $\Delta$ changes dramatically (from $\Delta \approx 0$ near the SMBH to $\Delta \approx a_d$ in the disk). A fixed $\Delta$ cannot capture this, and the estimated $J_R$ fluctuates -- not because the orbit is truly chaotic, but because the coordinate system used to compute the action no longer fits the local potential.

This is exactly the gap that $C_2 = L^2 + \Delta(r)^2\, p_z^2$ is designed to fill: instead of computing a phase-space integral with a fixed focal distance, it evaluates a simple formula with a **locally adapted** $\Delta(r)$ at each point along the orbit. Figure 2 shows the dynamic focal distance used in the implementation.

<figure className="scientific">
  <img
    src="/img/delta-profile.png"
    alt="Dynamic focal distance Delta as a function of radius"
  />
  <figcaption>
    <strong>Figure 2.</strong> Dynamic focal distance $\Delta(r)$ used in the
    Osculating Casimir $C_2 = L^2 + \Delta(r)^2\, p_z^2$. The profile is
    constructed from two sigmoid transitions: the first (centred at
    $r_\mathrm{core} = \mu\, a_b / M_b \approx 0.12$) lifts $\Delta$ from
    $\approx 0$ (spherical Kepler geometry) to the bulge scale $a_b = 0.5$;
    the second (centred at $r_\mathrm{disk} = a_d = 3.0$) raises it to the
    disk scale $a_d = 3.0$. Compare with the potential profile in Figure 1:
    each transition in $\Delta$ corresponds to the radius where a new
    component begins to dominate the potential.
  </figcaption>
</figure>

## The variance ratio metric

The test is a direct comparison of temporal stability. For each particle $k$ in the ensemble, we compute the variance of $C_2$ and $J_R$ over the integration window:

$$
\text{ratio}_k = \frac{\operatorname{Var}_t\bigl(C_{2,k}(t)\bigr)}{\operatorname{Var}_t\bigl(J_{R,k}(t)\bigr)}
$$

The summary statistic is the **median ratio** across all particles. Success means:

$$
\text{median ratio} \ll 1
$$

A ratio much less than 1 would demonstrate that $C_2$ tracks a near-conserved quantity through the symmetry transition, even as the traditional action $J_R$ fluctuates. A ratio near or above 1 means $C_2$ offers no advantage -- and the algebraic deformation framework should be rejected.

The [results section](../results/staeckel-potential) reports what happened when we ran these experiments.

## References

- Binney, J. (2012). Actions for axisymmetric potentials. _Monthly Notices of the Royal Astronomical Society_, 426(2), 1324-1327. [doi:10.1111/j.1365-2966.2012.21757.x](https://doi.org/10.1111/j.1365-2966.2012.21757.x)
- Bovy, J. (2015). galpy: A Python Library for Galactic Dynamics. _The Astrophysical Journal Supplement Series_, 216(2), 29. [doi:10.3847/0067-0049/216/2/29](https://doi.org/10.3847/0067-0049/216/2/29)
- Dehnen, W. (2000). The Effect of the Outer Lindblad Resonance of the Galactic Bar on the Local Stellar Velocity Distribution. _The Astronomical Journal_, 119(2), 800-812. [doi:10.1086/301226](https://doi.org/10.1086/301226)
- Goldstein, H., Poole, C. P. & Safko, J. L. (2002). _Classical Mechanics_ (3rd ed.). Addison-Wesley.
- Miyamoto, M. & Nagai, R. (1975). Three-dimensional models for the distribution of mass in galaxies. _Publications of the Astronomical Society of Japan_, 27(4), 533-543. [doi:10.1093/pasj/27.4.533](https://doi.org/10.1093/pasj/27.4.533)
- Plummer, H. C. (1911). On the problem of distribution in globular star clusters. _Monthly Notices of the Royal Astronomical Society_, 71(5), 460-470. [doi:10.1093/mnras/71.5.460](https://doi.org/10.1093/mnras/71.5.460)
- Sanders, J. (2012). Angle-action estimation in a general axisymmetric potential. _Monthly Notices of the Royal Astronomical Society_, 426(1), 128-139. [doi:10.1111/j.1365-2966.2012.21964.x](https://doi.org/10.1111/j.1365-2966.2012.21964.x)
