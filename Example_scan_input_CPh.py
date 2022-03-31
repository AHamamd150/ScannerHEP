VarMax =[] 
VarMin =[] 
VarLabel =[]
ConstMax =[]
ConstMin =[]
ConstLabel =[]
ConstNum =[]
ConstResNum =[]
ResLabel = []
ResNum = []
ResOpt = []
proc=[]
######################################
# Please do not change the above tags#
######################################
MODE = 2                   #1->spHeno , 2 cpsuperh,
npoints = 100            #Number of points you want to scan over
N_Cores = 6                   #Number of cores to be used 
############################################
pathS ='/Users/ahmed/work/CPsuperH2.3' #Path to SPheno directory betweenthe quotes
#################################
VarMin.append(2.000000E+00)     # define the minimum value of varible
VarMax.append(1.00000E+02)     # define the maximumvalue of varible 
VarLabel.append('! SSPARA( 3) = |mu| in GeV')         # define the label of varible from Leshouches file 


VarMin.append(1.000000E+01)
VarMax.append(5.000000E+01)
VarLabel.append('! SSPARA( 1) = tan\\beta')



TotVarScanned = 2  # Total number of variables scanned. 
###############################################################################
# Here to define the constraint spectrum you want out of SPheno               #
# TotConstScanned = 0   -----> no constraints will apply and                  #
#                              all spectrum files with out selection          #
###############################################################################

ConstMin.append(120)   # define the minimum value of constraint variable  
ConstMax.append(135)   # define the maximum value of constraint variable
ConstLabel.append('# H2') # define the label of constraint from Leshouches file 
ConstNum.append('25') # Leshouches number of constaint variable in Leshouches file 
ConstResNum.append('1')   # 1 for masses, 2 for matrices ( like yukawa & Sparticles mass matrix etc ), 0 for BR values 


ConstMin.append(400)   
ConstMax.append(800)   
ConstLabel.append('# Hpm_2') 
ConstNum.append('37') 
ConstResNum.append('1') 


TotConstScanned = 0 # Total number of constraint variables scanned.

########################## Higgs Bounds #####################################
HiggsBounds =1 #### if 1 ---> switch it on. if 0 swithch off 
HBPath = '/Users/ahmed/work/HiggsBounds-4.3.1'  ## Full path to Higgs bounds
NH     = '3'       # Number of neutral Higgs bosons 
NCH    = '1'       # Number of charged Higgs bosons 
ExcludeHB = 1      # if 1 --> remove the points excluded by HB. If 0 ---> keep the excluded points 
######################## Higgs Signals #######################################
HiggsSignal =1 #### if 1 ---> switch it on. if 0 swithch off 
HSPath = '/Users/ahmed/work/HiggsSignals-1.4.0'  ## Full path to Higgs bounds
ExcludeHS = 0     # put the upper value of chi square total ..  if 0 do not remove any spec

######################## Micro Omegas##########################################

MicoOmegas = 0  #### if 1 ---> switch it on. if 0 swithch off 
MicoOmegaspath = '/Users/ahmed/work/micromegas_5.0.8/MSSM'  ## Full path to the excutable main file in the MicroOmegas directory
######################### MadGraph ########################################

MadGraph = 0    # define how many processes you want to calculate 
proc.append('''import model mssm
 #define p = u1 u1bar        
 generate p p > e- e+ ''' )    # define the process as defined in usual using in madgrpah, feel free to write any thing and define any prticles or add process , etc 
proc.append('''import model mssm
 generate p p > mu- mu+ ''' ) 
madgraph_path = '/Users/ahmed/work/MG5_aMC_v2_4_3' 
RunCard_path = '/Users/ahmed/work/scanner'  #The run card has to neamed as  run_card.dat

