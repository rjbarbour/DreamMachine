"""Numba implementation of the spnet.m simulation, bit-identical to the oracle.

Spikes of the last D steps are read back from the (growing) global spike
arrays, newest first, which reproduces the order in which spnet.m walks its
``firings`` list.  Incoming synapses of excitatory neurons and outgoing
synapses grouped by delay are stored as flat CSR index arrays.
"""

from __future__ import annotations

import numpy as np
from numba import njit

from .network import STEPS_PER_SECOND, SpnetNetwork, SpnetParams, SpnetResult


def _build_indices(net: SpnetNetwork, params: SpnetParams):
    Ne, N, M, D = params.Ne, params.N, params.M, params.D
    delay = net.delay.astype(np.int64)
    if delay.min() < 1 or delay.max() > D:
        raise ValueError("delays must lie in 1..D")
    # incoming (excitatory presynaptic) synapses, grouped by target neuron
    pre_i = np.repeat(np.arange(Ne, dtype=np.int64), M)
    slot = np.tile(np.arange(M, dtype=np.int64), Ne)
    tgt = net.post[:Ne].astype(np.int64).ravel()
    dly = delay[:Ne].ravel()
    order = np.lexsort((slot, dly, pre_i, tgt))
    in_ptr = np.zeros(N + 1, dtype=np.int64)
    np.cumsum(np.bincount(tgt, minlength=N), out=in_ptr[1:])
    in_pre = pre_i[order].astype(np.int32)
    in_slot = slot[order].astype(np.int32)
    in_delay = dly[order].astype(np.int32)
    # outgoing synapses grouped by (neuron, delay), ascending slot
    n_all = np.repeat(np.arange(N, dtype=np.int64), M)
    slot_all = np.tile(np.arange(M, dtype=np.int64), N)
    dly_all = delay.ravel()
    order = np.lexsort((slot_all, dly_all, n_all))
    out_ptr = np.zeros(N * D + 1, dtype=np.int64)
    np.cumsum(np.bincount(n_all * D + dly_all - 1, minlength=N * D), out=out_ptr[1:])
    out_slot = slot_all[order].astype(np.int32)
    return in_ptr, in_pre, in_slot, in_delay, out_ptr, out_slot


@njit(cache=True)
def _simulate(
    inputs, post, s, a, d, in_ptr, in_pre, in_slot, in_delay, out_ptr, out_slot,
    Ne, D, sm, b, c, input_current, trace_amp, ltd_factor, trace_decay,
    sd_decay, w_drift,
):
    nsec = inputs.shape[0]
    N, M = post.shape
    L = 1000
    sd = np.zeros((N, M))
    trace = np.zeros((L + 1 + D, N))  # trace[column, neuron]
    v = np.full(N, c)
    u = b * v
    cap = 4096
    st = np.empty(cap, dtype=np.int64)
    sn = np.empty(cap, dtype=np.int32)
    ns = 0
    I = np.zeros(N)
    fired = np.empty(N, dtype=np.int64)
    for sec in range(nsec):
        for t in range(1, L + 1):
            tg = sec * L + t - 1
            I[:] = 0.0
            I[inputs[sec, t - 1]] = input_current
            nf = 0
            for n in range(N):
                if v[n] >= 30:
                    fired[nf] = n
                    nf += 1
            for q in range(nf):
                n = fired[q]
                v[n] = c
                u[n] = u[n] + d[n]
                trace[t + D - 1, n] = trace_amp
            for q in range(nf):
                f = fired[q]
                for e in range(in_ptr[f], in_ptr[f + 1]):
                    i = in_pre[e]
                    sl = in_slot[e]
                    sd[i, sl] = sd[i, sl] + trace[t + D - 1 - in_delay[e], i]
            if ns + nf > cap:
                while ns + nf > cap:
                    cap *= 2
                st2 = np.empty(cap, dtype=np.int64)
                sn2 = np.empty(cap, dtype=np.int32)
                st2[:ns] = st[:ns]
                sn2[:ns] = sn[:ns]
                st = st2
                sn = sn2
            for q in range(nf):
                st[ns] = tg
                sn[ns] = fired[q]
                ns += 1
            k = ns - 1
            while k >= 0 and st[k] > tg - D:
                fn = sn[k]
                dd = tg - st[k]  # zero-based delay index
                for e in range(out_ptr[fn * D + dd], out_ptr[fn * D + dd + 1]):
                    sl = out_slot[e]
                    tgt = post[fn, sl]
                    I[tgt] = I[tgt] + s[fn, sl]
                    sd[fn, sl] = sd[fn, sl] - ltd_factor * trace[t + D - 1, tgt]
                k -= 1
            for n in range(N):
                vn = v[n]
                vn = vn + 0.5 * ((0.04 * vn + 5) * vn + 140 - u[n] + I[n])
                vn = vn + 0.5 * ((0.04 * vn + 5) * vn + 140 - u[n] + I[n])
                v[n] = vn
                u[n] = u[n] + a[n] * (b * vn - u[n])
                trace[t + D, n] = trace_decay * trace[t + D - 1, n]
        for col in range(D + 1):
            for n in range(N):
                trace[col, n] = trace[L + col, n]
        for i in range(Ne):
            for j in range(M):
                x = w_drift + s[i, j] + sd[i, j]
                x = min(sm, x)
                s[i, j] = max(0.0, x)
        for i in range(N):
            for j in range(M):
                sd[i, j] = sd_decay * sd[i, j]
    return st[:ns].copy(), sn[:ns].copy(), s, sd, v, u


def run_kernel(net: SpnetNetwork, inputs: np.ndarray, params: SpnetParams) -> SpnetResult:
    assert STEPS_PER_SECOND == 1000
    in_ptr, in_pre, in_slot, in_delay, out_ptr, out_slot = _build_indices(net, params)
    st, sn, s, sd, v, u = _simulate(
        np.ascontiguousarray(inputs, dtype=np.int32),
        np.ascontiguousarray(net.post, dtype=np.int32),
        net.s.astype(np.float64).copy(),
        net.a.astype(np.float64),
        net.d.astype(np.float64),
        in_ptr, in_pre, in_slot, in_delay, out_ptr, out_slot,
        params.Ne, params.D, params.sm, params.b, params.c, params.input_current,
        params.trace_amp, params.ltd_factor, params.trace_decay, params.sd_decay,
        params.w_drift,
    )
    return SpnetResult(spike_time=st, spike_neuron=sn, s=s, sd=sd, v=v, u=u)
