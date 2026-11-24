import numpy as np

from dreammachine.spnet import SpnetParams, build_network, make_inputs

SMALL = SpnetParams(Ne=40, Ni=10, M=10, D=5)


def test_default_shapes_dtypes():
    p = SpnetParams()
    net = build_network(p, np.random.default_rng(0))
    assert net.post.shape == net.delay.shape == net.s.shape == (1000, 100)
    assert net.post.dtype == np.int32 and net.delay.dtype == np.int32
    assert net.s.dtype == np.float64
    assert net.a.shape == net.d.shape == (1000,)
    assert net.a.dtype == net.d.dtype == np.float64
    assert net.post.min() >= 0 and net.post.max() < 1000


def test_no_duplicate_targets_and_inhibitory_targets():
    for p in (SMALL, SpnetParams()):
        net = build_network(p, np.random.default_rng(3))
        for row in net.post:
            assert len(set(row.tolist())) == p.M
        assert net.post[p.Ne:].max() < p.Ne


def test_delays_and_weights_and_params():
    p = SMALL
    net = build_network(p, np.random.default_rng(4))
    assert net.delay[: p.Ne].min() >= 1 and net.delay[: p.Ne].max() <= p.D
    assert len(np.unique(net.delay[: p.Ne])) > 1
    assert np.all(net.delay[p.Ne:] == 1)
    assert np.all(net.s[: p.Ne] == p.w_exc) and np.all(net.s[p.Ne:] == p.w_inh)
    assert np.all(net.a[: p.Ne] == p.a_exc) and np.all(net.a[p.Ne:] == p.a_inh)
    assert np.all(net.d[: p.Ne] == p.d_exc) and np.all(net.d[p.Ne:] == p.d_inh)


def test_seed_determinism():
    n1 = build_network(SMALL, np.random.default_rng(7))
    n2 = build_network(SMALL, np.random.default_rng(7))
    n3 = build_network(SMALL, np.random.default_rng(8))
    assert np.array_equal(n1.post, n2.post) and np.array_equal(n1.delay, n2.delay)
    assert not np.array_equal(n1.post, n3.post)


def test_make_inputs():
    i1 = make_inputs(SMALL, 2, np.random.default_rng(1))
    assert i1.shape == (2, 1000) and i1.dtype == np.int32
    assert i1.min() >= 0 and i1.max() < SMALL.N
    assert np.array_equal(i1, make_inputs(SMALL, 2, np.random.default_rng(1)))
