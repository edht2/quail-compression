#!/usr/bin/env bash

sudo ln -s ./quail-compression/run.py /usr/local/bin/qcomp
if [ $? -ne 0 ]; then
    echo "Install failed!"
else
    echo "Link created"
    rm install.sh
fi