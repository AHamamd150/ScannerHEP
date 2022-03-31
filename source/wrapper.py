#!/usr/bin/python
import fileinput
import os
import random
import re
import sys
import shutil
import cmath 
import array
import time
from os import remove
from shutil import move
import tarfile
import glob
import multiprocessing
from multiprocessing import Pool
path = os.getcwd()
################################
############ colors ##############
def Red(prt): print("\033[91m {}\033[00m" .format(prt))
def Green(prt): print("\033[92m {}\033[00m" .format(prt))
def Yellow(prt): print("\033[93m {}\033[00m" .format(prt))
#############################################
argumentinput = str(sys.argv[-2]+'.'+sys.argv[-1])
args = str(sys.argv[-1])
argsinput = args.rsplit('.')
if (str(argsinput[-1]) != 'py'):
   sys.exit(Red('your input file %s has wrong exyension. please use .py'%str(argumentinput)))
#################################
from scan_input import *
paths = str(pathS)+'/'
#################################
def yes_no(question, default="yes"):
   valid = {"yes":True,   "y":True,  "ye":True}
   notvalid ={"no":False,     "n":False}
   if default == None:
      prompt = " [y/n] "
   elif default == "yes":
      prompt = " [Y/n] "
   elif default == "no":
      prompt = " [y/N] "
   else:
      raise ValueError("invalid answer: ")
   while True:
      sys.stdout.write(question + prompt)
      choice = raw_input().lower()
      if (MODE==1):
         if (choice in valid):
            shutil.rmtree(str(path)+'/Out_%s'%(str(SPHENOMODEL)))
            return valid[choice]    
         elif (choice in notvalid):
            if not os.path.exists(str(path)+'/Out_%s'%(str(SPHENOMODEL))+'_old'): 
               shutil.move(str(path)+'/Out_%s'%(str(SPHENOMODEL)),str(path)+'/Out_%s'%(str(SPHENOMODEL))+'_old')
               print 'Changing the old dir to %s'%(str(path)+'/Out_%s'%(str(SPHENOMODEL))+'_old')
               time.sleep(3)
            elif os.path.exists(str(path)+'/Out_%s'%(str(SPHENOMODEL))+'_old'):
               sys.exit(Red('%s exist please change it first,  Exit!!'%(str(path)+'/Out_%s'%(str(SPHENOMODEL))+'_old')) )   
            return notvalid[choice]
         else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                                           "(or 'y' or 'n').\n")
      if (MODE==2):   
         if (choice in valid):
            shutil.rmtree(str(path)+'/Out_CPsuperH')
            return valid[choice] 
         elif (choice in notvalid):           
            if os.path.exists(str(path)+'/Out_CPsuperH_old'):
               sys.exit(Red('%s exist please change it first,  Exit!!'%(str(path)+'/Out_CPsuperH_old')) )    
            if not os.path.exists(str(path)+'/Out_CPsuperH_old'): 
               shutil.move(str(path)+'/Out_CPsuperH',str(path)+'/Out_CPsuperH_old')
               print 'Changing the old dir to %s'%(str(path)+'/Out_CPsuperH_old')
               time.sleep(3)   
            return notvalid[choice]   
         else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                                           "(or 'y' or 'n').\n")                                           
#######################################################              
def logo(date):
   Yellow ('''
##########################################
#            Scanner code                #
# run as :                               #
#       1-  ./run.sh --help              #
#       2- ./run.sh input_file.py        #
#       3- ./run.sh --test               #
#             %s                   #
##########################################'''%(str(date)))
   time.sleep(3)
########################################################
logo('17/12/19')   
########################################################
##################checks #######################
print 'Checking your inputs in %s ..'%str(argumentinput)
time.sleep(3) 
if (HiggsBounds != 0 ):
   if  not os.path.exists(str(HBPath)+'/HiggsBounds'):
       sys.exit(Red('%s  not exist,  Exit!!'%(str(HBPath)+'/HiggsBounds ')) ) 
if (HiggsSignal != 0 ):       
   if  not os.path.exists(str(HSPath)+'/HiggsSignals'):
       sys.exit(Red('%s  not exist,  Exit!!'%(str(HSPath)+'/HiggsSignals ')) )  
if (MadGraph != 0):              
   if  not os.path.exists(madgraph_path):
       sys.exit(Red('%s  not exist,  Exit!!'%str(madgraph_path)) )      
   if  not os.path.exists(str(RunCard_path)+'/run_card.dat'):
       sys.exit(Red('%s  not exist,  Exit!!'%(str(RunCard_path)+'/run_card.dat')) )         
