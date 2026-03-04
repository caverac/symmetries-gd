"""Tests for DF-based initial condition sampling."""

from __future__ import annotations

from typing import cast
from unittest.mock import MagicMock, patch

import numpy as np
from symmetries._types import GalpyPotential, InitialConditionsConfig, PopulationConfig, PotentialConfig
from symmetries.initial_conditions import build_df, sample_initial_conditions, sample_population


def _make_population(n: int = 5, label: str = "test") -> PopulationConfig:
    """Create a minimal PopulationConfig for testing."""
    return PopulationConfig(
        n_particles=n,
        hr=1.0,
        sr=0.2,
        sz=0.1,
        hsr=2.0,
        hsz=2.0,
        r_min=0.5,
        r_max=2.0,
        label=label,
    )


class TestBuildDf:
    """Tests for build_df function."""

    @patch("symmetries.initial_conditions.quasiisothermaldf")
    @patch("symmetries.initial_conditions.actionAngleStaeckel")
    def test_creates_df_with_population_params(self, mock_aa: MagicMock, mock_df_cls: MagicMock) -> None:
        """Verify quasiisothermaldf is called with population parameters."""
        pop = _make_population()
        potential = [cast(GalpyPotential, MagicMock())]
        build_df(pop, potential)

        mock_aa.assert_called_once_with(pot=potential, delta=0.5)
        mock_df_cls.assert_called_once_with(
            hr=pop.hr,
            sr=pop.sr,
            sz=pop.sz,
            hsr=pop.hsr,
            hsz=pop.hsz,
            pot=potential,
            aA=mock_aa.return_value,
        )

    @patch("symmetries.initial_conditions.quasiisothermaldf")
    @patch("symmetries.initial_conditions.actionAngleStaeckel")
    def test_returns_df_instance(self, _mock_aa: MagicMock, mock_df_cls: MagicMock) -> None:
        """Verify build_df returns the DF instance."""
        pop = _make_population()
        result = build_df(pop, [])
        assert result is mock_df_cls.return_value


class TestSamplePopulation:
    """Tests for sample_population function."""

    @patch("symmetries.initial_conditions.quasiisothermaldf")
    @patch("symmetries.initial_conditions.actionAngleStaeckel")
    def test_returns_correct_shapes(self, _mock_aa: MagicMock, mock_df_cls: MagicMock) -> None:
        """Verify returned arrays have shape (n_particles,)."""
        n = 3
        pop = _make_population(n=n)
        mock_df = MagicMock()
        mock_df_cls.return_value = mock_df
        mock_df.sampleV.return_value = np.array([[0.1, 0.8, 0.05]])

        rng = np.random.default_rng(0)
        r_cyl, vr, vt, z, vz, phi = sample_population(pop, [], rng)

        assert r_cyl.shape == (n,)
        assert vr.shape == (n,)
        assert vt.shape == (n,)
        assert z.shape == (n,)
        assert vz.shape == (n,)
        assert phi.shape == (n,)

    @patch("symmetries.initial_conditions.quasiisothermaldf")
    @patch("symmetries.initial_conditions.actionAngleStaeckel")
    def test_radii_in_range(self, _mock_aa: MagicMock, mock_df_cls: MagicMock) -> None:
        """Verify sampled radii fall within [r_min, r_max]."""
        pop = _make_population(n=20)
        mock_df = MagicMock()
        mock_df_cls.return_value = mock_df
        mock_df.sampleV.return_value = np.array([[0.0, 1.0, 0.0]])

        rng = np.random.default_rng(42)
        r_cyl, _, _, _, _, _ = sample_population(pop, [], rng)

        assert np.all(r_cyl >= pop.r_min)
        assert np.all(r_cyl <= pop.r_max)

    @patch("symmetries.initial_conditions.quasiisothermaldf")
    @patch("symmetries.initial_conditions.actionAngleStaeckel")
    def test_z_is_zero(self, _mock_aa: MagicMock, mock_df_cls: MagicMock) -> None:
        """Verify z coordinates are initialized to zero."""
        pop = _make_population(n=4)
        mock_df = MagicMock()
        mock_df_cls.return_value = mock_df
        mock_df.sampleV.return_value = np.array([[0.0, 1.0, 0.0]])

        rng = np.random.default_rng(0)
        _, _, _, z, _, _ = sample_population(pop, [], rng)

        np.testing.assert_array_equal(z, np.zeros(4))

    @patch("symmetries.initial_conditions.quasiisothermaldf")
    @patch("symmetries.initial_conditions.actionAngleStaeckel")
    def test_velocities_from_df(self, _mock_aa: MagicMock, mock_df_cls: MagicMock) -> None:
        """Verify velocities are extracted from DF sampleV."""
        pop = _make_population(n=2)
        mock_df = MagicMock()
        mock_df_cls.return_value = mock_df
        mock_df.sampleV.side_effect = [
            np.array([[0.1, 0.9, 0.02]]),
            np.array([[0.2, 0.8, 0.03]]),
        ]

        rng = np.random.default_rng(0)
        _, vr, vt, _, vz, _ = sample_population(pop, [], rng)

        np.testing.assert_allclose(vr, [0.1, 0.2])
        np.testing.assert_allclose(vt, [0.9, 0.8])
        np.testing.assert_allclose(vz, [0.02, 0.03])


