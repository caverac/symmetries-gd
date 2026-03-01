"""Tests for the CLI entry point."""

from __future__ import annotations

import argparse
from unittest.mock import MagicMock, patch

from symmetries.cli import build_parser, main, run


class TestBuildParser:
    def test_defaults(self) -> None:
        parser = build_parser()
        args = parser.parse_args([])
        assert args.n_particles == 10
        assert args.r_min == 0.1
        assert args.r_max == 0.3
        assert args.t_end == 2.0
        assert args.n_steps == 100
        assert args.delta == 0.5
        assert args.seed == 42

    def test_custom_args(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["-n", "50", "--r-min", "0.2", "--seed", "99"])
        assert args.n_particles == 50
        assert args.r_min == 0.2
        assert args.seed == 99


class TestRun:
    @patch("symmetries.cli.compare_variances")
    @patch("symmetries.cli.compute_invariants")
    def test_calls_pipeline(self, mock_compute: MagicMock, mock_compare: MagicMock) -> None:
        import numpy as np
        from symmetries._types import InvariantResult, PhasePoint, VarianceComparison

        mock_result = InvariantResult(
            c2=np.ones((2, 10)),
            jr=np.ones((2, 10)),
            time=np.linspace(0, 1, 10),
            phase=PhasePoint(
                pos=np.zeros((2, 10, 3)),
                vel=np.zeros((2, 10, 3)),
                time=np.linspace(0, 1, 10),
            ),
        )
        mock_compute.return_value = mock_result
        mock_compare.return_value = VarianceComparison(
            var_c2=np.array([0.01, 0.02]),
            var_jr=np.array([1.0, 1.5]),
            ratio=np.array([0.01, 0.013]),
            median_ratio=0.012,
        )

        args = argparse.Namespace(
            n_particles=2,
            r_min=0.1,
            r_max=0.3,
            t_end=1.0,
            n_steps=10,
            delta=0.5,
            seed=42,
        )
        run(args)

        mock_compute.assert_called_once()
        mock_compare.assert_called_once_with(mock_result)


class TestMain:
    @patch("symmetries.cli.run")
    @patch("symmetries.cli.sys")
    def test_calls_run(self, mock_sys: MagicMock, mock_run: MagicMock) -> None:
        mock_sys.argv = ["symmetries", "-n", "5"]
        main()
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args.n_particles == 5
