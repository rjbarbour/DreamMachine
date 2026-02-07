"""Unit tests for Izhikevich neuron model.

Tests validate:
1. Correct firing patterns for different neuron types
2. Spike detection and reset mechanics
3. Vectorized vs Numba implementations match
4. Parameter heterogeneity
"""

import numpy as np
import pytest

from dreammachine.neurons.izhikevich import (
    IzhikevichPopulation,
    NeuronType,
    NeuronParams,
)


class TestNeuronParams:
    """Tests for NeuronParams dataclass."""

    def test_from_type_rs(self):
        """Regular Spiking parameters match literature."""
        params = NeuronParams.from_type(NeuronType.RS)
        assert params.a == pytest.approx(0.02)
        assert params.b == pytest.approx(0.2)
        assert params.c == pytest.approx(-65.0)
        assert params.d == pytest.approx(8.0)

    def test_from_type_fs(self):
        """Fast Spiking parameters match literature."""
        params = NeuronParams.from_type(NeuronType.FS)
        assert params.a == pytest.approx(0.1)
        assert params.d == pytest.approx(2.0)

    def test_all_types_have_params(self):
        """All NeuronType variants have defined parameters."""
        for ntype in NeuronType:
            params = NeuronParams.from_type(ntype)
            assert isinstance(params, NeuronParams)


class TestIzhikevichPopulation:
    """Tests for IzhikevichPopulation class."""

    def test_initialization(self):
        """Population initializes with correct dimensions."""
        pop = IzhikevichPopulation(100, NeuronType.RS)
        assert pop.n == 100
        assert pop.v.shape == (100,)
        assert pop.u.shape == (100,)
        assert pop.I.shape == (100,)

    def test_initial_state(self):
        """Initial membrane potential is at resting level."""
        pop = IzhikevichPopulation(10)
        assert np.allclose(pop.v, -65.0)

    def test_no_spontaneous_spikes(self):
        """Neurons at rest don't spike without input."""
        pop = IzhikevichPopulation(100, NeuronType.RS)
        for _ in range(100):
            spikes = pop.step(dt=0.5)
            assert not spikes.any(), "Spontaneous spike without input"

    def test_spikes_with_strong_input(self):
        """Neurons spike with sufficient input current."""
        pop = IzhikevichPopulation(10, NeuronType.RS)
        pop.I[:] = 20.0  # Strong input current

        # Run for 100ms
        total_spikes = 0
        for _ in range(200):
            spikes = pop.step(dt=0.5)
            total_spikes += spikes.sum()

        assert total_spikes > 0, "No spikes with strong input"

    def test_spike_reset(self):
        """Membrane potential resets after spike."""
        pop = IzhikevichPopulation(1, NeuronType.RS)
        pop.I[:] = 30.0

        # Run until spike
        for _ in range(1000):
            spikes = pop.step(dt=0.5)
            if spikes[0]:
                # Check reset
                assert pop.v[0] < 0, "v not reset after spike"
                break
        else:
            pytest.fail("No spike detected in 500ms")

    def test_recovery_variable_increases_on_spike(self):
        """Recovery variable u increases on spike."""
        pop = IzhikevichPopulation(1, NeuronType.RS)
        pop.I[:] = 25.0

        initial_u = pop.u[0].copy()
        for _ in range(1000):
            spikes = pop.step(dt=0.5)
            if spikes[0]:
                assert pop.u[0] > initial_u, "u didn't increase after spike"
                break

    def test_fs_faster_than_rs(self):
        """Fast Spiking neurons fire faster than Regular Spiking."""
        rng = np.random.default_rng(42)

        pop_rs = IzhikevichPopulation(10, NeuronType.RS, rng=rng)
        pop_fs = IzhikevichPopulation(10, NeuronType.FS, rng=rng)

        pop_rs.I[:] = 15.0
        pop_fs.I[:] = 15.0

        spikes_rs = 0
        spikes_fs = 0

        for _ in range(400):  # 200ms
            spikes_rs += pop_rs.step(dt=0.5).sum()
            spikes_fs += pop_fs.step(dt=0.5).sum()

        assert spikes_fs >= spikes_rs, "FS should fire at least as fast as RS"

    def test_heterogeneous_parameters(self):
        """Heterogeneous populations have varying parameters."""
        pop = IzhikevichPopulation(100, NeuronType.RS, heterogeneous=True, rng=np.random.default_rng(42))

        # Parameters should not all be identical
        assert pop.a.std() > 0, "Parameters should vary"
        assert pop.b.std() > 0
        assert pop.c.std() > 0
        assert pop.d.std() > 0

    def test_homogeneous_parameters(self):
        """Homogeneous populations have identical parameters."""
        pop = IzhikevichPopulation(100, NeuronType.RS, heterogeneous=False)

        # All parameters should be identical (std ~= 0, allowing float32 precision)
        assert pop.a.std() < 1e-6, "Parameters should be identical"
        assert pop.b.std() < 1e-6
        assert pop.c.std() < 1e-6
        assert pop.d.std() < 1e-6

    def test_reset(self):
        """Reset returns neurons to initial state."""
        pop = IzhikevichPopulation(10, NeuronType.RS)
        pop.I[:] = 20.0

        # Run and accumulate state changes
        for _ in range(100):
            pop.step(dt=0.5)

        pop.reset()

        assert np.allclose(pop.v, -65.0)
        assert np.allclose(pop.I, 0.0)

    def test_dtype_float32(self):
        """Arrays use float32 for memory efficiency."""
        pop = IzhikevichPopulation(100)
        assert pop.v.dtype == np.float32
        assert pop.u.dtype == np.float32
        assert pop.I.dtype == np.float32

    def test_step_returns_bool_array(self):
        """Step returns boolean spike array."""
        pop = IzhikevichPopulation(10)
        spikes = pop.step()
        assert spikes.dtype == np.bool_
        assert spikes.shape == (10,)


