#!/usr/bin/env bash

set -e

repository=${TAG_REPOSITORY:-'csc'}
filter=${1:-'*'}

for dockerfile in $filter.dockerfile; do

    name=$(basename -s .dockerfile $dockerfile)

    echo
    echo "Building $repository/$name"
    echo

    docker build -t "$repository/$name" -f "$dockerfile" $DOCKER_BUILD_OPTIONS .

done
