---
sidebar_position: 2
---

# The dynamic focal distance

The [Osculating Casimir](staeckel-potential) requires a focal distance $\Delta(r)$ that adapts to the local symmetry of the potential. This page describes how $\Delta$ is constructed and what it means physically.

## Ellipsoidal coordinates and $\Delta$

In Staeckel potential theory, orbits are described in **prolate spheroidal coordinates** $(\lambda, \nu, \phi)$ parameterized by a focal distance $\Delta$. When $\Delta = 0$, the coordinates reduce to spherical; as $\Delta$ grows, the coordinate surfaces stretch into ellipsoids.

The focal distance determines the shape of the coordinate system -- and therefore which third integral $I_3 = L^2 + \Delta^2 p_z^2$ is conserved. For a given axisymmetric potential, there exists an optimal $\Delta$ that minimizes the deviation from Staeckel form.

## The multi-stage path

A migrating star passes through three gravitational regimes, each with a different natural coordinate geometry:

| Regime                | Radius                    | Symmetry         | $\Delta$                   |
| --------------------- | ------------------------- | ---------------- | -------------------------- |
| **Spherical core**    | $r \ll r_{\text{core}}$   | Kepler / SO(4)   | $\approx 0$                |
| **Ellipsoidal bulge** | $r \sim r_{\text{bulge}}$ | Harmonic / SU(3) | $\approx a_{\text{bulge}}$ |
| **Flattened disk**    | $r \sim r_{\text{disk}}$  | Disk dynamics    | $\approx a_{\text{disk}}$  |

The implementation uses a two-stage sigmoid interpolation to smoothly connect these regimes:

$$
\Delta(r) = \bigl(1 - \sigma_{\text{disk}}(r)\bigr)\,\sigma_{\text{bulge}}(r)\, a_{\text{bulge}} + \sigma_{\text{disk}}(r)\, a_{\text{disk}}
$$

where each sigmoid is centered at the corresponding scale radius:

$$
\sigma(r) = \frac{1}{1 + e^{-4(r/r_{\text{scale}} - 1)}}
$$

The bulge transition scale $r_{\text{core}}$ is set by the SMBH sphere of influence: $r_{\text{core}} = \mu\, a_{\text{bulge}} / M_{\text{bulge}}$, where $\mu$ is the SMBH gravitational parameter.

## The key insight

The Lie algebra deformation parameter $\lambda$ and the Staeckel focal distance $\Delta$ are not merely analogous -- they are the **same quantity** viewed from different mathematical perspectives:

- **Algebraically**: $\lambda$ parameterizes the contraction $\mathfrak{so}(4) \to \mathfrak{su}(3)$, tracking how the symmetry group deforms
- **Geometrically**: $\Delta$ parameterizes the coordinate system, tracking how the orbital shape stretches from spherical to ellipsoidal

By treating $\Delta$ as a dynamic, radius-dependent variable -- an **osculating focal length** -- we allow the coordinate system itself to deform along with the potential. This is why $C_2(r)$ remains stable where fixed-coordinate actions break down: it measures the orbit in the locally correct geometry at every point.

The [experimental results](measuring-results) confirm this: during disk migration, the Osculating Casimir is 87 times more stable than the traditional radial action.
