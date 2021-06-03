#!/bin/bash

for i in {1..20}
do
    dir=$(printf "%0*d\n" 2 $i)
    echo "Test $dir"
    res=`python3 Parser.py < test$dir/test.in | diff test$dir/test.out -`
    if [ "$res" != "" ]
        then 
            echo "FAIL"
            echo $res
        else
            echo "OK"
        fi
done