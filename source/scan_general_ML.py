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
import vegas
import numpy as np
import tensorflow as tf
from tensorflow import keras
import sklearn
import time
############ colors ##############
def Red(prt): print("\033[91m {}\033[00m" .format(prt))
def Green(prt): print("\033[92m {}\033[00m" .format(prt))
def Yellow(prt): print("\033[93m {}\033[00m" .format(prt))
##############################################
################# VEGAS SAMPLING ##################
##############################################
def convert_to_unit_cube(x, limits):
    ndim = x.shape[1]
    new_x = np.empty(x.shape)

    for k in range(ndim):
        width = limits[k][1] - limits[k][0]
        new_x[:, k] = (x[:, k] - limits[k][0])/width

    return new_x


def convert_to_limits(x, limits):
    ndim = x.shape[1]
    new_x = np.empty(x.shape)

    for k in range(ndim):
        width = limits[k][1] - limits[k][0]
        # new_x[:, k] = (x[:, k] - limits[k][0])/width
        new_x[:, k] = x[:, k]*width + limits[k][0]

    return new_x



def vegas_map_samples(
        xtrain, ftrain, limits,
        ninc=200,
        nitn=15,
        alpha=1.0,
        nproc=1
):
    '''Train a mapping of the parameter space using vegas and a sample of points.
    Input Args:
        xtrain: array
            Coordinates of the sample. All the coordinates must be normalized to the [0, 1] range
        ftrain: array
            Result of evaluating a function on xtrain.
        ninc: int, optional
            number of increments used in the mapping (see vegas documentation for AdaptiveMap)
        nitn: int, optional
            number of iterations used to refine mapping (see vegas documentation for AdaptiveMap.adapt_to_samples())
        alpha: float, optional
            Damping parameter (see vegas documentation for AdaptiveMap.adapt_to_samples())
        nproc: int, optional
            Number of processes/processors to use (see vegas documentation for AdaptiveMap.adapt_to_samples())
    Returns:
        Callable function to create a random sample using the trained mapping
    '''
    ndim = xtrain.shape[1]
    _xtrain = convert_to_unit_cube(xtrain, limits)
    vg_AdMap = vegas.AdaptiveMap([[0, 1]]*ndim, ninc=ninc)
    vg_AdMap.adapt_to_samples(
        _xtrain, ftrain,
        nitn=nitn, alpha=alpha, nproc=nproc
    )

    def _vegas_sample(npts):
        '''Obtain an array of points from a trained vegas map.
        Input Args:
            npts: int
                Number of points
        Returns:
            sample: array
                Sample of points created according to mapping
            jacobian: array
                Jacobian corresponding to mapping of the points
        '''
        xrndu = np.random.uniform(0, 1, (int(_xtrain.shape[0]),int(_xtrain.shape[1])))
        xrndmap = np.empty(xrndu.shape, xrndu.dtype)
        jacmap = np.empty(xrndu.shape[0], xrndu.dtype)
        vg_AdMap.map(xrndu, xrndmap, jacmap)

        return convert_to_limits(xrndmap, limits), jacmap
        

    return _vegas_sample
###############################
####################MLP########
##############################
def MLP_Classifier(function_dim,num_FC_layers,neurons):
    ''' Function to create MLP classfier.
    Input args:
    function_dim: dimensions of the input
    num_FC_layers: Number of the fully connected layers
    neurons: number of neurons in each FC layer
    output args:
             MLP classifier network
    '''
    inp =keras.layers.Input((function_dim, ))
    x = keras.layers.Dense(neurons,activation=None)(inp)
    for _ in range(num_FC_layers):
      x = keras.layers.Dense(neurons,activation='relu')(x)
    output = keras.layers.Dense(1,activation="sigmoid")(x)
    model = keras.Model(inp,output)
    return model
