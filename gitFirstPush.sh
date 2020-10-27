#!/bin/bash

if [ $# != 1 ]; then
    echo 引数エラー: $*
    exit 1
else
    echo OK
fi

set -e
echo $1
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin_gl https://github.com/TakashiSugie/$1.git
git push -u origin_gl main
