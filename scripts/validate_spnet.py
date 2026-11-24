#!/usr/bin/env python
"""Long-run statistical validation of the spnet replication.

Usage: python scripts/validate_spnet.py --seeds 1 2 3 4 5 --seconds 3600 \
    --out benchmarks/records --figdir docs/validation/figures
Writes one JSON record per seed and figures built from the records.
Use --plot-only to rebuild figures from existing records.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import subprocess
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy.signal import welch  # noqa: E402

from dreammachine.spnet import (  # noqa: E402
    SpnetParams, build_network, make_inputs, run_kernel,
)

WIN = 60  # s
SEG = 2000  # Welch segment, ms
DELTA = (1.0, 5.0)
GAMMA = (30.0, 100.0)


def git_sha() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                              text=True, check=True, timeout=20).stdout.strip()
    except Exception as e:  # noqa: BLE001
        return f"unknown ({e})"


def spectrum(st, t0_s, t1_s):
    lo, hi = int(t0_s * 1000), int(t1_s * 1000)
    a, b = np.searchsorted(st, [lo, hi])
    counts = np.bincount(st[a:b] - lo, minlength=hi - lo).astype(float)
    counts -= counts.mean()
    f, p = welch(counts, fs=1000.0, nperseg=SEG, noverlap=SEG // 2, detrend=False)
    return f, p


def band_peak(f, p, lo, hi):
    m = (f >= lo) & (f <= hi)
    return float(f[m][np.argmax(p[m])])


def band_power(f, p, lo, hi):
    m = (f >= lo) & (f <= hi)
    return float(np.trapezoid(p[m], f[m]))


def spec_summary(st, t0, t1):
    f, p = spectrum(st, t0, t1)
    return {
        "window_s": [t0, t1],
        "freq_hz": f.tolist(), "psd": p.tolist(),
        "peak_1_10_hz": band_peak(f, p, 1, 10),
        "peak_20_100_hz": band_peak(f, p, 20, 100),
        "power_delta_1_5": band_power(f, p, *DELTA),
        "power_gamma_30_100": band_power(f, p, *GAMMA),
        "gamma_over_delta": band_power(f, p, *GAMMA) / band_power(f, p, *DELTA),
    }


def isi_cv_exc(st, sn, Ne, t0_s):
    a = np.searchsorted(st, int(t0_s * 1000))
    t, n = st[a:], sn[a:]
    m = n < Ne
    t, n = t[m], n[m]
    o = np.argsort(n, kind="stable")
    t, n = t[o], n[o]
    cvs = []
    bounds = np.flatnonzero(np.diff(n)) + 1
    for g in np.split(t, bounds):
        if len(g) >= 3:
            isi = np.diff(np.sort(g)).astype(float)
            cvs.append(isi.std() / isi.mean())
    return float(np.mean(cvs)), len(cvs)


def run_seed(seed, seconds, params, out):
    t_start = time.perf_counter()
    rng = np.random.default_rng(seed)
    net = build_network(params, rng)
    inputs = make_inputs(params, seconds, rng)
    t_run = time.perf_counter()
    res = run_kernel(net, inputs, params)
    wall_kernel = time.perf_counter() - t_run
    st, sn = res.spike_time, res.spike_neuron
    Ne, Ni, sm = params.Ne, params.Ni, params.sm
    if not np.all(np.diff(st) >= 0):
        o = np.argsort(st, kind="stable"); st, sn = st[o], sn[o]
    nwin = seconds // WIN
    win = (st // (WIN * 1000)).astype(np.int64)
    exc = sn < Ne
    ce = np.bincount(win[exc], minlength=nwin + 1)[:nwin]
    ci = np.bincount(win[~exc], minlength=nwin + 1)[:nwin]
    re_, ri_ = ce / (Ne * WIN), ci / (Ni * WIN)
    w = res.s[:Ne].ravel()
    hist, edges = np.histogram(w, bins=50, range=(0, sm))
    late0 = max(0, seconds - 100)
    cv, ncv = isi_cv_exc(st, sn, Ne, late0)
    rec = {
        "seed": seed, "seconds": seconds,
        "params": dataclasses.asdict(params),
        "git_sha": git_sha(), "wall_time_s": time.perf_counter() - t_start,
        "wall_time_kernel_s": wall_kernel, "n_spikes": int(len(st)),
        "window_s": WIN,
        "rate_exc_hz_series": re_.tolist(), "rate_inh_hz_series": ri_.tolist(),
        "rate_exc_first_min_hz": float(re_[0]), "rate_inh_first_min_hz": float(ri_[0]),
        "rate_exc_last_min_hz": float(re_[-1]), "rate_inh_last_min_hz": float(ri_[-1]),
        "weights": {
            "hist_counts": hist.tolist(), "hist_edges": edges.tolist(),
            "frac_below_0.5": float(np.mean(w < 0.5)),
            "frac_above_sm_minus_0.5": float(np.mean(w > sm - 0.5)),
            "mean": float(w.mean()),
        },
        "spectrum_early": spec_summary(st, 0, min(10, seconds)),
        "spectrum_late": spec_summary(st, late0, seconds),
        "isi_cv_exc_last_100s": cv, "isi_cv_n_neurons": ncv,
        "v_max_final": float(res.v.max()),
    }
    if seed == 1:
        def rast(t0):
            a, b = np.searchsorted(st, [t0 * 1000, (t0 + 1) * 1000])
            return {"t_ms": (st[a:b] - t0 * 1000).tolist(), "neuron": sn[a:b].tolist()}
        rec["raster_first_s"] = rast(0)
        rec["raster_last_s"] = rast(seconds - 1)
    path = Path(out) / f"validation-spnet-seed{seed}.json"
    path.write_text(json.dumps(rec))
    print(f"seed {seed}: {len(st)} spikes, wall {rec['wall_time_s']:.1f}s -> {path}", flush=True)
    return rec


def make_figures(recs, figdir):
    figdir = Path(figdir); figdir.mkdir(parents=True, exist_ok=True)
    cols = plt.get_cmap("tab10")
    # rates
    fig, ax = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    for k, r in enumerate(recs):
        x = (np.arange(len(r["rate_exc_hz_series"])) + 0.5) * r["window_s"] / 60
        ax[0].plot(x, r["rate_exc_hz_series"], color=cols(k), label=f"seed {r['seed']}")
        ax[1].plot(x, r["rate_inh_hz_series"], color=cols(k))
    ax[0].set_ylabel("Excitatory mean rate (Hz)"); ax[1].set_ylabel("Inhibitory mean rate (Hz)")
    ax[1].set_xlabel("Model time (min)"); ax[0].legend(ncol=5, fontsize=8)
    ax[0].set_title("Mean firing rate in 60 s windows")
    fig.tight_layout(); fig.savefig(figdir / "spnet-rates.png", dpi=120); plt.close(fig)
    # weights
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for k, r in enumerate(recs):
        h = r["weights"]; e = np.array(h["hist_edges"])
        ax.step(e[:-1], np.array(h["hist_counts"]) / sum(h["hist_counts"]), where="post",
                color=cols(k), label=f"seed {r['seed']}")
    ax.set_yscale("log"); ax.set_xlabel("Final excitatory synaptic weight (mV-equivalent units)")
    ax.set_ylabel("Fraction of synapses per bin (log)"); ax.legend(fontsize=8)
    ax.set_title("Final excitatory weight distribution (50 bins)")
    fig.tight_layout(); fig.savefig(figdir / "spnet-weights.png", dpi=120); plt.close(fig)
    # spectra
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
    for j, key in enumerate(["spectrum_early", "spectrum_late"]):
        for k, r in enumerate(recs):
            s = r[key]; f = np.array(s["freq_hz"]); m = (f > 0) & (f <= 120)
            ax[j].semilogy(f[m], np.array(s["psd"])[m], color=cols(k), label=f"seed {r['seed']}")
        w0, w1 = recs[0][key]["window_s"]
        ax[j].set_title(f"Population spike-count PSD, {w0}-{w1} s")
        ax[j].set_xlabel("Frequency (Hz)")
    ax[0].set_ylabel("PSD (counts$^2$/Hz per 1 ms bin)"); ax[0].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(figdir / "spnet-spectra.png", dpi=120); plt.close(fig)
    # rasters
    r1 = next((r for r in recs if r["seed"] == 1), None)
    if r1 and "raster_first_s" in r1:
        Ne = r1["params"]["Ne"]
        fig, ax = plt.subplots(2, 1, figsize=(10, 7))
        for a_, key, ttl in [(ax[0], "raster_first_s", "first second"),
                             (ax[1], "raster_last_s", "last second")]:
            t = np.array(r1[key]["t_ms"]); n = np.array(r1[key]["neuron"]); e = n < Ne
            a_.plot(t[e], n[e], ".", ms=2, color="tab:blue", label="excitatory")
            a_.plot(t[~e], n[~e], ".", ms=2, color="tab:red", label="inhibitory")
            a_.set_ylabel("Neuron index"); a_.set_title(f"Seed 1 spike raster, {ttl}")
            a_.set_xlabel("Time within second (ms)")
        ax[0].legend(markerscale=4, fontsize=8)
        fig.tight_layout(); fig.savefig(figdir / "spnet-raster-seed1.png", dpi=120); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    ap.add_argument("--seconds", type=int, default=3600)
    ap.add_argument("--out", default="benchmarks/records")
    ap.add_argument("--figdir", default="docs/validation/figures")
    ap.add_argument("--plot-only", action="store_true")
    a = ap.parse_args()
    Path(a.out).mkdir(parents=True, exist_ok=True)
    params = SpnetParams()
    recs = []
    for s in a.seeds:
        p = Path(a.out) / f"validation-spnet-seed{s}.json"
        recs.append(json.loads(p.read_text()) if a.plot_only else run_seed(s, a.seconds, params, a.out))
    make_figures(recs, a.figdir)


if __name__ == "__main__":
    main()
