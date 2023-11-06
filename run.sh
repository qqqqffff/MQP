#! /bin/bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  #SBATCH -n 1
  #SBATCH --gres=gpu:0
  #SBATCH --mem 1G

  # module load python/3.9.12/
  # module load cuda12.1/blas/
  # module load cuda12.1/fft/
  # module load cuda12.1/toolkit/

  python run.py eval 100000 /MQP-Wrist-Mouse-Apollo-Rowe-2023-10-05
elif [[ "$OSTYPE" == "cygwin"* ]]; then
  echo hi
fi