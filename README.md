


                ##########################################
                #              Scanner HEP               #
                #             Ahmed Hammad               #
                #             03/12/19                   #
                ##########################################


   
   Multi-cores python scanner package with Machine learning models that can link model spectrum calculators, Spheno or CPsuperH with HiggsBounds, HiggsSignals,MicroMegas and Madgraph.
   The user can control and specify which set of programs to be switched on or off in his input file.
   The user has to download and install all packages he/she wants to use. The paths to the main directory of the installed packages has to be given in the input file.
   If the package is switched off in the input file, then there is no need to adjust any thing while the whole block will be ignored by the code.

   Usage: \
   1- ./run.sh input_file.py: run the code with a given input file. please note the input file has  to be in python format. \
   2- ./run.sh -f input_file.py: run the code with force deleting the output "if exist" from previous run. \
   3- ./run.sh --demo: Run the test version of the code where all packages are installed ( Not yet adjusted )\
   4- ./run.sh --help:  help and documenation 

   Useful comments:\
   1- Please be carefule with the version competability of SPheno+HB/HS. Older versions of spheno produces 
      the input to HB/HS as (coupling)^2 which is not compatable with the latest versions of HB/HS \
   2- To use SPheno+HB/HS please be sure that key 76 in the Leshouches file if 1 (or two please look at Spheno wiki) \
   3- The competability between output spectrums from Spheno/CPsuperH with Madgraph input parameter card has been handeled 
      by the script "source/spectrum2paramcard.py" that fill the input paramter MG card from output spectrums \ 
   4- Using Madgraph for total cross section calculatios, please be sure that the number of events in the given run card is 1 \
   5- For using MicroMegas with different SARAH models, the model files has to be genearted form SARAH and replaced by the model files in work/models
      To let MicroMgas read the spectrum of the new models, the line "rd" line in the file  "func.mdl" with  "rd             |slhaRead("spc.slha",0)"   
      
   How to set up the input file:
   1- MODE : 1 for Spheno scan and 2 for CPsuperH. \
   2- npoints:  Integer indicates the number of points you want to scan over. \
   3- N_Cores: Number of parallel cores the user need to use. \
   4- VarMin&VarMax : Minimum and maximum values for the scanned parameter. \
   5- VarLabel: the scanned parameter label as written in the input LesHouch file. \
   6- VarNum: Number of the scanned parameter as written in the LesHouch file. \
   7- TotVarScanned: Total number of the parameters the user want to scan over. \
   8- GridVar.append('1 == 2 * 1'): That means set the first scanned parameter to the second one multiplied by 1. \
   9- GridNum: 2 for any matrices and 1 for masses,coupings,BR or any parameter that not matrix int he LesHouches file. \
   10- TotConstScanned: Total number of constrains . If zero no constrain will applied to the scan. \
   Also, please note if the output spectrum doesnt statisfy the constrain it will be deleted. \
   11- HiggsBounds: 0 not to use the HB, 1 run HB from the information given in the output spectrum, 2 (SPHENO only) consider the produced separate produced files \
   12- HBPath: Path to the main directory of HB. \
   13- NH: Number of nutral Higgs in the model. \
   14- NCH: Number of charged Higges in the model. \
   15- ExcludeHB: if 1 delete the spectrums that not satisfy the HB constraints. If 0 keep the spectrums that not satisfy the HB constrains. \
   16-HiggsSignal: if 0 dont use the HiggsSignals, if 1 run HS from the information given in the output spectrum,  2 (SPHENO only) consider the produced separate produced files \
   17- PATHMHUNCERTINITY: path to the file that contains the uncertinity of the Higgses measurements. \
   18-ExcludeHS: Upper value of chisquared reporeted by HS, if output spectrum has lower vchi squared value the spectrum will be deleted.
    if 0 means all spectrum will be kept. \
    19- MicoOmegas: if 1 trun on MicroMegas, if 0 skip it. \
    20- MicoOmegaspath: Path to the Model dierctroy in MicroMegas \
    21- MadGraph: 0 means skip madgraph, if 1 will be turned on. \
    22- proc.append: here the user has to write the process as typed in the Proc card in Madgrph. \
    23- madgraph_path: path to the main directory of madgraph \
    24- RunCard_path: path to the run card to be used in the cross section. 
