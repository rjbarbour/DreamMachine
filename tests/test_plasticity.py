"""Unit tests for STDP plasticity.

Tests validate:
1. STDP weight changes follow exponential window
2. LTP when pre fires before post
3. LTD when post fires before pre
4. Weight bounds are respected
5. Trace dynamics are correct
"""

import numpy as np
import pytest
from scipy import sparse

from dreammachine.plasticity.stdp import (
    STDPSynapses,
    STDPParams,
    create_random_connectivity,
)


class TestSTDPParams:
    """Tests for STDPParams dataclass."""

    def test_default_values(self):
        """Default parameters are reasonable."""
        params = STDPParams()
        assert params.tau_plus == 20.0
        assert params.tau_minus == 20.0
        assert params.A_plus > 0
        assert params.A_minus < 0
        assert params.w_min < params.w_max

    def test_validation_tau(self):
        """Negative time constants raise error."""
        with pytest.raises(ValueError, match="Time constants"):
            STDPParams(tau_plus=-1.0)

    def test_validation_A_plus(self):
        """Negative A_plus raises error."""
        with pytest.raises(ValueError, match="A_plus"):
            STDPParams(A_plus=-0.01)

    def test_validation_A_minus(self):
        """Positive A_minus raises error."""
        with pytest.raises(ValueError, match="A_minus"):
            STDPParams(A_minus=0.01)

    def test_validation_bounds(self):
        """Invalid weight bounds raise error."""
        with pytest.raises(ValueError, match="w_min"):
            STDPParams(w_min=1.0, w_max=0.5)


class TestSTDPSynapses:
    """Tests for STDPSynapses class."""

    def test_initialization_empty(self):
        """Empty synapse matrix initializes correctly."""
        syn = STDPSynapses(100, 100)
        assert syn.n_pre == 100
        assert syn.n_post == 100
        assert syn.weights.nnz == 0

    def test_initialization_with_connectivity(self):
        """Connectivity matrix is stored correctly."""
        conn = sparse.random(50, 50, density=0.1, format='csr', dtype=np.float32)
        conn.data[:] = 0.5
        syn = STDPSynapses(50, 50, connectivity=conn)
        assert syn.weights.nnz == conn.nnz
        assert np.allclose(syn.weights.data, 0.5)

    def test_traces_initial_zero(self):
        """Eligibility traces start at zero."""
        syn = STDPSynapses(100, 100)
        assert np.all(syn.pre_trace == 0)
        assert np.all(syn.post_trace == 0)

    def test_trace_decay(self):
        """Traces decay exponentially."""
        syn = STDPSynapses(10, 10, params=STDPParams(tau_plus=20.0))
        syn.pre_trace[:] = 1.0
        syn.post_trace[:] = 1.0

        # After 20ms (one time constant), should be ~1/e
        for _ in range(40):
            syn.update_traces(0.5)

        expected = np.exp(-20.0 / 20.0)
        assert np.allclose(syn.pre_trace, expected, rtol=0.01)

    def test_pre_spike_increases_trace(self):
        """Presynaptic spike increases pre trace."""
        syn = STDPSynapses(10, 10)
        initial = syn.pre_trace[0]

        syn.on_pre_spikes(np.array([0]))

        assert syn.pre_trace[0] == initial + 1.0

    def test_post_spike_increases_trace(self):
        """Postsynaptic spike increases post trace."""
        syn = STDPSynapses(10, 10)
        initial = syn.post_trace[0]

        syn.on_post_spikes(np.array([0]))

        assert syn.post_trace[0] == initial + 1.0


