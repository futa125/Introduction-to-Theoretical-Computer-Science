#!/bin/bash

for i in {1..33}
do
    dir=$(printf "%0*d\n" 2 $i)
    echo "Test $dir"
    res=`python3 SimEnka.py < test$dir/test.a | diff test$dir/test.b -`
    if [ "$res" != "" ]
        then 
            echo "FAIL"
            echo $res
        else
            echo "OK"
        fi
done