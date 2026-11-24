# Izhikevich's spiking-neuron modelling work, 2003-2007: the "simple model" (2003), "Which Model to Use" (2004), and *Dynamical Systems in Neuroscience* (2007)

Method note: the primary texts were read in full from the author's own site: spikes.pdf (4 pp.), whichmod.pdf, and the 519-page PDF of the book (dsn.pdf). Citation counts come from the OpenAlex API (retrieved 2026-11-24). Google Scholar and Semantic Scholar were not reachable: Semantic Scholar returned HTTP 429. Google Scholar counts are usually higher than OpenAlex counts.

## 1. "Simple Model of Spiking Neurons" (IEEE Trans. Neural Networks 14(6):1569-1572, Nov 2003)

### Takeaway
The model is a 2D system with one nonlinear term: v' = 0.04v² + 5v + 140 − u + I and u' = a(bv − u). When v ≥ +30 mV, v is reset to c and u to u + d. Izhikevich claimed it is "as biologically plausible as the Hodgkin–Huxley model, yet as computationally efficient as the integrate-and-fire model". He showed seven firing classes (RS, IB, CH, FS, LTS, TC, RZ) by changing only a, b, c and d. The paper prints a 1000-neuron MATLAB network and says a C++ version ran 10,000 neurons with 1,000,000 synapses in real time on a 1 GHz PC.

### Cited Findings
**Bibliographic and abstract**
- The paper is IEEE TNN vol. 14, no. 6, Nov 2003, pp. 1569–1572, DOI 10.1109/TNN.2003.820440. It was received Feb 2003 and revised Apr 2003. The author's affiliation was The Neurosciences Institute, San Diego. — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- The abstract says: "The model combines the biologically plausibility of Hodgkin–Huxley-type dynamics and the computational efficiency of integrate-and-fire neurons. Using this model, one can simulate tens of thousands of spiking cortical neurons in real time (1 ms resolution) using a desktop PC." — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf); [paper page](https://www.izhikevich.org/publications/spikes.htm)

**Equations**
- (1) v' = 0.04v² + 5v + 140 − u + I
- (2) u' = a(bv − u)
- (3) Reset: "if v ≥ 30 mV, then v ← c, u ← u + d".
- Izhikevich calls v, u, a, b, c and d "dimensionless". v is the membrane potential. u is a "membrane recovery variable, which accounts for the activation of K+ ionic currents and inactivation of Na+ ionic currents, and it provides negative feedback to v". +30 mV is the spike apex, not a threshold. — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- The term 0.04v² + 5v + 140 "was obtained by fitting the spike initiation dynamics of a cortical neuron… so that the membrane potential v has mV scale and the time t has ms scale". — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- Resting potential and threshold:
  - The resting potential is between −70 and −60 mV, depending on b.
  - There is "no fixed threshold": depending on history, the threshold can be "as low as −55 mV or as high as −40 mV". — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- Derivation and lineage:
  - The derivation rests on "bifurcation theory and normal form reduction". The v' = v² + I part "is sometimes referred to as being a quadratic integrate-and-fire neuron".
  - The full model was first published in a trigonometric form in Izhikevich (2000), "Neural excitability, spiking, and bursting", Int. J. Bifurc. Chaos, eqns (4)–(5).
  - The 2003 form is described as "more suitable for large-scale simulations". — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)

**Parameter meanings, as stated in the paper**
- **a** is the time scale of u. Smaller values give slower recovery. Typical value: a = 0.02.
- **b** is the sensitivity of u to subthreshold v. Typical value: b = 0.2. Greater values give "possible subthreshold oscillations and low-threshold spiking dynamics". The case b < a corresponds to a saddle-node bifurcation of rest, and b > a to an Andronov–Hopf bifurcation.
- **c** is the after-spike reset of v, "caused by the fast high-threshold K+ conductances". Typical value: c = −65 mV.
- **d** is the after-spike increment of u, "caused by slow high-threshold Na+ and K+ conductances". Typical value: d = 2.
- Source for all four: [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)

**Firing types and the parameter values given in the text** (the rest are the "typical" a = 0.02, b = 0.2, c = −65, d = 2)
- **RS** (regular spiking, excitatory): c = −65, d = 8. Shows spike-frequency adaptation.
- **IB** (intrinsically bursting): c = −55, d = 4. Fires an initial burst, then single spikes, as u builds up.
- **CH** (chattering): c = −50, d = 2. Fires bursts at inter-burst frequencies up to 40 Hz.
- **FS** (fast spiking, inhibitory): a = 0.1. Fires at high frequency with practically no adaptation.
- **LTS** (low-threshold spiking, inhibitory): b = 0.25. The paper adds: "to achieve a better quantitative fit… other parameters… need to be changed as well".
- **TC** (thalamo-cortical): fires tonically from rest near −60 mV and a rebound burst from about −90 mV.
- **RZ** (resonator): a = 0.1, b = 0.26. Shows damped or sustained subthreshold oscillations and bistability between rest and repetitive spiking.
- Source for all seven: [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- The full (a, b, c, d) table, including TC's d, is printed only in the image of Fig. 2, which uses step current I = 10 and 0.1 ms resolution. It could not be extracted as text (see Gaps).
- The paper says other cell types (brainstem, hippocampus, basal ganglia, olfactory bulb) "can also be described". — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- It concedes that for single-neuron studies other polynomials can be better. For example, 0.04v² + 4.1v + 108 with b = −0.1 gives RS cells a saddle-node on invariant circle (SNIC) bifurcation and Class 1 excitability. — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- A suggested extension treats u, a and b as vectors (Σu) for multiple slow time scales. Izhikevich found it "unnecessary for cortical neurons". — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)

