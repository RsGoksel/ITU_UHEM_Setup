#!/bin/bash
# Submit with: sbatch --account=YOUR_PROJECT examples/gpu-check.sbatch
#SBATCH --job-name=uhem-gpu-check
#SBATCH --partition=a100q
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --gres=gpu:1
#SBATCH --time=00:02:00
#SBATCH --output=gpu-check-%j.log
set -euo pipefail
[[ -n ${SLURM_JOB_ID:-} ]] || { echo 'Run through Slurm, not on the login node.' >&2; exit 1; }
date -Is
hostname
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
# Optional full-path Python from an existing, separately verified environment:
if [[ -n ${UHEM_PYTHON:-} ]]; then
    [[ $UHEM_PYTHON = /* && -x $UHEM_PYTHON ]] || { echo 'UHEM_PYTHON must be an executable absolute path.' >&2; exit 1; }
    "$UHEM_PYTHON" -c 'import torch; assert torch.cuda.is_available(), "CUDA unavailable"; a=torch.ones((128,128),device="cuda"); b=a@a; torch.cuda.synchronize(); assert b[0,0].item()==128; print(torch.__version__,torch.version.cuda,torch.cuda.get_device_name(0))'
fi
