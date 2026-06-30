#!/bin/bash

pip install uv

uv pip install -r reqs.txt

zensical "$@"
