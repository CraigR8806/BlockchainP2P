#!/bin/bash

for i in $(grep  -A3 "server:" testing/*.yaml | grep "port:" | awk '{print $3}');do 
    lsof -nP -i4TCP:$i | grep LISTEN | awk '{print $2}' | xargs kill -9 
done




