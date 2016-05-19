#!/bin/bash

cmd=$1
exe=$2

echo mspdebug tilib \"$cmd\" $exe
mspdebug tilib "$cmd $exe" 