**The 1000-neuron demo**
- The network has Ne = 800 excitatory and Ni = 200 inhibitory neurons, a 4:1 ratio, with stronger inhibitory synapses. Each neuron also gets noisy "thalamic" input: 5·randn for excitatory cells and 2·randn for inhibitory cells. — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- Heterogeneity uses a random number r_i ~ U[0,1]:
  - Excitatory cells: (a, b) = (0.02, 0.2) and (c, d) = (−65, 8) + (15, −6)·r_i². So r = 0 gives RS and r = 1 gives CH; squaring biases the population toward RS.
  - Inhibitory cells: (a, b) = (0.02, 0.25) + (0.08, −0.05)·r_i and (c, d) = (−65, 2).
  - Source: [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- Synapses form a pulse-coupled network (PCNN). Weights are S = [0.5·rand(Ne+Ni, Ne), −rand(Ne+Ni, Ni)], so each spike instantly adds s_ij to the target's input. There is no plasticity and no delays. — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- Verbatim integration loop. There is a 1 ms outer step, v gets two 0.5 ms Euler half-steps, and u gets a single 1 ms step:
  ```matlab
  for t=1:1000            % simulation of 1000 ms
    I=[5*randn(Ne,1);2*randn(Ni,1)]; % thalamic input
    fired=find(v>=30);    % indices of spikes
    firings=[firings; t+0*fired,fired];
    v(fired)=c(fired);
    u(fired)=u(fired)+d(fired);
    I=I+sum(S(:,fired),2);
    v=v+0.5*(0.04*v.^2+5*v+140-u+I); % step 0.5 ms
    v=v+0.5*(0.04*v.^2+5*v+140-u+I); % for numerical
    u=u+a.*(b.*v-u);                 % stability
  end;
  ```
  Initial values are v = −65 and u = b·v. — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- Reported network behaviour:
  - Neurons fire "Poisson spike trains with mean firing rates around 8 Hz", with episodes of alpha (~10 Hz) and gamma (~40 Hz) synchrony.
  - Changing synaptic strength or thalamic drive gives "spindle waves and sleep oscillations".
  - "Thus, there is no longer a contradiction between biological plausibility and computational efficiency." — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)

**Efficiency and "simplest possible" claims**
- "We have used this model to simulate a sparse network of 10 000 spiking cortical neurons with 1 000 000 synaptic connections in real time (resolution 1 ms) using a 1 GHz desktop PC and C++." The MATLAB 1000-neuron program also "simulates… in real time". — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- "Our model is the simplest possible model that can reproduce these types of neuronal behavior: It consists of only two equations and has only one nonlinear term, i.e., v²." — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- The paper calls the model "canonical": the difference between it and a whole class of Hodgkin–Huxley-type models "is just a matter of coordinate change". — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- The summary figure was released for free reuse if authors credit izhikevich.com, and an interactive MATLAB tutorial was provided. This likely helped the model spread. — [paper page](https://www.izhikevich.org/publications/spikes.htm)

**Citations**
- OpenAlex shows 5,656 citations as of 2026-11-24. Recent yearly counts: 358 (2021), 427 (2022), 447 (2023), 441 (2024), 504 (2025), and 430 in 2026 so far. — [OpenAlex record](https://api.openalex.org/works/doi:10.1109/TNN.2003.820440)

### Inferences
- The 0.5 ms × 2 half-step for v (with a 1 ms step for u) is a numerical-stability patch. The comment "for numerical stability" is in the original code. Because v and u use different step sizes, the published network is not a clean Euler discretisation of the ODE. This matters for later reproducibility (see Section 4).
- "As biologically plausible as Hodgkin–Huxley" is a claim about qualitative firing patterns under DC steps. It is not a claim about biophysical parameters, and Izhikevich himself says the variables are dimensionless and phenomenological.
- The citation rate is still rising 20+ years on (~500 per year in 2025). The model is a living standard, not a historical curiosity.

### Gaps
- The full numeric (a, b, c, d) table in Fig. 2 is an image. Widely circulated values such as TC d = 0.05, and the c and d values for FS and LTS, were not verified from extractable text. Only the values listed above are text-verified.
- Google Scholar counts were not retrieved; they are normally higher than OpenAlex.

## 2. "Which Model to Use for Cortical Spiking Neurons?" (IEEE TNN 15(5):1063-1070, Sept 2004)

### Takeaway
Izhikevich lists 20 "neuro-computational features" of real neurons. He ranks 11 ODE-based models by which features they show and by FLOPS per 1 ms of simulated time. His model comes out as reproducing all 20 at about 13 FLOPS/ms, against about 1200 for Hodgkin–Huxley. He dismisses leaky integrate-and-fire (I&F) for simulations ("should be avoided by all means"). The method is informal: the author tuned each model himself, and empty squares in the table mean he "failed to find the parameters within a reasonable period of time". That is the main weakness of the comparison. AdEx is not in the paper; it was published a year later.

### Cited Findings
**Bibliographic**
- The paper is IEEE TNN vol. 15, no. 5, Sept 2004, pp. 1063–1070, DOI 10.1109/TNN.2004.832719. It was received May 17, 2003, and the listed revision date is "June 31, 2004" (sic). — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)

**The 20 features (Fig. 1, labels A–T)**, all simulated with the 2003 model:
- (A) tonic spiking
- (B) phasic spiking
- (C) tonic bursting
- (D) phasic bursting
- (E) mixed mode (bursting then spiking)
- (F) spike frequency adaptation
- (G) Class 1 excitability
- (H) Class 2 excitability
- (I) spike latency
- (J) subthreshold oscillations
- (K) frequency preference and resonance
- (L) integration and coincidence detection
- (M) rebound spike
- (N) rebound burst
- (O) threshold variability
- (P) bistability of resting and spiking states
- (Q) depolarizing after-potentials
- (R) accommodation
- (S) inhibition-induced spiking
- (T) inhibition-induced bursting
- Source: [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- "No model should exhibit all these 20 neurocomputational properties simultaneously simply because some of the properties are mutually exclusive (e.g., integrator vs resonator)… all of the neuronal responses in Fig. 1 were obtained using a simple spiking model having four easily tunable parameters." — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- The paper also scores whether each model has "biophysically meaningful and measurable parameters" and whether it can show autonomous chaos. — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)

**Cost method**
- Each model is integrated with "fixed-step first-order Euler" and a step "chosen to achieve a reasonable numerical accuracy". Cost is FLOPS (additions, multiplications, etc.) per 1 ms. — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)

