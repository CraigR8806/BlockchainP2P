#!/bin/bash

this_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

numberOfNodes=$1

mkdir -p $this_dir/testing/testinglogs
rm -rf $this_dir/testing/testinglogs/*

pids=""
for i in $(seq $numberOfNodes);do
    python $this_dir/src/main.py $this_dir/testing/${i}.yaml 2>$this_dir/testing/testinglogs/$i.log 1>$this_dir/testing/testinglogs/$i.log & 
done
