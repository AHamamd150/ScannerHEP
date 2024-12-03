#!/bin/bash
[ $# -eq 0 ] && { echo "No input file is given, please run the code as  ./run.sh input_file.py"; exit 1; }
if [ $1 == '--help' ]; then
  cat "./source/help"
  exit 0
fi
if [ $1 == '--test' ]; then
  echo "            This is supposed to run a test file 
            where all the packges will install automatically and a test sample runs over 
            all spectrum generators... but not ready yet !!!!!!"
  exit 0
fi
test -f wrapper.py && rm -rf wrapper.py
cp -rf ./source/wrapper.py  . 
if [ $1 == '-f' ]; then
  string=$2
  set -f; IFS=.; arr=($string)
  sed  -i -e "s/from scan_input import /from ${arr[0]} import /g"  wrapper.py
  chmod 777 wrapper.py
  ./wrapper.py $1 $2
fi
if [ $1 != '-f' ]; then
  string=$1
  set -f; IFS=.; arr=($string)
  sed  -i -e "s/from scan_input import /from ${arr[0]} import /g"  wrapper.py
  chmod 777 wrapper.py
  ./wrapper.py $1
fi
rm -rf wrapper.py
rm -rf wrapper.py-e
