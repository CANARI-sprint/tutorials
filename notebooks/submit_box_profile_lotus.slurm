#!/bin/bash 
#SBATCH --account=short4hr 
#SBATCH -p short-serial-4hr 
#SBATCH -o %J.out 
#SBATCH -e %J.err 
#SBATCH --time 1:30:00 
#SBATCH --mem=32000 
#SBATCH --array=0-18

VAR='votemper'
MASK='atlmsk'
BOX='amv'
OUT="/gws/nopw/j04/canari/users/jmecking001/profiles/${BOX}_${VAR}_"
imin='-75'
imax='-7.5'
jmin='0'
jmax='60'
ENS=("1" "10" "11" "12" "13" "18" "2" "20" "22" "24" "28" "3" "30" "31" "4" "5" "6" "7" "9") 
conda activate /gws/smf/j04/canari/conda-env
python box_profile.py ${ENS[$SLURM_ARRAY_TASK_ID]} $VAR $MASK $imin $imax $jmin $jmax ${OUT}${ENS[$SLURM_ARRAY_TASK_ID]}.nc