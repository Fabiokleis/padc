#!/bin/bash

## run main.py

set -e

source ./env/bin/activate
cd src && python ./main.py
