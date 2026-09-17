#!/bin/zsh

conda activate python313
export BASE_URL="/thma_anm_en"
myst build --execute --html
ghp-import -n -f -p _build/html