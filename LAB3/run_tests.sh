#!/bin/bash

for i in {1..25}
do
    dir=$(printf "%0*d\n" 2 $i)
    echo "Test $dir"
    res=`python3 SimPa.py < test$dir/primjer.in | diff test$dir/primjer.out -`
    if [ "$res" != "" ]
        then 
            echo "FAIL"
            echo $res
        else
            echo "OK"
        fi
done