---
sidebar_position: 1
---

# The Staeckel connection

The [algebraic interpolation](../concepts/connection) between SO(4) and SU(3) Casimirs was elegant but ultimately failed. Here we describe the failure, its root cause, and the breakthrough that emerged from it.

## The algebraic failure

After refactoring the tensor construction to properly interpolate between the LRL and Fradkin tensors, we ran a systematic evaluation:

| Test                    | Result  | Details                                                                            |
| ----------------------- | ------- | ---------------------------------------------------------------------------------- |
| **Pure Kepler limit**   | PASS    | $\operatorname{Var}(C_2) < 10^{-25}$                                               |
| **Pure harmonic limit** | PASS    | $\operatorname{Var}(C_2) < 10^{-25}$                                               |
| **Transition region**   | FAIL    | $\operatorname{Var}(C_2) \sim 10^{-8}$, vs $\operatorname{Var}(J_R) \sim 10^{-12}$ |
| **Adiabatic test**      | FAIL    | Slower migration does not improve stability                                        |
| **Chaos stress test**   | NEUTRAL | Relative improvement at high bar strength, but absolute variance still worse       |

The boundary limits work perfectly -- $C_2$ is an exact Casimir in both the Kepler and harmonic potentials. But in the composite potential (SMBH + Plummer bulge), the invariant exhibits a variance floor 4-5 orders of magnitude higher than $J_R$.

The root cause: the intermediate potential does not possess a closed-form symmetry group. Smooth interpolation of the boundary algebras cannot capture the symmetry structure of the transition region.

**Recommendation at this point: NO-GO.** The algebraic deformation framework should be rejected.

## The geometric reinterpretation

The breakthrough came from asking a different question: instead of _"what Lie algebra does the transition region have?"_, we asked _"what coordinate system best fits the local potential at each radius?"_

The answer: **Staeckel potentials** -- the class of potentials separable in ellipsoidal coordinates, characterized by a focal distance parameter $\Delta$.

The Staeckel third integral takes the form:

$$
I_3 = L^2 + \Delta^2\, p_z^2
$$

In a fixed Staeckel potential, $\Delta$ is a constant and $I_3$ is exactly conserved. The insight is that our $C_2$ has exactly this form -- but with $\Delta$ allowed to vary with radius.

## The Osculating Casimir

We redefine $C_2$ not as a fixed algebraic Casimir, but as a **Staeckel integral with a dynamic focal distance**:

$$
C_2(r) = L^2 + \Delta(r)^2\, p_z^2
$$

The term "osculating" comes from the analogy with osculating orbits in celestial mechanics: at each radius, we evaluate the integral using the Staeckel system that best approximates the local potential -- then allow the focal distance to evolve as the star migrates.

This reframing connects two previously separate ideas:

1. **Lie algebra deformations**: The abstract transition $\mathfrak{so}(4) \to \mathfrak{su}(3)$
2. **Staeckel dynamics**: The practical construction of action integrals in ellipsoidal coordinates

The [deformation parameter](variable-delta) $\lambda$ of the Lie algebra turns out to be exactly the focal distance $\Delta$ of the ellipsoidal coordinate system.
