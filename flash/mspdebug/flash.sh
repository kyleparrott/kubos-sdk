#!/bin/bash

mspdebug=$1
cmd=$2
exe=$3

export LD_LIBRARY_PATH=$KUBOS_LIB_PATH:$LD_LIBRARY_PATH

echo $mspdebug tilib \"$cmd\" $exe --allow-fw-update
$mspdebug tilib "$cmd $exe" --allow-fw-update
