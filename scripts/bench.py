#!/usr/bin/env python
"""Benchmark harness: one JSON record per run under benchmarks/records/.

Usage (repo root, PYTHONPATH=src):
    python scripts/bench.py spnet-reference
    python scripts/bench.py prototype-baseline
    python scripts/bench.py spnet-scaling
Each subcommand prints the path of the record it wrote.
"""
from __future__ import annotations

import argparse
import json
import platform
import resource
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numba
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "benchmarks" / "records"


def _git_sha() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                              check=True, timeout=20, cwd=ROOT).stdout.strip()
    except Exception as e:  # noqa: BLE001
        return f"unknown ({e})"


def _cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def _peak_rss_mb() -> float:
    kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # KiB on Linux
    return kb / 1024.0


def _meta(name: str) -> dict:
    import os
    return {
        "benchmark": name,
        "git_sha": _git_sha(),
        "utc_time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cpu_model": _cpu_model(),
        "cpu_count": os.cpu_count(),
        "numba_threads": numba.config.NUMBA_NUM_THREADS,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "numba": numba.__version__,
    }


def _write(name: str, rec: dict) -> Path:
    RECORDS.mkdir(parents=True, exist_ok=True)
    stamp = rec["utc_time"].replace(":", "").replace("-", "")
    path = RECORDS / f"bench-{name}-{stamp}.json"
    path.write_text(json.dumps(rec, indent=2) + "\n")
    print(path)
    return path


def _times_summary(times: list[float]) -> dict:
    return {"wall_times_s": times, "min_s": min(times), "median_s": statistics.median(times)}


def cmd_reference(args) -> None:
    from dreammachine.spnet import SpnetParams, build_network, make_inputs, run_kernel
    params = SpnetParams()
    rng = np.random.default_rng(args.seed)
    net = build_network(params, rng)
    run_kernel(build_network(SpnetParams(), np.random.default_rng(0)),
               make_inputs(params, 1, np.random.default_rng(0)), params)  # JIT warm-up
    inputs = make_inputs(params, args.seconds, rng)
    times, nspikes = [], []
    for _ in range(args.repeats):
        t0 = time.perf_counter()
        res = run_kernel(net, inputs, params)
        times.append(time.perf_counter() - t0)
        nspikes.append(int(res.spike_time.size))
    rec = _meta("spnet-reference")
    rec.update(parameters={"spnet_params": params.__dict__, "model_seconds": args.seconds,
                           "seed": args.seed, "what": "run_kernel only; network built outside timing; same initial network each repeat"},
               repeats=args.repeats, n_spikes=nspikes, **_times_summary(times))
    rec["realtime_factor_min_wall"] = args.seconds / min(times)
    rec["realtime_factor_median_wall"] = args.seconds / statistics.median(times)
    rec["peak_rss_mb"] = _peak_rss_mb()
    _write("spnet-reference", rec)


def cmd_prototype(args) -> None:
    from dreammachine.network.simulator import create_network
    n_drive = 20
    drive = np.zeros(args.neurons, dtype=np.float32)
    drive[:n_drive] = 12.0  # same drive as examples/basic_simulation.py

    def ext(t, drive=drive):
        return drive

    _, _, warm = create_network(100, rng=np.random.default_rng(0))
    warm.run(10.0, dt=0.5, I_ext=lambda t: np.full(100, 12.0, dtype=np.float32))  # JIT warm-up
    times, nspikes = [], []
    for r in range(args.repeats):
        _, _, sim = create_network(args.neurons, connectivity_density=args.density,
                                   rng=np.random.default_rng(args.seed + r))
        t0 = time.perf_counter()
        res = sim.run(args.seconds * 1000.0, dt=0.5, I_ext=ext)
        times.append(time.perf_counter() - t0)
        nspikes.append(int(res.n_spikes))
    rec = _meta("prototype-baseline")
    rec.update(parameters={"neurons": args.neurons, "density": args.density, "dt_ms": 0.5,
                           "model_seconds": args.seconds, "seed": args.seed,
                           "external_input": "12.0 to first 20 neurons, constant (as examples/basic_simulation.py)",
                           "what": "dreammachine.network.simulator, create_network defaults; run() only timed; JIT warm-up on a 100-neuron network first"},
               repeats=args.repeats, n_spikes=nspikes, **_times_summary(times))
    rec["realtime_factor_min_wall"] = args.seconds / min(times)
    rec["peak_rss_mb"] = _peak_rss_mb()
    _write("prototype-baseline", rec)


