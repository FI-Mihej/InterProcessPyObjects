#!/bin/bash

SCRIPT=`realpath $BASH_SOURCE`
SCRIPTPATH=`dirname $SCRIPT`
WORKDIR=`realpath $SCRIPTPATH`

cd $WORKDIR/venv/bin
source activate

cd $WORKDIR
