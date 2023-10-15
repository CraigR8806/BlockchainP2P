#!/bin/bash

node_number=$1

readprop() {
    echo "$(grep -oP "(?<=^$1=).+" /apps/node/resources/podres/podman.properties)"
}

peer_container_name="$(readprop node${node_number}.podman.container.peer.name)"
peer_container_image_name="$(readprop node${node_number}.podman.container.peer.image.name)"
peer_container_image_tag="$(readprop node${node_number}.podman.container.peer.image.tag)"
peer_container_file="$(readprop node${node_number}.podman.container.peer.image.container_file)"
mongo_container_name="$(readprop node${node_number}.podman.container.mongo.name)"
mongo_container_image_name="$(readprop node${node_number}.podman.container.mongo.image.name)"
mongo_container_image_tag="$(readprop node${node_number}.podman.container.mongo.image.tag)"
mongo_container_file="$(readprop node${node_number}.podman.container.mongo.image.container_file)"
mongo_volume="-v $(readprop node${node_number}.podman.container.mongo.volume)"
pod_name="$(readprop node${node_number}.podman.pod.name)"
pod_ip="$(readprop node${node_number}.podman.pod.ip)"
network_name="$(readprop node${node_number}.podman.network.name)"
network_subnet="$(readprop node${node_number}.podman.network.subnet)"
dns="$(readprop podman.network.dns)"

stop_container() {
    podman container stop $1
}
rm_container() {
    podman container rm $1
}
rm_pod() {
    podman pod rm $pod_name
}
rm_network() {
    podman network rm $network_name
}
rm_image() {
    podman image rm $1:$2 -f
}
create_network() {
    podman network create --dns $dns  --subnet $network_subnet $network_name
}
create_pod() {
    podman pod create --network $network_name --ip=$pod_ip --name $pod_name
}
build_image() {
    image_name=$1
    image_tag=$2
    container_file=$3
    podman build -t ${image_name}:$image_tag -f=$container_file --dns=$dns
}
run_container() {
    container_name=$1
    image_name=$2
    image_tag=$3
    volume="$4"
    podman run  -d --pod=$pod_name --name=$container_name $volume ${image_name}:${image_tag}
}