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
          if str(ConstNum[zz])  == 'Decay':
            if (str(ConstLabel[zz])) in xxx:
              r = xxx.rsplit()
              if str(r[0])!= 'DECAY': continue
              l = float(r[2])
              if (l < (float(ConstMin[zz]))):
                 Red(str(ConstLabel[zz])+ '  decay width=   ' + str(l) + '\t Point rejected ....')
                 os.remove(str(i))
                 return
              if (l > (float(ConstMax[zz]))):
                 Red(str(ConstLabel[zz])+ '  decay width=   ' + str(l) + '\t Point rejected ....')
                 os.remove(str(i))
                 return   
      
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
                         
##################################################################              
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
       os.system("./bin/madevent MYfile.sh > a.txt ")
       l = open ('a.txt','r')
       for line in l:
           if 'Cross-section :' in line:
               o= line.rsplit()
               h2 = "%0.7E"%float(o[2])
               os.system("echo  Cross-sction:   %s  >> %s "%(str(h2),str(nn)))
       #os.system("cat cross_section.txt >> %s"%str(nn))
       #os.system("cat a.txt >> %s"%str(nn))
       os.system('rm  ./cross_section.txt')
       os.system('rm  ./a.txt')
       shutil.rmtree('Events/run_01')
       os.chdir(str(paths))
#############################################
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
###################################################
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
###############################################      
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
###############################################      
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
################################################         
if (npoints  != 0 ):
    if not os.path.exists(str(paths)+('bin/SPheno')):
        sys.exit ('"/bin/SPheno" NOT EXIST, PLEASE TYPE make.')
    if not  os.path.exists(str(paths)+str(Lesh)):
        sys.exit (str(paths)+str(Lesh)+' NOT EXIST.')
    if not  os.path.exists(str(paths)+'/bin/SPheno%s'%(str(SPHENOMODEL))):
        sys.exit (str(paths)+'/bin/SPheno%s'%(str(SPHENOMODEL))+' NOT EXIST.')
if os.path.exists(str(path)+'/Out_%s'%(str(SPHENOMODEL))):
    shutil.rmtree(str(path)+'/Out_%s'%(str(SPHENOMODEL)))
os.mkdir(str(path)+"/Out_%s"%(str(SPHENOMODEL)))
if os.path.exists(str(path)+'/Spec_out_%s'%(str(SPHENOMODEL))):
    shutil.rmtree(str(path)+'/Spec_out_%s'%(str(SPHENOMODEL)))
os.mkdir(str(path)+"/Spec_out_%s"%(str(SPHENOMODEL)))
if os.path.exists(str(path)+'/Les_out_%s'%(str(SPHENOMODEL))):
    shutil.rmtree(str(path)+'/Les_out_%s'%(str(SPHENOMODEL)))
os.mkdir(str(path)+"/Les_out_%s"%(str(SPHENOMODEL)))

os.chdir(paths)
oldrunfile = open(str(Lesh),'r+')
oldrunfile.close()
random.seed(1)
pointN = pathS.rsplit("/")
pointNMG = pathS.rsplit("_")
for xx in range(0,npoints):
    print ("""-------------------------------------------
NUMBER OF SCANNED POINTS %s = \t %i of  (%i)
-------------------------------------------"""%(str(pointN[-1]),(xx+1),npoints))
    newrunfile = open('newfile','w')
    oldrunfile = open(str(Lesh),'r+')
    for line in oldrunfile: 
        NewlineAdded = 0
        for yy in range(0,TotVarScanned):
            if str(VarLabel[yy]) in line:
                value = VarMin[yy] + (VarMax[yy] - VarMin[yy])*random.random()
                valuestr = str("%.4E" % value)
                newrunfile.write(VarNum[yy]+'   '+valuestr +str('     ')+ VarLabel[yy]+'\n')
                NewlineAdded = 1
        if NewlineAdded == 0:
            newrunfile.write(line)
    newrunfile.close()
    oldrunfile.close()
    os.remove(str(Lesh))
