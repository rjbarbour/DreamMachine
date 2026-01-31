#!/usr/bin/env python3
"""Basic DreamMachine simulation example.

Demonstrates:
1. Creating a network of Izhikevich neurons
2. Configuring STDP plasticity
3. Running simulation with external input
4. Analyzing spike patterns and weight changes
"""

import numpy as np
import sys

# Add src to path for development
sys.path.insert(0, str(__file__).rsplit('/', 2)[0] + '/src')

from dreammachine import (
    IzhikevichPopulation,
    NeuronType,
    STDPSynapses,
    STDPParams,
    NetworkSimulator,
)
from dreammachine.plasticity.stdp import create_random_connectivity
from dreammachine.network.simulator import create_network


def run_basic_example():
    """Run a basic network simulation."""
    print("=" * 60)
    print("DreamMachine: Basic Spiking Neural Network Simulation")
    print("=" * 60)

    # Configuration
    n_neurons = 100
    duration_ms = 1000.0
    dt = 0.5

    print(f"\nNetwork: {n_neurons} neurons, {duration_ms}ms simulation")

    # Create network with STDP
    rng = np.random.default_rng(42)
    neurons, synapses, sim = create_network(
        n_neurons=n_neurons,
        neuron_type=NeuronType.RS,
        connectivity_density=0.1,
        w_init=15.0,  # Strong initial weights for visible activity
        stdp_params=STDPParams(
            tau_plus=20.0,
            tau_minus=20.0,
            A_plus=0.01,
            A_minus=-0.012,
        ),
        heterogeneous=True,
        rng=rng,
    )

    # Initial weight stats
    initial_stats = synapses.get_weight_stats()
    print(f"Initial weights: mean={initial_stats['mean']:.3f}, "
          f"std={initial_stats['std']:.3f}, synapses={initial_stats['nnz']}")

    # External input: drive first 20 neurons with tonic input
    def external_input(t):
        I = np.zeros(n_neurons, dtype=np.float32)
        # Tonic input to input neurons
        I[:20] = 12.0
        # Add some noise to all neurons
        I += rng.standard_normal(n_neurons).astype(np.float32) * 2.0
        return I

    # Run simulation
    print("\nRunning simulation...")
    import time
    start = time.perf_counter()

    result = sim.run(duration_ms, dt=dt, I_ext=external_input)

    elapsed = time.perf_counter() - start
    print(f"Completed in {elapsed:.2f}s ({duration_ms/elapsed:.1f}x realtime)")

    # Results
    print(f"\nResults:")
    print(f"  Total spikes: {result.n_spikes}")
    print(f"  Mean firing rate: {result.mean_firing_rate:.1f} Hz")

    # Firing rate by group
    input_rate = result.firing_rates[:20].mean()
    other_rate = result.firing_rates[20:].mean()
    print(f"  Input neurons (0-19): {input_rate:.1f} Hz")
    print(f"  Other neurons (20-99): {other_rate:.1f} Hz")

    # Weight changes
    final_stats = synapses.get_weight_stats()
    print(f"\nFinal weights: mean={final_stats['mean']:.3f}, "
          f"std={final_stats['std']:.3f}")
    print(f"Weight change: {final_stats['mean'] - initial_stats['mean']:+.3f}")

    return result


def run_stdp_demo():
    """Demonstrate STDP weight changes with controlled spike timing."""
    print("\n" + "=" * 60)
    print("STDP Demonstration")
    print("=" * 60)

    # Create minimal network: pre -> post
    from scipy import sparse

    # Single synapse from neuron 0 to neuron 1
    conn = sparse.csr_matrix(
        ([0.5], ([0], [1])),
        shape=(2, 2),
        dtype=np.float32
    )

    synapses = STDPSynapses(
        2, 2,
        connectivity=conn,
        params=STDPParams(
            tau_plus=20.0,
            tau_minus=20.0,
            A_plus=0.1,
            A_minus=-0.12,
        )
    )

    print(f"Initial weight: {synapses.weights[0, 1]:.3f}")

    # Simulate LTP: pre fires, then post fires
    print("\nLTP scenario (pre before post):")
    synapses.weights.data[0] = 0.5

    # Pre spikes
    synapses.on_pre_spikes(np.array([0]))

    # 10ms delay
    for _ in range(10):
        synapses.update_traces(1.0)

    # Post spikes
    synapses.on_post_spikes(np.array([1]))

    print(f"  Weight after: {synapses.weights[0, 1]:.3f} (Δ={synapses.weights[0, 1] - 0.5:+.3f})")

    # Simulate LTD: post fires, then pre fires
    print("\nLTD scenario (post before pre):")
    synapses.weights.data[0] = 0.5
    synapses.reset_traces()

    # Post spikes first
    synapses.on_post_spikes(np.array([1]))

    # 10ms delay
    for _ in range(10):
        synapses.update_traces(1.0)

    # Pre spikes
    synapses.on_pre_spikes(np.array([0]))

    print(f"  Weight after: {synapses.weights[0, 1]:.3f} (Δ={synapses.weights[0, 1] - 0.5:+.3f})")


def benchmark_performance():
    """Benchmark simulation performance at different scales."""
    print("\n" + "=" * 60)
    print("Performance Benchmark")
    print("=" * 60)

    import time

    for n in [100, 500, 1000]:
        rng = np.random.default_rng(42)
        neurons, synapses, sim = create_network(
            n_neurons=n,
            connectivity_density=min(0.1, 1000 / n**2),  # Cap total synapses
            rng=rng,
        )

        n_synapses = synapses.weights.nnz

        def I_ext(t):
            return rng.standard_normal(n).astype(np.float32) * 3 + 10

        # Warmup
        sim.run(10.0, dt=0.5, I_ext=I_ext)
        sim.reset()

        # Timed run
        start = time.perf_counter()
        result = sim.run(100.0, dt=0.5, I_ext=I_ext)
        elapsed = time.perf_counter() - start

        realtime_factor = 100.0 / (elapsed * 1000)
        print(f"  N={n:4d}, synapses={n_synapses:5d}: "
              f"{elapsed*1000:.1f}ms ({realtime_factor:.1f}x realtime), "
              f"{result.n_spikes} spikes")


if __name__ == "__main__":
    run_basic_example()
    run_stdp_demo()
    benchmark_performance()

    print("\n" + "=" * 60)
    print("Simulation complete!")
    print("=" * 60)
