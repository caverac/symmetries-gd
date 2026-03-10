---
sidebar_position: 3
---

# From algebra to experiment

The [previous pages](lie-groups) established the symmetry breaking $\mathfrak{so}(3) \to \mathfrak{so}(2)$, the Staeckel focal distance $\Delta(R)$ as the deformation parameter, and the vertical action $J_z$ as the deformed Casimir. This page describes the concrete galactic model, the numerical methods, and the metric used to test the prediction.

## The galactic model

We construct a Milky-Way-like potential with four components ([Bovy 2015](https://doi.org/10.3847/0067-0049/216/2/29)):

1. **Hernquist bulge** ([Hernquist 1990](https://doi.org/10.1086/168845)) -- scale radius $a_b = 0.5$ kpc. Dominates the inner potential where the geometry is approximately spherical.
2. **Miyamoto-Nagai disk** ([Miyamoto & Nagai 1975](https://doi.org/10.1093/pasj/27.4.533)) -- scale length $a_d = 3$ kpc, scale height $b_d = 0.28$ kpc. Provides the flattened axisymmetric component that breaks $SO(3) \to SO(2)$.
3. **NFW halo** ([Navarro, Frenk & White 1997](https://doi.org/10.1086/304888)) -- scale radius $a_h = 16$ kpc. Ensures a flat rotation curve ($V_\mathrm{circ} \approx 220$ km/s) from $R \sim 4$ to $R \sim 16$ kpc.
4. **Dehnen bar** ([Dehnen 2000](https://doi.org/10.1086/301226)) -- bar radius $r_b = 4$ kpc, pattern speed $\Omega_b = 40$ km/s/kpc. Grows smoothly over $\sim$1 Gyr, then remains at full strength. Gaia-era measurements place the present-day Milky Way bar pattern speed at $\sim$33--41 km/s/kpc ([Portail et al. 2017](https://doi.org/10.1093/mnras/stw2819); [Sanders, Smith & Evans 2019](https://doi.org/10.1093/mnras/stz1830); [Clarke & Gerhard 2022](https://doi.org/10.1093/mnras/stac603)), with evidence that the bar has decelerated over time ([Chiba & Schoenrich 2021](https://doi.org/10.1093/mnras/stab1094)). Our choice of $\Omega_b = 40$ km/s/kpc is within this range and representative of earlier epochs.

Figure 1 shows the circular-velocity profile of the axisymmetric components and their sum.

<figure className="scientific scientific--narrow">
  <img
    src="/img/potential-profile.png"
    alt="Circular-velocity profile of the MW-like galactic potential"
  />
  <figcaption>
    <strong>Figure 1.</strong> Circular-velocity profile $V_{{\mathrm{{circ}}}}(R)$ of the
    axisymmetric model. Gray lines show the three components: Hernquist bulge
    (dashed), Miyamoto-Nagai disk (dash-dotted), and NFW halo (dotted). The solid
    black curve is the total. The disk dominates from $\sim$3 to $\sim$15 kpc;
    beyond that the NFW halo takes over, producing the flat rotation curve at
    $\sim$220 km/s characteristic of the Milky Way.
  </figcaption>
</figure>

Orbit integration and action computation use [galpy](https://doi.org/10.3847/1538-4365/aabead) ([Bovy 2015](https://doi.org/10.3847/0067-0049/216/2/29)). An updated Milky Way potential with revised solar parameters ($R_0 = 8.20$ kpc, $V_0 = 232.8$ km/s) is given by [McMillan (2017)](https://doi.org/10.1093/mnras/stw2759); we retain the classical values for direct comparison with the cited N-body studies.

## The Staeckel fudge and the focal distance

The composite potential is not separable in any coordinate system -- there is no closed-form expression for the actions. To estimate $J_R$ and $J_z$ numerically, galpy uses the **Staeckel fudge** ([Binney 2012](https://doi.org/10.1111/j.1365-2966.2012.21757.x); [Sanders 2012](https://doi.org/10.1111/j.1365-2966.2012.21964.x)).

The method evaluates the _real_ composite potential in confocal ellipsoidal coordinates parameterized by a focal distance $\Delta$, then assumes the potential separates in those coordinates to perform the action integrals analytically. It does not replace the potential with a Staeckel one -- it uses the actual potential values but exploits the Staeckel form to make the integrals tractable. For static, nearly axisymmetric potentials, this recovers actions to $\sim$1% accuracy.

[Sanders & Binney (2016)](https://doi.org/10.1093/mnras/stw075) provide a comprehensive comparison of action estimation methods -- Staeckel fudge, torus mapping, and generating-function approaches -- concluding that the Staeckel fudge offers the best speed-accuracy trade-off for smooth axisymmetric potentials. An independent, optimized implementation is available in the AGAMA library ([Vasiliev 2019](https://doi.org/10.1093/mnras/sty2672)).

### Why $\Delta(R)$ and not a constant

In galpy's standard usage, the Staeckel fudge takes a **single, fixed** $\Delta$ for the entire orbit. This is adequate when a star stays in one gravitational regime. But the algebraic framework requires us to understand how $\Delta$ varies with radius -- because $\Delta(R)$ _is_ the deformation parameter of the $\mathfrak{so}(3) \to \mathfrak{so}(2)$ transition.

### Deriving $\Delta(R)$ from the separability condition

A potential $\Phi(R, z)$ is _Staeckel-separable_ in prolate spheroidal coordinates $(u, v)$ with focal distance $\Delta$ if it can be written as $\Phi = [f(u) - g(v)] / (\sinh^2 u - \sin^2 v)$ for some functions $f, g$ ([de Zeeuw 1985](https://doi.org/10.1093/mnras/216.2.273)). Real galactic potentials are not exactly Staeckel, but the Miyamoto-Nagai disk is _close_ -- it was originally constructed as a flattened generalization of the Plummer sphere and nearly separates in oblate spheroidal coordinates.

To find the locally optimal $\Delta$ at each radius, we evaluate the separability condition at the midplane ($z = 0$). For a Miyamoto-Nagai disk with scale length $a$ and scale height $b$, this yields ([Batsleer & Dejonghe 1994](https://doi.org/10.1051/0004-6361:20021779); [Famaey & Dejonghe 2003](https://doi.org/10.1046/j.1365-8711.2003.06833.x)):

$$
\Delta^2(R) = \frac{4\,a\,\bigl(R^2 + (a + b)^2\bigr)}{3\,(a + b)} - R^2
$$

This is a closed-form expression -- no fitting, no free parameters. The disk geometry $(a, b)$ completely determines the focal distance at every radius.

The limiting behavior is physically transparent:

- **Small $R$** ($R \ll a + b$): $\Delta^2 \approx 4a(a+b)/3$, a constant set by the disk scales. The potential is nearly spherical in the inner region, and $\Delta$ is small.
- **Large $R$** ($R \gg a + b$): $\Delta^2 \approx (4a/3(a+b) - 1)\,R^2$. The focal distance grows with radius, reflecting the increasing dominance of the flattened disk.

This is exactly the behavior the algebraic framework predicts: $\Delta$ should be small where the potential is spherical ($SO(3)$) and large where it is flattened ($SO(2)$). Figure 2 shows $\Delta(R)$ for our MW-like disk parameters.

<figure className="scientific scientific--narrow">
  <img
    src="/img/delta-profile.png"
    alt="Staeckel focal distance as a function of radius"
  />
  <figcaption>
    <strong>Figure 2.</strong> Staeckel focal distance $\Delta(R)$ for the
    Miyamoto-Nagai disk ($a_d = 3$ kpc, $b_d = 0.28$ kpc). The focal distance is
    nearly constant at small radii (where the bulge dominates and the geometry
    is approximately spherical) and grows at large radii as the disk flattening
    becomes dominant. The dashed lines mark the bulge scale radius $a_b = 0.5$ kpc
    and the disk scale length $a_d = 3$ kpc. This function is the deformation
    parameter that governs the $\mathfrak{{so}}(3) \to \mathfrak{{so}}(2)$
    transition: small $\Delta$ corresponds to spherical symmetry, large $\Delta$
    to a flattened disk.
  </figcaption>
</figure>

The key point: $\Delta(R)$ is not a free parameter -- it is determined by the potential. It encodes the local departure from spherical symmetry at each radius, and it is the same quantity that defines the confocal coordinates in which $J_z$ is computed. This is the geometric link between the algebraic deformation and the action calculation.

## Initial conditions

Test particles are sampled from a quasi-isothermal distribution function ([Binney 2010](https://doi.org/10.1111/j.1365-2966.2010.16734.x)) matched to the axisymmetric potential (without the bar). Two populations are generated:

- **Center population** -- 1000 particles in the inner disk ($R \sim 1.6\text{--}4.0$ kpc), with small velocity dispersions.
- **Disk population** -- 1000 particles in the outer disk ($R \sim 4\text{--}16$ kpc), with dispersions matched to the Milky Way thin disk.

Particle positions $(R, z, \phi)$ and velocities $(v_R, v_T, v_z)$ are sampled from the quasi-isothermal DF, ensuring dynamical equilibrium at $t = 0$. Heights $z$ are drawn via rejection sampling from the DF's vertical density profile, giving particles realistic vertical oscillations and non-zero initial $J_z$. The bar then grows over $\sim$1 Gyr, driving migration through corotation resonance at $R_\mathrm{CR} \approx V_c / \Omega_b \approx 5.5$ kpc.

## The stability metric

The test is a direct comparison of how much each action varies during bar-driven migration. For each particle, we compute the temporal standard deviation of the action over all snapshots, normalized by the initial angular momentum to obtain a dimensionless quantity:

$$
\frac{\sigma(J)}{|L_{z,0}|}
$$

where $\sigma(J)$ is the standard deviation of the action time series. This captures both secular drift and fluctuations, rather than just the endpoint difference.

The prediction from the algebraic framework is:

$$
\frac{\sigma(J_z)}{|L_{z,0}|} \ll \frac{\sigma(J_R)}{|L_{z,0}|}
$$

If $J_z$ is the correct deformed Casimir -- adapting its definition to the local potential -- then its normalized variability should remain much smaller than that of $J_R$, reflecting its adiabatic protection from planar perturbations regardless of how far the star migrates.

The [results section](../results/staeckel-potential) reports the outcome.

## References

- Batsleer, P. & Dejonghe, H. (1994). Stackel fitting of galaxy surfaces. _Astronomy and Astrophysics_, 287, 43-52.
- Binney, J. (2010). Distribution functions for the Milky Way. _Monthly Notices of the Royal Astronomical Society_, 401(4), 2318-2330. [doi:10.1111/j.1365-2966.2010.16734.x](https://doi.org/10.1111/j.1365-2966.2010.16734.x)
- Binney, J. (2012). Actions for axisymmetric potentials. _Monthly Notices of the Royal Astronomical Society_, 426(2), 1324-1327. [doi:10.1111/j.1365-2966.2012.21757.x](https://doi.org/10.1111/j.1365-2966.2012.21757.x)
- Bovy, J. (2015). galpy: A Python Library for Galactic Dynamics. _The Astrophysical Journal Supplement Series_, 216(2), 29. [doi:10.3847/0067-0049/216/2/29](https://doi.org/10.3847/0067-0049/216/2/29)
- Chiba, R. & Schoenrich, R. (2021). Tree-ring structure of Galactic bar resonance. _Monthly Notices of the Royal Astronomical Society_, 505(2), 2412-2426. [doi:10.1093/mnras/stab1094](https://doi.org/10.1093/mnras/stab1094)
- Clarke, J. P. & Gerhard, O. (2022). The pattern speed of the Milky Way bar/bulge from VIRAC and Gaia. _Monthly Notices of the Royal Astronomical Society_, 512(2), 2171-2188. [doi:10.1093/mnras/stac603](https://doi.org/10.1093/mnras/stac603)
- Dehnen, W. (2000). The Effect of the Outer Lindblad Resonance of the Galactic Bar on the Local Stellar Velocity Distribution. _The Astronomical Journal_, 119(2), 800-812. [doi:10.1086/301226](https://doi.org/10.1086/301226)
- Famaey, B. & Dejonghe, H. (2003). The Staeckel approximation for orbits in galactic potentials. _Monthly Notices of the Royal Astronomical Society_, 340(3), 752-762. [doi:10.1046/j.1365-8711.2003.06833.x](https://doi.org/10.1046/j.1365-8711.2003.06833.x)
- Hernquist, L. (1990). An analytical model for spherical galaxies and bulges. _The Astrophysical Journal_, 356, 359-364. [doi:10.1086/168845](https://doi.org/10.1086/168845)
- McMillan, P. J. (2017). The mass distribution and gravitational potential of the Milky Way. _Monthly Notices of the Royal Astronomical Society_, 465(1), 76-94. [doi:10.1093/mnras/stw2759](https://doi.org/10.1093/mnras/stw2759)
- Miyamoto, M. & Nagai, R. (1975). Three-dimensional models for the distribution of mass in galaxies. _Publications of the Astronomical Society of Japan_, 27(4), 533-543. [doi:10.1093/pasj/27.4.533](https://doi.org/10.1093/pasj/27.4.533)
- Navarro, J. F., Frenk, C. S. & White, S. D. M. (1997). A Universal Density Profile from Hierarchical Clustering. _The Astrophysical Journal_, 490(2), 493-508. [doi:10.1086/304888](https://doi.org/10.1086/304888)
- Portail, M., Gerhard, O., Wegg, C. & Ness, M. (2017). Dynamical modelling of the galactic bulge and bar. _Monthly Notices of the Royal Astronomical Society_, 465(2), 1621-1644. [doi:10.1093/mnras/stw2819](https://doi.org/10.1093/mnras/stw2819)
- Sanders, J. (2012). Angle-action estimation in a general axisymmetric potential. _Monthly Notices of the Royal Astronomical Society_, 426(1), 128-139. [doi:10.1111/j.1365-2966.2012.21964.x](https://doi.org/10.1111/j.1365-2966.2012.21964.x)
- Sanders, J. L. & Binney, J. (2016). A review of action estimation methods for galactic dynamics. _Monthly Notices of the Royal Astronomical Society_, 457(2), 2107-2121. [doi:10.1093/mnras/stw075](https://doi.org/10.1093/mnras/stw075)
- Sanders, J. L., Smith, L. & Evans, N. W. (2019). The pattern speed of the Milky Way bar from transverse velocities. _Monthly Notices of the Royal Astronomical Society_, 488(4), 4552-4564. [doi:10.1093/mnras/stz1830](https://doi.org/10.1093/mnras/stz1830)
- Vasiliev, E. (2019). AGAMA: action-based galaxy modelling architecture. _Monthly Notices of the Royal Astronomical Society_, 482(2), 1525-1544. [doi:10.1093/mnras/sty2672](https://doi.org/10.1093/mnras/sty2672)
