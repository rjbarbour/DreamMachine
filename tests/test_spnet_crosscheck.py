"""Exact cross-check against the original spnet.m run under GNU Octave (small network)."""

import importlib.util
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "crosscheck_original.py"
SPNET_M = ROOT / "references" / "cache" / "izhikevich.org" / "spnet.m"


def test_small_network_matches_original_spnet_m():
    if shutil.which("octave") is None:
        pytest.skip("octave not on PATH")
    if not SPNET_M.exists():
        pytest.skip("cached spnet.m absent")
    spec = importlib.util.spec_from_file_location("crosscheck_original", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rec = mod.crosscheck(Ne=40, Ni=10, M=10, D=5, seconds=3, seed=1, timeout=600)
    assert rec["octave_spikes"] > 0
    for name in ("oracle", "kernel"):
        assert rec[name]["spikes_exact"], rec[name]
        assert rec[name]["s_bit_identical"], rec[name]
        assert rec[name]["max_abs_ds"] == 0.0
