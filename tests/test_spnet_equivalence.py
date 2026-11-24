import numpy as np
import pytest

from dreammachine.spnet import (
    SpnetParams,
    build_network,
    make_inputs,
    run_kernel,
    run_oracle,
)

FIELDS = ("spike_time", "spike_neuron", "s", "sd", "v", "u")


def _setup(p, seconds, seed=1):
    rng = np.random.default_rng(seed)
    net = build_network(p, rng)
    return net, make_inputs(p, seconds, rng)


def _assert_equal(a, b):
    for f in FIELDS:
        assert np.array_equal(getattr(a, f), getattr(b, f)), f
    assert a.spike_time.dtype == np.int64 and a.spike_neuron.dtype == np.int32


def test_small_network_equivalence():
    p = SpnetParams(Ne=40, Ni=10, M=10, D=5)
    net, inp = _setup(p, 3)
    o = run_oracle(net, inp, p)
    k = run_kernel(net, inp, p)
    assert len(o.spike_time) > 0
    _assert_equal(o, k)


# Runtime: oracle ~1.3 s per model second, so ~3 s here; kernel is negligible.
def test_default_network_equivalence_and_activity():
    p = SpnetParams()
    net, inp = _setup(p, 2)
    o = run_oracle(net, inp, p)
    k = run_kernel(net, inp, p)
    _assert_equal(o, k)
    exc = (k.spike_neuron < p.Ne).sum() / p.Ne / 2
    inh = (k.spike_neuron >= p.Ne).sum() / p.Ni / 2
    mean = len(k.spike_time) / p.N / 2
    print(f"rates exc={exc:.2f} Hz inh={inh:.2f} Hz mean={mean:.2f} Hz")
    assert 1.0 < mean < 30.0
    assert np.all(np.diff(k.spike_time) >= 0)


def test_weight_invariants_and_determinism():
    p = SpnetParams()
    net, inp = _setup(p, 5)
    k1 = run_kernel(net, inp, p)
    k2 = run_kernel(net, inp, p)
    _assert_equal(k1, k2)
    assert k1.s[: p.Ne].min() >= 0.0 and k1.s[: p.Ne].max() <= p.sm
    assert not np.array_equal(k1.s[: p.Ne], net.s[: p.Ne])  # plasticity acted
    assert np.array_equal(k1.s[p.Ne:], net.s[p.Ne:])
    assert np.all(net.s[p.Ne:] == p.w_inh)  # input network was not mutated


@pytest.mark.parametrize("seed", [2, 3])
def test_small_equivalence_other_seeds(seed):
    p = SpnetParams(Ne=30, Ni=8, M=8, D=7)
    net, inp = _setup(p, 2, seed)
    _assert_equal(run_oracle(net, inp, p), run_kernel(net, inp, p))
