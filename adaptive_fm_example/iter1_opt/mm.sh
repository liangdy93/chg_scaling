#mkdir frc_mm
rm -f mm.out
rm -f peo_mm-forces-1_0.xyz
for j in 1 
do
   cp pdb/set${j}/solvion.psf ./temp.psf
   bash sed_chg.sh
   for i in $(seq 1 20)
   do
      cp pdb/set${j}/f${i}.pdb ./temp.pdb
      cp pdb/set${j}/var${i}.inc ./temp.inc
      cp2k.psmp -i mm.inp -o mm.out
      mv peo_mm-forces-1_0.xyz frc_mm/set${j}/frc${i}.xyz
      mv mm.out frc_mm/set${j}/mm${i}.out
   done
done
