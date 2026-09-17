#!/usr/bin/env bash
# Build student Jupyter notebooks from the MyST markdown source of one chapter.
#
# Usage: ./build_notebooks.sh chapter01
#
# Copies chapterNN/*.md into notebooks/chapterNN, cleans the copies with
# convert_myst_to_notebook.py (drops learning objectives and solutions, turns
# exercise/project admonitions into plain headings, collects mini-exercises at
# the end). The cleaned .md still needs the code-along gaps filled in by hand
# before converting to .ipynb with jupytext (--to ipynb, then --set-formats
# ipynb).

set -euo pipefail

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate python313

if [ $# -ne 1 ]; then
    echo "Usage: $0 <chapterNN>" >&2
    exit 1
fi

chapter="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$script_dir/$chapter"
target_dir="$script_dir/notebooks/$chapter"

if [ ! -d "$source_dir" ]; then
    echo "No such chapter directory: $source_dir" >&2
    exit 1
fi

mkdir -p "$target_dir"
cp "$source_dir"/*.md "$target_dir"/

if [ -d "$source_dir/pics" ]; then
    mkdir -p "$target_dir/pics"
    cp "$source_dir"/pics/* "$target_dir/pics/"
fi

for md_file in "$target_dir"/*.md; do
    python3 "$script_dir/convert_myst_to_notebook.py" "$md_file"
done

echo "Cleaned markdown written to $target_dir"
echo "Fill in the code-along gaps, then run:"
echo "  jupytext --to ipynb $target_dir/*.md"
echo "  jupytext --set-formats ipynb $target_dir/*.ipynb"
