#!/bin/bash
this_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

intent=$1
version=$2

pids=""

for i in 1 2 3;do
    $this_dir/deploy/${intent}.sh $i $version &
    pids+="$! "
done

wait $pids