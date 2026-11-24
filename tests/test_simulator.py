"""Unit tests for network simulator.

Tests validate:
1. Simulation runs without errors
2. Spikes are recorded correctly
3. STDP is applied during simulation
4. External input is processed
"""

import numpy as np
import pytest

from dreammachine.neurons.izhikevich import IzhikevichPopulation, NeuronType
from dreammachine.plasticity.stdp import STDPSynapses, STDPParams, create_random_connectivity
from dreammachine.network.simulator import (
    NetworkSimulator,
    SimulationResult,
    create_network,
)


class TestSimulationResult:
    """Tests for SimulationResult dataclass."""

    @pytest.fixture
    def sample_result(self):
        """Create a sample simulation result."""
        return SimulationResult(
            spike_times=[np.array([10.0, 50.0]), np.array([30.0])],
            spike_indices=np.array([0, 1, 0], dtype=np.int32),
            spike_times_flat=np.array([10.0, 30.0, 50.0], dtype=np.float32),
            v_history=None,
            weight_history=None,
            duration_ms=100.0,
            dt=0.5,
            n_neurons=2,
        )

    def test_n_spikes(self, sample_result):
        """Total spike count is correct."""
        assert sample_result.n_spikes == 3

    def test_firing_rates(self, sample_result):
        """Firing rates computed correctly."""
        rates = sample_result.firing_rates
        # Neuron 0: 2 spikes in 100ms = 20 Hz
        # Neuron 1: 1 spike in 100ms = 10 Hz
        assert rates[0] == pytest.approx(20.0)
        assert rates[1] == pytest.approx(10.0)

    def test_mean_firing_rate(self, sample_result):
        """Mean firing rate is average of individual rates."""
        assert sample_result.mean_firing_rate == pytest.approx(15.0)

    def test_spike_raster(self, sample_result):
        """Spike raster data matches input."""
        times, neurons = sample_result.get_spike_raster()
        assert len(times) == 3
        assert len(neurons) == 3


class TestNetworkSimulator:
    """Tests for NetworkSimulator class."""

    @pytest.fixture
    def simple_network(self):
        """Create small test network."""
        neurons = IzhikevichPopulation(10, NeuronType.RS)
        conn = create_random_connectivity(10, 10, density=0.2, w_init=5.0)
        synapses = STDPSynapses(
            10, 10, connectivity=conn, params=STDPParams(w_max=10.0)
        )
        return NetworkSimulator(neurons, synapses)

    def test_run_completes(self, simple_network):
        """Simulation runs to completion."""
        result = simple_network.run(100.0, dt=0.5)
        assert isinstance(result, SimulationResult)
        assert result.duration_ms == 100.0

    def test_run_with_external_input_array(self, simple_network):
        """External input from array works."""
        n_steps = 200  # 100ms at dt=0.5
        I_ext = np.ones((n_steps, 10), dtype=np.float32) * 15.0

        result = simple_network.run(100.0, dt=0.5, I_ext=I_ext)
        assert result.n_spikes > 0, "Should have spikes with input"

    def test_run_with_external_input_callable(self, simple_network):
        """External input from callable works."""
        def I_func(t):
            return np.full(10, 15.0, dtype=np.float32)

        result = simple_network.run(100.0, dt=0.5, I_ext=I_func)
        assert result.n_spikes > 0, "Should have spikes with input"

    def test_record_voltage(self):
        """Voltage recording works."""
        neurons = IzhikevichPopulation(5, NeuronType.RS)
        sim = NetworkSimulator(neurons, record_v=True)

        result = sim.run(50.0, dt=0.5)

        assert result.v_history is not None
        assert result.v_history.shape == (100, 5)  # 50ms / 0.5ms = 100 steps

    def test_record_weights(self):
        """Weight recording works."""
        neurons = IzhikevichPopulation(10, NeuronType.RS)
        conn = create_random_connectivity(10, 10, density=0.2)
        synapses = STDPSynapses(10, 10, connectivity=conn)
        sim = NetworkSimulator(neurons, synapses, record_weights=True,
                              weight_record_interval=10.0)

        result = sim.run(100.0, dt=0.5)

        assert result.weight_history is not None
        assert len(result.weight_history) >= 9  # At least 9 snapshots in 100ms

    def test_stdp_modifies_weights(self):
        """STDP changes weights during simulation."""
        rng = np.random.default_rng(42)
        neurons = IzhikevichPopulation(20, NeuronType.RS, rng=rng)
        conn = create_random_connectivity(20, 20, density=0.3, w_init=0.5, rng=rng)
        synapses = STDPSynapses(20, 20, connectivity=conn,
                               params=STDPParams(A_plus=0.05, A_minus=-0.06))
        sim = NetworkSimulator(neurons, synapses)

        initial_weights = synapses.weights.data.copy()

        # Run with input to generate spikes
        def I_func(t):
            return rng.uniform(10, 20, 20).astype(np.float32)

        sim.run(500.0, dt=0.5, I_ext=I_func)

        final_weights = synapses.weights.data

        # At least some weights should change
        assert not np.allclose(initial_weights, final_weights), \
            "Weights should change during STDP"

    def test_reset(self, simple_network):
        """Reset restores initial state."""
        # Run simulation
        def I_func(t):
            return np.full(10, 15.0, dtype=np.float32)

        simple_network.run(100.0, I_ext=I_func)

        # Reset
        simple_network.reset()

        # Check neurons reset
        assert np.allclose(simple_network.neurons.v, -65.0)

    def test_no_synapses(self):
        """Simulator works without synapses."""
        neurons = IzhikevichPopulation(10, NeuronType.RS)
        sim = NetworkSimulator(neurons, synapses=None)

        result = sim.run(50.0)
        assert result.n_neurons == 10


