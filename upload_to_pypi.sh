#!/bin/bash

hatch version
hatch build

# https://github.com/pypa/hatch/issues/671
python -m twine upload dist/*
