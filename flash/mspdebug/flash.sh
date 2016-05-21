#!/bin/bash

mspdebug=$1
cmd=$2
exe=$3

echo $mspdebug tilib \"$cmd\" $exe
$mspdebug tilib "$cmd $exe" 