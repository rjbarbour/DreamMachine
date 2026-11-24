# Cross-check against the original spnet.m

**Compared:** our `run_oracle` and `run_kernel` versus Izhikevich's original
`spnet.m` (modified 2008 version) executed in GNU Octave 8.4.0. For the same
network and thalamic-input sequence we compare the ordered (time, neuron)
spike sequence and the final synaptic weights `s` (float64, exact equality).

**How the original runs without being copied:** `scripts/crosscheck_original.py`
writes the network (`post`, `delay`, initial `s`, input indices, 1-based) to a
temporary directory and generates a harness `.m` at run time. The harness takes
the original's `a/d/sm` lines, its own `pre`/`aux` construction code and its
simulation loop from the git-ignored cached file. Only mechanical edits are
made, each asserted to match exactly once: loop bound `60*60*24` becomes the
requested seconds, `I(ceil(N*rand))=20;` reads our input index, the plot lines
become a spike dump. The cached file's SHA-256 (e89495...e69d) equals the
`izhikevich_spnet_m` manifest value. Nothing from the file enters the repo.

**Command:** `python scripts/crosscheck_original.py --seconds 5`
(small: `--Ne 40 --Ni 10 --M 10 --D 5 --seconds 3`; seed 1 both).

| Network | Seconds | Spikes (Octave / oracle / kernel) | Exact | max abs ds |
|---|---|---|---|---|
| 40+10, M=10, D=5 | 3 | 1272 / 1272 / 1272 | yes | 0.0 |
| 800+200, M=100, D=20 | 5 | 31675 / 31675 / 31675 | yes | 0.0 |
| 800+200, M=100, D=20 | 20 | 70906 / 70906 / 70906 | yes | 0.0 |

Octave wall time: about 27 s for 5 s, 56 s for 20 s of the full network.

**Limits:** only the `.m` file was checked, not `spnet.cpp`; random numbers
are ours (numpy), not MATLAB's, so wiring and input are not Izhikevich's
stream; one seed; at most 20 simulated seconds, so behaviour over longer
runs (e.g. weight saturation) is not covered; Octave, not MATLAB, so
MATLAB-specific floating-point behaviour is untested.
