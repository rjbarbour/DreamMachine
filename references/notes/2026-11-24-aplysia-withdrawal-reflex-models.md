# Aplysia withdrawal-reflex learning: models, circuit, mechanisms, targets

**Compiled:** 2026-11-24 by a research sub-agent from web search results, web pages and public NCBI (PubMed abstracts, PMC full text). Not re-checked by a second reader. Page reads were summarised by a fetch tool, so quoted numbers should be checked against the paper before a task relies on them. Keys refer to `references/manifest.jsonl`. "Figure only" means the page text gave no number.

## 1. Computational models of withdrawal-reflex learning

| Model | Level | Phenomena | Code | Source |
|---|---|---|---|---|
| Gingrich & Byrne 1985 | Lumped-parameter model of one sensory-neuron synapse: Ca2+-channel inactivation, release, readily releasable and feeding pools | Depression and recovery, posttetanic potentiation, spike-broadening facilitation; most depression is pool depletion | none seen | `gingrich1985_simulation` (abstract, PMID 2580065) |
| Gingrich & Byrne 1987 | Single-cell subcellular model: CS spike Ca2+ primes adenylyl cyclase, US drives cAMP | Activity-dependent neuromodulation; predicts a characteristic ISI curve tied to Ca2+ buffering | none seen | `gingrich1987_associative` (abstract, PMID 3037039) |
| Lieb & Frost 1997 | Integrate-and-fire: 4 cell types (LFS, L29, L30, L34), 10 synapses | Motor output of the circuit; no learning rule in the abstract. L29-L30 electrical coupling had little impact | none seen | `lieb1997_siphon_circuit` (abstract, PMID 9084594) |
| Pettigrew 2005; Zhang 2011; Zhang 2021 | ODE models of PKA/ERK/CREB and growth-factor cascades | Massed vs spaced 5-HT, protocol design for LTF. 2021: ODEs, RK4 at 3 s, XPPAUT | 2021 paper says code "will be submitted" to ModelDB and GitHub; no accession seen | `pettigrew2005_motifs`, `zhang2011_protocols`, `zhang2021_kinases` |
| Zhou, Baxter & Byrne 2014 | Transmitter-release model, PKC-dependent mobilisation | Short-term facilitation at depressed and non-depressed synapses | C/C++ on ModelDB 152200, downloadable (page opened) | `zhou2014_pkc`, `zhou2014_modeldb` |
| SNNAP | Java simulator, conductance-based cells and synapses | Used for Aplysia models | Official page lists SNNAP v8.1 download; link not tested; no licence stated | `snnap_page`, `ziv1994_snnap` (unopened) |

I found no withdrawal-reflex learning model after 2018 other than the 2021 cascade model; NEURONpyxl (2026, PMID 42238303) appeared only as a PubMed title and is unopened (`dickman2026_neuronpyxl`). Hawkins & Kandel 1984 was seen only as a citation (`hawkins1984_alphabet`, unopened). Hawkins 1989 and Buonomano, Baxter & Byrne 1990 could not be located (see Not verified).

## 2. Minimal circuit

- Siphon CS activates LE sensory neurons, which excite LFS motor neurons monosynaptically and also drive interneurons (`byrne2015_nonassociative`; `antonov1999_monosynaptic`). The LE-to-LFS monosynaptic EPSPs mediate about one-third of the reflex and a tap activates about five LE cells (`antonov1999_monosynaptic`, text). The 2010 paper (full text) says the reflex is mediated by 5-8 LE and 3 LFS cells.
- Inhibitory interneuron L30 and excitatory L29 shape LFS firing; the sensory-to-motor path gives only the initial burst, the polysynaptic path sets duration (`lieb1997_siphon_circuit`).
- L29 neurons are facilitatory interneurons and express NO synthase (`antonov2007_no`). L7 and L28: no source opened.
- Electrical coupling: L29-L30 coupling had little effect in the 1997 model; two LFS cells showed no coupling (`antonov1999_monosynaptic`). Inference: it can be omitted in v0.
- Counts: nervous system about 10,000 neurons, withdrawal circuits tens to hundreds (`byrne2015_nonassociative`, text). No abdominal-ganglion count found in an opened source.

## 3. Mechanisms and the STDP question

