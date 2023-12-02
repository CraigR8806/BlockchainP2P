#!/bin/bash

this_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

getNodes() {
    echo "$(grep -oP "(?<=^node)[0-9]+" $this_dir/../resources/peer/env.properties | sort -u)"
}

createNodePropertyFile() {
    nodeNumber=$1
    peer_dir=$this_dir/../resources/peer
    node_dir=$peer_dir/node${nodeNumber}/
    rm -f $node_dir/properties.yaml
    cp $peer_dir/properties.tml.yaml $node_dir/properties.yaml

    nodevaris="$(grep -oP "(?<=^node${nodeNumber}\.).+" $peer_dir/env.properties | tr ' ' '~')"
    for i in $nodevaris;do
        name="$(echo $i | awk -F= '{print $1}')"
        value="$(echo $i | awk -F= '{print $2}' | tr '~' ' ')"

        sed -i "s~\${${name}}~${value}~" $node_dir/properties.yaml
    done
}


for n in $(getNodes);do

    createNodePropertyFile $n

done