class TestSampleInitialConditions:
    """Tests for sample_initial_conditions function."""

    @patch("symmetries.initial_conditions.build_axisymmetric")
    @patch("symmetries.initial_conditions.quasiisothermaldf")
    @patch("symmetries.initial_conditions.actionAngleStaeckel")
    def test_concatenates_populations(self, _mock_aa: MagicMock, mock_df_cls: MagicMock, mock_build: MagicMock) -> None:
        """Verify results from multiple populations are concatenated."""
        mock_build.return_value = []
        mock_df = MagicMock()
        mock_df_cls.return_value = mock_df
        mock_df.sampleV.return_value = np.array([[0.0, 1.0, 0.0]])

        pop1 = _make_population(n=3, label="a")
        pop2 = _make_population(n=4, label="b")
        ic_config = InitialConditionsConfig(populations=(pop1, pop2), seed=0)

        r_cyl, vr, vt, z, vz, phi, labels = sample_initial_conditions(ic_config, PotentialConfig())

        assert r_cyl.shape == (7,)
        assert vr.shape == (7,)
        assert vt.shape == (7,)
        assert z.shape == (7,)
        assert vz.shape == (7,)
        assert phi.shape == (7,)
        assert labels.shape == (7,)

    @patch("symmetries.initial_conditions.build_axisymmetric")
    @patch("symmetries.initial_conditions.quasiisothermaldf")
    @patch("symmetries.initial_conditions.actionAngleStaeckel")
    def test_labels_encode_population_index(
        self, _mock_aa: MagicMock, mock_df_cls: MagicMock, mock_build: MagicMock
    ) -> None:
        """Verify labels contain correct population indices."""
        mock_build.return_value = []
        mock_df = MagicMock()
        mock_df_cls.return_value = mock_df
        mock_df.sampleV.return_value = np.array([[0.0, 1.0, 0.0]])

        pop1 = _make_population(n=2, label="a")
        pop2 = _make_population(n=3, label="b")
        ic_config = InitialConditionsConfig(populations=(pop1, pop2), seed=0)

        _, _, _, _, _, _, labels = sample_initial_conditions(ic_config, PotentialConfig())

        np.testing.assert_array_equal(labels[:2], 0)
        np.testing.assert_array_equal(labels[2:], 1)

    @patch("symmetries.initial_conditions.build_axisymmetric")
    @patch("symmetries.initial_conditions.quasiisothermaldf")
    @patch("symmetries.initial_conditions.actionAngleStaeckel")
    def test_uses_axisymmetric_potential(
        self, _mock_aa: MagicMock, mock_df_cls: MagicMock, mock_build: MagicMock
    ) -> None:
        """Verify build_axisymmetric is called with the potential config."""
        mock_build.return_value = [MagicMock()]
        mock_df = MagicMock()
        mock_df_cls.return_value = mock_df
        mock_df.sampleV.return_value = np.array([[0.0, 1.0, 0.0]])

        pop = _make_population(n=1)
        pot_config = PotentialConfig(smbh_mass=0.2)
        ic_config = InitialConditionsConfig(populations=(pop,), seed=0)

        sample_initial_conditions(ic_config, pot_config)

        mock_build.assert_called_once_with(pot_config)
