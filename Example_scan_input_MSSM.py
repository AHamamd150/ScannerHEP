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
# Please do not change the above tags#
######################################
MODE = 1                   #1->spHeno , 2 cpsuperh,
npoints = 200000000           #Number of points you want to scan over
N_Cores = 46            #Number of cores to be used 
#####################################################
pathS ='//home/ahmed/work/SPheno-3.3.8' #Path to SPheno directory betweenthe quotes
Lesh ='LesHouches.in.MSSM_low_wino_inp_1'     
SPHENOMODEL ='MSSM'                   # Model Name as in spheno bin directory, like SPhenoMSSM, SPheno BLSSM, etc
#################################

VarMin.append(1.000000E+01)     # define the minimum value of varible
VarMax.append(1.00000E+03)     # define the maximumvalue of varible
VarLabel.append('# M1input')         # define the label of varible from Le
VarNum.append('1')              # Leshouches number of variable in Leshouches file

VarMin.append(9.000000E+01)
VarMax.append(1.000000E+03)
VarLabel.append('# M2input')
VarNum.append('2')

VarMin.append(-1.000000E+03)
VarMax.append(-9.000000E+01)
VarLabel.append('# Muinput')
VarNum.append('23')


VarMin.append(1.000000E+04)
VarMax.append(9.000000E+06)
VarLabel.append('# mA2input')
VarNum.append('24')


VarMin.append(2.000000E+00)
VarMax.append(5.000000E+01)
VarLabel.append('# TanBeta')
VarNum.append('25')

VarMin.append(1.000000E+06)
VarMax.append(25.000000E+06)
VarLabel.append('# Real(mQ2(1,1),dp)')
VarNum.append('  1  1 ')

VarMin.append(1.000000E+06)
VarMax.append(25.000000E+06)
VarLabel.append('# Real(mQ2(2,2),dp)')
VarNum.append('  2  2 ')


VarMin.append(1.000000E+06)
VarMax.append(25.000000E+06)
VarLabel.append('# Real(mQ2(3,3),dp)')
VarNum.append('  3  3 ')


VarMin.append(1.000000E+06)
VarMax.append(25.000000E+06)
VarLabel.append('# Real(md2(1,1),dp)')
VarNum.append('  1  1 ')


VarMin.append(1.000000E+06)
VarMax.append(25.000000E+06)
VarLabel.append('# Real(md2(2,2),dp)')
VarNum.append('  2  2 ')


VarMin.append(1.000000E+06)
VarMax.append(25.000000E+06)
VarLabel.append('# Real(md2(3,3),dp)')
VarNum.append('  3  3 ')


VarMin.append(1.000000E+06)
VarMax.append(25.000000E+06)
VarLabel.append('# Real(mu2(1,1),dp)')
VarNum.append('  1  1 ')


VarMin.append(1.000000E+06)
VarMax.append(25.000000E+06)
VarLabel.append('# Real(mu2(2,2),dp)')
VarNum.append('  2  2 ')

VarMin.append(1.000000E+06)
VarMax.append(25.000000E+06)
VarLabel.append('# Real(mu2(3,3),dp)')
VarNum.append('  3  3 ')


VarMin.append(1.000000E+04)
VarMax.append(9.000000E+06)
VarLabel.append('# Real(ml2(1,1),dp)')
VarNum.append('  1  1 ')


VarMin.append(1.000000E+04)
VarMax.append(9.000000E+06)
VarLabel.append('# Real(ml2(2,2),dp)')
VarNum.append('  2  2 ')


VarMin.append(1.000000E+04)
VarMax.append(9.000000E+06)
VarLabel.append('# Real(ml2(3,3),dp)')
VarNum.append('  3  3 ')


VarMin.append(1.000000E+04)
VarMax.append(9.000000E+06)
VarLabel.append('# Real(me2(1,1),dp)')
VarNum.append('  1  1 ')


VarMin.append(1.000000E+04)
VarMax.append(9.000000E+06)
VarLabel.append('# Real(me2(2,2),dp)')
VarNum.append('  2  2 ')


VarMin.append(1.000000E+04)
VarMax.append(9.000000E+06)
VarLabel.append('# Real(me2(3,3),dp)')
VarNum.append('  3  3 ')

VarMin.append(1.000000E+00)
VarMax.append(1.000000E+00)
VarLabel.append('# Real(Td(1,1),dp)')
VarNum.append('  1  1 ')


VarMin.append(1.000000E+00)
VarMax.append(1.000000E+00)
VarLabel.append('# Real(Td(2,2),dp)')
VarNum.append('  2  2 ')


VarMin.append(1.000000E+00)
VarMax.append(1.000000E+02)
VarLabel.append('# Real(Td(3,3),dp)')
VarNum.append('  3  3 ')

VarMin.append(1.000000E+00)
VarMax.append(1.000000E+00)
VarLabel.append('# Real(Te(1,1),dp)')
VarNum.append('  1  1 ')


VarMin.append(1.000000E+00)
VarMax.append(1.000000E+00)
VarLabel.append('# Real(Te(2,2),dp)')
VarNum.append('  2  2 ')


VarMin.append(1.000000E+00)
VarMax.append(1.000000E+02)
VarLabel.append('# Real(Te(3,3),dp)')
VarNum.append('  3  3 ')



VarMin.append(1.000000E+00)
VarMax.append(1.000000E+00)
VarLabel.append('# Real(Tu(1,1),dp)')
VarNum.append('  1  1 ')

