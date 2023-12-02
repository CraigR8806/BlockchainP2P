#!/bin/bash


this_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

node_number=$1

for i in $(ls /apps/node/resources/peer/node${node_number}/resources/react_dynamic/);do
    podman cp --overwrite /apps/node/resources/peer/node${node_number}/resources/react_dynamic/$i/${i}.js Node${node_number}_Peer:/app/resources/react_dynamic/$i/${i}.js
done
