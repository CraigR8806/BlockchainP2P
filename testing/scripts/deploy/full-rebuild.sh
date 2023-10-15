#!/bin/bash

this_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

node_number=$1
export BCP2PVERSION=$2

. $this_dir/podify-src.sh $node_number

stop_container $peer_container_name
stop_container $mongo_container_name

rm_container $peer_container_name
rm_container $mongo_container_name

rm_pod

rm_network

#rm_image $peer_container_image_name $peer_container_image_tag
#rm_image $mongo_container_image_name $mongo_container_image_tag

rm -rf /apps/node/data/node${node_number}/*
rm -f /apps/node/resources/peer/node${node_number}/*.Containerfile
cat /apps/node/resources/podres/ContainerfileTemplates/peer.Containerfile.tml | envsubst > /apps/node/resources/peer/node${node_number}/peer.Containerfile
cat /apps/node/resources/podres/ContainerfileTemplates/mongo.Containerfile.tml | envsubst > /apps/node/resources/peer/node${node_number}/mongo.Containerfile

create_network

create_pod

build_image $peer_container_image_name $peer_container_image_tag $peer_container_file
build_image $mongo_container_image_name $mongo_container_image_tag $mongo_container_file

run_container $mongo_container_name $mongo_container_image_name $mongo_container_image_tag "$mongo_volume"
run_container $peer_container_name $peer_container_image_name $peer_container_image_tag