#!/bin/bash
##sbatch commands
#SBATCH --job-name=cp2k
#SBATCH --output=sbatch.out
#SBATCH --error=sbatch.err

ulimit -s unlimited

export mdfd="../iter1_md"
echo "${mdfd}"

cp ${mdfd}/solvion.psf .
mkdir frc_qm
rm -f qm.out
rm -f peo_qm-forces-1_0.xyz
for i in $(seq 1 20)
do
   cp ${mdfd}/pdb/f${i}.pdb ./temp.pdb
   cp ${mdfd}/pdb/var${i}.inc ./temp.inc
   mpirun -np 40 cp2k.psmp -i qm.inp -o qm.out
   mv peo_qm-forces-1_0.xyz frc_qm/frc${i}.xyz
   mv qm.out frc_qm/qm${i}.out
   mv peo_qm-ELECTRON_DENSITY-1_0.cube frc_qm/edens${i}.cube
done
