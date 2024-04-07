#!/bin/bash

cd ../

rm data/packages -r
rm data/dump -r
rm data/csv -r
mkdir data/packages data/dump data/csv
unzip data/homebrew_dataset.zip -d data/dump
for folder in data/dump/* ;
do
  cp "${folder}"/*.rb data/packages/
done