**FLOPS per 1 ms, as stated in the text** (all from [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf))

| Model | Cost per 1 ms | Note |
|---|---|---|
| Leaky I&F | 4 FLOPS + 1 comparison | 1 ms step |
| I&F with adaptation | 10 | |
| Integrate-and-fire-or-burst (Smith et al. 2000) | 9–13 | |
| Resonate-and-fire | 10 | |
| Quadratic I&F (theta neuron / Ermentrout–Kopell) | 7 | |
| Izhikevich (2003) | 13 | |
| FitzHugh–Nagumo | 72 | 18 FLOPS per 0.25 ms step |
| Hindmarsh–Rose | 120 | 30 per 0.25 ms; called "an optimistic assessment that might never be achieved" |
| Wilson polynomial | 180 | 45 per 0.25 ms |
| Morris–Lecar | 600 | 60 per 0.1 ms |
| Hodgkin–Huxley | 1200 | 120 per 0.1 ms, "assuming that each exponent takes only ten operations" |

**Model-by-model judgements in the text**
- **Leaky I&F:** it cannot show phasic spiking, bursting, rebound, threshold variability, bistability, chaos or latency. "Despite its simplicity, I&F is one of the worst models to use in simulations, unless one wants to prove analytical results." — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- **Quadratic I&F:** it is canonical for Class 1 excitable systems and has latencies, an activity-dependent threshold and bistability. It "should be the model of choice when one simulates large-scale networks of integrators", but it is 1D, so it cannot burst or adapt. — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- **Izhikevich model:** it shows chaotic spiking at certain parameters, "though the integration time step should be small". The 30 mV value "is not a threshold, but the peak of the spike"; the threshold is "between –70 and −50, and it is dynamic". — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- **FitzHugh–Nagumo:** a 2D model without reset, so it cannot be autonomously chaotic or burst (except with noise). — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- **Morris–Lecar:** it bursts only with an added equation, and 0.1 ms is "the largest step that gives reasonable results". — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- **Wilson polynomial model:** it can show all properties, "provided that the parameters are chosen appropriately, which is not an easy task". — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- **Hodgkin–Huxley:** it "can actually exhibit all properties in Fig. 1, if the parameters are tuned". It is valuable for biophysically meaningful parameters, dendrites and so on, but "extremely expensive". — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- **Excluded:** the spike response model (Gerstner & Kistler), because it is not an ODE. — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)

**Conclusions**
- For dependence on measurable physiology, use Hodgkin–Huxley-type models, though you can simulate "only tens of coupled spiking neurons in real time". — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- On I&F: "should be avoided by all means… If no attempts to derive analytical results are made, then there is no excuse for using this model in simulations." — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- For fine temporal structure and spike timing, you need a model with all or most of the 20 features. "The model recently proposed by Izhikevich [15] was developed exactly for these purposes. It is the simplest possible model that can exhibit all the firing patterns in Fig. 1." — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)
- Network claims in the paper:
  - A fully connected network of 1000 neurons ran in real time on a 1 GHz PC in MATLAB, and C gives "speed up… by the factor of twenty".
  - A 100,000-neuron network with STDP and axonal delays self-organised into "polychronous groups" (the precursor of the 2006 polychronization work).
  - Source: [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)

**Method caveat in the paper itself**
- In Fig. 2, each empty square marks a property the model "should exhibit in principle… but the author failed to find the parameters within a reasonable period of time". — [whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)

