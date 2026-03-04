"""Pydantic configuration model for simulation runs."""

from __future__ import annotations

from pydantic import BaseModel
from symmetries import InitialConditionsConfig, PopulationConfig, PotentialConfig


class RunConfig(BaseModel):
    """Single flat configuration for a simulation run.

    Parameters
    ----------
    name : str
        Unique identifier for the simulation run.
    seed : int
        Random seed for reproducibility.
    t_end : float
        Integration end time (natural units).
    n_steps : int
        Number of integration time steps.
    delta : float
        Staeckel delta parameter.
    smbh_mass : float
        SMBH Kepler potential amplitude.
    plummer_mass : float
        Plummer bulge amplitude.
    plummer_scale : float
        Plummer sphere scale radius.
    disk_amp : float
        Miyamoto-Nagai disk amplitude.
    disk_a : float
        Disk scale length.
    disk_b : float
        Disk scale height.
    bar_strength : float
        Dehnen bar strength Af.
    bar_scale : float
        Dehnen bar radius rb.
    bar_tform : float
        Bar formation time.
    bar_tsteady : float
        Bar steady-state timescale.
    bar_pattern_speed : float
        Bar pattern speed.
    center_n : int
        Number of center/bulge population particles.
    center_hr : float
        Center population radial scale length.
    center_sr : float
        Center population radial velocity dispersion.
    center_sz : float
        Center population vertical velocity dispersion.
    center_hsr : float
        Center population radial dispersion scale length.
    center_hsz : float
        Center population vertical dispersion scale length.
    center_r_min : float
        Center population minimum radius.
    center_r_max : float
        Center population maximum radius.
    disk_n : int
        Number of disk population particles.
    disk_hr : float
        Disk population radial scale length.
    disk_sr : float
        Disk population radial velocity dispersion.
    disk_sz : float
        Disk population vertical velocity dispersion.
    disk_hsr : float
        Disk population radial dispersion scale length.
    disk_hsz : float
        Disk population vertical dispersion scale length.
    disk_r_min : float
        Disk population minimum radius.
    disk_r_max : float
        Disk population maximum radius.
    """

    # Simulation
    name: str
    seed: int = 42
    t_end: float = 500.0
    n_steps: int = 2000
    delta: float = 0.5

    # Potential
    smbh_mass: float = 1.0
    plummer_mass: float = 0.4
    plummer_scale: float = 0.5
    disk_amp: float = 0.5
    disk_a: float = 3.0
    disk_b: float = 0.3
    bar_strength: float = 0.0
    bar_scale: float = 1.0
    bar_tform: float = -100.0
    bar_tsteady: float = 50.0
    bar_pattern_speed: float = 0.3

    # Center population
    center_n: int = 100
    center_hr: float = 0.3
    center_sr: float = 0.4
    center_sz: float = 0.3
    center_hsr: float = 0.8
    center_hsz: float = 0.8
    center_r_min: float = 0.2
    center_r_max: float = 0.8

    # Disk population
    disk_n: int = 100
    disk_hr: float = 3.0
    disk_sr: float = 0.2
    disk_sz: float = 0.1
    disk_hsr: float = 4.0
    disk_hsz: float = 4.0
    disk_r_min: float = 1.0
    disk_r_max: float = 5.0

    def to_potential_config(self) -> PotentialConfig:
        """Convert to a ``PotentialConfig`` for the symmetries package.

        Returns
        -------
        PotentialConfig
            Potential configuration derived from this run config.
        """
        return PotentialConfig(
            smbh_mass=self.smbh_mass,
            plummer_mass=self.plummer_mass,
            plummer_scale=self.plummer_scale,
            disk_mass=self.disk_amp,
            disk_a=self.disk_a,
            disk_b=self.disk_b,
            bar_strength=self.bar_strength,
            bar_scale=self.bar_scale,
            bar_tform=self.bar_tform,
            bar_tsteady=self.bar_tsteady,
            bar_pattern_speed=self.bar_pattern_speed,
        )

    def to_ic_config(self) -> InitialConditionsConfig:
        """Convert to an ``InitialConditionsConfig`` with two populations.

        Returns
        -------
        InitialConditionsConfig
            IC configuration with center and disk populations.
        """
        center = PopulationConfig(
            n_particles=self.center_n,
            hr=self.center_hr,
            sr=self.center_sr,
            sz=self.center_sz,
            hsr=self.center_hsr,
            hsz=self.center_hsz,
            r_min=self.center_r_min,
            r_max=self.center_r_max,
            label="center",
        )
        disk_pop = PopulationConfig(
            n_particles=self.disk_n,
            hr=self.disk_hr,
            sr=self.disk_sr,
            sz=self.disk_sz,
            hsr=self.disk_hsr,
            hsz=self.disk_hsz,
            r_min=self.disk_r_min,
            r_max=self.disk_r_max,
            label="disk",
        )
        return InitialConditionsConfig(populations=(center, disk_pop), seed=self.seed)