############### Start Grid (if required)############################    
#    if (GridVariables != 0 ) :
#       op = {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y, '/': lambda x, y: x / y}
#       for gg in range(0,GridVariables):   
#          x0value  = 0
#          x1value  = 0
#          varlabelsplit = str(GridVar[gg]).rsplit('==')
#          var1 =  varlabelsplit[1].strip()
#         var1int = int(var1.rsplit()[0])-1  
#          opt =  var1.rsplit()[1]
#         value =  var1.rsplit()[2]
#          leshfile = open('newfile','r')
#         for n in leshfile:
#             if (str(VarLabel[var1int]) in n):   
#                x1 = n.rsplit() 
#                x1value = "%0.4E"%float(op[str(opt)](float(x1[int(GridNum[gg])]),float(value))  )
#             if str(VarLabel[int(varlabelsplit[0])-1]) in n:
#                x0 = n.rsplit()
#                x0value =  x0[int(GridNum[gg])]           
#          if (x0value !=0  or x1value != 0 ):      
#             os.system("sed  -i-e  's/%s/%s/g'  newfile "%(str(x0value),str(x1value)))
#          leshfile.close()
          
          
          
############### Start Grid (if required)############################    
    if (GridVariables != 0 ) :
       op = {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y, '/': lambda x, y: x / y}
       for gg in range(0,GridVariables):   
          x0value  = 0
          x1value  = 0
          varlabelsplit = str(GridVar[gg]).rsplit('<')
          var1_l =  varlabelsplit[0].strip()
          var1int_l = int(var1_l.rsplit()[0])-1  
          opt_l =  var1_l.rsplit()[1]
          value_l =  var1_l.rsplit()[2]
          
          var1_up =  varlabelsplit[-1].strip()
          var1int_up = int(var1_up.rsplit()[0])-1  
          opt_up =  var1_up.rsplit()[1]
          value_up =  var1_up.rsplit()[2]
          
          
          leshfile = open('newfile','r')
          for n in leshfile:
             if (str(VarLabel[var1int_l]) in n):   
                x1_l = n.rsplit() 
                x1value_l = "%0.4E"%float(op[str(opt_l)](float(x1_l[int(GridNum[gg])]),float(value_l))  )
             if (str(VarLabel[var1int_up]) in n):   
                x1_up = n.rsplit() 
                x1value_up = "%0.4E"%float(op[str(opt_up)](float(x1_up[int(GridNum[gg])]),float(value_up))  )     
             if str(VarLabel[int(varlabelsplit[1])-1]) in n:
                x0 = n.rsplit()
                x0value =  x0[int(GridNum[gg])]           
          if (x0value !=0  or x1value_l != 0 or x1value_up != 0 ):
             x1value = float(x1value_l) + (float(x1value_up) - float(x1value_l))*random.random()
             os.system("sed  -i-e  's/%s/%s/g'  newfile "%(str(x0value),str(x1value)))
          leshfile.close()
