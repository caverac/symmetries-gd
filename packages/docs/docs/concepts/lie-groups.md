---
sidebar_position: 1
---

# Lie group symmetries

A spherical galaxy has a layered gravitational structure ([Binney & Tremaine 2008](https://press.princeton.edu/books/paperback/9780691130279/galactic-dynamics)). At the very center sits a supermassive black hole (SMBH), whose gravity dominates at small radii -- the potential is Keplerian, $V \propto -1/r$. Moving outward, the enclosed stellar mass of the bulge grows and eventually overwhelms the black hole's contribution. In the limit of a uniform-density core, the potential becomes harmonic, $V \propto r^2$. Further out still, the flattened disk takes over with its own geometry.

A star driven outward by a [rotating bar perturbation](action-angles) crosses all of these regions ([Sellwood & Binney 2002](https://doi.org/10.1046/j.1365-8711.2002.05806.x)). At each radius, the potential has a different shape -- and a different **symmetry**. Every conserved quantity in mechanics corresponds to a symmetry of the potential ([Goldstein et al. 2002, Ch. 13](https://doi.org/10.1017/9781108679923)), so as the symmetry changes, the conserved quantities change too. The question is whether we can track that change continuously, rather than watching our invariants break down at the boundaries.

This is where Lie group theory enters. Each limiting potential has an exact symmetry group with its own conserved tensors and scalar invariants. Understanding these two limits is the starting point for building an invariant that [interpolates between them](connection).

## The Kepler potential: SO(4)

Near the SMBH, the potential is dominated by the point mass: $V = -\mu/r$. This has more symmetry than simple spherical invariance. Beyond conserving angular momentum $\mathbf{L}$, it also conserves the **Laplace-Runge-Lenz (LRL) vector** ([Goldstein et al. 2002, S3.9](https://doi.org/10.1017/9781108679923)):

$$
\mathbf{A} = \mathbf{v} \times \mathbf{L} - \mu\,\hat{r}
$$

The LRL vector points along the semi-major axis of the elliptical orbit and has fixed magnitude. Together, $\mathbf{L}$ and $\mathbf{A}$ generate the Lie algebra $\mathfrak{so}(4)$ -- the symmetry group of the 3-sphere ([Cordani 2003, Ch. 4](https://doi.org/10.1007/978-3-0348-8051-0)). The extra symmetry is why Kepler orbits close: it locks the ellipse in place.

Every Lie algebra has **Casimir invariants** -- scalar operators that commute with all generators of the algebra ([Hall 2015, S6.4](https://doi.org/10.1007/978-3-319-13467-3)). They label the representations of the group and are automatically conserved along any orbit. For $\mathfrak{so}(4)$, the quadratic Casimir is:

$$
C_K = L^2 + \frac{|\mathbf{A}|^2}{-2E_K}
$$

## The harmonic potential: SU(3)

Further out, the enclosed stellar mass of the bulge dominates and the potential flattens to $V = \frac{1}{2}m\omega^2 r^2$. This is a fundamentally different dynamical regime -- and it carries its own hidden symmetry.

Where the Kepler problem conserves a vector ($\mathbf{A}$), the harmonic oscillator conserves a rank-2 tensor -- the **Fradkin tensor** ([Fradkin 1965](https://doi.org/10.1119/1.1971373)):

$$
T_{ij} = \frac{p_i\, p_j}{2m} + \frac{1}{2}m\omega^2\, r_i\, r_j
$$

This symmetric tensor encodes the shape and orientation of the orbital ellipse in the harmonic well. The generators of $T_{ij}$ together with $\mathbf{L}$ form the Lie algebra $\mathfrak{su}(3)$ ([Cordani 2003, Ch. 5](https://doi.org/10.1007/978-3-0348-8051-0)).

The **harmonic Casimir** is:

$$
C_H = L^2 + \frac{\operatorname{Tr}(S^2)}{\omega^2}
$$

where $S_{ij} = T_{ij} - \frac{1}{3}\operatorname{Tr}(T)\,\delta_{ij}$ is the traceless part.

## Lie algebra deformation

The real potential is neither pure Kepler nor pure harmonic -- it transitions smoothly between the two. The key idea of this project is to model that transition as a **continuous deformation** (or contraction) of the Lie algebra ([Gilmore 2005, Ch. 13](https://store.doverpublications.com/products/9780486462752)):

$$
\mathfrak{so}(4) \xrightarrow{\lambda(r)} \mathfrak{su}(3)
$$

where $\lambda(r)$ is some function of radius that parameterizes the transition -- small near the SMBH, large in the bulge. The exact form of $\lambda(r)$ is not known _a priori_; finding the right one is the central challenge. Our [first attempt](connection) used $\lambda = r / r_{\text{core}}$ with sigmoid interpolation. The [eventual answer](../results/variable-delta) turned out to be the Staeckel focal distance $\Delta(r)$ -- a geometric quantity rather than a purely algebraic one.

To interpolate between the two limits, their conserved quantities must share the same mathematical structure. The Kepler side conserves a vector ($\mathbf{A}$) while the harmonic side conserves a rank-2 tensor ($T_{ij}$). We bridge this by promoting the LRL vector to a rank-2 tensor $A_{ij} = A_i A_j$, so that both limits live in the same space of symmetric $3 \times 3$ matrices.

The question is then whether the **Casimir invariant** -- the fundamental scalar identity of the algebra -- can be tracked through this deformation to produce a quantity that remains conserved even in the transition region. This is what the [interpolation tensor](connection) attempts to do.

## References

- Binney, J. & Tremaine, S. (2008). _Galactic Dynamics_ (2nd ed.). Princeton University Press.
- Cordani, B. (2003). _The Kepler Problem: Group Theoretical Aspects, Regularization and Quantization_. Birkhaeuser. [doi:10.1007/978-3-0348-8051-0](https://doi.org/10.1007/978-3-0348-8051-0)
- Fradkin, D. M. (1965). Three-Dimensional Isotropic Harmonic Oscillator and SU3. _American Journal of Physics_, 33(3), 207-211. [doi:10.1119/1.1971373](https://doi.org/10.1119/1.1971373)
- Gilmore, R. (2005). _Lie Groups, Lie Algebras, and Some of Their Applications_. Dover.
- Goldstein, H., Poole, C. P. & Safko, J. L. (2002). _Classical Mechanics_ (3rd ed.). Addison-Wesley.
- Hall, B. C. (2015). _Lie Groups, Lie Algebras, and Representations_ (2nd ed.). Springer. [doi:10.1007/978-3-319-13467-3](https://doi.org/10.1007/978-3-319-13467-3)
- Sellwood, J. A. & Binney, J. J. (2002). Radial mixing in galactic discs. _Monthly Notices of the Royal Astronomical Society_, 336(3), 785-796. [doi:10.1046/j.1365-8711.2002.05806.x](https://doi.org/10.1046/j.1365-8711.2002.05806.x)
