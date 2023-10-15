#!/bin/bash

pids=""

for i in 1 2 3;do
    podman container stop Node${i}_Peer &
    pids+="$! "
    podman container stop Node${i}_Database &
    pids+="$! "
done

wait $pids