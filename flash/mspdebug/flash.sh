#!/bin/bash

this_dir=$(cd "`dirname "$0"`"; pwd)
cmd=$1
exe=$2

echo mspdebug tilib \"$cmd\" $exe
mspdebug tilib "$cmd $exe" 