class TestSTDPLearning:
    """Tests for STDP weight changes."""

    @pytest.fixture
    def simple_synapse(self):
        """Create simple 2-neuron network with single synapse."""
        # Pre neuron 0 -> Post neuron 1
        conn = sparse.csr_matrix(
            ([0.5], ([0], [1])),
            shape=(2, 2),
            dtype=np.float32
        )
        return STDPSynapses(2, 2, connectivity=conn, params=STDPParams())

    def test_ltp_pre_before_post(self, simple_synapse):
        """Weight increases when pre fires before post."""
        syn = simple_synapse
        initial_weight = syn.weights[0, 1]

        # Pre fires at t=0
        syn.on_pre_spikes(np.array([0]))

        # Small delay
        for _ in range(10):
            syn.update_traces(1.0)

        # Post fires at t=10
        syn.on_post_spikes(np.array([1]))

        final_weight = syn.weights[0, 1]
        assert final_weight > initial_weight, "LTP should increase weight"

    def test_ltd_post_before_pre(self, simple_synapse):
        """Weight decreases when post fires before pre."""
        syn = simple_synapse
        initial_weight = syn.weights[0, 1]

        # Post fires at t=0
        syn.on_post_spikes(np.array([1]))

        # Small delay
        for _ in range(10):
            syn.update_traces(1.0)

        # Pre fires at t=10
        syn.on_pre_spikes(np.array([0]))

        final_weight = syn.weights[0, 1]
        assert final_weight < initial_weight, "LTD should decrease weight"

    def test_larger_delay_smaller_change(self, simple_synapse):
        """Larger spike timing difference produces smaller weight change."""
        syn = simple_synapse

        # Test short delay
        syn.on_pre_spikes(np.array([0]))
        for _ in range(5):
            syn.update_traces(1.0)
        syn.on_post_spikes(np.array([1]))
        short_delay_change = syn.weights[0, 1] - 0.5

        # Reset
        syn.weights.data[:] = 0.5
        syn.reset_traces()

        # Test long delay
        syn.on_pre_spikes(np.array([0]))
        for _ in range(40):
            syn.update_traces(1.0)
        syn.on_post_spikes(np.array([1]))
        long_delay_change = syn.weights[0, 1] - 0.5

        assert abs(short_delay_change) > abs(long_delay_change), \
            "Shorter delay should produce larger change"

    def test_weight_upper_bound(self):
        """Weight does not exceed maximum."""
        conn = sparse.csr_matrix(
            ([0.99], ([0], [1])),
            shape=(2, 2),
            dtype=np.float32
        )
        syn = STDPSynapses(2, 2, connectivity=conn,
                          params=STDPParams(w_max=1.0, A_plus=0.1))

        # Many LTP events
        for _ in range(100):
            syn.on_pre_spikes(np.array([0]))
            syn.on_post_spikes(np.array([1]))

        assert syn.weights[0, 1] <= 1.0, "Weight exceeded maximum"

    def test_weight_lower_bound(self):
        """Weight does not go below minimum."""
        conn = sparse.csr_matrix(
            ([0.01], ([0], [1])),
            shape=(2, 2),
            dtype=np.float32
        )
        syn = STDPSynapses(2, 2, connectivity=conn,
                          params=STDPParams(w_min=0.0, A_minus=-0.1))

        # Many LTD events
        for _ in range(100):
            syn.on_post_spikes(np.array([1]))
            syn.on_pre_spikes(np.array([0]))

        assert syn.weights[0, 1] >= 0.0, "Weight went below minimum"


class TestSynapticTransmission:
    """Tests for synaptic input computation."""

    def test_compute_input(self):
        """Synaptic input is weighted sum of presynaptic spikes."""
        # Pre 0 -> Post 0 (w=0.3), Pre 0 -> Post 1 (w=0.7)
        conn = sparse.csr_matrix(
            np.array([[0.3, 0.7], [0.0, 0.0]], dtype=np.float32)
        )
        syn = STDPSynapses(2, 2, connectivity=conn)

        # Pre 0 spikes
        spikes = np.array([True, False])
        I_syn = syn.compute_input(spikes)

        assert np.allclose(I_syn, [0.3, 0.7])

    def test_no_spikes_no_input(self):
        """No input when no presynaptic spikes."""
        conn = sparse.random(10, 10, density=0.5, format='csr', dtype=np.float32)
        syn = STDPSynapses(10, 10, connectivity=conn)

        spikes = np.zeros(10, dtype=bool)
        I_syn = syn.compute_input(spikes)

        assert np.allclose(I_syn, 0.0)


class TestRandomConnectivity:
    """Tests for connectivity generation."""

    def test_create_random_connectivity_density(self):
        """Random connectivity has approximately correct density."""
        conn = create_random_connectivity(100, 100, density=0.1)
        actual_density = conn.nnz / (100 * 100)
        assert 0.08 < actual_density < 0.12  # Allow 20% deviation

    def test_create_random_connectivity_weights(self):
        """All weights initialized to specified value."""
        conn = create_random_connectivity(50, 50, density=0.2, w_init=0.3)
        assert np.allclose(conn.data, 0.3)

    def test_create_random_connectivity_sparse(self):
        """Result is CSR sparse matrix."""
        conn = create_random_connectivity(100, 100, density=0.1)
        assert isinstance(conn, sparse.csr_matrix)
        assert conn.dtype == np.float32
