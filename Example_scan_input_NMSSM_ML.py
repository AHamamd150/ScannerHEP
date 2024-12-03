VarMax =[] 
VarMin =[] 
VarLabel =[]
VarNum =[]
ConstMax =[]
ConstMin =[]
ConstLabel =[]
ConstNum =[]
ConstResNum =[]
ResLabel = []
ResNum = []
ResOpt = []
proc=[]
GridVar=[]
GridNum=[]
######################################
# Please do not change the above tags#################
######################################
MODE = 1                   #1->spHeno , 2 cpsuperh,
npoints =20000       #Number of the collected points 
N_Cores = 150            #Number of cores to be used 
##################################
####### parameters for adaptive sampling #######
#################################
Use_vegas = False    # If using Vegas alone
Use_ML = True        # If using Vegas + ML 
test_points = 50000 # Size of the random points to be fitted by Vegas
points_init = 10  # Initial number of collected points, per core, to train vegas
batch_size = 200   # size of the batch predicted by vegas including the random points
random_frac= 0.1 # ratio of the random points included in the batch
###########ML setup###############
### This is considered only if Use_ML = True ####
lr = 0.001
Num_layers = 5
Num_neurons = 100
ML_batch_size =  50
epoch = 500
ML_verbose = 0
#####################################################
pathS ='/home/scanner/SPheno-4.0.3' #Path to SPheno directory betweenthe quotes
Lesh ='LesHouches.in.NMSSM_low2_1'     # The LesHouches file has to be in the main Spheno directory
SPHENOMODEL ='NMSSM'                   # Model Name as in spheno bin directory, like SPhenoMSSM ->  MSSSM or SPhenoNMSSM -> NMSSM.
#################################

VarMin.append(2.00000E+00)     # define the minimum value of varible
VarMax.append(5.0000E+01)     # define the maximumvalue of varible
VarLabel.append('# TanBeta')         # define the label of varible from Le
VarNum.append('3')              # Leshouches number of variable in Leshouches file

VarMin.append(0.050000E+00)  #2
VarMax.append(0.100000E+00)
VarLabel.append('# LambdaInput')
VarNum.append('61')

VarMin.append(0.0100E+00)   #3
VarMax.append(0.0900E+00)
VarLabel.append('# KappaInput')
VarNum.append('62')


VarMin.append(-2.5000000E+03)  #4
VarMax.append(-1.500000E+03)
VarLabel.append('# ALambdaInput')
VarNum.append('63')


VarMin.append(2.0000000E+02)  #5
VarMax.append(6.000000E+02)
VarLabel.append('# AKappaInput')
VarNum.append('64')

VarMin.append(-2.5000000E+02)  #6
VarMax.append(-1.00000E+02)
VarLabel.append('# MuEffinput')
VarNum.append('65')


VarMin.append(2.0000000E+02)  #7
VarMax.append(5.0000000E+02)
VarLabel.append('# M1')
VarNum.append('1')

VarMin.append(2.000000E+02)  #8
VarMax.append(7.000000E+02)
VarLabel.append('# M2')
VarNum.append('2')

VarMin.append(2.50000000E+03)  #9
VarMax.append(5.000000E+03)
VarLabel.append('# M3')
VarNum.append('3')



TotVarScanned = 9  # Total number of variables scanned. 

######### Bias the ML network predictions###########################
## If the user want to force the a formula to certian scanned parameter after the ML predictions# 
#GridVar.append('1 * 1 <  7  <  1 * 10')  ## This mean the scanned variable number 7 will sampled in ranges from variable number 1  to variable number 1 x 10 
#GridNum.append('1')  ## 2 for matrices and 1 for masses.

GridVar.append('6 * 0.5e-04 <  3  <  1 * -1') 
GridNum.append('1')

GridVar.append('6 * 1 <  7  <  6 * 1') 
GridNum.append('2')

GridVar.append('6 * 1 <  8  <  6 * 1') 
GridNum.append('2')

GridVar.append('6 * 1 <  9 <  6 * 1') 
GridNum.append('2')

GridVar.append('6 * 1 <  10  <  6 * 1') 
GridNum.append('2')

GridVar.append('6 * 1 <  11 <  6 * 1') 
GridNum.append('2')


