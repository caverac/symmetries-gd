"""Tests for galpy potential construction."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from symmetries._types import PotentialConfig
from symmetries.potentials import build_axisymmetric, build_bar, build_composite, build_kepler, build_plummer


class TestBuildKepler:
    """Tests for Kepler potential builder."""

    @patch("symmetries.potentials.KeplerPotential")
    def test_calls_with_mass(self, mock_kp: MagicMock) -> None:
        """Verify KeplerPotential is called with configured SMBH mass."""
        config = PotentialConfig(smbh_mass=0.1)
        build_kepler(config)
        mock_kp.assert_called_once_with(amp=0.1)

    @patch("symmetries.potentials.KeplerPotential")
    def test_returns_instance(self, mock_kp: MagicMock) -> None:
        """Verify build_kepler returns the KeplerPotential instance."""
        config = PotentialConfig()
        result = build_kepler(config)
        assert result is mock_kp.return_value


class TestBuildPlummer:
    """Tests for Plummer potential builder."""

    @patch("symmetries.potentials.PlummerPotential")
    def test_calls_with_params(self, mock_pp: MagicMock) -> None:
        """Verify PlummerPotential is called with configured mass and scale."""
        config = PotentialConfig(plummer_mass=0.9, plummer_scale=0.5)
        build_plummer(config)
        mock_pp.assert_called_once_with(amp=0.9, b=0.5)

    @patch("symmetries.potentials.PlummerPotential")
    def test_returns_instance(self, mock_pp: MagicMock) -> None:
        """Verify build_plummer returns the PlummerPotential instance."""
        config = PotentialConfig()
        result = build_plummer(config)
        assert result is mock_pp.return_value


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


class TestBuildAxiSymmetric:
    """Tests for axisymmetric potential builder."""

    @patch("symmetries.potentials.PlummerPotential")
    @patch("symmetries.potentials.KeplerPotential")
    def test_returns_two_components(self, mock_kp: MagicMock, mock_pp: MagicMock) -> None:
        """Verify axisymmetric returns only Kepler and Plummer."""
        config = PotentialConfig()
        result = build_axisymmetric(config)
        assert len(result) == 2
        assert result[0] is mock_kp.return_value
        assert result[1] is mock_pp.return_value


class TestBuildComposite:
    """Tests for composite potential builder."""

    @patch("symmetries.potentials.DehnenBarPotential")
    @patch("symmetries.potentials.PlummerPotential")
    @patch("symmetries.potentials.KeplerPotential")
    def test_returns_three_components(
        self,
        mock_kp: MagicMock,
        mock_pp: MagicMock,
        mock_db: MagicMock,
    ) -> None:
        """Verify composite returns Kepler, Plummer, and bar components."""
        config = PotentialConfig()
        result = build_composite(config)
        assert len(result) == 3
        assert result[0] is mock_kp.return_value
        assert result[1] is mock_pp.return_value
        assert result[2] is mock_db.return_value
