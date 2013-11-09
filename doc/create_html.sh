#!/bin/zsh

for file in $(ls src/*.md)
do
    echo $file
    filename=$(basename $file .md)
    pandoc -s -t html5 -c style.css -f markdown -o "$filename.html" $file
done
