"""Network construction for the spnet.m replication.

Random numbers come from ``numpy.random.Generator`` only; MATLAB's random
stream is not reproduced.  All indices are zero-based.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

STEPS_PER_SECOND = 1000


@dataclass(frozen=True)
class SpnetParams:
    Ne: int = 800
    Ni: int = 200
    M: int = 100  # synapses per neuron
    D: int = 20  # maximal conduction delay (ms)
    sm: float = 10.0
    w_exc: float = 6.0
    w_inh: float = -5.0
    a_exc: float = 0.02
    d_exc: float = 8.0
    a_inh: float = 0.1
    d_inh: float = 2.0
    b: float = 0.2
    c: float = -65.0
    input_current: float = 20.0
    trace_amp: float = 0.1
    ltd_factor: float = 1.2
    trace_decay: float = 0.95
    sd_decay: float = 0.9
    w_drift: float = 0.01

    @property
    def N(self) -> int:
        return self.Ne + self.Ni


@dataclass
class SpnetNetwork:
    post: np.ndarray  # (N, M) int32 targets
    delay: np.ndarray  # (N, M) int32 delays in 1..D
    s: np.ndarray  # (N, M) float64 initial weights
    a: np.ndarray  # (N,) float64
    d: np.ndarray  # (N,) float64


@dataclass
class SpnetResult:
    spike_time: np.ndarray  # int64 global ms index, detection order
    spike_neuron: np.ndarray  # int32
    s: np.ndarray
    sd: np.ndarray
    v: np.ndarray
    u: np.ndarray


def build_network(params: SpnetParams, rng: np.random.Generator) -> SpnetNetwork:
    Ne, Ni, M, D, N = params.Ne, params.Ni, params.M, params.D, params.N
    if M > Ne or M > N:
        raise ValueError("M must not exceed Ne (inhibitory targets are excitatory)")
    post = np.empty((N, M), dtype=np.int32)
    delay = np.ones((N, M), dtype=np.int32)
    for i in range(Ne):
        post[i] = rng.permutation(N)[:M]
        delay[i] = rng.integers(1, D + 1, size=M)
    for i in range(Ne, N):
        post[i] = rng.permutation(Ne)[:M]
    s = np.empty((N, M), dtype=np.float64)
    s[:Ne] = params.w_exc
    s[Ne:] = params.w_inh
    a = np.concatenate([np.full(Ne, params.a_exc), np.full(Ni, params.a_inh)])
    d = np.concatenate([np.full(Ne, params.d_exc), np.full(Ni, params.d_inh)])
    return SpnetNetwork(post=post, delay=delay, s=s, a=a, d=d)


def make_inputs(params: SpnetParams, seconds: int, rng: np.random.Generator) -> np.ndarray:
    """Index of the neuron receiving ``input_current`` in each millisecond."""
    return rng.integers(0, params.N, size=(seconds, STEPS_PER_SECOND), dtype=np.int32)
