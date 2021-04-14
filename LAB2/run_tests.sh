#!/bin/bash

for i in {1..14}
do
    dir=$(printf "%0*d\n" 2 $i)
    echo "Test $dir"
    res=`python MinDka.py < test$dir/t.ul | diff test$dir/t.iz -`
    if [ "$res" != "" ]
        then 
            echo "FAIL"
            echo $res
        else
            echo "OK"
        fi
done