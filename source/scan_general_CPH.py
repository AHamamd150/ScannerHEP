#!/usr/bin/python
import fileinput
import os
import random
import re
import sys
import shutil
import cmath 
#import numpy as np
import array
import time
from scan_input import * 
from os import remove
from shutil import move
import tarfile
import glob
path = os.getcwd()
paths = str(pathS)+'/'
############ colors ##############
def Red(prt): print("\033[91m {}\033[00m" .format(prt))
def Green(prt): print("\033[92m {}\033[00m" .format(prt))
def Yellow(prt): print("\033[93m {}\033[00m" .format(prt))
##############################################
def const(i):
   for Xz in range(0,TotConstScanned):
      null = os.system("grep '%s' %s  >/dev/null"%(str(ConstLabel[Xz]),str(i))) 
      if (null == 256):
         Red(str(ConstLabel[Xz])+ ' not exist!! \t Point rejected ....')
         os.remove(str(i))
         return  
   f=open(str(i), 'r')
   for xxx in f: 
      for zz in range(0,TotConstScanned):
          if (str(ConstNum[zz])  and str(ConstLabel[zz])) in xxx:
            r = xxx.rsplit()
            Xmm = int(ConstResNum[zz])
            if (Xmm == 1) :
               l = int(float(r[Xmm]))
               if (l not in range(int(ConstMin[zz]),int(ConstMax[zz])) and str(r[0])!= 'DECAY'):
                  Red(str(ConstLabel[zz])+ ' =   ' + str(l) + '\t Point rejected ....')
                  os.remove(str(i))
                  return
            if (Xmm != 1) :
               l =  float(r[Xmm])
               mm = float(ConstMin[zz])
               nm = float(ConstMax[zz])
               if (l < mm):
                  Red(str(ConstLabel[zz])+ ' =   ' + str(l) + '  ' +str(ConstMin[zz])+'   '+ str(ConstMax[zz]) +'\t Point rejected ....')
                  os.remove(str(i))
                  return
               if (l > nm):
                  Red(str(ConstLabel[zz])+ ' =   ' + str(l) + '  ' +str(ConstMin[zz])+'   '+ str(ConstMax[zz]) +'\t Point rejected ....')
                  os.remove(str(i))
                  return   
                         
###############Run MadEvent#############################              
def madevent_run(nn):
    for xx in range (1,MadGraph+1):
       os.chdir(str(paths)+'/Out_Scan_%s/'%str(xx))
       root=open ('Cards/me5_configuration.txt')
       f = open ('fout','w+')  
       for y in root :
         if str ('# run_mode = ') in y:
            x = y.rsplit()
            y = y.replace(str("# run_mode = 2"), str("run_mode = 0")) 
         f.write(y)
       os.rename('fout','Cards/me5_configuration.txt')   
       f.close()    
       if os.path.exists(str(madgraph_path)+'/Out_Scan_%s/RunWeb'%str(xx)):
          os.remove(str(madgraph_path)+'/Out_Scan_%s/RunWeb'%str(xx))
       os.system("chmod -u+xrw MYfile.sh")   
       os.system("./bin/madevent MYfile.sh >/dev/null")
       os.system("cat %s cross_section.txt > a.txt"%str(nn))
       os.rename('a.txt',str(nn))
       shutil.rmtree('Events/run_01')
       os.chdir(str(paths))
########refill the parameter card from the spectrum#################
def replace(i,k):
   root=open (str(i))
   f = open ('fout','w+')   
   for y in root :
      if str ('path_spc =') in y:
         x = y.rsplit()
         y = y.replace(str(x[-1]), str(" './spc.slha' "))  
      if str ('path_param_card =') in y:
         x = y.rsplit()
         y = y.replace(str(x[-1]), str(k))
               
      f.write(y)
   os.rename('fout',str(i))   
   f.close()                 
##############Prepare HS#######################
def replace_HS(i):
   root=open (str(i))
   f = open ('fout','w+')   
   for y in root :
      if str ('Block HiggsCouplingsFermions, #') in y :
         x = y.rsplit()
         y = y.replace('Block HiggsCouplingsFermions, #', 'Block HiggsBoundsInputHiggsCouplingsFermions #')     
      if str ('Block HiggsCouplingsBosons #') in y:
         x = y.rsplit()
         y = y.replace('Block HiggsCouplingsBosons #','Block HiggsBoundsInputHiggsCouplingsBosons #' )    
                   
      f.write(y)
   os.rename('fout',str(i))   
   f.close()           
###########Constraint HB########################      
def const_HB(hb):
   if (HiggsBounds==1 and ExcludeHB ==1):
      f1 = open(str(hb))
      for line in f1:
         if str('  # HBresult') in line:
            ohb1= line.rsplit()
            if (float(ohb1[2])==0):
               Red('Excluded by HiggsBounds, spectrum removed...')
               os.remove(str(hb))
               return
   if (HiggsBounds==2 and ExcludeHB ==1):
      f2 = open(str(hb))
      nhb = f2.readlines()
      mhb = nhb[-1]       
      ohb2 = mhb.rsplit() 
      if (float(ohb2[-4])==0):
         Red('Excluded by HiggsBounds, spectrum removed...')
         os.remove(str(hb))
         return
