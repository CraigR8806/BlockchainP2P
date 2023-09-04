#!/bin/bash

this_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

numberOfNodes=$1

mkdir -p $this_dir/testing/testinglogs
rm -rf $this_dir/testing/testinglogs/*

pids=""
for i in $(seq $numberOfNodes);do
    node $this_dir/index.js $this_dir/testing/${i}.properties 2>$this_dir/testing/testinglogs/$i.log 1>$this_dir/testing/testinglogs/$i.log & 
done
