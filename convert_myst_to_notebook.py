#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import sys
from pathlib import Path

ADMONITION_RE = re.compile(r'^(`{3,})\{admonition\}\s*(.*?)\s*$')
CODE_CELL_RE = re.compile(r'^(`+)\{code-cell\}')
DROPDOWN_RE = re.compile(r'^(`{3,})\{dropdown\}')
FIGURE_RE = re.compile(r'^(`{3,})\{figure\}\s*(.*?)\s*$')
OPTION_RE = re.compile(r'^:(\w+):\s*(.*)$')


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(
        description='Cleans a MyST markdown file for conversion to a Jupyter '
                    'notebook: drops learning objectives and solutions, turns '
                    'exercise/project admonitions into plain headings, and '
                    'collects mini-exercises at the end of the file.')
    parser.add_argument('filename', type=str)
    parser.add_argument('output_filename', type=str, nargs='?',
                         help='Defaults to overwriting filename in place.')

    if len(sys.argv) == 1:
        print('Provide a filename: convert_myst_to_notebook.py inputfile.md')
        sys.exit(1)

    return parser.parse_args()


def read_admonition_classes(lines, index):
    classes = []
    while index < len(lines) and lines[index].strip().startswith(':class:'):
        classes.append(lines[index].split(':class:', 1)[1].strip())
        index += 1
    return classes, index


def read_figure_options(lines, index):
    options = {}
    while index < len(lines):
        match = OPTION_RE.match(lines[index].strip())
        if not match:
            break
        options[match.group(1)] = match.group(2).strip()
        index += 1
    return options, index


def find_fence_close(lines, index, fence):
    while index < len(lines):
        if lines[index].rstrip('\n') == fence:
            return index
        index += 1
    raise ValueError(f'Unterminated fence {fence!r}')


def try_collect_code_cell(lines, index):
    """If the next non-blank line opens a ```{code-cell} block starting at
    `index`, return (lines from index through the closing fence, index after
    the block). Otherwise return (None, index) unchanged."""
    probe = index
    while probe < len(lines) and lines[probe].strip() == '':
        probe += 1

    match = CODE_CELL_RE.match(lines[probe]) if probe < len(lines) else None
    if not match:
        return None, index

    fence = match.group(1)
    close = find_fence_close(lines, probe + 1, fence)
    return lines[index:close + 1], close + 1


def collapse_blank_lines(lines):
    cleaned = []
    prev_blank = False
    for line in lines:
        is_blank = line.strip() == ''
        if is_blank and prev_blank:
            continue
        cleaned.append(line)
        prev_blank = is_blank
    return cleaned


def clean_myst_file(input_filename, output_filename):
    with open(input_filename) as file:
        lines = file.readlines()

    output_lines = []
    mini_exercises = []
    warning_tags = ['```{mermaid}']

    i = 0
    while i < len(lines):
        line = lines[i]

        dropdown_match = DROPDOWN_RE.match(line)
        if dropdown_match:
            fence = dropdown_match.group(1)
            close = find_fence_close(lines, i + 1, fence)
            i = close + 1
            continue  # Video dropdowns: dropped entirely

        figure_match = FIGURE_RE.match(line.rstrip('\n'))
        if figure_match:
            fence, image_path = figure_match.groups()
            options, body_start = read_figure_options(lines, i + 1)
            close = find_fence_close(lines, body_start, fence)
            caption = lines[body_start:close]
            i = close + 1

            alt_text = options.get('alt', Path(image_path).stem.replace('_', ' '))
            output_lines.append(f'![{alt_text}]({image_path})\n')
            output_lines.append('\n')
            output_lines.extend(caption)
            continue

        match = ADMONITION_RE.match(line.rstrip('\n'))

        if match is None:
            for tag in warning_tags:
                if tag in line:
                    print(f'warning line {i + 1}: {line.rstrip()}')
            output_lines.append(line)
            i += 1
            continue

        fence, title = match.groups()
        classes, body_start = read_admonition_classes(lines, i + 1)
        close = find_fence_close(lines, body_start, fence)
        body = lines[body_start:close]
        i = close + 1

        if 'attention' in classes:
            # Drop the admonition and the plain "## Learning objectives"
            # heading that always precedes it, so no empty section remains.
            while output_lines and output_lines[-1].strip() == '':
                output_lines.pop()
            if output_lines and output_lines[-1].strip().lstrip('#').strip().lower() == title.lower():
                output_lines.pop()
            continue

        if title.startswith('Solution'):
            continue  # Solutions: dropped entirely

        if 'warning' in classes:
            output_lines.append(f'**{title}**\n')
            output_lines.append('\n')
            output_lines.extend(body)
            output_lines.append('\n')
            continue

        if title.startswith('Mini-exercise'):
            code_cell, i = try_collect_code_cell(lines, i)
            mini_exercises.append((body, code_cell))
            continue

        # Remaining tip admonitions (Warm-up exercise, Exercise ..., Project:,
        # Part N:, Closing question, Bonus exercise): keep in place as a
        # plain heading; the code-cell that follows is untouched pass-through.
        output_lines.append(f'## {title}\n')
        output_lines.append('\n')
        output_lines.extend(body)

    output_lines = collapse_blank_lines(output_lines)

    if mini_exercises:
        output_lines.append('\n')
        output_lines.append('## Mini-exercises\n')
        output_lines.append('\n')
        for number, (body, code_cell) in enumerate(mini_exercises, start=1):
            output_lines.append(f'### Mini-exercise {number}\n')
            output_lines.append('\n')
            output_lines.extend(body)
            output_lines.append('\n')
            if code_cell:
                output_lines.extend(code_cell)
                output_lines.append('\n')

    with open(output_filename, 'w') as output_file:
        output_file.writelines(output_lines)


def main():
    args = parse_command_line_arguments()
    output_filename = args.output_filename or args.filename
    clean_myst_file(args.filename, output_filename)


if __name__ == "__main__":
    main()