#############Constrint HS########################      
def const_HS(hs):
   if (HiggsSignal==1 and ExcludeHS !=0):
      fs1 = open(str(hs))
      for line in fs1:
         if str('  # chi^2 (total)') in line:
            ohs1= line.rsplit()
            if (float(ohs1[1])>float(ExcludeHS)):
               hs1 = "%0.2E"%float(ohs1[1])
               Red('Excluded by HiggsSignals chi^2=%s , spectrum removed...'%str(hs1))
               os.remove(str(hs))
               return
   if (HiggsSignal==2 and ExcludeHS !=0):
      fs2 = open(str(hs))
      nhs = fs2.readlines()
      mhs = nhs[-1]       
      ohs2 = mhs.rsplit() 
      if (float(ohs2[-5])>float(ExcludeHS)):
         hs2 = "%0.2E"%float(ohs2[-5])
         Red('Excluded by HiggsSignals chi^2=%s, spectrum removed...'%str(hs2))
         os.remove(str(hs))
         return         
###############Start the scan for random points###################         
random.seed(1)
pointN = pathS.rsplit("/")
pointNMG = pathS.rsplit("_")
dirN = str(pointN[-1])

if os.path.exists(str(path)+'/Spec_out_CPsuperH%s'%(str(dirN))):
    shutil.rmtree(str(path)+'/Spec_out_CPsuperH%s'%(str(dirN)))
os.mkdir(str(path)+"/Spec_out_CPsuperH%s"%(str(dirN)))
if os.path.exists(str(path)+'/Les_out_CPsuperH%s'%(str(dirN))):
    shutil.rmtree(str(path)+'/Les_out_CPsuperH%s'%(str(dirN)))
os.mkdir(str(path)+"/Les_out_CPsuperH%s"%(str(dirN)))
os.chdir(paths)
oldrunfile = open('run','r')
oldrunfile.close()

