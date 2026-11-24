# Izhikevich's Two-Equation Neuron Outlasted His Grand Theories

Eugene M. Izhikevich's most lasting contribution is a small piece of applied mathematics. His 2003 "simple model of spiking neurons" uses two differential equations, one quadratic term and four parameters. It reproduces the firing repertoire of cortical neurons at roughly the cost of an integrate-and-fire unit. As of November 2026 it has **about 5,660 OpenAlex citations, still rising by about 500 a year**, and it ships as a standard neuron in NEST, Brian 2, CARLsim and SpiNNaker. The model was not a lucky shortcut. It came out of a decade of bifurcation theory: the 1997 *Weakly Connected Neural Networks* monograph with Frank Hoppensteadt, the 2000 burster taxonomy, and the integrator/resonator distinction. The 2007 MIT Press book *Dynamical Systems in Neuroscience* (about 5,090 citations) set all of this down in one place. The bolder theories from his years at Gerald Edelman's Neurosciences Institute fared unevenly:

- **Dopamine-gated STDP** (2007) became a standard template for "three-factor" learning rules, and the one-second eligibility trace it assumed later gained experimental support.
- **Polychronization** (2006) claimed networks hold more spike-timing groups than neurons. A 2018 replication found that the claim depends heavily on the numerical method.
- **The 100-billion-neuron simulation** (2005) was, in his own words, of no scientific value beyond learning what such a run takes.

After 2009 he largely left academic publishing. He ran Scholarpedia, which he had founded in 2006, and co-founded Brain Corporation. Brain Corp began as a Qualcomm-backed spiking-network lab and became a floor-scrubber autonomy company with more than 50,000 robots deployed; his name is on about 98 US patents. In December 2025 he returned with an arXiv "Spiking Manifesto", which claims a roughly thousandfold efficiency gain for AI. He spent 2026 promoting it on a seminar tour as CEO of a new startup, SpikeCore. As of November 2026 the manifesto is neither peer-reviewed nor independently replicated.

## A Moscow cyberneticist became a San Diego founder in four moves

Izhikevich's career divides into four phases: Moscow, Michigan and Arizona, the Neurosciences Institute, and Brain Corp. Each phase shifted what he worked on. One common biographical error should be corrected. His PhD is from **Michigan State University (Mathematics, 1996)**, not Arizona State. His advisor was Frank C. Hoppensteadt, who later moved to ASU, where Izhikevich did his postdoctoral work. His 1996 papers already carry ASU affiliations, which explains the confusion ([CV](https://www.izhikevich.org/cv/index.htm); [Mathematics Genealogy Project](https://www.mathgenealogy.org/id.php?id=8455); [bc1.pdf](https://www.izhikevich.org/publications/bc1.pdf)). OpenAlex gives the dissertation title as *Bifurcations in brain dynamics* ([OpenAlex](https://api.openalex.org/works?filter=author.id:A5091804814)).

| Period | Position | Main work |
|---|---|---|
| 1984–1992 | Student, Cybernetics & Computer Science and Biology, Moscow State (M.S. 1992); Navy service 1985–88 | Chaos and memory in neural networks; organised a "Mathematical Neuroscience" seminar 1990–93 |
| 1993–1996 | Graduate student, Mathematics, Michigan State (Ph.D. 1996, advisor Hoppensteadt) | Canonical models of weakly connected networks |
| 1996–2000 | Postdoc, then Faculty Research Associate, Arizona State | Oscillatory neurocomputers, bursting, excitability classes |
| 2000–2009 | Associate Fellow, then Senior Fellow (2005), The Neurosciences Institute, San Diego | Simple model, polychronization, DA-STDP, large-scale models, Scholarpedia |
| 2009–present | Co-founder of Brain Corp: CEO to Nov 2022, then Chairman; CEO of SpikeCore by 2026 | Robotics autonomy, patents, Spiking Manifesto |