class TestNeuronFiringPatterns:
    """Validation tests comparing to Izhikevich (2003) Figure 2."""

    def test_rs_tonic_spiking(self):
        """Regular Spiking produces tonic spiking with constant input."""
        pop = IzhikevichPopulation(1, NeuronType.RS)
        pop.I[:] = 14.0  # Moderate input

        spike_times = []
        for step in range(2000):  # 1000ms
            spikes = pop.step(dt=0.5)
            if spikes[0]:
                spike_times.append(step * 0.5)

        # Should have regular spikes
        assert len(spike_times) >= 5, "Should have multiple spikes"

        # Check regularity (ISIs should be similar)
        if len(spike_times) >= 3:
            isis = np.diff(spike_times)
            cv = isis.std() / isis.mean()  # Coefficient of variation
            assert cv < 0.3, f"Irregular spiking, CV={cv}"

    def test_fs_no_adaptation(self):
        """Fast Spiking shows minimal spike frequency adaptation."""
        pop = IzhikevichPopulation(1, NeuronType.FS)
        pop.I[:] = 10.0

        spike_times = []
        for step in range(2000):
            spikes = pop.step(dt=0.5)
            if spikes[0]:
                spike_times.append(step * 0.5)

        if len(spike_times) >= 6:
            isis = np.diff(spike_times)
            # Early vs late ISIs should be similar (no adaptation)
            early_isi = np.mean(isis[:3])
            late_isi = np.mean(isis[-3:])
            ratio = late_isi / early_isi
            assert 0.8 < ratio < 1.5, f"Too much adaptation, ratio={ratio}"


class TestNumpyNumbaEquivalence:
    """Verify NumPy and Numba implementations produce same results."""

    def test_step_equivalence(self):
        """NumPy and Numba produce identical results."""
        rng = np.random.default_rng(42)

        # Create two identical populations
        pop_np = IzhikevichPopulation(100, NeuronType.RS, rng=rng)
        pop_nb = IzhikevichPopulation(100, NeuronType.RS, rng=np.random.default_rng(42))

        # Force NumPy path
        pop_np._use_numba = False

        # Set same input
        I = rng.uniform(5, 15, 100).astype(np.float32)
        pop_np.I[:] = I
        pop_nb.I[:] = I.copy()

        # Run several steps
        for _ in range(100):
            spikes_np = pop_np._step_numpy(0.5)
            spikes_nb = pop_nb.step(0.5)

            # Results should match closely (rtol=1e-3 for float32 with fastmath/parallel)
            assert np.allclose(pop_np.v, pop_nb.v, rtol=1e-3, atol=0.01)
            assert np.allclose(pop_np.u, pop_nb.u, rtol=1e-3, atol=0.01)
