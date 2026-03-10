"""Initial condition sampling from galpy quasi-isothermal distribution functions.

Generates equilibrium initial conditions for orbit ensembles using
``quasiisothermaldf`` so that particles remain in place when the
potential is axisymmetric (no bar).
"""

from __future__ import annotations

import numpy as np
from galpy.actionAngle import actionAngleStaeckel
from galpy.df import quasiisothermaldf
from numpy.typing import NDArray
from symmetries._types import GalpyPotential, InitialConditionsConfig, PopulationConfig, PotentialConfig
from symmetries.potentials import build_axisymmetric


def build_df(population: PopulationConfig, potential: list[GalpyPotential]) -> quasiisothermaldf:
    """Create a quasi-isothermal distribution function for a population.

    Parameters
    ----------
    population : PopulationConfig
        Population parameters (scale lengths, dispersions).
    potential : list
        Axisymmetric galpy potential (list of potential instances).

    Returns
    -------
    quasiisothermaldf
        The galpy quasi-isothermal DF instance.
    """
    action_angle = actionAngleStaeckel(pot=potential, delta=0.5)
    return quasiisothermaldf(
        hr=population.hr,
        sr=population.sr,
        sz=population.sz,
        hsr=population.hsr,
        hsz=population.hsz,
        pot=potential,
        aA=action_angle,
    )


def sample_population(
    population: PopulationConfig,
    potential: list[GalpyPotential],
    rng: np.random.Generator,
) -> tuple[
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
]:
    """Sample phase-space coordinates for one population via DF.

    Parameters
    ----------
    population : PopulationConfig
        Population configuration with sampling parameters.
    potential : list
        Axisymmetric galpy potential.
    rng : numpy.random.Generator
        Random number generator for radii and azimuthal angles.

    Returns
    -------
    tuple of NDArray
        ``(r_cyl, vr, vt, z, vz, phi)`` arrays each of shape ``(n_particles,)``.
    """
    df = build_df(population, potential)
    n = population.n_particles
    z_max = population.z_max

    r_cyl = rng.uniform(population.r_min, population.r_max, size=n)
    phi = rng.uniform(0, 2 * np.pi, size=n)

    vr = np.empty(n)
    vt = np.empty(n)
    vz = np.empty(n)
    z = np.empty(n)

    for i in range(n):
        # Rejection-sample z from the DF vertical density profile
        rho_max = float(df.density(r_cyl[i], 0.0))
        while True:
            z_proposal = rng.uniform(-z_max, z_max)
            rho = float(df.density(r_cyl[i], z_proposal))
            if rng.uniform() < rho / max(rho_max, 1e-30):
                break
        z[i] = z_proposal

        vel_sample = df.sampleV(r_cyl[i], z[i], n=1)
        vr[i] = vel_sample[0, 0]
        vt[i] = vel_sample[0, 1]
        vz[i] = vel_sample[0, 2]

    return r_cyl, vr, vt, z, vz, phi


def sample_initial_conditions(
    config: InitialConditionsConfig,
    potential_config: PotentialConfig,
) -> tuple[
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.floating],
    NDArray[np.integer],
]:
    """Sample initial conditions for all populations.

    Parameters
    ----------
    config : InitialConditionsConfig
        IC configuration with population list and seed.
    potential_config : PotentialConfig
        Potential configuration (only the axisymmetric part is used).

    Returns
    -------
    tuple of NDArray
        ``(r_cyl, vr, vt, z, vz, phi, labels)`` concatenated across all
        populations. ``labels`` contains the population index (0, 1, ...).
    """
    rng = np.random.default_rng(config.seed)
    potential = build_axisymmetric(potential_config)

    all_r: list[NDArray[np.floating]] = []
    all_vr: list[NDArray[np.floating]] = []
    all_vt: list[NDArray[np.floating]] = []
    all_z: list[NDArray[np.floating]] = []
    all_vz: list[NDArray[np.floating]] = []
    all_phi: list[NDArray[np.floating]] = []
    all_labels: list[NDArray[np.integer]] = []

    for idx, pop in enumerate(config.populations):
        r_cyl, vr, vt, z, vz, phi = sample_population(pop, potential, rng)
        all_r.append(r_cyl)
        all_vr.append(vr)
        all_vt.append(vt)
        all_z.append(z)
        all_vz.append(vz)
        all_phi.append(phi)
        all_labels.append(np.full(pop.n_particles, idx, dtype=np.intp))

    return (
        np.concatenate(all_r),
        np.concatenate(all_vr),
        np.concatenate(all_vt),
        np.concatenate(all_z),
        np.concatenate(all_vz),
        np.concatenate(all_phi),
        np.concatenate(all_labels),
    )