Sources: [CV](https://www.izhikevich.org/cv/index.htm); [Brain Corp team page](https://braincorp.com/team/dr-eugene-izhikevich); [Brain Corp release, 2022](https://braincorp.com/resources/david-pinn-promoted-to-ceo-of-brain-corporation-eb694); [Redwood Center, Feb 2026](https://redwood.berkeley.edu/seminars/eugene-izhikevich-feb-2026/).

His publications page, the starting point for this review, is a legacy page still titled "old (NSI) list of publications". It lists **2 books, the Scholarpedia editorship and 52 article entries from 1991 to 2025** ([publications](https://www.izhikevich.org/publications/)). The page's navigation links to "patents" and "talks" sections, but neither exists. The list also leaves out items that other indexes record, including the dissertation, conference papers from 2000–2002, and a 2016 arXiv paper on cortical computation ([OpenAlex](https://api.openalex.org/works?filter=author.id:A5091804814)).

Two patterns in the list stand out. Hoppensteadt is his most frequent co-author, on **14 of the 52 entries**. And between the 2010 papers and the December 2025 manifesto, the only new entry is a 2015 Scholarpedia article on the Game of Life, co-written with John H. Conway and Anil Seth ([publications](https://www.izhikevich.org/publications/)). The bibliography shows that the scientist effectively went quiet once the company started.

## Canonical models made frequency and bifurcation the organizing ideas of the 1990s

The early work matters because it explains why the 2003 model works. Izhikevich's 1997 Springer monograph with Hoppensteadt, *Weakly Connected Neural Networks* (~400 pp., Applied Mathematical Sciences vol. 126), was built on two premises:

- **Weak coupling.** Synaptic coupling is weak compared with each neuron's own dynamics. Typical postsynaptic potentials are under 1 mV, against about 20 mV needed to reach threshold ([wcnn.htm](https://www.izhikevich.org/publications/wcnn.htm); [cusp.pdf](https://www.izhikevich.org/publications/cusp.pdf)).
- **Canonical models.** If a continuous change of variables, not necessarily invertible, maps every model in a family onto one simple system, then results proved for that system hold for the whole family ([arbib.pdf](https://www.izhikevich.org/publications/arbib.pdf)).

The type of bifurcation each neuron sits near determines which canonical model applies:

- multiple cusp points give a Hopfield-like gradient system;
- Andronov–Hopf points give complex-valued oscillators;
- a saddle-node on a limit cycle gives the Ermentrout–Kopell theta neuron;
- limit-cycle oscillators give phase models via Malkin's theorem.

Two results carried into everything that followed. First, **oscillators interact only when their frequencies are roughly resonant**. Second, **an anatomical synapse does not guarantee functional coupling** ([bc1.pdf](https://www.izhikevich.org/publications/bc1.pdf)).

From 1998 to 2001 Hoppensteadt and Izhikevich developed these theorems in two directions. In biology, the 1998 "FM radio" hypothesis proposed that cortical columns talk through the thalamus on frequency-defined channels. In that picture, "the frequency of oscillation encodes the channel of communication, while the information is transmitted via phase modulations" ([fmradio.pdf](https://www.izhikevich.org/publications/fmradio.pdf)). In engineering, they proposed "oscillatory neurocomputers" in which memories are phase-locked patterns rather than equilibria. A shared medium driven by an external input imposes "dynamic connectivity", so the design needs no n² programmable connections ([Phys Rev Lett 1999](https://www.izhikevich.org/publications/oscomp.pdf)). They worked out versions built from phase-locked-loop circuits ([IEEE TNN 2000](https://www.izhikevich.org/publications/pllnn.pdf)), lasers ([Phys Rev E 2000](https://www.izhikevich.org/publications/lasers.pdf)) and MEMS resonators ([IEEE TCAS-I 2001](https://www.izhikevich.org/publications/mems.pdf)), and filed provisional patents. The PLL paper still has about 470 citations ([OpenAlex](https://api.openalex.org/works?filter=author.id:A5091804814)). I found no evidence that the authors ever built any of these machines. The work is a hardware-agnostic theorem looking for a substrate, and it anticipates today's interest in oscillator computing.

The central paper of the period is the 96-page, 126-figure tutorial **"Neural Excitability, Spiking and Bursting"** (*Int. J. Bifurcation & Chaos*, 2000). It remains his most-cited pre-2003 work, with about 2,190 OpenAlex citations. Its claim is that a neuron's computational properties follow from the bifurcation its rest state is near:

- **Near a saddle-node:** the cell "can fire all-or-none spikes with an arbitrary low frequency, it has a well-defined threshold manifold, and it acts as an integrator".
- **Near an Andronov–Hopf bifurcation:** the cell "fires in a certain frequency range", "can fire in response to an inhibitory pulse", and "acts as a resonator".

The paper also introduced the **rest-bifurcation/spiking-bifurcation naming scheme for bursters**. It pairs 12 bifurcations of rest with 10 bifurcations of spiking to get **120 codimension-1 burster types**, 24 of them planar. Before this, only six burster types had been identified ([nesb.pdf](https://www.izhikevich.org/publications/nesb.pdf)). Square-wave bursting became "fold/homoclinic", parabolic became "circle/circle", and elliptic became "subHopf/fold cycle". The method was deliberately top-down: list every pair mathematically, then invent a conductance model for each. Many of the resulting bursters were, in the paper's own words, "'theoretical' in the sense that they have yet to be seen in experiments" ([nesb.pdf](https://www.izhikevich.org/publications/nesb.pdf)).

The integrator/resonator split then produced three linked papers. In 1999 he proved that weakly connected networks of Class 1 neurons with conventional synapses reduce to a canonical pulse-coupled model. The paper concludes that the difference between such a model and a Hodgkin–Huxley network "is just a matter of a coordinate change" ([pulse.pdf](https://www.izhikevich.org/publications/pulse.pdf)). This gave integrate-and-fire-style networks a mathematical justification. In 2001 he built the resonator counterpart, the **resonate-and-fire neuron**, with a complex state variable ([resfire.pdf](https://www.izhikevich.org/publications/resfire.pdf); about 620 citations). And in 2002–03 he argued, in *BioSystems* and in a *Trends in Neurosciences* review with Desai, Walcott and Hoppensteadt, that **bursts act as a unit of information**. Changing the interspike frequency within a burst lets a cell "selectively affect some postsynaptic targets, but not others" ([tins.pdf](https://www.izhikevich.org/publications/tins.pdf); about 690 citations). Recognition from the applied mathematics community came early:

- a SIAM best student paper award for "Multiple Cusp Bifurcations" ([cusp.pdf](https://www.izhikevich.org/publications/cusp.pdf));
- selection of his elliptic-burster paper as a SIAM Review SIGEST featured article ([sirev.pdf](https://www.izhikevich.org/publications/sirev.pdf)).

## Two equations and four parameters became a field standard

The 2003 *IEEE Transactions on Neural Networks* letter is four pages long. The model is v′ = 0.04v² + 5v + 140 − u + I, u′ = a(bv − u), with the reset rule "if v ≥ 30 mV, then v ← c, u ← u + d" ([spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)). The quadratic term comes from fitting the spike-initiation dynamics of a cortical neuron so that the variables read in millivolts and milliseconds. The model had already appeared in trigonometric form in the 2000 review. By changing only a, b, c and d, the paper produces seven cortical and thalamic cell classes: regular spiking, intrinsically bursting, chattering, fast spiking, low-threshold spiking, thalamocortical and resonator.

The selling point was cost. A printed 1,000-neuron MATLAB program ran in real time, and a C++ version simulated "10 000 spiking cortical neurons with 1 000 000 synaptic connections in real time" on a 1 GHz PC. The paper declared that "there is no longer a contradiction between biological plausibility and computational efficiency" ([spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)). Izhikevich also made the summary figure free to reuse with credit and posted interactive code ([paper page](https://www.izhikevich.org/publications/spikes.htm)). That openness probably helped the model spread as much as the mathematics did.

The 2004 follow-up, **"Which Model to Use for Cortical Spiking Neurons?"**, made the case for the model through comparison. It lists 20 "neuro-computational features", labelled A–T, from tonic spiking to inhibition-induced bursting; that figure has since become iconic. It then scores 11 models on those features and on floating-point operations per simulated millisecond ([whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)):

| Model | FLOPS per 1 ms | Izhikevich's verdict |
|---|---|---|
| Leaky integrate-and-fire | 4 (+1 comparison) | "should be avoided by all means" unless proving theorems |
| Quadratic I&F | 7 | model of choice for large networks of integrators, but cannot burst or adapt |
| Izhikevich (2003) | 13 | "the simplest possible model that can exhibit all the firing patterns" |
| FitzHugh–Nagumo | 72 | cannot burst or be chaotic without noise |
| Hindmarsh–Rose | 120 | "optimistic assessment" |
| Morris–Lecar | 600 | needs an extra equation to burst |
| Hodgkin–Huxley | 1,200 | can do everything "if the parameters are tuned", but "extremely expensive" |

The paper is better read as advocacy than as a benchmark, and its own text concedes as much. Izhikevich tuned every model himself. An empty cell in the table means he "failed to find the parameters within a reasonable period of time". The cost figures depend on time steps he chose for each model: 1 ms for his own model, 0.1–0.25 ms for the conductance-based ones ([whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)). The paper still has about 3,020 citations ([OpenAlex](https://api.openalex.org/works/doi:10.1109/TNN.2004.832719)).

**_Dynamical Systems in Neuroscience: The Geometry of Excitability and Bursting_** (MIT Press, 2007; xvi+441 pp.) collected the whole program in one volume. Its thesis, set out in the preface, is that two neurons with similar ionic currents "may respond to the same synaptic input in very different manners because of each cell's bifurcation dynamics". Excitability class, thresholds, rebound spiking, bistability and integrator-versus-resonator behaviour all follow from the bifurcation the cell is near ([book PDF](https://www.izhikevich.org/publications/dsn.pdf)). Chapter 8 rewrites the simple model in dimensional form, C v′ = k(v − v_r)(v − v_t) − u + I, and fits it to recordings of cortical, thalamic, hippocampal and other cells. It also states plainly that the ten apparent parameters reduce to four independent ones. Here the model is described more modestly than in 2003: it is a "local canonical model" for spike initiation and upstroke, "not a global canonical model because it ignores the spike downstroke" ([book PDF](https://www.izhikevich.org/publications/dsn.pdf)). The book also attacks plain integrate-and-fire models, saying they are "not a spiking model" and that their spikes are drawn in by hand "to fool the reader".

Reviewers praised the book's clarity and limited scope. Jeff Moehlis in *SIAM Review* called it "a tour de force" with "over 400 figures, which are all of high quality". He also judged the "minimal models" approach "too cavalier to be ultimately satisfying" for serious modeling, and its single-neuron focus too narrow for a general course. The synchronization chapter was cut from print as "off-topic" and published online ([Moehlis review](https://sites.me.ucsb.edu/~moehlis/moehlis_papers/book_review.pdf)). Izhikevich hosts the full PDF, in-vitro recording data and an errata list running from 2006 to 2014 that credits readers from several universities. Both suggest heavy classroom use ([book page](https://www.izhikevich.org/publications/dsn/index.htm)).

The model's spread is easy to document. NEST has a native `izhikevich` model ([NEST docs](https://nest-simulator.readthedocs.io/en/stable/models/izhikevich.html)). Brian 2 ships "Izhikevich_2003" and "Izhikevich_2007" examples ([Brian 2](https://brian2.readthedocs.io/en/stable/examples/frompapers.Izhikevich_2007.html)). CARLsim describes itself as a GPU library for "networks of Izhikevich spiking neurons" ([CARLsim6](https://uci-carl.github.io/CARLsim6/)). SpiNNaker's PyNN interface lists "LIF and Izhikevich's dynamical systems model" as its standard neurons ([PMC6257411](https://pmc.ncbi.nlm.nih.gov/articles/PMC6257411)). Hardware groups have built it in asynchronous digital circuits ([Yale IJCNN 2013](https://csl.yale.edu/~rajit/ps/ijcnn2013.pdf)) and on FPGAs ([NeuroFlow](https://www.doc.ic.ac.uk/~wl/papers/16/fns16kc.pdf)). Citations keep growing more than twenty years on: 358 in 2021 and **504 in 2025** ([OpenAlex](https://api.openalex.org/works/doi:10.1109/TNN.2003.820440)). I could not confirm whether the mainstream digital neuromorphic chips, Intel's Loihi and IBM's TrueNorth, implement the model natively, so its hardware influence beyond SpiNNaker and FPGA work is not established here.

## Polychronization and dopamine-gated STDP made spike timing a theory of memory and reward

Edelman's Neurosciences Institute gave Izhikevich a theory to build on: the theory of neuronal group selection (TNGS, or "neural Darwinism"). Its key ideas are selection among groups of neurons, reentrant connectivity, degeneracy and value systems. Izhikevich's network papers from 2004 to 2010 are explicitly TNGS worked out at millisecond resolution ([reentry.pdf](https://www.izhikevich.org/publications/reentry.pdf); [PMC review of TNGS](https://pmc.ncbi.nlm.nih.gov/articles/PMC3111444)).

The first was a 2004 *Cerebral Cortex* paper with Joseph Gally and Edelman. It simulated **100,000 simple-model neurons and 8.5 million synapses on a sphere**, with distance-dependent axonal delays and spike-timing-dependent plasticity (STDP). STDP and delays together produced about 900 "neuronal groups" that fired in a time-locked but not synchronous way. Shuffling the weights cut the count to 80, and those survivors vanished within a minute. Patterned stimulation increased the number of groups originating at the stimulated site 60-fold ([reentry.pdf](https://www.izhikevich.org/publications/reentry.pdf)).

### Polychronous groups promised huge capacity that replication could not confirm

**"Polychronization: Computation with Spikes"** (*Neural Computation*, 2006) shrank the setup to 1,000 neurons with random axonal delays of 1–20 ms, STDP and a 1 ms time step. It named the phenomenon "reproducible time-locked but not synchronous firing patterns with millisecond precision". The motivation came from biology: cortical conduction delays range from 0.1 to 44 ms yet are reproducible to under a millisecond for a given pair of neurons. "Why would the brain maintain different delays with such precision if spike timing were not important?" ([spnet.pdf](https://www.izhikevich.org/publications/spnet.pdf)). The paper defined groups anatomically. A triplet of "anchor" neurons firing in a given pattern sets off a predictable cascade, and a group counts as active when at least half its excitatory members fire within ±1 ms of their predicted times.

The headline result was **over 5,000 groups in a 1,000-neuron network**, a number fluctuating between 5,000 and 6,000 as STDP created and destroyed them. The paper presented this as "an unprecedented memory capacity" ([spnet.htm](https://www.izhikevich.org/publications/spnet.htm)). It then extrapolated that a brain of 10^11 neurons might hold "more groups than the number of particles in the universe". It also linked groups to binding, gamma rhythms, attention and "consciousness as 'attention to memories'" ([spnet.pdf](https://www.izhikevich.org/publications/spnet.pdf)). Conceptually, polychrony generalizes Abeles's synfire chains, which assume synchronous pools and equal delays, to heterogeneous delays. Bienenstock had earlier called this kind of activity "synfire braids".

The paper's own numbers support a more modest reading:

- **Few groups persisted.** Only 471 groups survived the full 24-hour simulation.
- **Most spikes were noise.** Under 4% of spikes belonged to group activations.
- **Activation was partial.** Precision decayed along the length of each group.
- **The search was incomplete.** Izhikevich called his group-finding algorithm "extremely inefficient" and said it probably missed many groups ([spnet.pdf](https://www.izhikevich.org/publications/spnet.pdf)).
- **The released code disagreed with the paper.** His website reports 1,973 groups for the MATLAB run, or 6,071 with a looser setting, and notes that the MATLAB and C++ programs "are similar but not equivalent" ([spnet.htm](https://www.izhikevich.org/publications/spnet.htm)).

What the count measures is subgraphs that could support a cascade, not memories that can be stored and recalled.

The decisive test came in **Pauli, Weidel, Kunkel and Morrison (2018)**. They re-implemented the network in NEST and reproduced it exactly. Their first faithful-looking attempt found only 5 groups across 10 random seeds. Matching the original required nearest-neighbour STDP pairing, a 1 ms shift in spike processing, a particular order of potentiation and depression updates, and other undocumented details. They then mapped how fragile the result was:

- **Time step.** The original 1 ms Euler integration was unstable, with membrane potentials reaching about 1,000 mV. A 0.1 ms step cut the group count from about 4,300 to **151**.
- **STDP pairing.** All-to-all pairing yielded at most 11 groups.
- **Input.** Poisson input cut groups by about 90%.
- **Detection settings.** The minimum chain length swung the count between 608 and 27,116.
- **Bugs.** Three bugs in the original group finder, once fixed, roughly doubled the groups found.

They concluded that the original "significantly overstates the number of groups to be found in such networks", mainly because the coarse time step created artificial synchrony ([Pauli et al. 2018](https://www.frontiersin.org/articles/10.3389/fninf.2018.00046/full)). The concept itself survived and was extended:

- distinctions between groups that are structurally possible and groups that actually fire ([Martinez & Paugam-Moisy 2009](https://hal-univ-tlse3.archives-ouvertes.fr/INRIA/inria-00425514));
- metaplasticity, which enlarged groups by about 16% ([Guise, Knott & Benuskova 2015](https://www.frontiersin.org/articles/10.3389/fncom.2015.00009/full));
- hierarchical visual models in which polychronization emerges ([Eguchi et al. 2018](https://www.psy.ox.ac.uk/publications/857618));
- Izhikevich's own spike-timing theory of working memory with Botond Szatmáry, in which short-term plasticity lets a cued group reactivate for tens of seconds without persistent-activity attractors ([PLoS CB 2010](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000879)).

Guise and colleagues also noted that polychronization is easy to detect in simulation but hard to confirm in biological data ([Frontiers 2015](https://www.frontiersin.org/articles/10.3389/fncom.2015.00009/full)). I found no direct in vivo confirmation of delay-based polychronous groups. The 2006 paper itself has about 1,175 Semantic Scholar citations ([Semantic Scholar](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1162/089976606775093882?fields=title,year,citationCount,influentialCitationCount)).

### The distal-reward paper aged better than its author's other big theory

**"Solving the Distal Reward Problem through Linkage of STDP and Dopamine Signaling"** (*Cerebral Cortex*, 2007) addressed a credit-assignment puzzle. How does the brain know which firing pattern earned a reward that arrives seconds later, when "most neurons and synapses are active during the waiting period"? ([dastdp.htm](https://www.izhikevich.org/publications/dastdp.htm)). His answer has two parts:

- each synapse keeps an eligibility trace c, set by STDP, that decays with a time constant of **τ_c = 1 s**;
- the weight changes only as ṡ = c·d, where d is extracellular dopamine.

Random spikes during the wait leave no lasting trace, so the network need not fall silent between action and reward. That was the feature he said set his model apart from earlier eligibility-trace models by Houk, Seung and Hasselmo ([dastdp.pdf](https://www.izhikevich.org/publications/dastdp.pdf)).

The results were striking. In a network of 1,000 neurons with about 100,000 synapses, rewards delivered 1–3 s late singled out one chosen synapse among 80,000 and potentiated it to maximum after **only 40 ± 8 rewards**. The network also learned instrumental stimulus-response tasks and reversed them in under 50 trials. It reproduced the shift of the dopamine response from an unconditioned to a conditioned stimulus. The paper stated its limits openly. The model's dopamine signal "is not a true error prediction signal": there is no dip when an expected reward is omitted, because the model has no internal clock ([dastdp.pdf](https://www.izhikevich.org/publications/dastdp.pdf)).

The paper's place in the literature is now clear. Frémaux and Gerstner list it alongside Farries & Fairhall (2007) and Florian (2007) among the founding reward-modulated STDP (R-STDP) models. They classify it as "gated-Hebbian" learning, whose LTD-dominated STDP window creates "a downward drift of all synaptic weights" except the rewarded one ([Frémaux & Gerstner 2016](https://www.frontiersin.org/articles/10.3389/fncir.2015.00085/full)). Later theory identified the weakness of gating plasticity with raw reward. Such rules carry an unsupervised bias that can be removed only if the third factor signals reward minus expected reward, which requires a critic ([Frémaux, Sprekeler & Gerstner 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC6634722); [Legenstein, Pecevski & Maass 2008](https://igi-web.tugraz.at/people/Abstracts/LegensteinETAL:08a)).

Experiments later supported the timescale he had assumed. Yagishita et al. (2014) found that dopamine enlarged striatal spines only when it arrived within about 0.3–2 s of an STDP protocol ([Science, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4225776)). Gerstner and colleagues' 2018 review cites Izhikevich's "τ_c = 1s" as an example of a theoretical prediction later borne out ("Assumptions are predictions") ([Gerstner et al. 2018](https://arxiv.org/abs/1801.05219)). He also patented the idea at Brain Corp, as US 8,849,735 ([uspto.report](https://uspto.report/company/Izhikevich-Eugene-M)). An earlier analytical result with Niraj Desai (2003) belongs here too. Under Poisson firing, nearest-neighbour STDP reduces to the BCM rule, with a sliding threshold near 12 Hz. That result is now a standard link in plasticity theory ([bcm.pdf](https://www.izhikevich.org/publications/bcm.pdf); [Gerstner et al. 2018](https://arxiv.org/abs/1801.05219)).

## Scale before detail: the 100-billion-neuron run and the 2008 thalamocortical model

On **27 October 2005** Izhikevich finished a one-second simulation of a thalamocortical model the size of the human brain: **10^11 neurons and almost 10^15 synapses**. It took **50 days on 27 processors** ([izhikevich.org](https://www.izhikevich.org/human_brain_simulation/Blue_Brain.htm)). Storing the synapses would have needed about 10,000 terabytes, so he regenerated the anatomy at every 1 ms step instead. His own verdict is candid: "no significant contribution to neuroscience could be made by simulating one second of a model, even if it has the size of the human brain. However, I learned what it takes." His take-home message: "Size doesn't matter; it's what you put into your model and how you embed it into the environment" ([why.htm](https://www.izhikevich.org/human_brain_simulation/why.htm)). The run was never published in a peer-reviewed paper. Brain Corp's biography still calls it the world's largest such simulation ([Brain Corp](https://braincorp.com/team/dr-eugene-izhikevich)), which overstates what a one-second, non-learning demonstration showed.

The scientific version came with Edelman in *PNAS* (2008). It simulated **one million multicompartment neurons of 22 types and almost half a billion synapses**, with short-term plasticity and dopamine-modulated dendritic STDP. The data came from several species and scales:

- global white-matter anatomy from diffusion tensor imaging, partly of Izhikevich's own brain;
- laminar microcircuitry from cat visual cortex;
- neuron types calibrated to rat recordings.

It ran on 60 processors at about one minute of computing per second of model time ([PNAS PDF](https://www.izhikevich.org/publications/large-scale_model_of_human_brain.pdf)). Several properties emerged:

- **Self-sustained activity**, but only after STDP had tuned the network, and only above 10,000 neurons.
- **Region-specific rhythms** in the delta, alpha, beta and gamma bands, even though every region used identical microcircuitry.
- **Propagating waves.**
- **Anticorrelated fronto-parietal oscillations** in a simulated fMRI signal.
- **Extreme sensitivity to single spikes.** Adding or removing one spike of one neuron "completely changed the state of the entire cortex in <0.5 s" ([PNAS PDF](https://www.izhikevich.org/publications/large-scale_model_of_human_brain.pdf)).

The paper has about 1,100 citations ([Semantic Scholar](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1073/pnas.0712231105?fields=title,year,citationCount,influentialCitationCount)).

That single-spike chaos sits awkwardly with the precise-timing program of polychronization, and the authors left both readings open. On one, "only firing patterns in a statistical sense should be considered"; on the other, "every spike of every neuron counts". In vivo work in rat barrel cortex by London et al. (2010) found that one extra spike triggers about 28 extra spikes downstream. They took this as evidence that cortex works mainly with a rate code ([Nature](https://www.nature.com/articles/nature09086)). That is a substantive counter-reading of the same phenomenon.

Izhikevich framed his approach as the opposite of the Blue Brain Project. Blue Brain built a cortical column "to a much greater detail than the models I develop", whereas his goal was "a large-scale biologically accurate computer model of the whole human brain" ([izhikevich.org](https://www.izhikevich.org/human_brain_simulation/Blue_Brain.htm)). Blue Brain's 2015 reconstruction modelled about 31,000 neurons in detail ([PubMed](https://pubmed.ncbi.nlm.nih.gov/26451489/)). When IBM claimed a "cat-scale" simulation with simple neurons in 2009, Henry Markram called it "a mass deception" and objected to the "simplest possible equation you can imagine to simulate a neuron" ([IEEE Spectrum](https://spectrum.ieee.org/blue-brain-project-leader-angry-about-cat-brain)). I found no source in which Markram names Izhikevich. Still, that critique, scale without demonstrated function, applies equally to the 2005 run, and Izhikevich's own "size doesn't matter" largely concedes the point.

## Critiques cluster around numerics, overclaiming and parameter meaning

The technical critiques of the simple model come in four groups.

**Cutoff sensitivity.** Jonathan Touboul showed that in quadratic adaptive models both variables "blow up in finite time whatever the parameters". As a result, the 30 mV cutoff is "essential for the model to be well defined". Changing it "dramatically changes the spike patterns produced", and the time step must be tiny or adaptive to capture the recovery variable u correctly at reset ([Touboul 2008](https://arxiv.org/pdf/0812.1164)). This conflicts with the book's claim that reset timing error is "infinitesimal" ([book PDF](https://www.izhikevich.org/publications/dsn.pdf)). That claim may hold for v but not for u.

**The published integration scheme.** In the original code, v takes two 0.5 ms Euler steps while u takes one 1 ms step. Pauli et al. showed that this scheme is unstable and produces artificial synchrony ([Pauli et al. 2018](https://www.frontiersin.org/articles/10.3389/fninf.2018.00046/pdf)). NEST now defaults to "consistent" integration and keeps the published form only "for replicating published results" ([NEST docs](https://nest-simulator.readthedocs.io/en/stable/models/izhikevich.html)). A SpiNNaker visual-thalamus model built from Izhikevich neurons likewise needed a step finer than 1 ms and so ran slower than real time ([PMC5552764](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5552764/)). The headline "real time on a desktop PC" claim depended partly on a step too coarse to be trusted.

**Phenomenological parameters and spike shape.** Izhikevich himself called a, b, c and d "dimensionless" ([spikes.pdf](https://www.izhikevich.org/publications/spikes.pdf)) and conceded a too-slow upstroke and an instantaneous downstroke ([book PDF](https://www.izhikevich.org/publications/dsn.pdf)). The Brette–Gerstner adaptive exponential model (AdEx, 2005) answered this directly. It "differs from the model of Izhikevich only by the spike mechanism", which is exponential rather than quadratic. Its parameters are closer to measurable quantities, the cutoff matters little, and it predicted **96% of spikes within ±2 ms** of a conductance-based reference neuron ([Brette & Gerstner 2005](https://cenl.ucsd.edu/CompNeuro/Readings/week13/Brette-Gerstner+Adaptive-exponential-integrate-fire-effective+JNP+2005.pdf)). AdEx is the better-behaved version of the same idea. That the Izhikevich model still dominates in GPU and hardware settings reflects cost, simplicity and an early start more than accuracy.

**Overclaiming at network scale.** Polychronization's capacity claim did not survive careful replication ([Pauli et al. 2018](https://www.frontiersin.org/articles/10.3389/fninf.2018.00046/full)). DA-STDP needs a reward-prediction critic to generalize ([Frémaux et al. 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC6634722)). The human-scale run was a feasibility stunt by its author's own admission ([why.htm](https://www.izhikevich.org/human_brain_simulation/why.htm)). The 2004 model comparison was self-scored ([whichmod.pdf](https://www.izhikevich.org/publications/whichmod.pdf)), and the 2007 book was faulted for narrow scope ([Moehlis](https://sites.me.ucsb.edu/~moehlis/moehlis_papers/book_review.pdf)).

These critiques have something in common. None overturns the mathematics, and all of them hit where Izhikevich turned a mechanism into a sweeping functional claim. His habit of releasing code is what made that checking possible: Pauli's team could audit the polychronization network only because spnet.m and spnet.cpp were public.

## After 2009, the founder outworked the scientist until the 2025 manifesto

**Scholarpedia.** Izhikevich created Scholarpedia in February 2006 at the Neurosciences Institute. It is an expert-written, anonymously peer-reviewed wiki, pitched as a cross between Britannica and Wikipedia and seeded with computational neuroscience and dynamical systems ([Wikipedia](https://en.wikipedia.org/wiki/Scholarpedia); [Connectionists announcement](https://mailman.srv.cs.cmu.edu/pipermail/connectionists/2006-September/022566.html)). He recruited notable co-authors for his own entries, among them Richard FitzHugh on the FitzHugh–Nagumo model, Yoshiki Kuramoto on weakly coupled oscillators, Bard Ermentrout on phase models and John Conway on the Game of Life ([publications](https://www.izhikevich.org/publications/)). Brain Corp pays for its servers. The article count was essentially flat at **1,816 in December 2022 and 1,812 in August 2023** ([Wikipedia](https://en.wikipedia.org/wiki/Scholarpedia)), and the site returned HTTP 503 when checked on 24 November 2026; that was a single check and may have been a transient outage. He is still billed as its editor-in-chief in 2026 ([Redwood Center](https://redwood.berkeley.edu/seminars/eugene-izhikevich-feb-2026/)). Scholarpedia now works mostly as a static archive of authoritative reviews, and its survival depends on him and his company.

**Brain Corporation.** Brain Corp was co-founded in San Diego in 2009 and housed inside Qualcomm's research lab for several years ([TechCrunch 2017](https://techcrunch.com/2017/07/19/self-driving-robot-ai-company-brain-corp-raises-114m/)). In 2013 Qualcomm said it had been "computing like a neuron" through Brain Corp ([Xconomy 2013](https://legacy.xconomy.com/2013/04/03/qualcomm-started-its-brain-initiative-years-before-president-obama/2)), and it disclosed **Zeroth**, a spiking neural-processing project developed with Brain Corp ([Electronics360](https://electronics360.globalspec.com/article/3124/qualcomm-working-on-neural-processor-core)). No source I found confirms that Zeroth used the Izhikevich neuron specifically.

The company then pivoted. Its first product, in 2016, was autonomy software for commercial floor scrubbers. In 2017 it raised a $114M Series C led by the SoftBank Vision Fund ([Business Wire](https://businesswire.com/news/home/20170719005694/en/Brain-Corp-Announces-114-Million-Series-Funding)). Its robots went on to clean Walmart stores ([Fortune 2019](https://fortune.com/2019/07/23/robots-walmart-brain-corp/)). Izhikevich handed the CEO role to CFO David Pinn on **1 November 2022** and became executive chairman ([Brain Corp release](https://braincorp.com/resources/david-pinn-promoted-to-ceo-of-brain-corporation-eb694)). By August 2026 Brain Corp reported **more than 50,000 BrainOS robots worldwide** and deployments up 68% year on year. Pinn is the only person quoted in that announcement; Izhikevich is not mentioned ([Robotics & Automation News](https://roboticsandautomationnews.com/2026/08/07/brain-corp-reports-68-percent-growth-and-surpasses-50000-autonomous-robots-worldwide/104006/)).

The patent record preserves the spiking-network phase. A third-party tracker counts about **98 issued US patents with Izhikevich as inventor, about 78 assigned to Brain Corp**. They cover reward-modulated spiking plasticity, robot learning and adaptive control ([Patent Leaderboard](https://www.patentleaderboard.com/brain/eugene-izhikevich/444937?page=4); [uspto.report](https://uspto.report/company/Izhikevich-Eugene-M)). No source from 2016 to 2026 ties BrainOS to spiking computation. The company that grew out of his spiking-network research succeeded selling conventional robot navigation.

**SpikeCore and the Spiking Manifesto.** In December 2025 Izhikevich posted **"Spiking Manifesto"** (arXiv:2512.11843, sole author, revised 31 December 2025, code on GitHub) ([arXiv](https://arxiv.org/abs/2512.11843)). It argues three things:

- current AI is about **1000× less efficient than the brain** because it relies on large matrix multiplications on GPUs;
- small spiking networks have combinatorially large capacity through polychronous spike-timing patterns;
- spiking activity is "nature's way" of implementing lookup tables, so popular AI models can be recast as spiking networks for a potential thousandfold gain ([Redwood abstract](https://redwood.berkeley.edu/seminars/eugene-izhikevich-feb-2026/)).

He presented it on a 2026 seminar circuit: UCSD in January ([flier](https://inc.ucsd.edu/events/neuroscience-seminar/fliers/26-01-27%20Izhikevich.pdf)), Berkeley's Redwood Center and a Technion webinar in February ([Technion](https://acrc.net.technion.ac.il/2026/02/01/acrc-webinar-spiking-manifesto-a-new-way-to-build-and-train-artificial-neural-networks/)), and Stanford ([Stanford](https://neuroscience.stanford.edu/node/4942)). The speaker bios name him founder and CEO of **SpikeCore**, San Diego. I found nothing about SpikeCore's funding, staff or product beyond those bios. I also found no peer review, independent benchmark or published critique of the manifesto as of November 2026.

The manifesto rests on the polychronization capacity argument, the same claim Pauli et al. found fragile. Its central promise of efficiency at scale is therefore unproven on two counts.

## Legacy as of November 2026: a default neuron, a textbook and an open bet

The citation record shows where his influence lies. OpenAlex credits him with **27,169 citations across 97 works, h-index 39**. Other aggregators report 23,816 (SciSpace, h-index 51) and 32,264 (Research.com) ([OpenAlex](https://api.openalex.org/authors?search=Eugene%20Izhikevich); [SciSpace](https://typeset.io/authors/eugene-m-izhikevich-txyadlia2o); [Research.com](https://research.com/u/eugene-m-izhikevich)). I could not reach Google Scholar, which usually reports higher counts.

| Work | Year | OpenAlex citations |
|---|---|---|
| Simple Model of Spiking Neurons | 2003 | 5,656 |
| *Dynamical Systems in Neuroscience* | 2007 | 5,087 |
| Which Model to Use for Cortical Spiking Neurons? | 2004 | 3,021 |
| Neural Excitability, Spiking and Bursting | 2000 | 2,189 |
| *Weakly Connected Neural Networks* | 1997 | 1,388 |
| Polychronization | 2006 | 1,247 |
| Large-Scale Model of Mammalian Thalamocortical Systems | 2008 | 1,163 |
| Distal reward / DA-STDP | 2007 | 831 |

Source: [OpenAlex works list](https://api.openalex.org/works?filter=author.id:A5091804814).

The top five entries all belong to the dynamical-systems program: the model, its justification, its textbook and its mathematical ancestors. The network theories rank below them, even though they made larger claims. Yearly citations to the 2003 paper still rise, while the book holds steady at about 300 a year ([OpenAlex](https://api.openalex.org/works/doi:10.7551/mitpress/2526.001.0001)). The model has become infrastructure, the default "cheap but rich" neuron that neuromorphic, FPGA and spiking-machine-learning engineers reach for. Even Touboul's critique opens by calling it "very interesting for its computational efficiency" and "widely used, in particular for large scale simulations" ([Touboul 2008](https://arxiv.org/pdf/0812.1164)). His influence on the theory of neuronal excitability is just as deep, if less visible. The integrator/resonator distinction and the rest/spike burster names are now standard vocabulary in the field.

## Conclusion

Izhikevich's career shows a split between rigor and reach. His proofs, about canonical models, excitability classes, burster taxonomy and STDP-to-BCM, have held up almost entirely. His speculative syntheses, about memory capacity, consciousness and whole-brain scale, have held up least. The one exception is instructive. The DA-STDP paper made a specific, falsifiable mechanistic bet, a one-second eligibility trace gated by dopamine, and experiments a decade later broadly confirmed it. His best work combines a minimal mechanism with a stated assumption, and his weakest combines a large number with an open-ended interpretation. Open code connects the two: the reproducibility culture he helped start, by releasing MATLAB and C++ code for nearly everything, is what allowed his overclaims to be found and corrected.

The 2025 manifesto restages the decisive open question. Brain Corp became a commercial success by not depending on spiking computation. SpikeCore now bets that polychronous spiking can beat matrix multiplication on efficiency. Benchmarks, not citations, will decide that bet. The capacity argument it inherits needs to survive the time-step and detection-threshold checks that undid the 2006 numbers, and the claimed thousandfold gain needs a head-to-head comparison on real tasks. Until those exist, the safest reading of Izhikevich's legacy as of November 2026 is the one the citation curves already give. He gave computational neuroscience its standard cheap neuron and its standard geometric vocabulary for excitability. Whether he also gave AI a new computing paradigm is still an open, unverified claim.
