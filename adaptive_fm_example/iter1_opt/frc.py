import math
import numpy as np
import subprocess

def frc( fname1, fname2 ):
   
   # fname1 - input, fname2 - output

   fwrite = open(fname2,'w')

   for fn in fname1:
      #print(fn)
      fopen = open(fn,'r')
      flag = 0
      line = fopen.readline()
      tokens = line.split()
      while (flag == 0):
         line = fopen.readline()
         tokens = line.split()
         if len(tokens) > 0:
            if tokens[0] == "1":
               flag = 1 
      num = int(0)
      while (flag == 1):
         if len(tokens) > 0:
            if (tokens[2] == "Li"):
               fwrite.write("%s\n%s\n%s\n" %(tokens[3],tokens[4],tokens[5]))
         flag = 0
         num = int(tokens[0])
         line = fopen.readline()
         tokens = line.split()
         if len(tokens) > 0:
            if tokens[0] == str(num + 1):
               flag = 1
      fopen.close()
   fwrite.close()

   return
