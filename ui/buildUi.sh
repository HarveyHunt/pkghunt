#!/bin/bash
# My first ever shell script.
for file in *.ui
do
pyuic4 $file > ${file%.*}.py
done;
