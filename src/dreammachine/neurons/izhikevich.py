"""Izhikevich spiking neuron model implementation.

Based on: Izhikevich, E.M. (2003). "Simple model of spiking neurons."
IEEE Transactions on Neural Networks, 14(6):1569-1572.

The model combines computational efficiency with biological plausibility,
using only 13 FLOPs per neuron per ms while reproducing 20+ firing patterns.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

import numpy as np
from numpy.typing import NDArray

# Numba import with fallback for environments without JIT
try:
    from numba import jit, prange
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    def jit(*args, **kwargs):  # noqa: D103
        def decorator(func):
            return func
        return decorator
    prange = range


class NeuronType(Enum):
    """Standard Izhikevich neuron types with canonical parameters.

    Parameters (a, b, c, d) from Izhikevich (2003) Figure 2.
    """

    # Excitatory types
    RS = "regular_spiking"       # Regular Spiking (most common excitatory)
    IB = "intrinsically_bursting"
    CH = "chattering"

    # Inhibitory types
    FS = "fast_spiking"          # Fast Spiking (common inhibitory)
    LTS = "low_threshold_spiking"

    # Thalamic types
    TC = "thalamocortical"
    RZ = "resonator"


@dataclass(frozen=True)
class NeuronParams:
    """Izhikevich neuron parameters.

    Attributes
    ----------
    a : float
        Time scale of recovery variable u. Smaller values = slower recovery.
        Typical range: 0.02 (RS) to 0.1 (FS).
    b : float
        Sensitivity of u to subthreshold fluctuations.
        Typical range: 0.2 to 0.26.
    c : float
        After-spike reset value of v (mV).
        Typical range: -65 to -50.
    d : float
        After-spike increment of u.
        Typical range: 0.05 to 8.
    """

    a: float
    b: float
    c: float
    d: float

    @classmethod
    def from_type(cls, neuron_type: NeuronType) -> NeuronParams:
        """Create parameters from a standard neuron type."""
        params = {
            NeuronType.RS: cls(a=0.02, b=0.2, c=-65.0, d=8.0),
            NeuronType.IB: cls(a=0.02, b=0.2, c=-55.0, d=4.0),
            NeuronType.CH: cls(a=0.02, b=0.2, c=-50.0, d=2.0),
            NeuronType.FS: cls(a=0.1, b=0.2, c=-65.0, d=2.0),
            NeuronType.LTS: cls(a=0.02, b=0.25, c=-65.0, d=2.0),
            NeuronType.TC: cls(a=0.02, b=0.25, c=-65.0, d=0.05),
            NeuronType.RZ: cls(a=0.1, b=0.26, c=-65.0, d=2.0),
        }
        return params[neuron_type]


# JIT-compiled core update function for maximum performance
@jit(nopython=True, parallel=True, cache=True, fastmath=False)
def _step_numba(
    v: NDArray[np.float32],
    u: NDArray[np.float32],
    a: NDArray[np.float32],
    b: NDArray[np.float32],
    c: NDArray[np.float32],
    d: NDArray[np.float32],
    I: NDArray[np.float32],
    dt: float,
    v_thresh: float,
    v_peak: float,
) -> NDArray[np.bool_]:
    """JIT-compiled Izhikevich update step.

    Uses two half-steps of Euler integration for stability.
    """
    n = len(v)
    spikes = np.zeros(n, dtype=np.bool_)

    # All arithmetic is done in float32, mirroring _step_numpy. Bare Python
    # float literals/arguments are float64 in Numba and would silently promote
    # every intermediate to double precision, so cast them explicitly.
    f32 = np.float32
    k04 = f32(0.04)
    k5 = f32(5.0)
    k140 = f32(140.0)
    half_dt = f32(dt / 2.0)
    dt32 = f32(dt)
    thresh = f32(v_thresh)

    for i in prange(n):
        v_i = v[i]
        u_i = u[i]
        I_i = I[i]
        a_i = a[i]
        b_i = b[i]

        # Two half-steps (same operation order as _step_numpy)
        dv = k04 * (v_i * v_i) + k5 * v_i + k140 - u_i + I_i
        v_i = v_i + half_dt * dv
        dv = k04 * (v_i * v_i) + k5 * v_i + k140 - u_i + I_i
        v_i = v_i + half_dt * dv

        # Recovery variable update
        u_i = u_i + dt32 * a_i * (b_i * v_i - u_i)

        # Spike detection and reset
        if v_i >= thresh:
            spikes[i] = True
            v[i] = c[i]
            u[i] = u_i + d[i]
        else:
            v[i] = v_i
            u[i] = u_i

    return spikes


class IzhikevichPopulation:
    """Vectorized population of Izhikevich spiking neurons.

    This class efficiently simulates large populations of neurons using
    vectorized NumPy operations and optional Numba JIT compilation.

    Parameters
    ----------
    n : int
        Number of neurons in the population.
    params : NeuronParams | NeuronType | None
        Neuron parameters. If NeuronType, uses standard parameters.
        If None, defaults to Regular Spiking (RS).
    heterogeneous : bool
        If True, adds small random variations to parameters.
    v_init : float
        Initial membrane potential (mV). Default: -65.0 (resting).
    u_init : float | None
        Initial recovery variable. If None, uses b * v_init.
    rng : np.random.Generator | None
        Random number generator for heterogeneity. If None, creates new one.

    Attributes
    ----------
    v : ndarray
        Membrane potentials (mV), shape (n,).
    u : ndarray
        Recovery variables, shape (n,).
    I : ndarray
        Input currents, shape (n,). Set externally each step.

    Examples
    --------
    >>> pop = IzhikevichPopulation(1000, NeuronType.RS)
    >>> pop.I = np.random.randn(1000) * 5 + 10  # Random input
    >>> spikes = pop.step(dt=0.5)
    >>> print(f"Spikes: {spikes.sum()}")
    """

    V_THRESH: float = 30.0   # Spike threshold (mV)
    V_PEAK: float = 30.0     # Peak voltage for recording

    def __init__(
        self,
        n: int,
        params: Optional[NeuronParams | NeuronType] = None,
        heterogeneous: bool = False,
        v_init: float = -65.0,
        u_init: Optional[float] = None,
        rng: Optional[np.random.Generator] = None,
    ) -> None:
        """Initialize neuron population."""
        self.n = n
        self._rng = rng or np.random.default_rng()

        # Resolve parameters
        if params is None:
            params = NeuronParams.from_type(NeuronType.RS)
        elif isinstance(params, NeuronType):
            params = NeuronParams.from_type(params)

        # Initialize state arrays (float32 for memory efficiency)
        self.v = np.full(n, v_init, dtype=np.float32)
        self.u = np.full(
            n,
            u_init if u_init is not None else params.b * v_init,
            dtype=np.float32,
        )
        self.I = np.zeros(n, dtype=np.float32)

        # Initialize parameter arrays
        if heterogeneous:
            # Add ~5% variation to parameters
            noise = lambda x: x * (1.0 + 0.05 * self._rng.standard_normal(n))
            self.a = noise(params.a).astype(np.float32)
            self.b = noise(params.b).astype(np.float32)
            self.c = noise(params.c).astype(np.float32)
            self.d = noise(params.d).astype(np.float32)
        else:
            self.a = np.full(n, params.a, dtype=np.float32)
            self.b = np.full(n, params.b, dtype=np.float32)
            self.c = np.full(n, params.c, dtype=np.float32)
            self.d = np.full(n, params.d, dtype=np.float32)

        self._use_numba = NUMBA_AVAILABLE

    def step(self, dt: float = 0.5) -> NDArray[np.bool_]:
        """Advance simulation by one timestep.

        Parameters
        ----------
        dt : float
            Timestep in milliseconds. Default 0.5ms provides good accuracy.
            Use 1.0ms for faster but less accurate simulations.

        Returns
        -------
        spikes : ndarray of bool
            Boolean mask indicating which neurons spiked, shape (n,).
        """
        if self._use_numba:
            return _step_numba(
                self.v, self.u, self.a, self.b, self.c, self.d,
                self.I, dt, self.V_THRESH, self.V_PEAK
            )
        else:
            return self._step_numpy(dt)

    def _step_numpy(self, dt: float) -> NDArray[np.bool_]:
        """Pure NumPy implementation (fallback when Numba unavailable)."""
        # Two half-steps for stability
        # Python-float scalars are weak under NumPy 2 promotion, so everything
        # stays float32.
        dv = 0.04 * self.v**2 + 5.0 * self.v + 140.0 - self.u + self.I
        self.v += (dt / 2.0) * dv
        dv = 0.04 * self.v**2 + 5.0 * self.v + 140.0 - self.u + self.I
        self.v += (dt / 2.0) * dv

        # Recovery update
        self.u += dt * self.a * (self.b * self.v - self.u)

        # Spike detection and reset
        spikes = self.v >= self.V_THRESH
        self.v[spikes] = self.c[spikes]
        self.u[spikes] += self.d[spikes]

        return spikes

    def reset(self, v_init: float = -65.0) -> None:
        """Reset all neurons to initial state."""
        self.v[:] = v_init
        self.u[:] = self.b * v_init
        self.I[:] = 0.0

    @property
    def firing_rate(self) -> float:
        """Estimate instantaneous firing rate (requires external tracking)."""
        raise NotImplementedError("Use NetworkSimulator for firing rate tracking")

    def __repr__(self) -> str:
        """Return string representation."""
        return f"IzhikevichPopulation(n={self.n}, numba={self._use_numba})"
