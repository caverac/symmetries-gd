---
sidebar_position: 4
---

# Reinterpreting the confocal distance

The [Lie group page](lie-groups) introduced $\Delta(R)$ as the deformation parameter of the $\mathfrak{so}(3) \to \mathfrak{so}(2)$ symmetry breaking, and the [experiment page](connection) showed that it is determined by the potential geometry. This page develops a deeper interpretation: $\Delta(R)$ is not merely a parameter but a **connection on a fiber bundle** of symmetry algebras over the galactic disk.

## The fiber bundle

A migrating star moves radially through regions of different local symmetry. At each guiding radius $R$, the gravitational potential defines a local symmetry algebra -- nearly $\mathfrak{so}(3)$ in the inner bulge, progressively deformed toward $\mathfrak{so}(2)$ in the outer disk. This structure is naturally described as a fiber bundle:

- **Base manifold $\mathcal{B}$**: the radial coordinate $R$ -- the space of guiding radii along which stars migrate.
- **Fiber $\mathcal{F}_R$**: at each $R$, the vertical phase space $(z, p_z)$, equipped with confocal ellipsoidal coordinates parameterized by $\Delta(R)$. This is the space in which $J_z$ is defined.
- **Structure group**: the symmetry group acting on the vertical phase space, which transitions continuously from $SO(3)$ at small $R$ to $SO(2)$ at large $R$.

The total space $\mathcal{E} = \bigcup_R \mathcal{F}_R$ is a bundle of vertical phase spaces over the disk. A star at guiding radius $R$ lives in the fiber $\mathcal{F}_R$; when it migrates to $R'$, it must be transported to the fiber $\mathcal{F}_{R'}$, which has a different coordinate geometry.

## $\Delta(R)$ as a connection