###################################################################              
###################################################################    
    os.rename('newfile',str(Lesh))
    os.system('./bin/SPheno'+str(SPHENOMODEL)+' '+str(Lesh)+' spc.slha'+' >  out.txt')
    out = open(str(paths)+'out.txt','r+')
    for l in out:
        #print l
        if str('Finished!') in l:
                    if (TotConstScanned !=0):
                       const(str(paths)+'spc.slha')     
                                      
                       if (HiggsBounds == 1 ):
                          if os.path.exists(str(paths)+'spc.slha'):
                             replace_HS(str(paths)+'spc.slha')
                             Green('Runing HiggsBounds......')
                             os.system('eval  %s/HiggsBounds LandH SLHA  %s %s %s/spc.slha >/dev/null'%(str(HBPath),str(NH),str(NCH),str(pathS))) 
                             const_HB(str(paths)+'spc.slha')                                 
                       if (HiggsBounds == 2 ):
                          if os.path.exists(str(paths)+'spc.slha'):
                             replace_HS(str(paths)+'spc.slha')
                             Green('Runing HiggsBounds......')
                             os.system("eval  %s/HiggsBounds LandH effC  %s %s '%s' >/dev/null"%(str(HBPath),str(NH),str(NCH),str(paths))) 
                             os.system('cat %s/spc.slha %s/HiggsBounds_results.dat > %s/sps1.out'%(str(pathS),str(pathS),str(pathS)))  
                             os.rename(str(pathS)+'/sps1.out',str(pathS)+'/spc.slha') 
                             const_HB(str(paths)+'spc.slha')                                 
                       if (HiggsSignal == 1 ):
                          if os.path.exists(str(paths)+'spc.slha'):
                             replace_HS(str(paths)+'spc.slha')
                             print('Runing HiggsSignals......')
                             os.system('eval  %s/HiggsSignals latestresults peak 2 SLHA  %s %s %s/spc.slha >/dev/null'%(str(HSPath),str(NH),str(NCH),str(pathS))) 
                             const_HS(str(paths)+'spc.slha')    
                       if (HiggsSignal == 2 ):
                          if os.path.exists(str(paths)+'spc.slha'):
                             replace_HS(str(paths)+'spc.slha')
                             Green('Runing HiggsSignals......')
                             os.system('eval  %s/HiggsSignals latestresults peak 2 effC  %s %s %s >/dev/null'%(str(HSPath),str(NH),str(NCH),str(paths))) 
                             os.system('cat %s/spc.slha %s/HiggsSignals_results.dat > %s/sps2.out'%(str(pathS),str(pathS),str(pathS)))  
                             os.rename(str(pathS)+'/sps2.out',str(pathS)+'/spc.slha')    
                             const_HS(str(paths)+'spc.slha')      
                       if (MicoOmegas != 0 ):
                          if os.path.exists(str(paths)+'spc.slha'):
                             Yellow('Runing MicroOmegas.....')
                             os.system('eval  %s/main %s/spc.slha > omega.out " ./" '%(str(MicoOmegaspath),str(pathS))) 
                             os.system('echo  === ===================  >> spc.slha ')
                             os.system('echo  === Results Summary for micoMegas===  >> spc.slha ')
                             os.system('echo  === ===================  >> spc.slha ')
                             os.system('cat spc.slha omega.out > sps1.out')  
                             os.rename('sps1.out','spc.slha')   
                       if (MadGraph != 0):
                          if os.path.exists(str(paths)+'spc.slha'):
                              for mm in range (1,MadGraph+1):
                                 os.system('cp -rf  %s/Out_Scan_%s/Cards/param_card_default.dat  %s/Out_Scan_%s/Cards/param_card.dat' %(str(paths),str(mm),str(paths),str(mm)) )
                                 replace(str(paths)+'spectrum2paramcard.py'," './Out_Scan_%s/Cards/param_card.dat' "%str(mm))   
                                 os.system('python %s/spectrum2paramcard.py >/dev/null'%str(paths))
                              Yellow('Running MadGraph_%s ...'%(str(pointNMG[-1])))
                              os.system('echo  === ===================  >> spc.slha ')
                              os.system('echo  === Results Summary for MadGraph===  >> spc.slha ')
                              os.system('echo  === ===================  >> spc.slha ')
                              madevent_run(str(paths)+'spc.slha')                              
                       if os.path.exists(str(paths)+'spc.slha'):      
                          os.rename('spc.slha','SPheno.spc.%s_%i'%(str(SPHENOMODEL),(xx+1)))
                          shutil.move('SPheno.spc.%s_%i'%(str(SPHENOMODEL),(xx+1)),path+"/Spec_out_%s/"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh),str(Lesh)+'%s_%i'%(str(SPHENOMODEL[-1]),(xx+1)))
                          shutil.copy(str(Lesh)+'%s_%i'%(str(SPHENOMODEL[-1]),(xx+1)),path+"/Les_out_%s"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh)+'%s_%i'%(str(SPHENOMODEL[-1]),(xx+1)),str(Lesh))
                   
                    if (TotConstScanned ==0):
                    
                       if (HiggsBounds == 1 ):
                          if os.path.exists(str(paths)+'spc.slha'):
                             replace_HS(str(paths)+'spc.slha')
                             print('Runing HiggsBounds......')
                             os.system('eval  %s/HiggsBounds LandH SLHA  %s %s %s/spc.slha >/dev/null'%(str(HBPath),str(NH),str(NCH),str(pathS))) 
                             const_HB(str(paths)+'spc.slha')                                 
                       if (HiggsBounds == 2 ):
                          if os.path.exists(str(paths)+'spc.slha'):
                             replace_HS(str(paths)+'spc.slha')
                             print('Runing HiggsBounds......')
                             os.system("eval  %s/HiggsBounds LandH effC  %s %s '%s' >/dev/null"%(str(HBPath),str(NH),str(NCH),str(paths))) 
                             os.system('cat %s/spc.slha %s/HiggsBounds_results.dat > %s/sps1.out'%(str(pathS),str(pathS),str(pathS)))  
                             os.rename(str(pathS)+'/sps1.out',str(pathS)+'/spc.slha')                 
                             const_HB(str(paths)+'spc.slha')                                                   
                       if (HiggsSignal == 1 ):
                          if os.path.exists(str(paths)+'spc.slha'):
                             replace_HS(str(paths)+'spc.slha')
                             print('Runing HiggsSignals......')
                             os.system('eval  %s/HiggsSignals latestresults peak 2 SLHA  %s %s %s/spc.slha >/dev/null'%(str(HSPath),str(NH),str(NCH),str(pathS))) 
                             const_HS(str(paths)+'spc.slha')   
                       if (HiggsSignal == 2 ):
                          if os.path.exists(str(paths)+'spc.slha'):
                             replace_HS(str(paths)+'spc.slha')
                             print('Runing HiggsSignals......')
                             os.system('eval  %s/HiggsSignals latestresults peak 2 effC  %s %s %s >/dev/null'%(str(HSPath),str(NH),str(NCH),str(paths))) 
                             os.system('cat %s/spc.slha %s/HiggsSignals_results.dat > %s/sps2.out'%(str(pathS),str(pathS),str(pathS)))  
                             os.rename(str(pathS)+'/sps2.out',str(pathS)+'/spc.slha')    
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
                                 os.system('cp -rf  %s/Out_Scan_%s/Cards/param_card_default.dat  %s/Out_Scan_%s/Cards/param_card.dat' %(str(paths),str(mm),str(paths),str(mm)) )
                                 replace(str(paths)+'spectrum2paramcard.py'," './Out_Scan_%s/Cards/param_card.dat' "%str(mm))   
                                 os.system('python %s/spectrum2paramcard.py >/dev/null'%str(paths))
                              print ('Running MadGraph_%s ...'%(str(pointNMG[-1])))
                              madevent_run(str(paths)+'spc.slha')
                       if os.path.exists(str(paths)+'spc.slha'):      
                          os.rename('spc.slha','SPheno.spc.%s_%i'%(str(SPHENOMODEL),(xx+1)))
                          shutil.move('SPheno.spc.%s_%i'%(str(SPHENOMODEL),(xx+1)),path+"/Spec_out_%s/"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh),str(Lesh)+'%s_%i'%(str(SPHENOMODEL[-1]),(xx+1)))
                          shutil.copy(str(Lesh)+'%s_%i'%(str(SPHENOMODEL[-1]),(xx+1)),path+"/Les_out_%s"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh)+'%s_%i'%(str(SPHENOMODEL[-1]),(xx+1)),str(Lesh))                         
    os.remove('out.txt')
