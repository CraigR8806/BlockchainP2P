#!/bin/bash

this_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

node_number=$1
export BCP2PVERSION=$2

. $this_dir/podify-src.sh $node_number

stop_container $peer_container_name

rm_container $peer_container_name

rm -f /apps/node/resources/peer/node${node_number}/peer.Containerfile
cat /apps/node/resources/podres/ContainerfileTemplates/peer.Containerfile.tml | envsubst > /apps/node/resources/peer/node${node_number}/peer.Containerfile

build_image $peer_container_image_name $peer_container_image_tag $peer_container_file
run_container $peer_container_name $peer_container_image_name $peer_container_image_tag