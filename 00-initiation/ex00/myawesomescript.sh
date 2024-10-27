#!/bin/sh

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 bit.ly/your-link"
  exit 1
fi

short_url="$1"

curl -I "$short_url"

long_url=$(curl -sI "$short_url" | grep -i "location" | cut -d " " -f 2)

echo $long_url