"""Cross-check our spnet re-implementation against Izhikevich's original spnet.m in Octave.

The original source (references/cache/izhikevich.org/spnet.m, no licence) is never
copied into the repo: a harness .m file is generated in a temporary directory at
run time from the cached file and deleted afterwards.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dreammachine.spnet import (  # noqa: E402
    SpnetParams, build_network, make_inputs, run_kernel, run_oracle,
)

SPNET_M = ROOT / "references" / "cache" / "izhikevich.org" / "spnet.m"
MANIFEST = ROOT / "references" / "manifest.jsonl"


def manifest_sha() -> str | None:
    for line in MANIFEST.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("key") == "izhikevich_spnet_m":
            return rec.get("sha256")
    return None


def _sub_once(text: str, pattern: str, repl: str) -> str:
    n = len(re.findall(pattern, text, flags=re.M))
    assert n == 1, f"substitution {pattern!r} matched {n} times, expected exactly 1"
    return re.sub(pattern, lambda _m: repl, text, flags=re.M)


def _take_once(text: str, pattern: str) -> str:
    ms = list(re.finditer(pattern, text, flags=re.M | re.S))
    assert len(ms) == 1, f"extraction {pattern!r} matched {len(ms)} times, expected exactly 1"
    return ms[0].group(0)


def build_harness(src_text: str, seconds: int) -> str:
    """Compose the harness from the cached original; asserts every edit matches once."""
    src = src_text.replace("\r\n", "\n")
    # variables the original builds with constant sizes (a, d, sm); sizes come from files
    consts = _take_once(src, r"^a=\[0\.02.*?^sm=10;[^\n]*\n")
    # original's own construction code for pre / aux
    prefix = _take_once(src, r"^pre = cell\(N,1\);.*?(?=^STDP = zeros\(N,1001\+D\);)")
    # original simulation loop text
    loop = _take_once(src, r"^STDP = zeros\(N,1001\+D\);.*\Z")
    loop = _sub_once(loop, r"1:60\*60\*24", f"1:{seconds}")
    loop = _sub_once(loop, r"^    I\(ceil\(N\*rand\)\)=20;", "    I(inp(sec,t))=20;")
    loop = _sub_once(loop, r"^  axis\(\[0 1000 0 N\]\); drawnow;[^\n]*\n", "")
    loop = _sub_once(
        loop, r"^  plot\(firings\(:,1\),firings\(:,2\),'\.'\);[^\n]*\n",
        "  idx_ = find(firings(:,1) >= 1);\n"
        "  if ~isempty(idx_)\n"
        "    fprintf(fo_, '%d %d\\n', [(sec-1)*1000 + firings(idx_,1) - 1, firings(idx_,2) - 1]');\n"
        "  end\n",
    )
    head = (
        "more off;\n"
        "P_ = load('params.txt'); M=P_(1); D=P_(2); Ne=P_(3); Ni=P_(4); N=Ne+Ni;\n"
        "post = load('post.txt'); dly_ = load('delay.txt'); s = load('s0.txt');\n"
        "inp = load('inputs.txt');\n"
        "post = reshape(post, M, N)'; dly_ = reshape(dly_, M, N)'; s = reshape(s, M, N)';\n"
        "inp = reshape(inp, 1000, [])';\n"
        "delays = cell(N,D);\n"
        "for i_=1:N\n"
        "  for j_=1:M\n"
        "    delays{i_, dly_(i_,j_)}(end+1) = j_;\n"
        "  end\n"
        "end\n"
    )
    tail = (
        "fclose(fo_);\n"
        "fs_ = fopen('s_final.txt','w'); fprintf(fs_, '%.17g\\n', s'); fclose(fs_);\n"
        "fv_ = fopen('v_final.txt','w'); fprintf(fv_, '%.17g\\n', v); fclose(fv_);\n"
    )
    return head + consts + "sd=zeros(N,M);\n" + prefix + "fo_ = fopen('spikes.txt','w');\n" + loop + tail


def octave_version() -> str:
    out = subprocess.run(["octave", "--no-gui", "--version"], capture_output=True, text=True, timeout=60)
    return out.stdout.splitlines()[0].strip() if out.stdout else "unknown"


def crosscheck(Ne=800, Ni=200, M=100, D=20, seconds=5, seed=1, timeout=3600, keep=False) -> dict:
    assert SPNET_M.exists(), f"{SPNET_M} missing"
    sha = hashlib.sha256(SPNET_M.read_bytes()).hexdigest()
    msha = manifest_sha()
    params = SpnetParams(Ne=Ne, Ni=Ni, M=M, D=D)
    rng = np.random.default_rng(seed)
    net = build_network(params, rng)
    inputs = make_inputs(params, seconds, rng)
    N = params.N
    harness = build_harness(SPNET_M.read_text(), seconds)

    tmp = Path(tempfile.mkdtemp(prefix="spnet_cc_"))
    try:
        np.savetxt(tmp / "params.txt", [M, D, Ne, Ni], fmt="%d")
        np.savetxt(tmp / "post.txt", net.post.ravel() + 1, fmt="%d")
        np.savetxt(tmp / "delay.txt", net.delay.ravel(), fmt="%d")
        np.savetxt(tmp / "s0.txt", net.s.ravel(), fmt="%.17g")
        np.savetxt(tmp / "inputs.txt", inputs.ravel() + 1, fmt="%d")
        (tmp / "harness.m").write_text(harness)
        r = subprocess.run(
            ["octave", "--no-gui", "--quiet", "--norc", "harness.m"],
            cwd=tmp, capture_output=True, text=True, timeout=timeout,
        )
        if r.returncode != 0:
            raise RuntimeError(f"octave failed:\n{r.stdout}\n{r.stderr}")
        sp = np.loadtxt(tmp / "spikes.txt", dtype=np.int64, ndmin=2).reshape(-1, 2)
        s_oct = np.loadtxt(tmp / "s_final.txt").reshape(N, M)
    finally:
        if not keep:
            shutil.rmtree(tmp, ignore_errors=True)

    rec = {
        "octave": octave_version(), "source_sha256": sha, "manifest_sha256": msha,
        "source_sha_matches_manifest": sha == msha,
        "seed": seed, "Ne": Ne, "Ni": Ni, "M": M, "D": D, "seconds": seconds,
        "octave_spikes": int(len(sp)),
    }
    for name, fn in (("oracle", run_oracle), ("kernel", run_kernel)):
        res = fn(net, inputs, params)
        same_len = len(res.spike_time) == len(sp)
        spikes_eq = same_len and np.array_equal(res.spike_time, sp[:, 0]) and np.array_equal(
            res.spike_neuron.astype(np.int64), sp[:, 1])
        s_eq = bool(np.array_equal(res.s, s_oct))
        rec[name] = {
            "spikes": int(len(res.spike_time)), "spikes_exact": bool(spikes_eq),
            "s_bit_identical": s_eq, "max_abs_ds": float(np.max(np.abs(res.s - s_oct))),
        }
        if not spikes_eq:
            k = min(len(sp), len(res.spike_time))
            bad = np.nonzero((res.spike_time[:k] != sp[:k, 0]) | (res.spike_neuron[:k] != sp[:k, 1]))[0]
            i = int(bad[0]) if len(bad) else k
            ot = int(sp[i, 0]) if i < len(sp) else None
            rec[name]["first_divergence"] = {
                "spike_index": i, "octave": sp[i].tolist() if i < len(sp) else None,
                "ours": [int(res.spike_time[i]), int(res.spike_neuron[i])] if i < len(res.spike_time) else None,
                "second": (ot // 1000 + 1) if ot is not None else None,
            }
    rec["exact_match"] = all(rec[n]["spikes_exact"] and rec[n]["s_bit_identical"] for n in ("oracle", "kernel"))
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--Ne", type=int, default=800)
    ap.add_argument("--Ni", type=int, default=200)
    ap.add_argument("--M", type=int, default=100)
    ap.add_argument("--D", type=int, default=20)
    ap.add_argument("--seconds", type=int, default=5)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=3600)
    ap.add_argument("--keep", action="store_true", help="keep the temporary directory")
    ap.add_argument("--record", type=Path, default=None, help="write JSON record here")
    a = ap.parse_args(argv)
    rec = crosscheck(a.Ne, a.Ni, a.M, a.D, a.seconds, a.seed, a.timeout, a.keep)
    text = json.dumps(rec, indent=2)
    if a.record:
        a.record.write_text(text + "\n")
    print(text)
    print("EXACT MATCH" if rec["exact_match"] else "MISMATCH")
    return 0 if rec["exact_match"] else 1


if __name__ == "__main__":
    sys.exit(main())
