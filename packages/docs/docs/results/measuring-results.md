---
sidebar_position: 3
---

# Measuring the results

The Osculating Casimir $C_2(r) = L^2 + \Delta(r)^2 p_z^2$ is tested against the traditional radial action $J_R$ by comparing their temporal variance during bar-driven radial migration.

## The variance ratio metric

For each test particle $k$, we compute the temporal variance of both quantities over the integration period:

$$
\text{ratio}_k = \frac{\operatorname{Var}_t\bigl(C_{2,k}(t)\bigr)}{\operatorname{Var}_t\bigl(J_{R,k}(t)\bigr)}
$$

A ratio less than 1 means $C_2$ is more stable than $J_R$. The summary statistic is the **median ratio** across all particles.

## Disk migration stress test

We simulated orbits migrating from the inner bulge ($r = 0.5$) into the galactic disk ($r = 3.0$) in a composite potential containing a supermassive black hole (Kepler), a Plummer bulge, a Miyamoto-Nagai disk, and a rotating Dehnen bar.

**Result: median ratio = 0.0115**

The Osculating Casimir is **87 times more stable** than the radial action during migration through three gravitational regimes.

### Variance comparison

The plot below shows per-particle variance of $C_2$ versus $J_R$. Points below the diagonal indicate particles where $C_2$ is more stable:

![Variance comparison between C_2 and J_R](/img/variance-comparison.png)

### Stress test

Under increasing bar strength, the ratio $\operatorname{Var}(C_2)/\operatorname{Var}(J_R)$ drops -- $C_2$ becomes _relatively_ more stable as the perturbation grows and traditional actions deteriorate:

![Stress test under increasing bar perturbation](/img/stress-test.png)

## Reproducing the results

Run the disk migration simulation:

```bash
uv run experiments simulate \
  --smbh-mass 0.1 \
  --plummer-mass 0.4 \
  --plummer-scale 0.5 \
  --disk-mass 0.5 \
  --disk-a 3.0 \
  --disk-b 0.2 \
  --bar-strength 0.05 \
  --output-dir results/disk_migration
```

Generate the variance plot:

```bash
uv run experiments variance-plot --data-dir results/disk_migration
```

## Summary of findings

| Test                                 | Median ratio  | Interpretation                 |
| ------------------------------------ | ------------- | ------------------------------ |
| Pure Kepler limit                    | $< 10^{-13}$  | Both exactly conserved         |
| Pure harmonic limit                  | $< 10^{-13}$  | Both exactly conserved         |
| Algebraic $C_2$ (transition)         | $\sim 10^{4}$ | Algebraic approach fails       |
| **Geometric $C_2$ (disk migration)** | **0.0115**    | **87x more stable than $J_R$** |

The geometric reinterpretation -- treating the [Lie algebra deformation parameter as a dynamic Staeckel focal distance](variable-delta) -- transforms $C_2$ from a failed algebraic invariant into a robust, near-conserved quantity across multiple gravitational regimes.
