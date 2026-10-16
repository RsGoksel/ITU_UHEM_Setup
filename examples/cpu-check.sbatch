#!/bin/bash
# Submit with: sbatch --account=YOUR_PROJECT examples/cpu-check.sbatch
#SBATCH --job-name=uhem-cpu-check
#SBATCH --partition=cpu2dq
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH --time=00:02:00
#SBATCH --output=cpu-check-%j.log
set -euo pipefail
[[ -n ${SLURM_JOB_ID:-} ]] || { echo 'Run through Slurm, not on the login node.' >&2; exit 1; }
date -Is
hostname
printf 'job=%s account=%s allocated_cpus=%s\n' "$SLURM_JOB_ID" "$SLURM_JOB_ACCOUNT" "${SLURM_CPUS_ON_NODE:-unknown}"
python3 -c 'import platform; print(platform.python_version())'