if (MicoOmegas != 0 ):       
   if  not os.path.exists(MicoOmegaspath):
       sys.exit(Red('%s  not exist,  Exit!!'%str(MicoOmegaspath)) ) 
if (MODE ==1) :
   if  not os.path.exists(pathS):
       sys.exit(Red('%s  not exist,  Exit!!'%str(pathS)) )
   if  not os.path.exists(str(path)+'/'+str(Lesh)):
       sys.exit(Red('%s  not exist,  Exit!!'%(str(path)+'/'+str(Lesh))) )    
   if  not os.path.exists(str(pathS)+'/bin/SPheno'+str(SPHENOMODEL)):
       sys.exit(Red('%s  not exist,  Exit!!'%(str(pathS)+'/bin/SPheno'+str(SPHENOMODEL))) )    
if (MODE ==2) :
   if  not os.path.exists(pathS):
       sys.exit(Red('%s  not exist,  Exit!!'%str(pathS)) )
   if  not os.path.exists(pathS+'/run'):
       sys.exit(Red('%s  not exist,  Exit!!'%str(pathS)+'/run') )    
   if  not os.path.exists(pathS+'/cpsuperh2.exe'):
       sys.exit(Red('%s  not exist,  Exit!!'%str(pathS)+'/cpsuperh2.exe') )
######################Check dir################################
if (MODE==1):
   if os.path.exists(str(path)+'/Out_%s'%(str(SPHENOMODEL))):
       if (str(sys.argv[1]) == '-f'):
          shutil.rmtree(str(path)+'/Out_%s'%(str(SPHENOMODEL)))
       else:   
          print ('The directory %s/Out_%s exists'%(str(path),str(SPHENOMODEL)))
          yes_no('Do you want to overwrite it?')
   os.mkdir(str(path)+"/Out_%s"%(str(SPHENOMODEL)))
if (MODE==2):
   if os.path.exists(str(path)+'/Out_CPsuperH'):
       if (str(sys.argv[1]) == '-f'):
          shutil.rmtree(str(path)+'/Out_CPsuperH')
       else:   
          print ('The directory %s/Out_CPsuperH exists'%(str(path)))
          yes_no('Do you want to overwrite it?')
   os.mkdir(str(path)+"/Out_CPsuperH")   
        
##############Prepare madgraph#########################
def replace_MG(i):
   root=open (str(i))
   f = open ('fout','w+')   
   for y in root :
      if (str ('000 #') in y and str('DECAY') not in y):
         x = y.rsplit()
         y = y.replace(str(x[1]), str(" 0.000e+00 #"))
      if str ('000 #') in y :
         x = y.rsplit()
         y = y.replace(str(x[2]), str(" 0.000e+00 #"))     
      if str (' 80.939007 #') in y:
         x = y.rsplit()
         y = y.replace(str(x[1]), str("8.093e+01 "))    
                   
      f.write(y)
   os.rename('fout',str(i))   
   f.close()     

###############Run madgraph and create the dir##################    
if (MadGraph !=0):
   for i in range (1,MadGraph+1):
      if os.path.exists(str(madgraph_path)+'/Out_Scan_%s/'%str(i)):   
         shutil.rmtree(str(madgraph_path)+'/Out_Scan_%s/'%str(i)) 
      if not os.path.exists(str(madgraph_path)+'/Out_Scan_%s/'%str(i)):
         os.chdir(str(madgraph_path))
         if os.path.exists(str(madgraph_path)+'/MYfile.sh'):
            os.remove(str(madgraph_path)+'/MYfile.sh')
         f = open('MYfile.sh','w+r+x')
         f.write("""
#! /bin/sh
%s 
output Out_Scan_%s
quit

"""%(str(proc[i-1]),str(i)))
         f.close()
         os.system("chmod -u+xrw MYfile.sh")
         os.system("chmod 777 %s/bin/mg5_aMC"%(str(madgraph_path)))
         os.system('eval  %s/bin/mg5_aMC MYfile.sh >/dev/null '%(str(madgraph_path)))
         if os.path.exists(str(madgraph_path)+'/MYfile.sh'):
            os.remove(str(madgraph_path)+'/MYfile.sh')
         shutil.copy(str(RunCard_path)+'/run_card.dat',str(madgraph_path)+'/Out_Scan_%s/Cards/'%str(i))
         replace_MG(str(madgraph_path)+'/Out_Scan_%s/Cards/param_card.dat'%str(i))