######################################################
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
def generate_init_HEP(n,TotVarScanned,paths,Lesh,VarLabel,VarMin,VarMax):
    AI_2 = np.empty(shape=[0,TotVarScanned])
    for i in range(n):
        LHEfile = open(str(paths)+str(Lesh),'r+')
        AI_1 = []
        for line in LHEfile: 
            NewlineAdded = 0
            for yy in range(0,TotVarScanned):
                if str(VarLabel[yy]) in line:
                    value = VarMin[yy] + (VarMax[yy] - VarMin[yy])*random.random()
                    AI_1.append(value)
        AI_1= np.array(AI_1).reshape(1,TotVarScanned)   
        AI_2 = np.append(AI_2,AI_1,axis=0)    
    return AI_2       

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

##########################
##########################
##########################
def train_init(points):
    AI_X = np.empty(shape=[0,TotVarScanned])
    AI_Y = []
    xx = 0 
    while xx< points:
        print ("""-------------------------------------------
NUMBER OF COLLECTED POINTS %s  (Random scan) = \t %i  of  %i
-------------------------------------------"""%(str(pointN[-1]),(xx),points_init))
        newrunfile = open('newfile','w')
        oldrunfile = open(str(Lesh),'r+')
        AI_L = []
        for line in oldrunfile: 
            NewlineAdded = 0
            for yy in range(0,TotVarScanned):
                if str(VarLabel[yy]) in line:
                    value = VarMin[yy] + (VarMax[yy] - VarMin[yy])*random.random()
                    AI_L.append(value)
                    valuestr = str("%.4E" % value)
                    newrunfile.write(VarNum[yy]+'   '+valuestr +str('     ')+ VarLabel[yy]+'\n')
                    NewlineAdded = 1
            if NewlineAdded == 0:
                newrunfile.write(line)
        newrunfile.close()
        oldrunfile.close()
        os.remove(str(Lesh))
        AI_L= np.array(AI_L).reshape(1,TotVarScanned)
       ##################################
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
             ##################         
          
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
         ########################    
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
                       
                       if not os.path.exists(str(paths)+'spc.slha'):
                           AI_Y.append(0)
                       if  os.path.exists(str(paths)+'spc.slha'):
                           AI_Y.append(1)    
                           xx +=1    
                       AI_X = np.append(AI_X,AI_L,axis=0)      
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
                          st = time.time()
                          os.rename('spc.slha','SPheno.spc.%s_%i_%s'%(str(SPHENOMODEL),(xx+1),str(st)))
                          shutil.move('SPheno.spc.%s_%i_%s'%(str(SPHENOMODEL),(xx+1),str(st)),path+"/Spec_out_%s/"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh),str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(xx+1),str(st)))
                          shutil.copy(str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(xx+1),str(st)),path+"/Les_out_%s"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(xx+1),str(st)),str(Lesh))
                       
                       if os.path.exists(str(paths)+'spc.slha'): 
                           os.remove(str(paths)+'spc.slha')   
                      
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
                             
                       if not os.path.exists(str(paths)+'spc.slha'):
                           AI_Y.append(0)
                       if  os.path.exists(str(paths)+'spc.slha'):
                           AI_Y.append(1)    
                           xx +=1  
                       AI_X = np.append(AI_X,AI_L,axis=0)    
                       if (MadGraph != 0):
                          if os.path.exists(str(paths)+'spc.slha'):
                              for mm in range (1,MadGraph+1):
                                 os.system('cp -rf  %s/Out_Scan_%s/Cards/param_card_default.dat  %s/Out_Scan_%s/Cards/param_card.dat' %(str(paths),str(mm),str(paths),str(mm)) )
                                 replace(str(paths)+'spectrum2paramcard.py'," './Out_Scan_%s/Cards/param_card.dat' "%str(mm))   
                                 os.system('python %s/spectrum2paramcard.py >/dev/null'%str(paths))
                              print ('Running MadGraph_%s ...'%(str(pointNMG[-1])))
                              madevent_run(str(paths)+'spc.slha')
                       if os.path.exists(str(paths)+'spc.slha'):      
                          st = time.time()
                          os.rename('spc.slha','SPheno.spc.%s_%i_%s'%(str(SPHENOMODEL),(xx+1),str(st)))
                          shutil.move('SPheno.spc.%s_%i_%s'%(str(SPHENOMODEL),(xx+1),str(st)),path+"/Spec_out_%s/"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh),str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(xx+1),str(st)))
                          shutil.copy(str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(xx+1),str(st)),path+"/Les_out_%s"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(xx+1),str(st)),str(Lesh))                         
                       
                       if os.path.exists(str(paths)+'spc.slha'): 
                           os.remove(str(paths)+'spc.slha')
                            
        os.remove('out.txt')
    return np.array(AI_X),np.array(AI_Y)
    
