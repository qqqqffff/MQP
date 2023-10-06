#! /bin/bash
# #SBATCH -n 1
# #SBATCH --gres=gpu:0
# #SBATCH --mem 1G

# module load python/3.9.12/
# module load cuda12.1/blas/
# module load cuda12.1/fft/
# module load cuda12.1/toolkit/

python run.py 100000
#!/usr/bin/env bash

python run.py 100000