GridVariables = 0
###############################################################################
# Here to define the constraint spectrum you want out of SPheno               #
# TotConstScanned = 0   -----> no constraints will apply and                  #
#                              all spectrum files with out selection          #
###############################################################################
ConstMin.append(92)  
ConstMax.append(98) 
ConstLabel.append('# hh_1') 
ConstNum.append('25') 
ConstResNum.append('1')  

ConstMin.append(124)  
ConstMax.append(126) 
ConstLabel.append('# hh_2') 
ConstNum.append('35') 
ConstResNum.append('1')

ConstMin.append(500)  
ConstMax.append(100000000) 
ConstLabel.append('# Hpm_2') 
ConstNum.append('37') 
ConstResNum.append('1')

ConstMin.append(1000021)    
ConstMax.append(1000023)   
ConstLabel.append('   # LSP ') 
ConstNum.append(' 1 ') 
ConstResNum.append('1')   


ConstMin.append(1.000000E-12)   
ConstMax.append(1000)   
ConstLabel.append('# Chi_2') 
ConstNum.append('Decay') 
ConstResNum.append('1')   


ConstMin.append(1.000000E-12)   
ConstMax.append(1000)   
ConstLabel.append('# Cha_1') 
ConstNum.append('Decay') 
ConstResNum.append('1') 


TotConstScanned = 6 # Total number of constraint. If the scanned point doesnt satisfy any of the constrained the spectrum will removed

########################## Higgs Bounds #####################################
HiggsBounds = 0   #### if 1 ---> switch it on. if 0 swithch off 
HBPath = '/hammad/HiggsBounds-4.3.1' ## Full path to Higgs bounds
NH     = '5'       # Number of neutral Higgs bosons 
NCH    = '1'       # Number of charged Higgs bosons 
ExcludeHB = 1    # if 1 --> remove the points excluded by HB. If 0 ---> keep the excluded points 
######################## Higgs Signals #######################################
HiggsSignal = 0 #### if 1 ---> switch it on. if 0 swithch off 
HSPath =  '/hammad/HiggsSignals-1.4.0'  ## Full path to Higgs bounds
PATHMHUNCERTINITY = '/hammad/MHall_uncertainties.dat' ## mass_uncertinity file needed by higgssignals
ExcludeHS = 95     # put the upper value of chi square total ..  if 0 do not remove any spec

######################## Micro Omegas##########################################
MicoOmegas = 0  #### if 1 ---> switch it on. if 0 swithch off 
MicoOmegaspath = '/hammad/micromegas_5.2.1/NMSSM_new'  ## Full path to the excutable main file in the MicroOmegas directory
######################### MadGraph ########################################
MadGraph = 0       #Number of the processes Madgrpah is going to compute. 
madgraph_path = '/hammad/MG5_aMC_v3_4_2/' 
RunCard_path = '/hammad/MG5_aMC_v3_4_0_RC3/'  # The run card must have the name "run_card.dat"

proc.append('''import model NMSSM_UFO -modelname
define c11 = c1 c1bar
define c22 = c2 c2bar
define ca = c11 c22
define w = wm wmc 
define n = n2
define p = g u1 u1bar d1 d1bar u2 u2bar d2 d2bar
generate p p > c11 n / n2 n3 n4 n5 h1 h2 h3 ah2 ah3 hm2c z go sd1 sd2 sd3 sd4 sd5 sd6 su1 su2 su3 su4 su5 su6 sd1c sd2c sd3c sd4c sd5c sd6c su1c su2c su3c su4c su5c su6c  hm2 hm2c  c1 c1bar c2 c2bar  d1 d1bar d2 d2bar d3 d3bar u1  u1bar u2 u2bar u3 u3bar sd1 sd1c sd2 sd2c sd3 sd3c sd4 sd4c sd5 sd5c sd6 sd6c
''' )   


proc.append('''import model MSSM_SLHA2
define n = n2 n3 n4
define c11 = x1+ x1-
define c22 = x2+ x2-
define ca = c11 c22
define w = w+ w-
define l = l+ l-
define e = e+ e-
define mu = mu+ mu-
define vee = ve ve~
define vmm = vm vm~
define vv = vee vmm
define q = u c d s b
define qb = u~ c~ d~ s~ b~
generate p p > ca n / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, n > n1 e+ e- / a  h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, ca > n1 e vee / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
''' )   



proc.append('''import model MSSM_SLHA2
define n = n2 
define c11 = x1+ x1-
generate p p > c11 n / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~
''' )   



 
  



