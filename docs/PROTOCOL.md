# Project 15 Protocol

## Estimand

The primary cohort is ProteinGym v1.3 single amino-acid substitutions. Other mutation classes are excluded or separately labeled. This repository's public fixtures are independently synthetic and are not benchmark evidence.

## Grouped evaluation

Partition assignments keep all observations for a UniProt ID and its deterministic sequence-similarity cluster together. The declared settings are `min_seq_id=0.90`, coverage `0.80`, and a recorded seed. The split manifest hash belongs in every evaluation provenance record.

## Representations and comparisons

The registered comparisons are median, mutation-plus-position Ridge, physicochemical Ridge, frozen ESM2 Ridge, official five-checkpoint ESM1v masked-marginal scoring, and optional T4-gated LoRA. ESM2 WT and mutant sequences are encoded independently and represented as pooled mutant-minus-WT features.

## Evaluation

Compute Spearman and supervised MSE per assay before macro summaries. Report counts, failures, runtime, and structured skips. Uncertainty must resample the declared protein/cluster or assay group rather than independent mutation rows. UMAP is exploratory only.

## Artifact boundary

Raw and derived rows, sequences, embeddings, checkpoints, hidden predictions, caches, fitted artifacts, and raw tracking payloads are restricted. Public output is limited to independent synthetic fixtures and sanitized aggregate summaries that pass the privacy checker.
