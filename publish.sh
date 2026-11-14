#!/usr/bin/env zsh

# conda finden: erst über $CONDA_EXE, dann über PATH, dann an üblichen Orten
for c in "$CONDA_EXE" \
         "$(command -v conda 2>/dev/null)" \
         /opt/homebrew/Caskroom/miniconda/base/bin/conda \
         "$HOME/miniconda3/bin/conda" \
         "$HOME/anaconda3/bin/conda" \
         "$HOME/miniforge3/bin/conda" \
         /opt/conda/bin/conda; do
  if [[ -n "$c" && -x "$c" ]]; then
    eval "$("$c" shell.zsh hook)"
    break
  fi
done

if ! typeset -f conda >/dev/null; then
  echo "conda nicht gefunden" >&2
  exit 1
fi

conda activate python313 || exit 1

export BASE_URL="/thma_anm_en"
myst build --execute --html
ghp-import -n -f -p _build/html