############Prepare the multirun directroies  for SPheno#################### 
def dir_prepare(i):

    if os.path.exists(str(path)+"/Out_%s/SPheno_%s"%(str(SPHENOMODEL),str(i))):
       shutil.rmtree(str(path)+"/Out_%s/SPheno_%s"%(str(SPHENOMODEL),str(i)))
    shutil.copytree(str(pathS)+"/bin/",str(path)+"/Out_%s/SPheno_%s/bin/"%(str(SPHENOMODEL),str(i)))
    shutil.copy(str(path)+'/'+str(argumentinput),str(path)+"/Out_%s/SPheno_%s"%(str(SPHENOMODEL),str(i)))
    shutil.copy(str(path)+'/source/scan_general.py',str(path)+"/Out_%s/SPheno_%s"%(str(SPHENOMODEL),str(i)))
    shutil.copy(str(path)+'/source/spectrum2paramcard.py',str(path)+"/Out_%s/SPheno_%s"%(str(SPHENOMODEL),str(i)))
    shutil.copy(str(path)+'/'+str(Lesh),str(path)+"/Out_%s/SPheno_%s"%(str(SPHENOMODEL),str(i)))
    if (HiggsSignal == 2 ):
       shutil.copy(str(PATHMHUNCERTINITY),str(path)+"/Out_%s/SPheno_%s"%(str(SPHENOMODEL),str(i)))
    if (MicoOmegas !=0 ):
       mm =  str(MicoOmegaspath)+'/'
       mmspl = mm.rsplit('/')
       shutil.copytree(str(MicoOmegaspath)+'/',str(path)+"/Out_%s/SPheno_%s/%s/"%(str(SPHENOMODEL),str(i),str(mmspl[-2])))
    if (MadGraph !=0):
       for xx in range (1,MadGraph+1):
          shutil.copytree(str(madgraph_path)+'/Out_Scan_%s/'%str(xx),str(path)+"/Out_%s/SPheno_%s/Out_Scan_%s/"%(str(SPHENOMODEL),str(i),str(xx)))
          ff = open(str(path)+"/Out_%s/SPheno_%s/Out_Scan_%s/MYfile.sh"%(str(SPHENOMODEL),str(i),str(xx)),'w+r+x')
          ff.write("""#! /bin/bash
set automatic_html_opening False
launch -f
print_results --path=./cross_section.txt
exit
""")
          ff.close()
    newrunfile = open(str(path)+"/Out_%s/SPheno_%s/newfile"%(str(SPHENOMODEL),str(i)),'w')
    oldrunfile = open(str(path)+"/Out_%s/SPheno_%s/%s"%(str(SPHENOMODEL),str(i),str(argumentinput)))
    for line in oldrunfile:
           
        if str('pathS') in line:
           m = line.split('=')
           line = line.replace(str(m[-1]) ,"'"+str(path)+"/Out_%s/SPheno_%s' \n"%(str(SPHENOMODEL),str(i)))               
        if str('SPHENOMODEL') in line:
           m = line.split('=')
           line = line.replace(str(m[-1]) ,"'"+str(SPHENOMODEL)+str(i)+"' \n") 
        if str('npoints') in line:
           m = line.split('=')
           line = line.replace(str(m[-1]) ,str(npoints/N_Cores)+" \n")        
        newrunfile.write(line)
           
    newrunfile.close()
    os.rename(str(path)+"/Out_%s/SPheno_%s/newfile"%(str(SPHENOMODEL),str(i)),str(path)+"/Out_%s/SPheno_%s/%s"%(str(SPHENOMODEL),str(i),str(argumentinput)))

    newrunfile1 = open(str(path)+"/Out_%s/SPheno_%s/newfile1"%(str(SPHENOMODEL),str(i)),'w')
    oldrunfile1 = open(str(path)+"/Out_%s/SPheno_%s/scan_general.py"%(str(SPHENOMODEL),str(i)))
    for line in oldrunfile1:
        if str("from scan_input import") in line:
           m = line.split()
           line = line.replace(str(m[1]) , str(sys.argv[-2]))

           
        if str('random.seed(1)') in line:
           m = line.split('.')
           line = line.replace(str(m[-1]) ,"seed(%s) \n"%str(i*npoints))
     
        newrunfile1.write(line)
           
    newrunfile1.close()
    os.rename(str(path)+"/Out_%s/SPheno_%s/newfile1"%(str(SPHENOMODEL),str(i)),str(path)+"/Out_%s/SPheno_%s/scan_general.py"%(str(SPHENOMODEL),str(i)))
    os.rename(str(path)+"/Out_%s/SPheno_%s/bin/SPheno%s"%(str(SPHENOMODEL),str(i),str(SPHENOMODEL)),str(path)+"/Out_%s/SPheno_%s/bin/SPheno%s"%(str(SPHENOMODEL),str(i),str(SPHENOMODEL)+str(i)))
