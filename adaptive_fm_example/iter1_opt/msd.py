import math
import numpy as np
import frc
import subprocess

def msd( para ):

   # write parameter(s) to file 

   # scaling factor for charges
   fopen = open("solvion.psf","r")
   fwrite1 = open("sed_chg.sh","w")
   fwrite2 = open("sed_nbf.sh","w")
   res = ["TFSI","LIT"]
   atm = []

   # now we assign this factor 

   fct = float(para[0])
   for line in fopen:
      tokens = line.split()
      if (len(tokens) > 4):
         if tokens[3] in res:
            temp = [tokens[3],tokens[4]]
            if temp not in atm:
               atm.append(temp)
               chg1 = float(tokens[6])
               chg2 = float(tokens[6]) * fct
               fwrite1.write("sed -i \"s/%-9s%-6s%11.6f/%-9s%-6s%11.6f/g\" temp.psf\n" %(tokens[4],tokens[5],chg1,tokens[4],tokens[5],chg2))
   fopen.close()
   fwrite1.close()

   # nbfix
   para = np.abs(para)
   if len(para) > 0:
      fwrite2.write("cp par_ref2.inc par_temp.inc\n")
      for i in range(1,len(para)): 
         sedstr = 'nbf' + str(i)
         fwrite2.write("sed -i \"s/%s/%f/g\" par_temp.inc\n" %(sedstr,para[i]))
   fwrite2.close()

   # run bash for nbfix
   subst = subprocess.Popen("bash sed_nbf.sh", shell=True)
   subst.communicate() # wait to finish

   # run cp2k (yes, another bash script)

   chm = subprocess.Popen("bash mm.sh", shell=True)
   chm.communicate() # wait to finish

   # rewrite forces to files

   frc_qm = []
   frc_mm = []
   iset = [1] # replica used for fitting

   for i in iset:
      for j in range(1,21):
         fn_temp1 = "frc_qm/set" + str(i) + "/frc" + str(j) + ".xyz"
         fn_temp2 = "frc_mm/set" + str(i) + "/frc" + str(j) + ".xyz"
         frc_qm.append(fn_temp1)
         frc_mm.append(fn_temp2)
   fftemp = open("frc_names.txt","w")
   for i in range(len(frc_qm)):
      fftemp.write("%s\t%s\n" %(frc_qm[i],frc_mm[i]))
   fftemp.close()
   frc.frc(frc_qm,"frc_qm.dat")
   frc.frc(frc_mm,"frc_mm.dat")

   # read forces

   fmm = open("frc_mm.dat","r")
   fref = open("frc_qm.dat","r")
   mm = []
   ref = []
   for line in fmm:
      tokens = line.split()
      mm.append(float(tokens[0]))
   for line in fref:
      tokens = line.split()
      ref.append(float(tokens[0]))

   # calculate msd

   fmsd = open("msd.dat","w")
   tot_msd = 0.0

   if (len(mm) == len(ref)):
      for i in range(len(ref)):
         diff = mm[i] - ref[i]
         msd = diff * diff
         fmsd.write("%f\n" %(msd))
         tot_msd = tot_msd + msd
      tot_msd = tot_msd * 3 / float(len(ref)) 
      
   fmsd.close()

   # return total msd
   print([para,tot_msd])
   return tot_msd

