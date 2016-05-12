#!/usr/bin/env bash

cd ../cppSetupTools/ && ./setup.py --libs cppitertools:v0.1 && cd -
./renderSite.R