############Prepare the multirun directroies  for CPsuperH#################### 
def dir_prepare_CP(i):
    if os.path.exists(str(path)+"/Out_CPsuperH/Run_%s"%(str(i))):
       shutil.rmtree(str(path)+"/Out_CPsuperH/Run_%s"%(str(i)))
    os.mkdir(str(path)+"/Out_CPsuperH/Run_%s"%(str(i)))    
    shutil.copy(str(paths)+"/cpsuperh2.exe",str(path)+"/Out_CPsuperH/Run_%s/"%(str(i)))
    shutil.copy(str(paths)+"/run",str(path)+"/Out_CPsuperH/Run_%s/"%(str(i)))
    shutil.copy(str(path)+'/'+str(argumentinput),str(path)+"/Out_CPsuperH/Run_%s"%(str(i)))
    shutil.copy(str(path)+'/source/scan_general_CPH.py',str(path)+"/Out_CPsuperH/Run_%s"%(str(i)))
    shutil.copy(str(path)+'/source/spectrum2paramcard.py',str(path)+"/Out_CPsuperH/Run_%s"%(str(i)))
   
    if (HiggsSignal == 2 ):
       shutil.copy(str(PATHMHUNCERTINITY),str(path)+"/Out_CPsuperH/Run_%s"%(str(i)))
   # if (MicoOmegas !=0 ):
   #    mm =  str(MicoOmegaspath)+'/'
    #   mmspl = mm.rsplit('/')
     #  shutil.copytree(str(MicoOmegaspath)+'/',str(path)+"/Out_%s/SPheno_%s/%s/"%(str(SPHENOMODEL),str(i),str(mmspl[-2])))
    if (MadGraph !=0):
       for xx in range (1,MadGraph+1):
          shutil.copytree(str(madgraph_path)+'/Out_Scan_%s/'%str(xx),str(path)+"/Out_CPsuperH/Run_%s/Out_Scan_%s/"%(str(i),str(xx)))

          ff = open(str(path)+"/Out_CPsuperH/Run_%s/Out_Scan_%s/MYfile.sh"%(str(i),str(xx)),'w+r+x')
          ff.write("""#! /bin/bash
set automatic_html_opening False
launch -f
print_results --path=./cross_section.txt
exit
""")
          ff.close()
    newrunfile = open(str(path)+"/Out_CPsuperH/Run_%s/newfile"%(str(i)),'w')
    oldrunfile = open(str(path)+"/Out_CPsuperH/Run_%s/%s"%(str(i),str(argumentinput)))
    for line in oldrunfile:
                        
        if str('pathS') in line:
           m = line.split('=')
           line = line.replace(str(m[-1]) ,"'"+str(path)+"/Out_CPsuperH/Run_%s' \n"%(str(i)))               
        if str('npoints') in line:
           m = line.split('=')
           line = line.replace(str(m[-1]) ,str(npoints/N_Cores)+" \n")        
        newrunfile.write(line)
           
    newrunfile.close()
    os.rename(str(path)+"/Out_CPsuperH/Run_%s/newfile"%(str(i)),str(path)+"/Out_CPsuperH/Run_%s/%s"%(str(i),str(argumentinput)))

    newrunfile1 = open(str(path)+"/Out_CPsuperH/Run_%s/newfile1"%(str(i)),'w')
    oldrunfile1 = open(str(path)+"/Out_CPsuperH/Run_%s/scan_general_CPH.py"%(str(i)))
    for line in oldrunfile1:
        if str("from scan_input import") in line:
           m = line.split()
           line = line.replace(str(m[1]) , str(sys.argv[-2]))

           
        if str('random.seed(1)') in line:
           m = line.split('.')
           line = line.replace(str(m[-1]) ,"seed(%s) \n"%str(i*npoints))
     
        newrunfile1.write(line)
           
    newrunfile1.close()
    os.rename(str(path)+"/Out_CPsuperH/Run_%s/newfile1"%(str(i)),str(path)+"/Out_CPsuperH/Run_%s/scan_general_CPH.py"%(str(i)))
##################Run the defined functions in ######################################
p=Pool(processes=N_Cores)
if MODE ==1:
   print 'Creating SPheno directory for multi-runs Using %s Cores, please be patient ...'%str(N_Cores)
   p.map(dir_prepare,range(1,N_Cores+1),chunksize=1)    
if MODE ==2:
   print 'Creating CPsuperH directory for multi-runs Using %s Cores, please be patient ...'%str(N_Cores)
   p.map(dir_prepare_CP,range(1,N_Cores+1),chunksize=1)   
