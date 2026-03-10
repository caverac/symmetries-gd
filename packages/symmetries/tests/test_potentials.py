"""Tests for galpy potential construction."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from symmetries._types import PotentialConfig
from symmetries.potentials import (
    build_axisymmetric,
    build_bar,
    build_bulge,
    build_composite,
    build_disk,
    build_halo,
)


class TestBuildBulge:
    """Tests for Hernquist bulge potential builder."""

    @patch("symmetries.potentials.HernquistPotential")
    def test_calls_with_params(self, mock_hp: MagicMock) -> None:
        """Verify HernquistPotential is called with configured mass and scale."""
        config = PotentialConfig(bulge_mass=0.9, bulge_scale=0.5)
        build_bulge(config)
        mock_hp.assert_called_once_with(amp=0.9, a=0.5)

    @patch("symmetries.potentials.HernquistPotential")
    def test_returns_instance(self, mock_hp: MagicMock) -> None:
        """Verify build_bulge returns the HernquistPotential instance."""
        config = PotentialConfig()
        result = build_bulge(config)
        assert result is mock_hp.return_value


class TestBuildBar:
    """Tests for Dehnen bar potential builder."""

    @patch("symmetries.potentials.DehnenBarPotential")
    def test_calls_with_params(self, mock_db: MagicMock) -> None:
        """Verify DehnenBarPotential is called with all bar parameters."""
        config = PotentialConfig(
            bar_strength=0.01,
            bar_scale=1.0,
            bar_tform=-5.0,
            bar_tsteady=2.0,
            bar_pattern_speed=40.0,
        )
        build_bar(config)
        mock_db.assert_called_once_with(
            Af=0.01,
            rb=1.0,
            tform=-5.0,
            tsteady=2.0,
            omegab=40.0,
        )

    @patch("symmetries.potentials.DehnenBarPotential")
    def test_returns_instance(self, mock_db: MagicMock) -> None:
        """Verify build_bar returns the DehnenBarPotential instance."""
        config = PotentialConfig()
        result = build_bar(config)
        assert result is mock_db.return_value


class TestBuildDisk:
    """Tests for Miyamoto-Nagai disk potential builder."""

    @patch("symmetries.potentials.MiyamotoNagaiPotential")
    def test_calls_with_params(self, mock_mn: MagicMock) -> None:
        """Verify MiyamotoNagaiPotential is called with configured disk parameters."""
        config = PotentialConfig(disk_mass=0.5, disk_a=3.0, disk_b=0.2)
        build_disk(config)
        mock_mn.assert_called_once_with(amp=0.5, a=3.0, b=0.2)

    @patch("symmetries.potentials.MiyamotoNagaiPotential")
    def test_returns_instance(self, mock_mn: MagicMock) -> None:
        """Verify build_disk returns the MiyamotoNagaiPotential instance."""
        config = PotentialConfig()
        result = build_disk(config)
        assert result is mock_mn.return_value


class TestBuildHalo:
    """Tests for NFW halo potential builder."""

    @patch("symmetries.potentials.NFWPotential")
    def test_calls_with_params(self, mock_nfw: MagicMock) -> None:
        """Verify NFWPotential is called with configured halo parameters."""
        config = PotentialConfig(halo_amp=5.0, halo_a=3.0)
        build_halo(config)
        mock_nfw.assert_called_once_with(amp=5.0, a=3.0)

    @patch("symmetries.potentials.NFWPotential")
    def test_returns_instance(self, mock_nfw: MagicMock) -> None:
        """Verify build_halo returns the NFWPotential instance."""
        config = PotentialConfig()
        result = build_halo(config)
        assert result is mock_nfw.return_value


class TestBuildAxiSymmetric:
    """Tests for axisymmetric potential builder."""

    @patch("symmetries.potentials.NFWPotential")
    @patch("symmetries.potentials.MiyamotoNagaiPotential")
    @patch("symmetries.potentials.HernquistPotential")
    def test_returns_three_components(self, mock_hp: MagicMock, mock_mn: MagicMock, mock_nfw: MagicMock) -> None:
        """Verify axisymmetric returns bulge, disk, and halo."""
        config = PotentialConfig()
        result = build_axisymmetric(config)
        assert len(result) == 3
        assert result[0] is mock_hp.return_value
        assert result[1] is mock_mn.return_value
        assert result[2] is mock_nfw.return_value


class TestBuildComposite:
    """Tests for composite potential builder."""

    @patch("symmetries.potentials.DehnenBarPotential")
    @patch("symmetries.potentials.NFWPotential")
    @patch("symmetries.potentials.MiyamotoNagaiPotential")
    @patch("symmetries.potentials.HernquistPotential")
    def test_returns_four_components(
        self,
        mock_hp: MagicMock,
        mock_mn: MagicMock,
        mock_nfw: MagicMock,
        mock_db: MagicMock,
    ) -> None:
        """Verify composite returns bulge, disk, halo, and bar components."""
        config = PotentialConfig()
        result = build_composite(config)
        assert len(result) == 4
        assert result[0] is mock_hp.return_value
        assert result[1] is mock_mn.return_value
        assert result[2] is mock_nfw.return_value
        assert result[3] is mock_db.return_value