##########################
##########################
##########################
def train_refine(points_r):
    AI_X = np.empty(shape=[0,TotVarScanned])
    AI_Y = []
    xx=0
    for xx in range(0,points_r.shape[0]):
        #    print ("""-------------------------------------------
#NUMBER OF COLLECTED POINTS %s = \t %i of  (%i)
#-------------------------------------------"""%(str(pointN[-1]),(xx+1),npoints))
            newrunfile = open('newfile','w')
            oldrunfile = open(str(Lesh),'r+')
            AI_L = []
            for line in oldrunfile: 
                NewlineAdded = 0
                for yy in range(0,TotVarScanned):
                    if str(VarLabel[yy]) in line:
                        value = points_r[xx,yy]
                        AI_L.append(value)
                        valuestr = str("%.4E" % value)
                        newrunfile.write(str(VarNum[yy])+'   '+valuestr +str('     ')+ VarLabel[yy]+'\n')
                        NewlineAdded = 1
                if NewlineAdded == 0:
                    newrunfile.write(line)
            newrunfile.close()
            oldrunfile.close()
            os.remove(str(Lesh))
            AI_L= np.array(AI_L).reshape(1,TotVarScanned)
           ##################################
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
                 ##################         
          
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
             ###              
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
                       
                       if not os.path.exists(str(paths)+'spc.slha'):
                           AI_Y = np.append(AI_Y,0)
                       if  os.path.exists(str(paths)+'spc.slha'):
                           AI_Y = np.append(AI_Y,1)    
 
                       AI_X = np.append(AI_X,AI_L,axis=0)      
                       
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
                          st =time.time()    
                          os.rename('spc.slha','SPheno.spc.%s_%i_%s'%(str(SPHENOMODEL),(AI_Y.sum()+1),str(st)))
                          shutil.move('SPheno.spc.%s_%i_%s'%(str(SPHENOMODEL),(AI_Y.sum()+1),str(st)),path+"/Spec_out_%s/"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh),str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(AI_Y.sum()+1),str(st)))
                          shutil.copy(str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(AI_Y.sum()+1),str(st)),path+"/Les_out_%s"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(AI_Y.sum()+1),str(st)),str(Lesh))
                       
                       if os.path.exists(str(paths)+'spc.slha'): 
                           os.remove(str(paths)+'spc.slha')   
                      
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
                             
                       if not os.path.exists(str(paths)+'spc.slha'):
                           AI_Y = np.append(AI_Y,0)
                       if  os.path.exists(str(paths)+'spc.slha'):
                           AI_Y = np.append(AI_Y,1)   

                       AI_X = np.append(AI_X,AI_L,axis=0)    
                       if (MadGraph != 0):
                          if os.path.exists(str(paths)+'spc.slha'):
                              for mm in range (1,MadGraph+1):
                                 os.system('cp -rf  %s/Out_Scan_%s/Cards/param_card_default.dat  %s/Out_Scan_%s/Cards/param_card.dat' %(str(paths),str(mm),str(paths),str(mm)) )
                                 replace(str(paths)+'spectrum2paramcard.py'," './Out_Scan_%s/Cards/param_card.dat' "%str(mm))   
                                 os.system('python %s/spectrum2paramcard.py >/dev/null'%str(paths))
                              print ('Running MadGraph_%s ...'%(str(pointNMG[-1])))
                              madevent_run(str(paths)+'spc.slha')
                       if os.path.exists(str(paths)+'spc.slha'):      
                          st = time.time()
                          os.rename('spc.slha','SPheno.spc.%s_%i_%s'%(str(SPHENOMODEL),(AI_Y.sum()+1),str(st)))
                          shutil.move('SPheno.spc.%s_%i_%s'%(str(SPHENOMODEL),(AI_Y.sum()+1),str(st)),path+"/Spec_out_%s/"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh),str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(AI_Y.sum()+1),str(st)))
                          shutil.copy(str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(AI_Y.sum()+1),str(st)),path+"/Les_out_%s"%(str(SPHENOMODEL)))
                          os.rename(str(Lesh)+'%s_%i_%s'%(str(SPHENOMODEL[-1]),(AI_Y.sum()+1),str(st)),str(Lesh))                         
                       
                       if os.path.exists(str(paths)+'spc.slha'): 
                           os.remove(str(paths)+'spc.slha')
                            
            os.remove('out.txt')
    return np.array(AI_X),np.array(AI_Y)
