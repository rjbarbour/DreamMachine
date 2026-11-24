---
id: m-1
title: "M1 - Replicate Izhikevich spnet (correctness)"
---

## Description

Reproduce the network in Izhikevich (2006) Polychronization: Computation with Spikes (spnet): 800 RS + 200 FS neurons, 100 synapses each, 1-20 ms conduction delays, STDP applied through a slowly updated derivative. Correctness before speed. Exit: our kernel matches a line-by-line transcription of spnet.m spike for spike, and the long-run statistics match the paper.
