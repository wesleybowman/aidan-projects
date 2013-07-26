#$ -S /bin/bash
#$ -cwd
#$ -N capeisle2D
#$ -R y
#$ -j y
#$ -l h_rt=47:59:00
#$ -pe ompi 128
gridname=capeisle
time mpirun ./fvcom2d_noturbine  --casename=$gridname>run_output
echo "Application ends at `date`"
