# spnet long-run statistics

Command (from repo root, `PYTHONPATH=src`; about 44-50 s wall per seed, 5 seeds, 3600 s model time each, one kernel call per seed):

```
python scripts/validate_spnet.py --seeds 1 2 3 4 5 --seconds 3600 --out benchmarks/records --figdir docs/validation/figures
```

Default `SpnetParams` (800 exc + 200 inh, M=100, D=20, sm=10), git SHA `cb6b9113e515`. Records: `benchmarks/records/validation-spnet-seed<k>.json`. Spectra are Welch (2 s segments, 50% overlap) of 1 ms population spike counts; early = 0-10 s, late = last 100 s. Weight fractions: below 0.5 / above sm-0.5.

| Seed | Rate exc Hz first / last min | Rate inh Hz first / last min | Late delta peak (Hz) | Late gamma peak (Hz) | Gamma/delta power early / late | Frac w<0.5 | Frac w>9.5 | Mean w |
|---|---|---|---|---|---|---|---|---|
| 1 | 2.93 / 3.51 | 18.3 / 28.8 | 2.5 | 29.5 | 0.108 / 1.246 | 0.232 | 0.491 | 6.24 |
| 2 | 3.38 / 3.49 | 22.0 / 28.7 | 3.0 | 30.5 | 0.083 / 1.148 | 0.235 | 0.495 | 6.22 |
| 3 | 2.76 / 4.27 | 16.9 / 33.0 | 1.0 | 58.0 | 0.086 / 0.761 | 0.387 | 0.485 | 5.39 |
| 4 | 2.85 / 4.45 | 17.7 / 35.5 | 1.5 | 55.5 | 0.095 / 0.717 | 0.355 | 0.503 | 5.64 |
| 5 | 2.87 / 4.21 | 17.9 / 33.6 | 1.0 | 55.5 | 0.105 / 0.702 | 0.347 | 0.500 | 5.65 |

Early gamma-range peaks were 26.5-32 Hz in all seeds. Excitatory ISI CV (last 100 s) was 0.64-0.78. Excitatory 60 s rates stayed within 2.76-4.85 Hz throughout.

## Comparison with what has been reported

Caveats: our networks use our own random numbers (numpy) and the random-delay variant of spnet.m (2008 modification). The comparison values come from a summary note (`references/notes/2026-11-24-spnet-replications-and-simulators.md`), not from our own reading of the papers, and are stated as reported, not re-verified.

- **(a) Sleep-like oscillations and gamma (about 40 Hz), per the paper abstract.** Partly consistent. Delta-range (1-3 Hz) peaks are present in all seeds and gamma/delta power rises about 7-14x from early to late, but late gamma peaks sit near 30 Hz (seeds 1-2) or 55-58 Hz (seeds 3-5), not at 40 Hz. Whether this counts as "gamma" depends on the band definition; not comparable beyond that.
- **(b) Pauli et al. 2018 as summarised.** Rates of 2-5 Hz: consistent for excitatory neurons (2.8-4.9 Hz); we have no reported inhibitory figure to compare, and ours is 17-35 Hz. Bimodal weights: consistent in shape (about 23-39% near 0 and about 49-50% near sm), see figure. Gamma near 60 Hz in most seeds and 40 Hz in some: seeds 3-5 (55-58 Hz) are near 60 Hz; seeds 1-2 (about 30 Hz) match neither mode. With 5 seeds this is only suggestive, and the bin width is 0.5 Hz.

## Figures

- [Rates](figures/spnet-rates.png)
- [Weights](figures/spnet-weights.png)
- [Spectra](figures/spnet-spectra.png)
- [Seed 1 raster](figures/spnet-raster-seed1.png)

## Open questions

- Why do seeds 1-2 settle at a roughly 30 Hz peak and seeds 3-5 at 55-58 Hz? Is this a bimodality like the reported 40/60 Hz split, or an artefact of our small sample?
- Inhibitory rates rise from about 17-22 Hz to 29-36 Hz over the hour; we do not know if the original does this.
- Final membrane potentials of the neurons caught mid-spike reach 1000-1600 in all seeds, which fits the reported large-v behaviour of the original integration scheme but was not checked.
- Weight fractions below 0.5 differ between seed groups (0.23 vs 0.35-0.39), tracking the gamma split.
