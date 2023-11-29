import sys
import time

start = time.time()
project = sys.argv[1]
print(f'Project: {project}')

sh_script = f'''
#! /bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --mem 1G

module load python/3.9.12/
module load cuda11.6/blas/
module load cuda11.6/fft/
module load cuda11.6/toolkit/

. ./tensorENV/bin/activate

#python run.py extract {project}
#python run.py eval {project}
#python run.py train {project} 50000
#python run.py analyze {project} *
'''

with open(f'run_{project}.sh', 'w') as rsh:
    rsh.write(sh_script)

print(f'Finished in {time.time() - start}ms')
