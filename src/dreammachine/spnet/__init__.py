"""Replication of Izhikevich's spnet.m (spiking network with delays and STDP)."""

from .kernel import run_kernel
from .network import (
    SpnetNetwork,
    SpnetParams,
    SpnetResult,
    build_network,
    make_inputs,
)
from .oracle import run_oracle

__all__ = [
    "SpnetNetwork",
    "SpnetParams",
    "SpnetResult",
    "build_network",
    "make_inputs",
    "run_kernel",
    "run_oracle",
]