if not os.listdir(path+"/Spec_out_%s/"%(str(SPHENOMODEL))) == []:
    tar_spec = tarfile.open(path+"/Out_%s/Spectrum_%s.tar.gz"%(str(SPHENOMODEL),str(SPHENOMODEL)), "w:gz")
    tar_spec.add(path+"/Spec_out_%s/"%(str(SPHENOMODEL)), arcname="Spectrum_%s"%(str(SPHENOMODEL)))
    tar_spec.close()
    print ('******************************************')
    Green("Spectrum_%s.tar.gz , GENERATED."%(str(SPHENOMODEL)))
else:
    sys.exit(str(path)+"/Spec_out_%s/  EMPTY. NO SPECTRUM GENERATED."%(str(SPHENOMODEL)))
if not os.listdir(path+"/Les_out_%s/"%(str(SPHENOMODEL))) == []:
    tar_les = tarfile.open(path+"/Out_%s/Leshouches_%s.tar.gz"%(str(SPHENOMODEL),str(SPHENOMODEL)), "w:gz")
    tar_les.add(path+"/Les_out_%s/"%(str(SPHENOMODEL)), arcname="Leshouches_%s"%(str(SPHENOMODEL)))
    tar_les.close()
    Green ("Leshouches_%s.tar.gz , GENERATED."%(str(SPHENOMODEL)))
    print('******************************************')
else:
    sys.exit(str(path)+"/Les_out_%s/  EMPTY. NO SPECTRUM GENETRAED."%(str(SPHENOMODEL)))
os.chdir(path)


