#!/bin/bash

## publish package at pypi or test.pypi

function show_help() {
    echo "publish.sh [OPT] [OPT]"
    echo "usage: "
    echo "     help                      To show this help message"
    echo "     build                     To build package in dist/"
    echo "     clean                     To clean package in dist/"
    echo "     build test                To build and publish in testpypi"
    echo "     build pypi                To build and publish in pypi"
}

set -e
[ "$1" = "help" ] && show_help && exit 0
[ "$1" = "clean" ] && rm -r dist/ && exit 0
[ "$1" = "build" ] && python -m build
[ "$2" = "test" ] && twine upload --skip-existing -r testpypi dist/* && exit 0
[ "$2" = "pypi" ] && twine upload --skip-existing dist/* && exit 0
