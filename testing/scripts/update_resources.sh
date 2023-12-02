#!/bin/bash

this_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

version=$1

if [ -f /tmp/update/resources/peer/BlockchainP2P-${version}.tar.gz ];then

        cp -f /tmp/update/resources/peer/BlockchainP2P-${version}.tar.gz /apps/node/resources/peer/node1
        cp -f /tmp/update/resources/peer/BlockchainP2P-${version}.tar.gz /apps/node/resources/peer/node2
        cp -f /tmp/update/resources/peer/BlockchainP2P-${version}.tar.gz /apps/node/resources/peer/node3
fi

mkdir -p /apps/node/resources/peer/node1/resources
mkdir -p /apps/node/resources/peer/node2/resources
mkdir -p /apps/node/resources/peer/node3/resources

if [ -d /tmp/update/resources/react_dynamic ];then
        cp -rf /tmp/update/resources/react_dynamic /apps/node/resources/peer/node1/resources
        cp -rf /tmp/update/resources/react_dynamic /apps/node/resources/peer/node2/resources
        cp -rf /tmp/update/resources/react_dynamic /apps/node/resources/peer/node3/resources
fi

[ -f /tmp/update/resources/peer/env.properties ] && mv -f /tmp/update/resources/peer/env.properties /apps/node/resources/peer

[ -f /tmp/update/resources/peer/properties.tml.yaml ] && mv -f /tmp/update/resources/peer/properties.tml.yaml /apps/node/resources/peer

[ -d /tmp/update/resources/podres/ContainerfileTemplates ] && mv -f /tmp/update/resources/podres/ContainerfileTemplates/* /apps/node/resources/podres/ContainerfileTemplates
[ -f /tmp/update/resources/podres/podman.properties ] && mv -f /tmp/update/resources/podres/podman.properties /apps/node/resources/podres/

if [ -d /tmp/update/scripts ];then
        cp -rf /tmp/update/scripts/* /apps/node/scripts
        find /apps/node/scripts -name "*.sh" | xargs -i chmod 740 {}
fi


rm -rf /tmp/update