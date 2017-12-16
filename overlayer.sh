#!/bin/bash

rm catfile.txt
python3 overlayer.py $1
mv final.mp4 final.temp
rm -rfv *.mp4 *.png catfile.txt
mv final.temp $1-final.mp4
