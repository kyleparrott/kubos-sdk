#!/bin/bash
dfu_util=$1
exe=$2

echo $dfu_util --alt 0 -D $exe -S 335F33813433 -s 0x08000000
$dfu_util --alt 0 -D $exe -S 335F33813433 -s 0x08000000