time.sleep(5)        
#############################################################################
def  spheno_runs(i):
          os.chdir(str(path)+"/Out_%s/"%(str(SPHENOMODEL)))
          os.system('python '+str(path)+"/Out_%s/SPheno_%s/scan_general.py"%(str(SPHENOMODEL),str(i)))
def  CPH_runs(i):
          os.chdir(str(path)+"/Out_CPsuperH/")
          os.system('python '+str(path)+"/Out_CPsuperH/Run_%s/scan_general_CPH.py"%(str(i)))

      
p1=Pool(processes=N_Cores)
if (MODE==1):
   p1.map(spheno_runs,range(1,N_Cores+1),chunksize=1)    
if (MODE==2):
   p1.map(CPH_runs,range(1,N_Cores+1),chunksize=1)    
##########Clean up SPheno#########
if (MODE==1):
   for xx in range (1,N_Cores+1):
       m = glob.glob(str(path)+"/Out_%s/Out_%s/*"%(str(SPHENOMODEL),str(SPHENOMODEL)+str(xx)))
       for file in m:
           shutil.copy(file,str(path)+"/Out_%s/"%(str(SPHENOMODEL)))
       if os.path.exists(str(path)+"/Out_%s/SPheno_%s"%(str(SPHENOMODEL),str(xx))):
          shutil.rmtree(str(path)+"/Out_%s/SPheno_%s"%(str(SPHENOMODEL),str(xx)))
       if os.path.exists(str(path)+"/Out_%s/Out_%s"%(str(SPHENOMODEL),str(SPHENOMODEL)+str(xx))):
          shutil.rmtree(str(path)+"/Out_%s/Out_%s"%(str(SPHENOMODEL),str(SPHENOMODEL)+str(xx)))
       if os.path.exists(str(path)+"/Out_%s/Les_out_%s"%(str(SPHENOMODEL),str(SPHENOMODEL)+str(xx))):
          shutil.rmtree(str(path)+"/Out_%s/Les_out_%s"%(str(SPHENOMODEL),str(SPHENOMODEL)+str(xx))) 
       if os.path.exists(str(path)+"/Out_%s/Spec_out_%s"%(str(SPHENOMODEL),str(SPHENOMODEL)+str(xx))):
          shutil.rmtree(str(path)+"/Out_%s/Spec_out_%s"%(str(SPHENOMODEL),str(SPHENOMODEL)+str(xx)))
            
   if not os.listdir(path+"/Out_%s/"%(str(SPHENOMODEL))) == []:   
      Green('''
-------------------------------------------------- 
 ALL OUTPUT STORED IN %s/Out_%s
--------------------------------------------------'''% (str(path),str(SPHENOMODEL)))   
   else:
      Red('''
--------------------------------------------------
 NO SPECTRUM GENERATED !!
--------------------------------------------------''')
##########Clean up CPsuperH#########
if (MODE==2):
   for xx in range (1,N_Cores+1):
       
       if os.path.exists(str(path)+"/Out_CPsuperH/Run_%s"%(str(xx))):
          shutil.rmtree(str(path)+"/Out_CPsuperH/Run_%s"%(str(xx)))
       if os.path.exists(str(path)+"/Out_CPsuperH/Les_out_CPsuperHRun_%s"%(str(xx))):
          shutil.rmtree(str(path)+"/Out_CPsuperH/Les_out_CPsuperHRun_%s"%(str(xx))) 
       if os.path.exists(str(path)+"/Out_CPsuperH/Spec_out_CPsuperHRun_%s"%(str(xx))):
          shutil.rmtree(str(path)+"/Out_CPsuperH/Spec_out_CPsuperHRun_%s"%(str(xx)))
            
   if not os.listdir(path+"/Out_CPsuperH/") == []:   
      Green('''
-------------------------------------------------- 
 ALL OUTPUT STORED IN %s/Out_CPsuperH
--------------------------------------------------'''% (str(path)))   
   else:
      Red('''
--------------------------------------------------
 NO SPECTRUM GENERATED !!
--------------------------------------------------''')      
################Clean UP ###########
for i in range (1,MadGraph+1):       
   if os.path.exists(str(madgraph_path)+'/Out_Scan_%s/'%str(i)):   
      shutil.rmtree(str(madgraph_path)+'/Out_Scan_%s/'%str(i))
if os.path.exists(str(path)+'/'+str(argumentinput)+'c'):   
   os.remove(str(path)+'/'+str(argumentinput)+'c')
if os.path.exists(str(path)+'/wrapper.pyc/'):   
   os.remove(str(path)+'/wrapper.pyc/')
   

