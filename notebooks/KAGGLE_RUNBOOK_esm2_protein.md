# Kaggle Runbook - ESM2 Protein

## Purpose

Use this runbook only after explicit approval for platform-provided ProteinGym/model assets. The notebook keeps local defaults offline, preserves historical evidence, and stops before real data, checkpoint downloads, provider calls, GPU training, or heavy CPU work unless approval is recorded in the Kaggle session. Before that approval, do not download ProteinGym or model checkpoints.

## Cell-by-cell sequence

1. Read the purpose, safety rules, and expected outputs cell.
2. Run environment inspection to capture Python, platform, working directory, and GPU visibility.
3. Inspect available Kaggle input roots without assuming a dataset path.
4. Copy the source tree into `/kaggle/working/esm2-protein`.
5. Install dependencies only inside Kaggle if the environment needs them.
6. Restart the kernel after installation, then rerun cells 1 through 4.
7. Run provider-free synthetic validation.
8. Inspect and preserve existing evidence files without deleting historical records.
9. Stop at the approval gate unless real data/model/GPU/heavy CPU approval is explicitly present.
10. If approved, run each optional runtime command in its own isolated cell.
11. Write the final sanitized evidence summary, then stop.

## Required evidence

Record the source revision, notebook timestamp, Python version, device status, approved input paths, command, exit status, sanitized output path, structured skips or failures, and remaining blocker.

## Approval Gate

Do not cross the approval gate unless the user has explicitly approved real data access, checkpoint/model access, providers if any, GPU or heavy CPU work, and the exact output boundary for restricted artifacts.

## Stop conditions

Stop on missing approval, missing dataset/model path, checksum mismatch, dependency failure, failed synthetic validation, unavailable T4 for LoRA, privacy rejection, raw sequence exposure in a public artifact, or any unexpected generated restricted file.