for xx in range(0,npoints):
    print ("""-------------------------------------------
NUMBER OF SCANNED POINTS CPsuperH %s = \t %i
-------------------------------------------"""%(str(pointN[-1]),(xx+1)))
    newrunfile = open('newfile','w')
    oldrunfile = open('run','r')
    for line in oldrunfile: 
        NewlineAdded = 0
        for yy in range(0,TotVarScanned):
            if str(VarLabel[yy]) in line:
                value = VarMin[yy] + (VarMax[yy] - VarMin[yy])*random.random()
                valuestr = str("%.4E" % value)
                newrunfile.write(valuestr +str('     ')+ VarLabel[yy]+'\n')
                NewlineAdded = 1
        if NewlineAdded == 0:
            newrunfile.write(line)
    newrunfile.close()
    oldrunfile.close()
    os.remove('run')
    os.rename('newfile','run')
    os.system('chmod 777 run')
    os.system('./run >  out.txt')
    if os.path.exists(str(paths)+'cpsuperh2_slha.out'):
       os.rename(str(paths)+'cpsuperh2_slha.out',str(paths)+'spc.slha')
       if (TotConstScanned !=0):
          const(str(paths)+'spc.slha')     
                                      
          if (HiggsBounds != 0 ):
             if os.path.exists(str(paths)+'spc.slha'):
                replace_HS(str(paths)+'spc.slha')
                print('Runing HiggsBounds......')
                os.system('eval  %s/HiggsBounds LandH SLHA  %s %s %s/spc.slha >/dev/null'%(str(HBPath),str(NH),str(NCH),str(pathS))) 
                const_HB(str(paths)+'spc.slha')                                 
          if (HiggsSignal != 1 ):
             if os.path.exists(str(paths)+'spc.slha'):
                replace_HS(str(paths)+'spc.slha')
                print('Runing HiggsSignals......')
                os.system('eval  %s/HiggsSignals latestresults peak 2 SLHA  %s %s %s/spc.slha >/dev/null'%(str(HSPath),str(NH),str(NCH),str(pathS))) 
                const_HS(str(paths)+'spc.slha')                              
          if (MicoOmegas != 0 ):
             if os.path.exists(str(paths)+'spc.slha'):
                print('Runing MicroOmegas.....')
                os.system('eval  %s/main %s/spc.slha > omega.out " ./" '%(str(MicoOmegaspath),str(pathS))) 
                os.system('cat spc.slha omega.out > sps1.out')  
                os.rename('sps1.out','spc.slha')   
          if (MadGraph != 0):
             if os.path.exists(str(paths)+'spc.slha'):
                 for mm in range (1,MadGraph+1):
                    replace(str(paths)+'spectrum2paramcard.py'," './Out_Scan_%s/Cards/param_card.dat' "%(str(mm)))   
                    os.system('python %s/spectrum2paramcard.py >/dev/null'%(str(paths)))
                 print ('Running MadGraph_%s ...'%(str(pointNMG[-1])))
                 madevent_run(str(paths)+'spc.slha')                              
          if os.path.exists(str(paths)+'spc.slha'):      
             os.rename('spc.slha','CPsuperH.spc_%s_%i'%(str(dirN),(xx+1)))
             shutil.move('CPsuperH.spc_%s_%i'%(str(dirN),(xx+1)),path+"/Spec_out_CPsuperH%s"%(str(dirN)))
             os.rename('run','LesHouches_CPsuperH_%s_%i'%(str(dirN),(xx+1)))
             shutil.copy('LesHouches_CPsuperH_%s_%i'%(str(dirN),(xx+1)),path+"/Les_out_CPsuperH%s"%(str(dirN)))
             os.rename('LesHouches_CPsuperH_%s_%i'%(str(dirN),(xx+1)),'run')
                   
       if (TotConstScanned ==0):
                    
          if (HiggsBounds != 0 ):
             if os.path.exists(str(paths)+'spc.slha'):
                replace_HS(str(paths)+'spc.slha')
                print('Runing HiggsBounds......')
                os.system('eval  %s/HiggsBounds LandH SLHA  %s %s %s/spc.slha >/dev/null'%(str(HBPath),str(NH),str(NCH),str(pathS))) 
                const_HB(str(paths)+'spc.slha')                                 
          if (HiggsSignal != 0 ):
             if os.path.exists(str(paths)+'spc.slha'):
                replace_HS(str(paths)+'spc.slha')
                print('Runing HiggsSignals......')
                os.system('eval  %s/HiggsSignals latestresults peak 2 SLHA  %s %s %s/spc.slha >/dev/null'%(str(HSPath),str(NH),str(NCH),str(pathS))) 
                const_HS(str(paths)+'spc.slha')   
          if (MicoOmegas != 0 ):
             if os.path.exists(str(paths)+'spc.slha'):
                print('Runing MicroOmegas.....')
                os.system('eval  %s/main %s/spc.slha > omega.out " ./" '%(str(MicoOmegaspath),str(pathS))) 
                os.system('cat spc.slha omega.out > sps1.out')  
                os.rename('sps1.out','spc.slha')  
          if (MadGraph != 0):
             if os.path.exists(str(paths)+'spc.slha'):
                for mm in range (1,MadGraph+1):
                   replace(str(paths)+'spectrum2paramcard.py'," './Out_Scan_%s/Cards/param_card.dat' "%(str(mm)))   
                   os.system('python %s/spectrum2paramcard.py >/dev/null'%(str(paths)))
                print ('Running MadGraph_%s ...'%(str(pointNMG[-1])))
                madevent_run(str(paths)+'spc.slha')
          if os.path.exists(str(paths)+'spc.slha'):      
             os.rename('spc.slha','CPsuperH.spc_%s_%i'%(str(dirN),(xx+1)))
             shutil.move('CPsuperH.spc_%s_%i'%(str(dirN),(xx+1)),path+"/Spec_out_CPsuperH%s"%(str(dirN)))
             os.rename('run','LesHouches_CPsuperH_%s_%i'%(str(dirN),(xx+1)))
             shutil.copy('LesHouches_CPsuperH_%s_%i'%(str(dirN),(xx+1)),path+"/Les_out_CPsuperH%s"%(str(dirN)))
             os.rename('LesHouches_CPsuperH_%s_%i'%(str(dirN),(xx+1)),'run')                        
    os.remove('out.txt')

if not os.listdir(path+"/Spec_out_CPsuperH%s"%str(dirN)) == []:
    tar_spec = tarfile.open(path+"/Spectrum_%s.tar.gz"%(str(dirN)), "w:gz")
    tar_spec.add(path+"/Spec_out_CPsuperH%s/"%(str(dirN)), arcname="Spectrum_%s"%(str(dirN)))
    tar_spec.close()
    print ('******************************************')
    print ("Spectrum_%s.tar.gz , GENERATED."%(str(dirN)))
else:
    sys.exit(str(path)+"/Spec_out_CPsuperH%s/  EMPTY. NO SPECTRUM GENERATED."%(str(dirN)))
if not os.listdir(path+"/Les_out_CPsuperH%s/"%(str(dirN))) == []:
    tar_les = tarfile.open(path+"/Leshouches_CPsuperH%s.tar.gz"%(str(dirN)), "w:gz")
    tar_les.add(path+"/Les_out_CPsuperH%s/"%(str(dirN)), arcname="Leshouches_%s"%(str(dirN)))
    tar_les.close()
    print ("Leshouches_%s.tar.gz , GENERATED."%(str(dirN)))
    print ('******************************************')
else:
    sys.exit(str(path)+"/Les_out_CPsuperH%s/  EMPTY. NO SPECTRUM GENETRAED."%(str(dirN)))
os.chdir(path)