- **Habituation:** homosynaptic depression at sensory-motor synapses (`byrne2015_nonassociative`). Presynaptic: fewer quanta per impulse, receptor sensitivity unchanged (`castellucci1974_quantal`, abstract). Depletion of release pools explains much of it (`gingrich1985_simulation`).
- **Sensitization, dishabituation:** tail shock drives facilitatory interneurons releasing 5-HT; PKA, spike broadening, mobilisation (`byrne2015_nonassociative`). One shock uses PKA and CaMKII; four shocks add postsynaptic Ca2+; dishabituation by four shocks uses presynaptic PKC instead (`antonov2010_itm`). PKC acts on mobilisation (`zhou2014_pkc`).
- **Classical conditioning:** US-driven facilitation is amplified when CS spikes precede it (`hawkins1983_amplification`). Hebb's postulate alone was neither necessary nor sufficient (`carew1984_hebb`). Later work added an NMDA-dependent postsynaptic LTP component (`murphy1997_ltp`, `murphy1999_apv`, `roberts2003_both_sides`), both mechanisms being required and interacting through retrograde signalling (`antonov2003_neuron`).
- **Long-term facilitation:** five 5-HT pulses or five tail shocks 15 min apart; PKA-CREB1, ERK-CREB2, protein synthesis (`byrne2015_nonassociative`).

**Answer.** Pair-based STDP is not an appropriate model for any of these as the primary mechanism. Habituation needs short-term depression (depletion with recovery). Sensitization and dishabituation need neuromodulator-gated facilitation that does not depend on postsynaptic spikes. Conditioning needs presynaptic-activity-times-modulator coincidence with a forward ISI near 0.5 s (a three-factor rule), plus a Hebbian postsynaptic term. Only that last term resembles pair-based plasticity. I found no source measuring a pre/post spike-timing window at these synapses (an absence from searches, not proof).

## 4. Validation targets

| Target | Value | Where |
|---|---|---|
| Habituation protocol | 10 siphon stimuli, 10 s ISI; behavioural habituation about 1 h; EPSP decrement "approximately paralleled" it | `antonov2010_itm`; EPSP magnitude figure only |
| Habituation, 1974 quantal data | Decrement and recovery times not read | `castellucci1974_quantal` abstract only |
| Facilitation after tail shock | 25 mA, 1 s shock; one shock: behavioural sensitization significant at 2.5 and 17.5 min, about 30 min; four shocks (2 s apart): EPSP facilitation significant 2.5-62.5 min, about 1 h. Pretest EPSP 5.9-6.1 mV | `antonov2010_itm`; percent facilitation figure only |
| Facilitation after 5-HT | About 1 min 5-HT: short-term; about 10 min: intermediate (hours) | `byrne2015_nonassociative`, text |
| ISI dependence, behaviour | Differential conditioning at CS+ leading US by 0.5 s; marginal at 1.0 s; none at 2, 5, 10 s, simultaneous, or backward (US leading by 0.5-1.5 s) | `hawkins1986_isi`, abstract text; magnitudes not read |
| Contingency | Extra unpaired USs abolished conditioning | `hawkins1986_isi` |
| Pairing in cells | Paired > unpaired > US alone EPSP facilitation | `hawkins1983_amplification` (no numbers) |

## Implications for the simulator

- Build short-term depression and recovery first; it carries habituation and is the baseline for facilitation of depressed synapses.
- Implement serotonin-like facilitation as a modulator-gated multiplier on release with PKA-like and PKC-like (mobilisation) routes, not as STDP.
- Make conditioning a three-factor rule: presynaptic activity, a modulator burst, a CS-to-US delay window of about 0.5 s; add a postsynaptic Hebbian term as a separate option.
- Izhikevich neurons cannot represent spike broadening; model release probability or a facilitation variable directly.
- Skip kinase cascades and LTF in v0; ODE models exist (`zhang2021_kinases`) to cite.
- Most numeric targets are in figures; plan extraction and label comparisons qualitative where no number exists.

Order of experiments: (1) depression and recovery at one synapse; (2) habituation, 10 stimuli at 10 s; (3) tail-shock facilitation and dishabituation; (4) ISI sweep from 0 to 10 s, including backward; (5) contingency; (6) postsynaptic-block control.

## Not verified

- Hawkins 1989 and Buonomano, Baxter & Byrne 1990: not located. Hawkins & Kandel 1984 seen only as a citation.
- Whether SNNAP's download link works; its licence.
- Abdominal-ganglion neuron count; L7 and L28 roles; facilitator counts.
- Castellucci 1974 numbers; any figure values; trial spacing in the 1986 ISI study.
- ModelDB listing of other Aplysia models (the site returned 503 once).
- Neuron count "about 10,000" and "5-8 LE, 3 LFS" are from fetch-tool summaries of full text.
