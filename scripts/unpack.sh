#!/bin/bash

cd ../

rm data/packages/*
for folder in data/dump/* ;
do
  cp "${folder}"/*.rb data/packages/
done