A **connection** on a fiber bundle is a rule for identifying fibers at neighboring points -- it defines **parallel transport** along the base manifold ([Nakahara 2003, Ch. 9](https://doi.org/10.1201/9781315275826); [Frankel 2011, Ch. 9](https://doi.org/10.1017/CBO9781139061377)).

$\Delta(R)$ plays exactly this role. At each radius, it specifies the confocal coordinate system -- the shape of the ellipsoidal surfaces, the separation of the Hamilton-Jacobi equation, the definition of $p_z$ and $J_z$. As $R$ changes, $\Delta(R)$ smoothly rotates the coordinate frame from nearly spherical to oblate spheroidal, providing a continuous identification between neighboring fibers.

Concretely: at radius $R$, the vertical action is computed as

$$
J_z(R) = \frac{1}{2\pi} \oint p_\nu\, d\nu \Big|_{\Delta = \Delta(R)}
$$

where $\nu$ is the short-axis confocal coordinate defined by $\Delta(R)$. When a star migrates to $R + dR$, the connection $\Delta(R)$ determines how the coordinate $\nu$ and the momentum $p_\nu$ transform, so that $J_z$ can be compared between the two fibers. The statement that $J_z$ is conserved during migration is the statement that $J_z$ is **parallel-transported** by this connection.

## Automatic flatness

A connection has **curvature** when parallel transport around a closed loop in the base manifold fails to return a vector to its starting value. Curvature requires at least two independent directions in the base -- it is measured by a 2-form $F = dA + A \wedge A$ ([Nakahara 2003, Ch. 10](https://doi.org/10.1201/9781315275826)).

Since our base manifold is one-dimensional ($R$ alone), **any connection on it is automatically flat**. There is no closed loop in a 1D space, so there is no curvature, and parallel transport is path-independent. This has a direct physical consequence: it does not matter _how_ a star migrates -- whether it drifts outward steadily, scatters inward then outward, or oscillates back and forth across the disk. As long as the transport follows the connection $\Delta(R)$, the vertical action $J_z$ is preserved regardless of the radial path.

This is a stronger statement than what the [numerical results](../results/variable-delta) alone can establish. The simulations show that $J_z$ is conserved for several representative migration histories. The flatness of the connection guarantees it for _all_ radial paths.

## The smoothness condition

The connection interpretation gives geometric content to a requirement that was previously just an observation: $\Delta(R)$ must be **smooth**.

A connection is well-defined only if the transition maps between neighboring fibers are smooth ([Nakahara 2003, Ch. 9](https://doi.org/10.1201/9781315275826)). For $\Delta(R)$, this means the confocal coordinate system must vary continuously with radius. A discontinuity in $\Delta$ -- a sudden jump in the shape of the coordinate surfaces -- would break the identification between neighboring fibers. Parallel transport of $J_z$ across the discontinuity would be undefined, and conservation would fail.

The [closed-form expression](connection#deriving-deltar-from-the-separability-condition) for $\Delta(R)$ in the Miyamoto-Nagai disk is manifestly smooth (it is an algebraic function of $R$, $a$, and $b$). This is not a coincidence -- it reflects the smooth geometry of the gravitational potential. The connection is smooth because the potential is smooth.

## When the connection breaks down

The fiber-bundle picture also clarifies _when_ the algebraic protection should fail:

1. **Non-planar perturbations.** The connection governs transport of $J_z$ under radial migration driven by planar perturbations (the bar, spiral arms). Perturbations that act _outside_ the disk plane -- such as gravitational scattering off giant molecular clouds ([Arora et al. 2025](https://doi.org/10.1093/mnras/stae2707)) or satellite impacts -- do not respect the $SO(2)$ structure and can change the fiber directly, bypassing the connection.

2. **Higher-dimensional base.** If the base manifold is extended beyond $R$ alone -- for instance, to the full orbital torus $(R, \phi, z)$ -- then the connection could have **nonzero curvature**. Curvature would mean that parallel transport of $J_z$ depends on the path through the extended base, introducing a geometric obstruction to conservation. Whether the natural extension of $\Delta$ to higher dimensions has curvature is an open question with physical content: nonzero curvature would predict specific regimes where $J_z$ conservation degrades, even for purely planar perturbations.

3. **Strong deformation gradients.** Even in 1D, the connection can become practically ineffective if $\Delta(R)$ varies too rapidly -- analogous to a gauge field with large gradients causing non-adiabatic transitions. In disc-dominant galaxies with strong bars, the effective potential geometry can change abruptly near resonances, and [Mikkola, McMillan & Hobbs (2020)](https://doi.org/10.1093/mnras/staa364) observed degraded $J_z$ conservation in precisely these regimes.

## Relation to gauge theory

$\Delta(R)$ is not a gauge field in the dynamical sense -- it has no equation of motion, no kinetic term, and no independent degrees of freedom. It is entirely determined by the gravitational potential. The appropriate mathematical object is an **Ehresmann connection** on a fiber bundle of Lie algebras ([Kobayashi & Nomizu 1963](https://doi.org/10.1002/9781118032756)), not a Yang-Mills gauge field.

Nevertheless, the analogy to gauge theory is instructive:

| Gauge theory               | Galactic dynamics                      |
| -------------------------- | -------------------------------------- |
| Base manifold (spacetime)  | Radial coordinate $R$                  |
| Fiber (internal space)     | Vertical phase space $(z, p_z)$        |
| Structure group            | $SO(3) \to SO(2)$                      |
| Connection $A_\mu$         | Focal distance $\Delta(R)$             |
| Parallel transport         | Conservation of $J_z$ during migration |
| Curvature $F_{\mu\nu}$     | Zero (1D base)                         |
| Gauge-invariant observable | $J_z$ (the deformed Casimir)           |

The Casimir $J_z$ is the gauge-invariant observable of this bundle: it is the quantity that does not depend on the choice of local coordinates (the specific confocal system at each $R$), and it is preserved under parallel transport (radial migration). This is why $J_z$ has physical meaning even as the coordinate system in which it is computed changes from point to point across the disk.

## References

- Arora, N. et al. (2025). Fundamental limits to orbit reconstruction due to non-conservation of stellar actions. _Monthly Notices of the Royal Astronomical Society_, 543(1), 358. [doi:10.1093/mnras/stae2707](https://doi.org/10.1093/mnras/stae2707)
- Frankel, T. (2011). _The Geometry of Physics_ (3rd ed.). Cambridge University Press. [doi:10.1017/CBO9781139061377](https://doi.org/10.1017/CBO9781139061377)
- Kobayashi, S. & Nomizu, K. (1963). _Foundations of Differential Geometry_, Vol. I. Wiley. [doi:10.1002/9781118032756](https://doi.org/10.1002/9781118032756)
- Mikkola, D., McMillan, P. J. & Hobbs, D. (2020). Radial migration and vertical action in N-body simulations. _Monthly Notices of the Royal Astronomical Society_, 495(3), 3295-3306. [doi:10.1093/mnras/staa364](https://doi.org/10.1093/mnras/staa364)
- Nakahara, M. (2003). _Geometry, Topology and Physics_ (2nd ed.). CRC Press. [doi:10.1201/9781315275826](https://doi.org/10.1201/9781315275826)
