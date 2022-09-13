#!/bin/bash

if [ $# -lt 1 ]; then
    cat <<HELP

dockertags  --  list all tags for a Docker image on a remote registry.

EXAMPLE: 
    - list all tags for ubuntu:
       dockertags ubuntu

    - list all php tags containing apache:
       dockertags php apache

HELP
fi

im="$1"

if [ -z "$(echo "$im" | grep -o '/')" ]; then
    hub="https://registry.hub.docker.com/v2/repositories/library/$im/tags/"
else
    hub="https://registry.hub.docker.com/v2/repositories/$im/tags/"
fi

# Get number of pages
if [ -z "$(command -v curl)" ]; then
    first=$(wget -q -O - $hub)
else
    first=$(curl -sL $hub)
fi
count=$(echo $first | sed -E 's/\{\s*"count":\s*([0-9]+).*/\1/')
pagination=$(echo $first | grep -Eo '"name":\s*"[a-zA-Z0-9_.-]+"' | wc -l)
pages=$(expr $count / $pagination + 1)

# Get all tags one page after the other
tags=
i=0
while [ $i -le $pages ]; do
    i=$(expr $i + 1)
    if [ -z "$(command -v curl)" ]; then
        page=$(wget -q -O - "$hub?page=$i")
    else
        page=$(curl -sL "$hub?page=$i")
    fi
    ptags=$(echo $page | grep -Eo '"name":\s*"[a-zA-Z0-9_.-]+"' | sed -E 's/"name":\s*"([a-zA-Z0-9_.-]+)"/\1/')
    tags="${ptags} $tags"
done
echo "${tags}" >tags.txt