def cmd_scaling_one(args) -> None:
    """Child process: one size, prints a JSON dict on the last stdout line."""
    from dreammachine.spnet import SpnetParams, build_network, make_inputs, run_kernel
    n = args.n
    params = SpnetParams(Ne=int(n * 0.8), Ni=n - int(n * 0.8), M=100, D=20)
    # JIT warm-up on a tiny network
    sp = SpnetParams(Ne=40, Ni=10, M=10, D=5)
    run_kernel(build_network(sp, np.random.default_rng(0)), make_inputs(sp, 1, np.random.default_rng(0)), sp)
    rng = np.random.default_rng(args.seed)
    t0 = time.perf_counter()
    net = build_network(params, rng)
    build_s = time.perf_counter() - t0
    t0 = time.perf_counter()
    run_kernel(net, make_inputs(params, 1, rng), params)
    probe_s = time.perf_counter() - t0
    nsec = max(1, min(args.max_seconds, int(args.budget_s / probe_s)))
    net = build_network(params, np.random.default_rng(args.seed))
    inputs = make_inputs(params, nsec, np.random.default_rng(args.seed + 1))
    t0 = time.perf_counter()
    res = run_kernel(net, inputs, params)
    wall = time.perf_counter() - t0
    print(json.dumps({"n": n, "model_seconds": nsec, "wall_s": wall, "realtime_factor": nsec / wall,
                      "probe_1s_wall_s": probe_s, "build_network_s": build_s,
                      "n_spikes": int(res.spike_time.size),
                      "mean_rate_hz": res.spike_time.size / n / nsec,
                      "synapses": n * 100, "peak_rss_mb": _peak_rss_mb(),
                      "bytes_per_synapse": _peak_rss_mb() * 1024 * 1024 / (n * 100)}))


def cmd_scaling(args) -> None:
    results = []
    for n in args.sizes:
        cmd = [sys.executable, str(Path(__file__).resolve()), "_scaling-one", "--n", str(n),
               "--seed", str(args.seed), "--budget-s", str(args.budget_s),
               "--max-seconds", str(args.max_seconds)]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout_s,
                               cwd=ROOT, env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")})
        except subprocess.TimeoutExpired:
            results.append({"n": n, "failed": f"timeout after {args.timeout_s} s"})
            continue
        if p.returncode != 0:
            results.append({"n": n, "failed": f"exit code {p.returncode}: {p.stderr.strip()[-500:]}"})
            continue
        results.append(json.loads(p.stdout.strip().splitlines()[-1]))
    ok = [r for r in results if "failed" not in r]
    below = [r["n"] for r in ok if r["realtime_factor"] < 1.0]
    rec = _meta("spnet-scaling")
    rec.update(parameters={"sizes": args.sizes, "split": "80/20", "M": 100, "D": 20, "seed": args.seed,
                           "budget_s": args.budget_s, "max_model_seconds": args.max_seconds,
                           "what": "each size in its own process; JIT warm-up on a tiny network; 1 s probe then model_seconds chosen to fit budget; single run per size"},
               repeats=1, results=results,
               first_measured_size_below_realtime=(min(below) if below else None))
    _write("spnet-scaling", rec)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("spnet-reference")
    p.add_argument("--seconds", type=int, default=10)
    p.add_argument("--repeats", type=int, default=7)
    p.add_argument("--seed", type=int, default=1)
    p.set_defaults(fn=cmd_reference)
    p = sub.add_parser("prototype-baseline")
    p.add_argument("--neurons", type=int, default=1000)
    p.add_argument("--density", type=float, default=0.1)
    p.add_argument("--seconds", type=float, default=1.0)
    p.add_argument("--repeats", type=int, default=3)
    p.add_argument("--seed", type=int, default=1)
    p.set_defaults(fn=cmd_prototype)
    p = sub.add_parser("spnet-scaling")
    p.add_argument("--sizes", type=int, nargs="+", default=[1000, 10000, 100000])
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--budget-s", type=float, default=150.0)
    p.add_argument("--max-seconds", type=int, default=20)
    p.add_argument("--timeout-s", type=int, default=600)
    p.set_defaults(fn=cmd_scaling)
    p = sub.add_parser("_scaling-one")
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--budget-s", type=float, default=150.0)
    p.add_argument("--max-seconds", type=int, default=20)
    p.set_defaults(fn=cmd_scaling_one)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
