#!/bin/bash

SCRIPT=`realpath $BASH_SOURCE`
SCRIPTPATH=`dirname $SCRIPT`
WORKDIR=`realpath $SCRIPTPATH`

cd $WORKDIR

if [ ! -d $WORKDIR/venv ]; then
    mkdir -p $WORKDIR/venv;
fi
virtualenv -p python3.8 $WORKDIR/venv

cd $WORKDIR/venv/bin
source activate

cd $WORKDIR

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools

requirements_txt=./requirements.txt
if [ -f "$requirements_txt" ]; then
    pip install -r $requirements_txt
fi

requirements_py=./__requirements__.py
if [ -f "$requirements_py" ]; then
    python $requirements_py
fi
