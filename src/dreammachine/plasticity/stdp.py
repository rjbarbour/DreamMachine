"""Spike-Timing-Dependent Plasticity (STDP) implementation.

Based on:
- Bi, G. & Poo, M. (1998). "Synaptic modifications in cultured hippocampal neurons."
- Song, S. et al. (2000). "Competitive Hebbian learning through STDP."

Uses trace-based implementation for O(1) computational complexity per spike.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

import numpy as np
from numpy.typing import NDArray
from scipy import sparse

try:
    from numba import jit
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    def jit(*args, **kwargs):  # noqa: D103
        def decorator(func):
            return func
        return decorator


@dataclass
class STDPParams:
    """STDP learning rule parameters.

    Implements exponential STDP window:
        Δw = A+ * exp(-Δt/τ+) if Δt > 0 (pre before post, LTP)
        Δw = A- * exp(Δt/τ-)  if Δt < 0 (post before pre, LTD)

    Attributes
    ----------
    tau_plus : float
        LTP time constant (ms). Default 20.0ms from Bi & Poo.
    tau_minus : float
        LTD time constant (ms). Default 20.0ms.
    A_plus : float
        LTP amplitude (positive). Default 0.01.
    A_minus : float
        LTD amplitude (negative). Default -0.012 for slight LTD dominance.
    w_min : float
        Minimum synaptic weight. Default 0.0.
    w_max : float
        Maximum synaptic weight. Default 1.0.
    """

    tau_plus: float = 20.0
    tau_minus: float = 20.0
    A_plus: float = 0.01
    A_minus: float = -0.012
    w_min: float = 0.0
    w_max: float = 1.0

    def __post_init__(self) -> None:
        """Validate parameters."""
        if self.tau_plus <= 0 or self.tau_minus <= 0:
            raise ValueError("Time constants must be positive")
        if self.A_plus <= 0:
            raise ValueError("A_plus must be positive for LTP")
        if self.A_minus >= 0:
            raise ValueError("A_minus must be negative for LTD")
        if self.w_min >= self.w_max:
            raise ValueError("w_min must be less than w_max")


@jit(nopython=True, cache=True, fastmath=True)
def _decay_traces(traces: NDArray[np.float32], decay: float) -> None:
    """In-place exponential decay of eligibility traces."""
    traces *= decay


@jit(nopython=True, cache=True)
def _apply_stdp_on_post_spike(
    post_idx: int,
    pre_indices: NDArray[np.int32],
    pre_traces: NDArray[np.float32],
    weights_data: NDArray[np.float32],
    weight_indices: NDArray[np.int32],
    A_plus: float,
    w_max: float,
) -> None:
    """Apply LTP for all presynaptic connections to a spiking post neuron."""
    for i, pre_idx in enumerate(pre_indices):
        # LTP: pre fired before post
        dw = A_plus * pre_traces[pre_idx]
        new_w = weights_data[weight_indices[i]] + dw
        weights_data[weight_indices[i]] = min(new_w, w_max)


@jit(nopython=True, cache=True)
def _apply_stdp_on_pre_spike(
    pre_idx: int,
    post_indices: NDArray[np.int32],
    post_traces: NDArray[np.float32],
    weights_data: NDArray[np.float32],
    weight_indices: NDArray[np.int32],
    A_minus: float,
    w_min: float,
) -> None:
    """Apply LTD for all postsynaptic connections from a spiking pre neuron."""
    for i, post_idx in enumerate(post_indices):
        # LTD: pre fired after post
        dw = A_minus * post_traces[post_idx]
        new_w = weights_data[weight_indices[i]] + dw
        weights_data[weight_indices[i]] = max(new_w, w_min)


class STDPSynapses:
    """Trace-based STDP synaptic plasticity.

    Implements efficient all-to-all STDP using eligibility traces that
    decay exponentially between spikes. Updates are O(1) per spike.

    Parameters
    ----------
    n_pre : int
        Number of presynaptic neurons.
    n_post : int
        Number of postsynaptic neurons.
    connectivity : sparse.csr_matrix | None
        Sparse connectivity matrix (pre x post). If None, creates empty.
    params : STDPParams | None
        STDP parameters. If None, uses defaults.

    Attributes
    ----------
    weights : sparse.csr_matrix
        Synaptic weight matrix (pre x post), CSR format for efficiency.
    pre_trace : ndarray
        Presynaptic eligibility traces, shape (n_pre,).
    post_trace : ndarray
        Postsynaptic eligibility traces, shape (n_post,).

    Examples
    --------
    >>> # Create random sparse connectivity
    >>> conn = sparse.random(100, 100, density=0.1, format='csr')
    >>> conn.data[:] = 0.5  # Initialize weights to 0.5
    >>> synapses = STDPSynapses(100, 100, connectivity=conn)
    >>> synapses.update_traces(dt=0.5)
    >>> synapses.on_post_spikes(np.array([0, 5, 10]))
    """

    def __init__(
        self,
        n_pre: int,
        n_post: int,
        connectivity: Optional[sparse.csr_matrix] = None,
        params: Optional[STDPParams] = None,
    ) -> None:
        """Initialize STDP synapses."""
        self.n_pre = n_pre
        self.n_post = n_post
        self.params = params or STDPParams()

        # Initialize weight matrix
        if connectivity is not None:
            self.weights = connectivity.astype(np.float32)
            if not isinstance(self.weights, sparse.csr_matrix):
                self.weights = self.weights.tocsr()
        else:
            self.weights = sparse.csr_matrix(
                (n_pre, n_post), dtype=np.float32
            )

        # Transpose for efficient post->pre lookups
        self._weights_csc = self.weights.tocsc()

        # Initialize eligibility traces
        self.pre_trace = np.zeros(n_pre, dtype=np.float32)
        self.post_trace = np.zeros(n_post, dtype=np.float32)

        # Precompute decay factors
        self._decay_pre = 0.0  # Set in update_traces based on dt
        self._decay_post = 0.0
        self._last_dt = 0.0

        self._use_numba = NUMBA_AVAILABLE

    def update_traces(self, dt: float) -> None:
        """Decay eligibility traces by one timestep.

        Parameters
        ----------
        dt : float
            Timestep in milliseconds.
        """
        # Recompute decay if dt changed
        if dt != self._last_dt:
            self._decay_pre = np.exp(-dt / self.params.tau_plus).astype(np.float32)
            self._decay_post = np.exp(-dt / self.params.tau_minus).astype(np.float32)
            self._last_dt = dt

        # Apply exponential decay
        if self._use_numba:
            _decay_traces(self.pre_trace, self._decay_pre)
            _decay_traces(self.post_trace, self._decay_post)
        else:
            self.pre_trace *= self._decay_pre
            self.post_trace *= self._decay_post

    def on_pre_spikes(self, spike_indices: NDArray[np.int64]) -> None:
        """Process presynaptic spikes.

        Updates pre traces and applies LTD to relevant synapses.

        Parameters
        ----------
        spike_indices : ndarray
            Indices of neurons that spiked.
        """
        if len(spike_indices) == 0:
            return

        # Update pre-synaptic traces (all-to-all: add 1 on spike)
        self.pre_trace[spike_indices] += 1.0

        # Apply LTD: for each pre spike, depress synapses to post neurons
        # that fired recently (have nonzero post_trace)
        for pre_idx in spike_indices:
            # Get post-synaptic targets of this pre neuron
            start, end = self.weights.indptr[pre_idx], self.weights.indptr[pre_idx + 1]
            if start == end:
                continue

            post_indices = self.weights.indices[start:end]
            weight_indices = np.arange(start, end, dtype=np.int32)

            if self._use_numba:
                _apply_stdp_on_pre_spike(
                    pre_idx, post_indices.astype(np.int32),
                    self.post_trace, self.weights.data,
                    weight_indices, self.params.A_minus, self.params.w_min
                )
            else:
                # NumPy fallback
                dw = self.params.A_minus * self.post_trace[post_indices]
                self.weights.data[start:end] = np.clip(
                    self.weights.data[start:end] + dw,
                    self.params.w_min, self.params.w_max
                )

    def on_post_spikes(self, spike_indices: NDArray[np.int64]) -> None:
        """Process postsynaptic spikes.

        Updates post traces and applies LTP to relevant synapses.

        Parameters
        ----------
        spike_indices : ndarray
            Indices of neurons that spiked.
        """
        if len(spike_indices) == 0:
            return

        # Update post-synaptic traces
        self.post_trace[spike_indices] += 1.0

        # Apply LTP: for each post spike, potentiate synapses from pre neurons
        # that fired recently (have nonzero pre_trace)
        for post_idx in spike_indices:
            # Get pre-synaptic sources for this post neuron (using CSC)
            start = self._weights_csc.indptr[post_idx]
            end = self._weights_csc.indptr[post_idx + 1]
            if start == end:
                continue

            pre_indices = self._weights_csc.indices[start:end]

            # Find corresponding positions in CSR data array
            for pre_idx in pre_indices:
                # Find position in CSR
                row_start = self.weights.indptr[pre_idx]
                row_end = self.weights.indptr[pre_idx + 1]
                col_pos = np.searchsorted(
                    self.weights.indices[row_start:row_end], post_idx
                )
                data_idx = row_start + col_pos

                # Apply LTP
                dw = self.params.A_plus * self.pre_trace[pre_idx]
                new_w = self.weights.data[data_idx] + dw
                self.weights.data[data_idx] = min(new_w, self.params.w_max)

    def on_spikes(
        self,
        pre_spikes: NDArray[np.bool_],
        post_spikes: NDArray[np.bool_],
    ) -> None:
        """Process spikes from both populations.

        Convenience method when pre and post populations are the same
        or when processing in a single call.

        Parameters
        ----------
        pre_spikes : ndarray of bool
            Boolean spike mask for presynaptic population.
        post_spikes : ndarray of bool
            Boolean spike mask for postsynaptic population.
        """
        pre_indices = np.where(pre_spikes)[0]
        post_indices = np.where(post_spikes)[0]

        # Order matters: process pre first (LTD), then post (LTP)
        self.on_pre_spikes(pre_indices)
        self.on_post_spikes(post_indices)

    def compute_input(self, pre_spikes: NDArray[np.bool_]) -> NDArray[np.float32]:
        """Compute synaptic input current from presynaptic spikes.

        Parameters
        ----------
        pre_spikes : ndarray of bool
            Boolean mask of spiking presynaptic neurons.

        Returns
        -------
        I_syn : ndarray
            Synaptic input current to each postsynaptic neuron.
        """
        # Sparse matrix-vector multiply: sum of weights from spiking neurons
        return self.weights.T.dot(pre_spikes.astype(np.float32))

    def get_weight_stats(self) -> dict:
        """Get statistics about current weight distribution."""
        if self.weights.nnz == 0:
            return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "nnz": 0}

        return {
            "mean": float(self.weights.data.mean()),
            "std": float(self.weights.data.std()),
            "min": float(self.weights.data.min()),
            "max": float(self.weights.data.max()),
            "nnz": self.weights.nnz,
        }

    def reset_traces(self) -> None:
        """Reset all eligibility traces to zero."""
        self.pre_trace[:] = 0.0
        self.post_trace[:] = 0.0

    def sync_transpose(self) -> None:
        """Synchronize CSC transpose with CSR weights after modifications."""
        self._weights_csc = self.weights.tocsc()

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"STDPSynapses(n_pre={self.n_pre}, n_post={self.n_post}, "
            f"synapses={self.weights.nnz})"
        )


def create_random_connectivity(
    n_pre: int,
    n_post: int,
    density: float,
    w_init: float = 0.5,
    rng: Optional[np.random.Generator] = None,
) -> sparse.csr_matrix:
    """Create random sparse connectivity matrix.

    Parameters
    ----------
    n_pre : int
        Number of presynaptic neurons.
    n_post : int
        Number of postsynaptic neurons.
    density : float
        Connection probability (0 to 1).
    w_init : float
        Initial weight value for all connections.
    rng : Generator | None
        Random number generator.

    Returns
    -------
    connectivity : csr_matrix
        Sparse connectivity matrix with uniform initial weights.
    """
    rng = rng or np.random.default_rng()

    # Generate random connectivity
    conn = sparse.random(
        n_pre, n_post,
        density=density,
        format='csr',
        dtype=np.float32,
        random_state=rng.integers(0, 2**31),
    )

    # Set all nonzero entries to initial weight
    conn.data[:] = w_init

    return conn
