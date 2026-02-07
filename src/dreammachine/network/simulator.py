"""Network simulation engine.

Orchestrates neuron updates, synaptic transmission, and plasticity
in a time-stepped simulation loop.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, List

import numpy as np
from numpy.typing import NDArray

from dreammachine.neurons.izhikevich import IzhikevichPopulation, NeuronType
from dreammachine.plasticity.stdp import STDPSynapses, STDPParams, create_random_connectivity


@dataclass
class SimulationResult:
    """Results from a network simulation run.

    Attributes
    ----------
    spike_times : list of ndarray
        Spike times for each neuron (variable length arrays).
    spike_indices : ndarray
        Flattened array of neuron indices that spiked.
    spike_times_flat : ndarray
        Flattened array of corresponding spike times.
    v_history : ndarray | None
        Membrane potential history if recorded, shape (n_steps, n_neurons).
    weight_history : list of ndarray | None
        Weight snapshots if recorded.
    duration_ms : float
        Simulation duration in milliseconds.
    dt : float
        Timestep used.
    n_neurons : int
        Number of neurons.
    """

    spike_times: List[NDArray[np.float32]]
    spike_indices: NDArray[np.int32]
    spike_times_flat: NDArray[np.float32]
    v_history: Optional[NDArray[np.float32]]
    weight_history: Optional[List[NDArray[np.float32]]]
    duration_ms: float
    dt: float
    n_neurons: int

    @property
    def n_spikes(self) -> int:
        """Total number of spikes across all neurons."""
        return len(self.spike_times_flat)

    @property
    def firing_rates(self) -> NDArray[np.float32]:
        """Mean firing rate (Hz) for each neuron."""
        duration_s = self.duration_ms / 1000.0
        counts = np.array([len(times) for times in self.spike_times])
        return counts / duration_s

    @property
    def mean_firing_rate(self) -> float:
        """Population mean firing rate (Hz)."""
        return float(self.firing_rates.mean())

    def get_spike_raster(self) -> tuple[NDArray, NDArray]:
        """Get spike raster data for plotting.

        Returns
        -------
        times : ndarray
            Spike times.
        neurons : ndarray
            Corresponding neuron indices.
        """
        return self.spike_times_flat, self.spike_indices


class NetworkSimulator:
    """Main simulation engine for spiking neural networks.

    Manages the simulation loop, coordinating neuron updates,
    synaptic transmission, and plasticity.

    Parameters
    ----------
    neurons : IzhikevichPopulation
        Population of neurons to simulate.
    synapses : STDPSynapses | None
        Synaptic connections with STDP. If None, neurons are unconnected.
    record_v : bool
        Whether to record membrane potential history. Memory intensive.
    record_weights : bool
        Whether to record weight snapshots.
    weight_record_interval : float
        Interval (ms) between weight snapshots.

    Examples
    --------
    >>> pop = IzhikevichPopulation(100, NeuronType.RS)
    >>> conn = create_random_connectivity(100, 100, density=0.1)
    >>> syn = STDPSynapses(100, 100, connectivity=conn)
    >>> sim = NetworkSimulator(pop, syn)
    >>> result = sim.run(1000.0)  # Run 1 second
    >>> print(f"Mean rate: {result.mean_firing_rate:.1f} Hz")
    """

    def __init__(
        self,
        neurons: IzhikevichPopulation,
        synapses: Optional[STDPSynapses] = None,
        record_v: bool = False,
        record_weights: bool = False,
        weight_record_interval: float = 100.0,
    ) -> None:
        """Initialize simulator."""
        self.neurons = neurons
        self.synapses = synapses
        self.record_v = record_v
        self.record_weights = record_weights
        self.weight_record_interval = weight_record_interval

    def run(
        self,
        duration_ms: float,
        dt: float = 0.5,
        I_ext: Optional[NDArray[np.float32] | Callable[[float], NDArray[np.float32]]] = None,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> SimulationResult:
        """Run simulation for specified duration.

        Parameters
        ----------
        duration_ms : float
            Duration in milliseconds.
        dt : float
            Timestep in milliseconds. Default 0.5ms.
        I_ext : ndarray | callable | None
            External input current. Can be:
            - None: no external input
            - ndarray shape (n_steps, n_neurons): precomputed input
            - callable: function(t) -> ndarray of shape (n_neurons,)
        progress_callback : callable | None
            Called with progress fraction (0-1) for status updates.

        Returns
        -------
        result : SimulationResult
            Simulation results including spike times and optional recordings.
        """
        n_steps = int(duration_ms / dt)
        n = self.neurons.n

        # Initialize spike recording
        spike_times_list: List[List[float]] = [[] for _ in range(n)]
        spike_indices_list: List[int] = []
        spike_times_flat_list: List[float] = []

        # Initialize optional recordings
        v_history = np.zeros((n_steps, n), dtype=np.float32) if self.record_v else None
        weight_history: List[NDArray[np.float32]] = []

        # Handle external input
        if I_ext is None:
            I_ext_func = lambda t: np.zeros(n, dtype=np.float32)
        elif callable(I_ext):
            I_ext_func = I_ext
        else:
            # Precomputed array
            I_ext_array = I_ext
            I_ext_func = lambda t, arr=I_ext_array: arr[int(t / dt) % len(arr)]

        # Previous spikes for synaptic transmission
        prev_spikes = np.zeros(n, dtype=np.bool_)

        # Weight recording timing
        last_weight_record = -self.weight_record_interval

        # Main simulation loop
        for step in range(n_steps):
            t = step * dt

            # 1. Compute synaptic input from previous spikes
            if self.synapses is not None and prev_spikes.any():
                I_syn = self.synapses.compute_input(prev_spikes)
            else:
                I_syn = np.zeros(n, dtype=np.float32)

            # 2. Set total input current
            self.neurons.I = I_ext_func(t) + I_syn

            # 3. Update neuron states and detect spikes
            spikes = self.neurons.step(dt)

            # 4. Update plasticity
            if self.synapses is not None:
                self.synapses.update_traces(dt)
                if spikes.any() or prev_spikes.any():
                    self.synapses.on_spikes(prev_spikes, spikes)

            # 5. Record spikes
            spike_idx = np.where(spikes)[0]
            for idx in spike_idx:
                spike_times_list[idx].append(t)
                spike_indices_list.append(idx)
                spike_times_flat_list.append(t)

            # 6. Optional recordings
            if v_history is not None:
                v_history[step] = self.neurons.v

            if self.record_weights and t - last_weight_record >= self.weight_record_interval:
                if self.synapses is not None:
                    weight_history.append(self.synapses.weights.data.copy())
                last_weight_record = t

            # 7. Update for next iteration
            prev_spikes = spikes

            # 8. Progress callback
            if progress_callback is not None and step % 1000 == 0:
                progress_callback(step / n_steps)

        # Sync weight transpose after simulation
        if self.synapses is not None:
            self.synapses.sync_transpose()

        # Convert to arrays
        spike_times = [np.array(times, dtype=np.float32) for times in spike_times_list]

        return SimulationResult(
            spike_times=spike_times,
            spike_indices=np.array(spike_indices_list, dtype=np.int32),
            spike_times_flat=np.array(spike_times_flat_list, dtype=np.float32),
            v_history=v_history,
            weight_history=weight_history if self.record_weights else None,
            duration_ms=duration_ms,
            dt=dt,
            n_neurons=n,
        )

    def reset(self) -> None:
        """Reset network to initial state."""
        self.neurons.reset()
        if self.synapses is not None:
            self.synapses.reset_traces()


def create_network(
    n_neurons: int,
    neuron_type: NeuronType = NeuronType.RS,
    connectivity_density: float = 0.1,
    w_init: float = 0.5,
    stdp_params: Optional[STDPParams] = None,
    heterogeneous: bool = True,
    rng: Optional[np.random.Generator] = None,
) -> tuple[IzhikevichPopulation, STDPSynapses, NetworkSimulator]:
    """Convenience function to create a complete network.

    Parameters
    ----------
    n_neurons : int
        Number of neurons.
    neuron_type : NeuronType
        Type of neurons (RS, FS, etc.).
    connectivity_density : float
        Connection probability.
    w_init : float
        Initial synaptic weight.
    stdp_params : STDPParams | None
        STDP parameters.
    heterogeneous : bool
        Add parameter heterogeneity to neurons.
    rng : Generator | None
        Random number generator.

    Returns
    -------
    neurons : IzhikevichPopulation
        Neuron population.
    synapses : STDPSynapses
        Synaptic connections.
    simulator : NetworkSimulator
        Configured simulator.
    """
    rng = rng or np.random.default_rng()

    # Create neurons
    neurons = IzhikevichPopulation(
        n=n_neurons,
        params=neuron_type,
        heterogeneous=heterogeneous,
        rng=rng,
    )

    # Create synapses
    connectivity = create_random_connectivity(
        n_neurons, n_neurons,
        density=connectivity_density,
        w_init=w_init,
        rng=rng,
    )
    synapses = STDPSynapses(
        n_neurons, n_neurons,
        connectivity=connectivity,
        params=stdp_params or STDPParams(),
    )

    # Create simulator
    simulator = NetworkSimulator(neurons, synapses)

    return neurons, synapses, simulator
