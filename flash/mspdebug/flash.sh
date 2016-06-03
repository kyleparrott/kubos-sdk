#!/bin/bash

mspdebug=$1
cmd=$2
exe=$3

echo $mspdebug tilib \"$cmd\" $exe --allow-fw-update
$mspdebug tilib "$cmd $exe" --allow-fw-update