VarMin.append(1.000000E+00)
VarMax.append(1.000000E+00)
VarLabel.append('# Real(Tu(2,2),dp)')
VarNum.append('  2  2 ')


VarMin.append(1.000000E+00)
VarMax.append(1.000000E+02)
VarLabel.append('# Real(Tu(3,3),dp)')
VarNum.append('  3  3 ')



TotVarScanned = 29  # Total number of variables scanned. 

#################### Grid ###########################

GridVar.append('1 == 2 * 10') ## This mean the first variable equales by second variable times 10
GridNum.append('1')    ##One if masses two if matrices  

GridVar.append('6 == 7 * 1')## This mean the third variable equales by second 
GridNum.append('2')

GridVariables = 2
###############################################################################
# Here to define the constraint spectrum you want out of SPheno               #
# TotConstScanned = 0   -----> no constraints will apply and                  #
#                              all spectrum files with out selection          #
###############################################################################


ConstMin.append(1000021)    
ConstMax.append(1000023)   
ConstLabel.append('   # LSP ') 
ConstNum.append(' 1 ') 
ConstResNum.append('1')   



TotConstScanned = 0 # Total number of constraint variables scanned.

########################## Higgs Bounds #####################################
HiggsBounds =0 #### if 1 ---> switch it on. if 0 swithch off 
HBPath = '/work/HiggsBounds-4.3.1' ## Full path to Higgs bounds
NH     = '3'       # Number of neutral Higgs bosons 
NCH    = '1'       # Number of charged Higgs bosons 
ExcludeHB = 1      # if 1 --> remove the points excluded by HB. If 0 ---> keep the excluded points 
######################## Higgs Signals #######################################
HiggsSignal =0 #### if 1 ---> switch it on. if 0 swithch off 
HSPath =  '/work/HiggsSignals-1.4.0'  ## Full path to Higgs bounds
PATHMHUNCERTINITY = '/work/scan_THDMV/scanner_3/MHall_uncertainties.dat' ## mass_uncertinity file needed by higgssignals
ExcludeHS = 86     # put the upper value of chi square total ..  if 0 do not remove any spec

######################## Micro Omegas##########################################

MicoOmegas = 0  #### if 1 ---> switch it on. if 0 swithch off 
MicoOmegaspath = '/home/ahmed/work/micromegas_5.0.8/MSSM'  ## Full path to the excutable main file in the MicroOmegas directory
######################### MadGraph ########################################

MadGraph = 0   
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
define q = u c d s b
define qb = u~ c~ d~ s~ b~
generate p p > ca n / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, n > n1 e vee q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, ca > n1 q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
add process p p > ca n / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, n > n1 mu vmm q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, ca > n1 q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~''' )    

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
define q = u c d s b
define qb = u~ c~ d~ s~ b~
generate p p > c22 n / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, n > n1 e vee q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, (c22 > c11 z / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, z > q qb)
add process p p > c22 n / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, n > n1 mu vmm q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, (c22 > c11 z / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, z > q qb)''' )
proc.append('''
import model MSSM_SLHA2
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
define q = u c d s b
define qb = u~ c~ d~ s~ b~
generate p p > n1 c22 j/ h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, c22 > n1 e vee / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
add process p p > n1 c22 j/ h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, c22 > n1 mu vmm / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
add process p p > n1 c22 j j/ h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, c22 > n1 e vee / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
add process p p > n1 c22 j j/ h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, c22 > n1 mu vmm / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
add process p p > n1 c22 j j j/ h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, c22 > n1 e vee / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
add process p p > n1 c22 j j j/ h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, c22 > n1 mu vmm / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
''')
proc.append('''
import model MSSM_SLHA2
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
define q = u c d s b
define qb = u~ c~ d~ s~ b~
generate p p > n1 n / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, n > n1 e vee q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
add process p p > n1 n / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, n > n1 mu vmm q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
''')
proc.append('''
import model MSSM_SLHA2
define n = n2 n3 n4
define np = n2 n3 n4
define c11 = x1+ x1-
define c22 = x2+ x2-
define ca = c11 c22
define w = w+ w-
define l = l+ l-
define e = e+ e-
define mu = mu+ mu-
define vee = ve ve~
define vmm = vm vm~
define q = u c d s b
define qb = u~ c~ d~ s~ b~
generate p p > n np / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, n > n1 e vee q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, np > n1 q qb / a w h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
add process p p > n np / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, n > n1 mu vmm q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, np > n1 q qb / a w h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
''')
proc.append('''
import model MSSM_SLHA2
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
define q = u c d s b
define qb = u~ c~ d~ s~ b~
generate p p > c22 c11 / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, c22 > n1 e vee / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, c11 > n1 q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
add process p p > c22 c11 / h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~, c22 > n1 mu vmm / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~, c11 > n1 q qb / a z h01 h2 h3 h+ h- ul cl t1 ur cr t2 dl sl b1 dr sr b2 ul~ cl~ t1~ ur~ cr~ t2~ dl~ sl~ b1~ dr~ sr~ b2~ el- mul- ta1- er- mur- ta2- el+ mul+ ta1+ er+ mur+ ta2+ h- h+ sve svm svt sve~ svm~ svt~
''')
madgraph_path = '/home/ahmed/work/madGraph' 
RunCard_path = '/home/ahmed/work/scan_MSSM'  #The run card has to neamed as  run_card.dat

