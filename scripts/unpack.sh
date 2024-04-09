#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"

cd "$SCRIPT_DIR/../data"

rm packages -r
rm dump -r
mkdir packages dump csv
unzip homebrew_dataset.zip -d dump
for folder in dump/* ; do
  cp "${folder}"/*.rb packages/
done