##########################################################
#############Loop Using ####################################
####################Machine Learning models   ####################
##########################################################
model = MLP_Classifier(TotVarScanned,Num_layers ,Num_neurons)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=lr), loss=keras.losses.BinaryCrossentropy())
Xf,ob1 = train_init(points_init)    
X_g = Xf[ob1==1]    # It is good to have some initial guide
obs1_g = ob1[ob1==1]
X_b =Xf[ob1==0][:len(obs1_g)]
obs1_b =ob1[ob1==0][:(len(obs1_g))]
print('\nNumber of initial points in the traget region:  ', len(obs1_g) )
x_t = np.concatenate((X_g,X_b))
y_t = np.concatenate((obs1_g,obs1_b))
model.fit(x_t,y_t,epochs=epoch, batch_size=ML_batch_size,verbose=ML_verbose)
q=0
while len(X_g) < npoints:
        q+=1
        x_test = generate_init_HEP(test_points,TotVarScanned,paths,Lesh,VarLabel,VarMin,VarMax)
        x_vegas  = np.concatenate((X_g,X_b))
        y_vegas  = np.concatenate((obs1_g,obs1_b))
        limits = np.column_stack((VarMin,VarMax))
        Veg_map = vegas_map_samples(x_vegas,y_vegas,limits)
        x,_ = Veg_map(x_test)
        pred = model.predict(x,verbose=ML_verbose).flatten()
        qs = np.argsort(pred)[::-1]
        if len(x[pred>0.9]) > round(batch_size*random_frac): # How to choose the good points
            xsel1 = x[pred>0.9][:round(batch_size*(1-random_frac))]
        else:
            xsel1 = x[qs][:round(batch_size*(1-random_frac))]
        xsel1 = np.append(xsel1,x[:round(batch_size*(random_frac))],axis=0)
        xsel2,ob =train_refine(xsel1)
        X_g = np.append(X_g,xsel2[ob==1],axis=0)
        obs1_g = np.append(obs1_g,ob[ob==1],axis=0)
        X_b = np.append(X_b,xsel2[ob==0],axis=0)
        obs1_b = np.append(obs1_b,ob[ob==0],axis=0)
        X = np.concatenate([X_g,X_b],axis=0)
        obs = np.concatenate([obs1_g,obs1_b],axis=0)
        X_shuffled, Y_shuffled = sklearn.utils.shuffle(X, obs)
        model.fit(X_shuffled, Y_shuffled,epochs=epoch, batch_size=ML_batch_size,verbose=ML_verbose)
        print('DNN_model- Run Number {} - Number of collected points= {} out of  {}'.format(q,len(X_g), npoints))
################################
########################

    
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

