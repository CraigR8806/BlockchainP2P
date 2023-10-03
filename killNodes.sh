#!/bin/bash

for i in $(grep -oE -e "server.port=.+" testing/*.properties | awk -F= '{print $2}');do 
    lsof -nP -i4TCP:$i | grep LISTEN | awk '{print $2}' | xargs kill -9 
done




