"""Slow, statement-by-statement transcription of the loop in spnet.m.

Deliberate deviations from spnet.m:

* Random numbers: the thalamic input neuron of every millisecond comes from
  the ``inputs`` array; the network wiring comes from ``build_network``.
* Indices are zero-based (neurons, synapse slots, trace columns).  Time ``t``
  inside a second stays 1-based (1..1000) as in the .m file, so trace column
  ``t + D - 1`` (zero-based) is MATLAB's ``STDP(:, t+D)``.
* ``pre`` stores (presynaptic neuron, slot) pairs instead of MATLAB linear
  indices into ``sd``; ``aux`` stores (presynaptic neuron, D-1-j) and the
  zero-based trace column is ``t + aux_offset`` (MATLAB: ``STDP(N*t+aux)``).
* No plotting; the number of seconds is given by ``inputs.shape[0]``.
* Initial ``v`` is ``c`` and initial ``u`` is ``b*c`` (MATLAB: -65, 0.2*v);
  the reset value is ``c``; the 0.2 in the u update is ``b``.
* The firing list keeps the sentinel row and the carry-over, but recorded
  spikes use a global millisecond index ``1000*sec + t - 1``.
* Sizes (N, M, D, Ne, Ni) and all constants are parameters.
"""

from __future__ import annotations

import numpy as np

from .network import STEPS_PER_SECOND, SpnetNetwork, SpnetParams, SpnetResult


def run_oracle(net: SpnetNetwork, inputs: np.ndarray, params: SpnetParams) -> SpnetResult:
    Ne, N, M, D = params.Ne, params.N, params.M, params.D
    sm = params.sm
    a, d = net.a, net.d
    post = net.post.astype(np.int64)
    s = net.s.astype(np.float64).copy()
    sd = np.zeros((N, M))

    # delays{i, j}: slots of neuron i with delay j+1 (ascending slot order)
    delays = [[[] for _ in range(D)] for _ in range(N)]
    for i in range(N):
        for slot in range(M):
            delays[i][int(net.delay[i, slot]) - 1].append(slot)
    delays = [[np.array(x, dtype=np.int64) for x in row] for row in delays]

    pre = [[] for _ in range(N)]
    aux = [[] for _ in range(N)]
    for i in range(Ne):
        for j in range(1, D + 1):
            for slot in delays[i][j - 1]:
                tgt = int(post[i, slot])
                pre[tgt].append((i, int(slot)))
                aux[tgt].append((i, D - 1 - j))

    STDP = np.zeros((N, STEPS_PER_SECOND + 1 + D))
    v = np.full(N, params.c)
    u = params.b * v
    firings = [(-D, 0)]  # (time, neuron) with the sentinel row
    spike_time: list[int] = []
    spike_neuron: list[int] = []

    for sec in range(inputs.shape[0]):
        for t in range(1, STEPS_PER_SECOND + 1):
            I = np.zeros(N)
            I[int(inputs[sec, t - 1])] = params.input_current
            fired = np.nonzero(v >= 30)[0]
            v[fired] = params.c
            u[fired] = u[fired] + d[fired]
            STDP[fired, t + D - 1] = params.trace_amp
            for f in fired:
                for (i, slot), (_, off) in zip(pre[f], aux[f]):
                    sd[i, slot] = sd[i, slot] + STDP[i, t + off]
            for f in fired:
                firings.append((t, int(f)))
                spike_time.append(sec * STEPS_PER_SECOND + t - 1)
                spike_neuron.append(int(f))
            k = len(firings) - 1
            while firings[k][0] > t - D:
                ft, fn = firings[k]
                dl = delays[fn][t - ft]  # delay index t-ft+1 (zero-based t-ft)
                ind = post[fn, dl]
                I[ind] = I[ind] + s[fn, dl]
                sd[fn, dl] = sd[fn, dl] - params.ltd_factor * STDP[ind, t + D - 1]
                k -= 1
            v = v + 0.5 * ((0.04 * v + 5) * v + 140 - u + I)
            v = v + 0.5 * ((0.04 * v + 5) * v + 140 - u + I)
            u = u + a * (params.b * v - u)
            STDP[:, t + D] = params.trace_decay * STDP[:, t + D - 1]
        STDP[:, : D + 1] = STDP[:, STEPS_PER_SECOND : STEPS_PER_SECOND + D + 1]
        firings = [(-D, 0)] + [
            (ft - STEPS_PER_SECOND, fn)
            for ft, fn in firings
            if ft > STEPS_PER_SECOND + 1 - D
        ]
        s[:Ne] = np.maximum(0, np.minimum(sm, params.w_drift + s[:Ne] + sd[:Ne]))
        sd = params.sd_decay * sd

    return SpnetResult(
        spike_time=np.array(spike_time, dtype=np.int64),
        spike_neuron=np.array(spike_neuron, dtype=np.int32),
        s=s,
        sd=sd,
        v=v,
        u=u,
    )