**Citations**
- OpenAlex shows 3,021 citations, with roughly 170–215 per year from 2021 to 2025. — [OpenAlex record](https://api.openalex.org/works/doi:10.1109/TNN.2004.832719)

**AdEx and later critiques**
- The adaptive exponential IF model (AdEx/aEIF) is not in the 2004 table. Brette & Gerstner published it in J. Neurophysiol. 94:3637–3642 in 2005. — [Brette & Gerstner 2005 (PDF)](https://cenl.ucsd.edu/CompNeuro/Readings/week13/Brette-Gerstner+Adaptive-exponential-integrate-fire-effective+JNP+2005.pdf); [PubMed](https://pubmed.ncbi.nlm.nih.gov/16014787/)
- Brette & Gerstner explicitly build on Izhikevich's adaptation-with-reset, and say AdEx "differs from the model of Izhikevich only by the spike mechanism": exponential rather than quadratic. Their quantitative test against a conductance-based RS model predicted 96% of spikes within ±2 ms, against 88% for leaky I&F with adaptation. — [Brette & Gerstner 2005 (PDF)](https://cenl.ucsd.edu/CompNeuro/Readings/week13/Brette-Gerstner+Adaptive-exponential-integrate-fire-effective+JNP+2005.pdf)
- Naud et al. (2008) say the quadratic model with linear recovery reproduces most firing types but produces spikes with an unrealistic delay; the exponential term fixes this. This comes from a search summary; the PDF was not opened. — [Naud et al. 2008 PDF](https://lcnwww.epfl.ch/gerstner/PUBLICATIONS/Naud08.pdf)

### Inferences
- The FLOPS figures are back-of-envelope operation counts. Each depends on a time step that Izhikevich chose for each model (1 ms for his own and for I&F, 0.1–0.25 ms for conductance models). So the 13-vs-1200 contrast partly reflects the 1 ms step allowed for his model. Section 4 shows that step is numerically fragile.
- The feature scoring is the author's own trial-and-error: "failed to find parameters within a reasonable period". The author is also comparing his own model against others, so the table is an advocacy document as much as a benchmark. It also rewards qualitative reproduction of DC-step responses, not quantitative spike-time prediction (the criterion Brette–Gerstner and Jolivet/Gerstner used).
- The paper is best read as a taxonomy of firing phenomena (the A–T figure has become iconic) plus a rough cost argument, not a rigorous benchmark.

### Gaps
- The per-model counts of features (out of 20) in the Fig. 2 table are an image and were not extracted. Exact counts per model (e.g., how many features I&F or Hodgkin–Huxley got) are not given here, to avoid fabrication.
- The table cell for leaky I&F may say "5" (4 operations plus a comparison). The text says "four floating-point operations… plus one comparison"; the image was not verified.
- No published formal rebuttal focused specifically on the 2004 comparison table was found within the search budget. The critiques above are indirect, via AdEx and Touboul.

## 3. *Dynamical Systems in Neuroscience: The Geometry of Excitability and Bursting* (MIT Press, 2007)

### Takeaway
The book is a ~440-page geometric (phase-plane and bifurcation) treatment of single-neuron dynamics in MIT Press's Computational Neuroscience series. Its thesis is that a neuron's computational properties are set by the bifurcation it is near, not just by its ionic currents. Key consequences are Class 1/2/3 excitability and integrators vs resonators. Chapter 8 recasts the simple model in a dimensional 10-parameter form and fits it to many recorded cell types. Reviews praised its clarity, its 400+ figures and its worked solutions, but noted its single-neuron focus. Chapter 10, on synchronization, was moved online. Izhikevich hosts a free full PDF.

### Cited Findings
**Bibliographic**
- *Dynamical Systems in Neuroscience: The Geometry of Excitability and Bursting*, MIT Press, Cambridge MA, © 2007. Computational Neuroscience series, edited by Sejnowski & Poggio. Hardcover ISBN 978-0-262-09043-8; LC catalog QP363.3.I94 2007. Typeset by the author in LaTeX. Dedication: "To my beautiful daughters, Liz and Kate." — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- The SIAM Review book review lists "$60.00. xvi+441 pp., hardcover". — [Moehlis, SIAM Review](https://sites.me.ucsb.edu/~moehlis/moehlis_papers/book_review.pdf)
- A paperback edition has ISBN 9780262514200. — [MIT Press Bookstore](https://mitpressbookstore.mit.edu/book/9780262514200)
- OpenAlex dates the record 2006 (DOI 10.7551/mitpress/2526.001.0001); the copyright year is 2007. — [OpenAlex](https://api.openalex.org/works/doi:10.7551/mitpress/2526.001.0001)
- The author's book page offers:
  - the full PDF, "all chapters";
  - in-vitro data files in MATLAB format, recorded from layer-5 pyramidal cells in rat V1, IB and CH cells, an LTS interneuron (Connors), FS and LS interneurons (Hestrin lab), and mesencephalic V and mitral cells;
  - an errata list with corrections dated 2006–2014.
  - Source: [book page](https://www.izhikevich.org/publications/dsn/index.htm)

**Chapter structure** (from the book's table of contents, [book PDF](https://www.izhikevich.org/publications/dsn.pdf))
- Preface
- Ch 1, Introduction (p. 1): neurons; what is a spike; where is the threshold; phase portraits; bifurcations; Hodgkin classification; neurocomputational properties
- Ch 2, Electrophysiology of Neurons (p. 25): Nernst potential, conductances, voltage-gated channels, the Hodgkin–Huxley model, dendritic compartments
- Ch 3, One-Dimensional Systems (p. 53): I-V relations, equilibria, stability, threshold, bistability and hysteresis, saddle-node bifurcation, quadratic I&F (§3.3.8)
- Ch 4, Two-Dimensional Systems (p. 89): nullclines, limit cycles, relaxation oscillators, classification of equilibria, FitzHugh–Nagumo, stable and unstable manifolds, homoclinic orbits, saddle-node and Andronov–Hopf bifurcations
- Ch 5, Conductance-Based Models and Their Reductions (p. 127):
  - "minimal models" (I_Na,p+I_K, I_Na,t, I_Na,p+I_h, I_h+I_Kir, I_K+I_Kir, I_A, Ca-gated)
  - amplifying vs resonant gating variables
  - reduction of Hodgkin–Huxley
  - "Reduction to Simple Model" (§5.2.4)
- Ch 6, Bifurcations (p. 159):
  - of the rest state: saddle-node, SNIC, supercritical and subcritical Andronov–Hopf
  - of the limit cycle: SNIC, supercritical Hopf, fold limit cycle, homoclinic
  - other cases: cusp, pitchfork, Bogdanov–Takens, canards, Bautin, saddle-node homoclinic
- Ch 7, Neuronal Excitability (p. 215): Hodgkin's classification; Classes 1, 2 and 3; integrators vs resonators; frequency preference; threshold manifolds; rheobase; postinhibitory spikes; inhibition-induced spiking; spike latency; AHP and ADP
- Ch 8, Simple Models (p. 267):
  - I&F; resonate-and-fire; quadratic I&F; "Simple Model of Choice"; canonical models
  - cortex: RS, IB, multi-compartment dendrite, CH, LTS, FS, LS, diversity of interneurons
  - thalamus: TC, RTN, interneurons
  - other cells: CA1 pyramidal, spiny projection neurons, mesencephalic V, entorhinal stellate, mitral cells
- Ch 9, Bursting (p. 325): fast–slow dynamics, minimal models, CPGs, averaging, classification (fold/homoclinic, circle/circle, subHopf/fold cycle, fold/fold cycle, fold/Hopf, fold/circle), bursts as a unit of information, chirps, synchronization
- Ch 10, Synchronization (p. 385): PRCs, isochrons, type 0/1 phase response, Arnold tongues, Winfree/Kuramoto/Malkin approaches, phase models, mean-field. This chapter was dropped from the print book (see the review below) but is in the full PDF.
- Solutions to Exercises (p. 441), References (p. 481), Index (p. 497)

**Central thesis (Preface)**
- The book builds on Hodgkin's 1948 observation that axons with similar currents fire differently (some at arbitrarily low frequencies, others in a narrow band), as explained by Rinzel & Ermentrout (1989) through different bifurcations. — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- The book's restatement of McCormick: "Information-processing depends not only on the electrophysiological properties of neurons but also on their dynamical properties. Even if two neurons in the same region… possess similar electrophysiological features, they may respond to the same synaptic input in very different manners because of each cell's bifurcation dynamics." — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- The type of bifurcation determines the class of excitability, whether a threshold exists, all-or-none spikes, subthreshold oscillations, rebound, bistability, and integrator vs resonator. — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- Style: "few equations but a lot of figures". Exercises marked [M.S.] or [Ph.D.] are suggested thesis topics. — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- Chapter 7 summary:
  - SNIC gives Class 1 (arbitrarily low firing rate). Saddle-node off the invariant circle and Andronov–Hopf give Class 2.
  - Neurons near a saddle-node are integrators: they prefer high-frequency input, have well-defined thresholds, and fire all-or-none spikes with latencies.
  - Neurons near Andronov–Hopf are resonators: they have oscillatory potentials, prefer resonant-frequency input, and fire postinhibitory spikes easily. — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)

**Generalised simple model (Ch. 8, §8.1.4)**
- Dimensionless form: v' = I + v² − u, u' = a(bv − u), with "if v ≥ 1, then v ← c, u ← u + d" (eqs. 8.3–8.4). — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- Fitting form (eqs. 8.5–8.6), C v' = k(v − v_r)(v − v_t) − u + I and u' = a{b(v − v_r) − u}, with "if v ≥ v_peak, then v ← c, u ← u + d". Variable meanings:
  - C is the capacitance (pF).
  - v_r is the resting potential and v_t the instantaneous threshold potential.
  - k and b are fitted from rheobase and input resistance.
  - The sign of b decides whether u is amplifying (b < 0) or resonant (b > 0).
  - v_peak is the spike cutoff.
  - "Though the model seems to have ten parameters… it is equivalent to (8.3, 8.4) and hence has only four independent parameters."
  - Source: [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- The printed RS pyramidal example uses C = 100, v_r = −60, v_t = −40, k = 0.7, a = 0.03, b = −2, c = −50, d = 100 and v_peak = 35, with a forward Euler step tau = 1 ms and a 70 pA step current. Spikes are "padded to vpeak to avoid amplitude jitter associated with the finite simulation time step". — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- Admitted discrepancies against a real pyramidal neuron:
  - The real cell has a sharper upstroke. The proposed fix is a voltage-dependent k (0.7 below v_t, 7 above).
  - The real cell has a smoother downstroke, because the model resets instantaneously. — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- Relation to other models:
  - With b = 0, the model is a quadratic I&F with adaptation.
  - With b < 0, it is a quadratic I&F with a passive dendritic compartment.
  - With b > 0, "the connection to the quadratic integrate-and-fire neuron is lost, and the simple model represents a novel class of spiking models".
  - Source: [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- The book calls the model a "local canonical model for the spike generation mechanism and the spike upstroke of Hodgkin-Huxley-type neuronal models. It is not a global canonical model because it ignores the spike downstroke." — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- Polemic against I&F:
  - I&F "is not a spiking model". Spikes in such figures "are drawn by hand". The book's Fig. 8.1 caption says the spike is added "to fool the reader into believing that this is a spiking neuron".
  - I&F has a logarithmic rather than square-root F–I curve, no latency, and non-unique solutions.
  - "The quadratic integrate-and-fire model is the simplest truly spiking model."
  - Source: [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- Numerical-error argument: spike-timing error scales inversely with v' at reset. It is small for I&F, which needs clever threshold-crossing methods, and "nearly infinite" for the simple model, "hence the error is infinitesimal, and no special methods are needed". — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
  - Touboul's analysis in Section 4 complicates this for the u variable.

**Reception**
- SIAM Review, by Jeff Moehlis (UCSB):
  - "a tour de force on the use of dynamical systems concepts to understand the dynamics of single neurons".
  - "over 400 figures, which are all of high quality".
  - Detailed solutions cover nearly all non-thesis exercises.
  - The simple model "deserves further study and wider use".
  - Criticisms: the "minimal models" approach "seems too cavalier to be ultimately satisfying… useful for pedagogy, but may be not for serious modeling"; the book "focuses too exclusively on the dynamics of single neurons" and does not develop dendritic structure. "The focus on single neurons limits the book's usefulness as a textbook for a general course on mathematical or computational neuroscience."
  - The synchronization chapter was moved online because "some of the reviewers and the publisher felt that it was 'off-topic'… and that its inclusion… would make it too long".
  - Verdict: "What the book does cover, it covers very well."
  - Source: [Moehlis, SIAM Review](https://sites.me.ucsb.edu/~moehlis/moehlis_papers/book_review.pdf)
- The MIT Press listing reportedly quotes a Mathematical Reviews notice by Jonathan E. Rubin calling the book suitable for students and researchers in theoretical neuroscience. This comes from a search summary and the original was not read. — [MIT Press Bookstore](https://mitpressbookstore.mit.edu/book/9780262514200)
- Goodreads reader reviews are mostly positive. One critic says the book under-acknowledges the limits of dynamical-systems techniques. These are informal reviews, read via a search summary. — [Goodreads](https://www.goodreads.com/book/show/818045)
- Draft reviewers named in the Preface include Ermentrout, FitzHugh, Golomb, Rinzel, Medvedev and Doiron. — [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- The errata page credits readers at UCSB, Barcelona, Missouri, Korea University and elsewhere from 2006 to 2014, a sign of classroom use. — [book page](https://www.izhikevich.org/publications/dsn/index.htm)
- OpenAlex shows 5,087 citations, with about 276–320 per year from 2021 to 2025. — [OpenAlex](https://api.openalex.org/works/doi:10.7551/mitpress/2526.001.0001)
- MathWorks lists the book among its academia books. — [MathWorks](https://au.mathworks.com/academia/books/dynamical-systems-in-neuroscience-izkevich.html)

### Inferences
- Chapter 8 is where the 2003 model gets its fullest justification and its dimensional, fittable form (the "9-parameter Izhikevich" form used by CARLsim and other simulators).
- Free hosting of the full PDF plus real recording data has likely helped the book's wide adoption in courses.
- The reviewer's comment that it is not a general computational neuroscience text suggests it is typically used as a specialised text for neuronal dynamics or excitability, next to broader texts such as Dayan & Abbott or Gerstner et al.

### Gaps
- Course syllabi were not surveyed systematically, so the claim that the book is widely used as a textbook rests on reviews, errata contributors and citation counts.
- The full Rubin MathSciNet review and any reviews in J. Neurophysiology or Trends in Neurosciences were not retrieved.

## 4. Known limitations and critiques: numerics, interpretability, fitting, AdEx, Touboul

### Takeaway
The main technical critiques are:
- **Cutoff sensitivity:** the quadratic upswing blows up in finite time, so the 30 mV cutoff and reset of u are sensitive to its value and to the time step (Touboul 2008).
- **Unstable published numerics:** the original 1 ms / 0.5 ms Euler scheme is unstable and produces artefacts. NEST now defaults to "consistent" integration (Pauli et al. 2018).
- **Phenomenological parameters:** a, b, c and d have no direct biophysical meaning, and fit is qualitative.
- **Spike shape:** spikes have an unrealistically slow upstroke, which AdEx's exponential term addresses (Brette & Gerstner 2005; Naud et al. 2008).

### Cited Findings
**Touboul**
- Touboul, "Sensitivity to the cutoff value in the quadratic adaptive integrate-and-fire model" (arXiv 0812.1164, 2008; later published in Neural Computation 2009). He shows that when the system does not converge to an equilibrium, "both variables of the subthreshold dynamical system blow up in finite time whatever the parameters". So "the cutoff is therefore essential for the model to be well defined". The divergence of u "makes the system very sensitive to the cutoff: changing this parameter dramatically changes the spike patterns produced". The time step "needs to be very small (or adaptive) in order to catch an accurate value of the adaptation at the time of the spike". The quartic (Touboul 2008) and exponential (AdEx) models do not have this problem. — [Touboul arXiv 0812.1164](https://arxiv.org/pdf/0812.1164)
- The same note opens by acknowledging that the model "is recognized as very interesting for its computational efficiency and its ability to reproduce many behaviors observed in cortical neurons… currently widely used, in particular for large scale simulations". — [Touboul arXiv 0812.1164](https://arxiv.org/pdf/0812.1164)
- Touboul, "Bifurcation analysis of a general class of nonlinear integrate-and-fire neurons", SIAM J. Appl. Math. 68(4):1045–1079 (2008); also INRIA RR-6161. It gives a full bifurcation analysis of the class of 2D adaptive nonlinear IF models with F(v) convex, which includes the Izhikevich (F = v²) and AdEx models. Bifurcations found are Hopf, saddle-node, Bogdanov–Takens and Bautin. Read via search summary; the full text was not opened. — [arXiv 0812.1164 references](https://arxiv.org/html/0812.1164); [Springer, Touboul & Brette 2008](https://link.springer.com/doi/10.1007/s00422-008-0267-4)

**Pauli et al. 2018 (reproducing the 2006 polychronization network)**
- They quote the original update `v+=0.5*(...); v+=0.5*(...); u+=a*(0.2*v-u)` and note that:
  - "the forward Euler integration is a first order method";
  - "1 ms as the integration time step is ten times longer than usual";
  - "v is integrated in two 0.5 ms steps whilst u is integrated in one 1 ms step";
  - forcing spikes onto a 1 ms grid "may result in artefactual synchrony".
  - Source: [Pauli et al. 2018, Front. Neuroinform.](https://www.frontiersin.org/articles/10.3389/fninf.2018.00046/pdf)
- "The numerical integration used in the original code is not sufficiently stable, as evidenced by the membrane voltage frequently reaching values around 1,000 mV." "The numerical integration of the dynamics is critical for the model behavior." — [Pauli et al. 2018](https://www.frontiersin.org/articles/10.3389/fninf.2018.00046/pdf)
- Related work:
  - Trensch et al. (2018) reproduced the network on SpiNNaker and analysed time step and data type in detail.
  - Blundell et al. (2018) addressed solver choice. — [Pauli et al. 2018](https://www.frontiersin.org/articles/10.3389/fninf.2018.00046/pdf); [Trensch et al. 2018 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6275234)

**NEST's response**
- NEST's `izhikevich` model has a `consistent_integration` flag:
  - false gives "the published form of the dynamics (for replicating published results)", where V_m is updated with half the step of U_m;
  - true, the default, gives "the standard Euler method (recommended for general use)".
  - The documentation cites Pauli et al. 2018. — [NEST izhikevich docs](https://nest-simulator.readthedocs.io/en/stable/models/izhikevich.html)

**Interpretability and fitting**
- The 2003 paper itself calls the variables and parameters dimensionless. It says better quantitative LTS fits need other parameters changed, and that single-neuron work may need other polynomials. — [spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)
- The book's own position, in Ch. 8:
  - Measured conductance-based parameters are "averaged, and then fine-tuned (a fancy term meaning 'to make arbitrary choices')", so biophysical meaning does not guarantee correct dynamics.
  - The simple model's 10-parameter form has only 4 independent parameters, with k and b set from rheobase and input resistance.
  - Admitted shape discrepancies: slow upstroke and instantaneous downstroke.
  - Source: [book PDF](https://www.izhikevich.org/publications/dsn.pdf)
- The Moehlis SIAM Review notes that the model "dynamically captures the upstroke of an action potential, although not the downstroke". — [Moehlis, SIAM Review](https://sites.me.ucsb.edu/~moehlis/moehlis_papers/book_review.pdf)

**AdEx vs Izhikevich**
- In AdEx, a reset value can be changed (e.g., Vr from −70 to −47 mV makes it burst), "the same properties" as Izhikevich's model. AdEx parameters (gL, EL, ΔT, VT, τw, a, b) are closer to measurable quantities, and the cutoff "is not critical because it only shifts spike times by a fraction of millisecond". It predicted 96% of spikes against a conductance-based model. — [Brette & Gerstner 2005 (PDF)](https://cenl.ucsd.edu/CompNeuro/Readings/week13/Brette-Gerstner+Adaptive-exponential-integrate-fire-effective+JNP+2005.pdf)
- Naud et al. (2008, Biol. Cybern.) catalogued AdEx firing patterns in the style of Izhikevich's A–T figure. Per a search summary, they note the quadratic model's unrealistic spike-initiation delay. — [Naud et al. 2008 PDF](https://lcnwww.epfl.ch/gerstner/PUBLICATIONS/Naud08.pdf); [Springer](https://link.springer.com/article/10.1007/s00422-008-0264-7)

**Platform constraints**
- An LGN model on SpiNNaker built from Izhikevich neurons needed a time step finer than 1 ms, so it ran slower than real time. — [LGN on SpiNNaker (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5552764/)

### Inferences
- The book claims the simple model's reset error is "infinitesimal" because v' is nearly infinite at the peak. Touboul's result is in tension with that claim: v's timing error may be small, but u also blows up, so the value of u carried through the reset (and hence the next ISI and the firing pattern) depends on the cutoff and the time step.
- Many "Izhikevich network" results, especially those copying the 1 ms MATLAB/C++ scheme, may include numerical artefacts (spurious synchrony, voltage overshoots). Reproductions should state the integration scheme.
- AdEx is generally positioned as the "same idea, better-behaved spike". In practice the field split: AdEx became popular in Gerstner/Brette-linked and European (e.g., BrainScaleS) contexts, while Izhikevich stayed popular in GPU and engineering contexts (CARLsim, SpiNNaker). This split is an inference and not directly sourced.

### Gaps
- Humphries & Gurney (2007) and Stewart & Bair (2009, Parker–Sochacki integration) are believed to analyse Izhikevich-model solvers, but were not retrieved and so are not cited.
- Touboul's SIAM J. Appl. Math. 2008 theorems were not read in full text.

## 5. Adoption: simulators, neuromorphic hardware, citation counts

### Takeaway
The model is a built-in standard in most major SNN simulators: NEST, Brian 2 (examples), CARLsim (its core neuron), and PyNN-compatible SpiNNaker (sPyNNaker), with FPGA simulators and many FPGA papers as well. Citation counts (OpenAlex, Nov 2026) are about 5,660 for the 2003 paper, about 3,020 for the 2004 paper, and about 5,090 for the book, with the 2003 paper still gaining about 450–500 per year. Mainstream digital neuromorphic chips (Loihi, TrueNorth) use their own LIF-family neurons, not Izhikevich, as far as could be found.

### Cited Findings
**Simulators**
- **NEST:** a native `izhikevich` model with defaults a = 0.02, b = 0.2, c = −65, d = 8, and both published and consistent integration (see Section 4). — [NEST izhikevich docs](https://nest-simulator.readthedocs.io/en/stable/models/izhikevich.html)
- **Brian 2:** the example gallery includes "Izhikevich_2003" and "Izhikevich_2007" (alongside Naud_et_al_2008_adex_firing_patterns, Hindmarsh_Rose_1984, Morris_Lecar_1981). — [Brian 2 examples](https://brian2.readthedocs.io/en/stable/examples/frompapers.Izhikevich_2007.html)
- **CARLsim:**
  - describes itself as a GPU-accelerated library that "allows execution of networks of Izhikevich spiking neurons with realistic synaptic dynamics on both generic x86 CPUs and standard off-the-shelf GPUs", with a PyNN-like C/C++ API;
  - v3.1 added the "9-parameter Izhikevich" model (the book's form) and Runge–Kutta integration (Beyeler et al. 2014);
  - the current release is CARLsim6.
  - Source: [CARLsim6 site](https://uci-carl.github.io/CARLsim6/)
- **SpiNNaker / PyNN:** SpiNNaker's PyNN interface (sPyNNaker) provides standard neuron models "such as LIF and Izhikevich's dynamical systems model". — [PMC6257411](https://pmc.ncbi.nlm.nih.gov/articles/PMC6257411)
  - Hardware parameter constraints such as weight precision mean Izhikevich parameters may not map exactly. — [arXiv 2004.01656](https://arxiv.org/pdf/2004.01656)
- **FPGA:**
  - NeuroFlow (Imperial College), an FPGA simulator taking PyNN descriptions, supports Izhikevich models. — [NeuroFlow paper](https://www.doc.ic.ac.uk/~wl/papers/16/fns16kc.pdf)
  - A Politecnico di Torino thesis implemented an Izhikevich pipeline on PYNQ-Z2 for signal-to-spike encoding, using about 50% of FPGA resources. — [PoliTo thesis](https://webthesis.biblio.polito.it/secure/37606/1/tesi.pdf)
- **SpiNNaker applications:** an LGN model chose Izhikevich neurons for "versatility and low computational cost". — [LGN on SpiNNaker (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5552764/)
- **Reproduction tooling:** the SpiNNaker reproduction of the Izhikevich polychronization network was validated statistically against the original. — [Trensch et al. 2018 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6275234); [Pauli et al. 2018](https://www.frontiersin.org/articles/10.3389/fninf.2018.00046/pdf)

**Citation counts (OpenAlex, retrieved 2026-11-24)**

| Work | Total citations | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (partial) |
|---|---|---|---|---|---|---|---|
| Simple model (2003) | 5,656 | 358 | 427 | 447 | 441 | 504 | 430 |
| Which model (2004) | 3,021 | 177 | 190 | 202 | 196 | 214 | 172 |
| DSN book | 5,087 | 276 | 284 | 281 | 294 | 320 | 305 |

- Sources: [OpenAlex 2003](https://api.openalex.org/works/doi:10.1109/TNN.2003.820440), [OpenAlex 2004](https://api.openalex.org/works/doi:10.1109/TNN.2004.832719), [OpenAlex book](https://api.openalex.org/works/doi:10.7551/mitpress/2526.001.0001)

### Inferences
- The model's mix of a cheap update, rich behaviour and a public figure with a free licence made it a default "biologically flavoured" neuron for GPU and neuromorphic engineering. That is the community most citing the 2003 paper now: neuromorphic hardware, memristor and FPGA neurons, and SNNs for machine learning.
- Google Scholar totals are likely substantially higher than OpenAlex totals: plausibly more than 8,000 for the 2003 paper. This is unverified.

### Gaps
- The NEURON, GeNN and PyNN-standard-library documentation pages could not be fetched in this session. Possible support exists through NEURON's `Izhi2007` example mechanism (ModelDB), GeNN's built-in `Izhikevich` / `IzhikevichVariable` models, and PyNN's `Izhikevich` standard cell type, but it is unconfirmed here and should be checked before stating it as fact.
- Intel Loihi (CUBA LIF compartments) and IBM TrueNorth (an augmented LIF neuron) are believed not to implement the Izhikevich model natively. No source was retrieved in this session to confirm this.
- No direct Google Scholar numbers were obtained.