class TestCreateNetwork:
    """Tests for create_network convenience function."""

    def test_creates_all_components(self):
        """Function creates neurons, synapses, and simulator."""
        neurons, synapses, sim = create_network(100)

        assert neurons.n == 100
        assert synapses.n_pre == 100
        assert synapses.n_post == 100
        assert isinstance(sim, NetworkSimulator)

    def test_neuron_type(self):
        """Neuron type is applied."""
        neurons, _, _ = create_network(50, neuron_type=NeuronType.FS)
        # FS has a=0.1
        assert neurons.a[0] == pytest.approx(0.1, rel=0.1)

    def test_connectivity_density(self):
        """Connectivity density is approximately correct."""
        _, synapses, _ = create_network(100, connectivity_density=0.05)
        actual = synapses.weights.nnz / (100 * 100)
        assert 0.03 < actual < 0.07

    def test_reproducible_with_rng(self):
        """Results reproducible with same RNG seed."""
        n1, s1, _ = create_network(50, rng=np.random.default_rng(123))
        n2, s2, _ = create_network(50, rng=np.random.default_rng(123))

        assert np.allclose(n1.a, n2.a)
        assert np.allclose(s1.weights.data, s2.weights.data)


class TestIntegration:
    """Integration tests for full simulation pipeline."""

    def test_small_network_simulation(self):
        """Complete simulation of small network."""
        rng = np.random.default_rng(42)
        neurons, synapses, sim = create_network(
            n_neurons=50,
            neuron_type=NeuronType.RS,
            connectivity_density=0.1,
            w_init=10.0,
            stdp_params=STDPParams(w_min=0.0, w_max=20.0),
            heterogeneous=True,
            rng=rng,
        )

        # Tonic input to subset
        def I_ext(t):
            I = np.zeros(50, dtype=np.float32)
            I[:10] = 15.0  # Drive first 10 neurons
            return I

        result = sim.run(500.0, dt=0.5, I_ext=I_ext)

        # Should have activity
        assert result.n_spikes > 0
        # Driven neurons should fire more
        driven_rates = result.firing_rates[:10].mean()
        other_rates = result.firing_rates[10:].mean()
        assert driven_rates > other_rates, "Driven neurons should fire more"

    def test_performance_1000_neurons(self):
        """Performance test: 1000 neurons for 100ms."""
        import time

        neurons, synapses, sim = create_network(
            n_neurons=1000,
            connectivity_density=0.02,  # 2% = ~20000 synapses
            rng=np.random.default_rng(42),
        )

        def I_ext(t):
            return np.random.randn(1000).astype(np.float32) * 3 + 8

        start = time.perf_counter()
        result = sim.run(100.0, dt=0.5, I_ext=I_ext)
        elapsed = time.perf_counter() - start

        print(f"\n1000 neurons, 100ms: {elapsed:.3f}s, {result.n_spikes} spikes")

        # Should complete in reasonable time (not a hard requirement in tests)
        # This is informational only
        assert result.duration_ms == 100.0
