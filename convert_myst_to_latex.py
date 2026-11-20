"""Converts the exercises chapter of the MyST script into a LaTeX sheet.

Reads chapterNN/chapterNN_secMM.md with the H1 "N.M Exercises" and writes a
LaTeX file in the style of the CA documents (latex/exercises_preamble.tex):
every exercise in an aufgabe box on a new page, with its approximate time on
the right,
given code in code boxes, no solutions and no empty "# code cell" cells.
With --pdf the file is compiled with lualatex (twice) and the PDF is put
next to the .tex file. Constructs the converter does not know (figures,
tables, dropdowns other than solutions) are reported and skipped.

Usage: python3 convert_myst_to_latex.py [--pdf] chapter07/chapter07_sec03.md \
           notebooks/chapter07/chapter07_sec03.tex
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PREAMBLE = SCRIPT_DIR / 'latex' / 'exercises_preamble.tex'

FENCE_RE = re.compile(r'^(\s*)(`{3,})(.*)$')
H1_RE = re.compile(r'^# (\d+)\.(\d+) Exercises\s*$')
HEADING_RE = re.compile(r'^(#{2,4}) (.*)$')
BULLET_RE = re.compile(r'^([*+-]) (.*)$')
NUMBER_RE = re.compile(r'^(\d+)\. (.*)$')
OPTION_RE = re.compile(r'^:(\w+):\s*(.*)$')
STARS_RE = re.compile(r'\((✩+)\)')
TIME_RE = re.compile(r'^(✩+) .*\(approx\. (\d+) min\)')
INLINE_RE = re.compile(r'(`[^`]+`|\$[^$]+\$|\[[^\]]+\]\([^)]+\))')
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
# longer exercises (lines in the master) may be split across pages
MAX_UNBROKEN_LINES = 60

PRACTICE = r"""\subsection*{How to Practice}

\begin{itemize}[noitemsep]
  \item Open a new Jupyter notebook on your own computer, switch off the
        internet connection and do not use AI tools.
  \item Type the given code yourself and pay attention to indentation,
        parentheses and quotation marks. A gray arrow
        \textcolor{gray}{$\hookrightarrow$} marks a line that is too long for
        the page. Type it as one line.
  \item Write your predictions and explanations in Markdown cells.
\end{itemize}
"""


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(
        description='Converts the exercises chapter of the MyST script into '
                    'a LaTeX exercise sheet without solutions and, with '
                    '--pdf, compiles it with lualatex.')
    parser.add_argument('source', type=Path)
    parser.add_argument('target', type=Path)
    parser.add_argument('--pdf', action='store_true',
                        help='compile the .tex file and put the PDF next to it')
    return parser.parse_args()


# ── Inline markup ─────────────────────────────────────────────────────────────

def escape(text):
    text = text.replace('\\', '\x00')
    for char in '&%#_{}':
        text = text.replace(char, '\\' + char)
    text = text.replace('~', r'\textasciitilde{}').replace('^', r'\textasciicircum{}')
    return text.replace('\x00', r'\textbackslash{}')


def markup(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'\\emph{\1}', text)
    return re.sub(r'"([^"]+)"', '“\\1”', text)


def inline_code(code):
    for delim in '|!+@=;':
        if delim not in code:
            return f'\\py{delim}{code}{delim}'
    raise ValueError(f'no delimiter for inline code {code!r}')


def inline(text):
    out = []
    for part in INLINE_RE.split(text):
        if part.startswith('`') and part.endswith('`') and len(part) > 1:
            out.append(inline_code(part[1:-1]))
        elif part.startswith('$') and part.endswith('$') and len(part) > 1:
            out.append(part)
        elif LINK_RE.fullmatch(part):
            label, url = LINK_RE.fullmatch(part).groups()
            out.append(f'\\href{{{url}}}{{{inline(label)}}}')
        else:
            out.append(markup(escape(part)))
    return ''.join(out)


# ── Blocks ────────────────────────────────────────────────────────────────────

class Context:
    def __init__(self, source):
        self.source = source
        self.times = {}
        self.warnings = []

    def warn(self, message):
        self.warnings.append(message)


def indent_of(line):
    return len(line) - len(line.lstrip(' '))


def dedent(lines, width):
    return [line[width:] if line[:width].strip() == '' else line.lstrip()
            for line in lines]


def box(environment, code_lines):
    while code_lines and not code_lines[0].strip():
        code_lines = code_lines[1:]
    while code_lines and not code_lines[-1].strip():
        code_lines = code_lines[:-1]
    return [f'\\begin{{{environment}}}', *code_lines, f'\\end{{{environment}}}', '']


def split_options(body):
    options = {}
    while body and OPTION_RE.match(body[0].strip()):
        key, value = OPTION_RE.match(body[0].strip()).groups()
        options.setdefault(key, []).append(value)
        body = body[1:]
    return options, body


def convert_fence(info, body, ctx):
    if info.startswith('{code-cell}'):
        options, code = split_options(body)
        if '\n'.join(code).strip() == '# code cell':
            return []
        if any('hide-input' in tags for tags in options.get('tags', [])):
            ctx.warn('code cell with hide-input: long given code is hard to '
                     'type from paper')
        return box('code', code)
    if info.startswith('{admonition}'):
        title = info[len('{admonition}'):].strip()
        options, content = split_options(body)
        classes = ' '.join(options.get('class', []))
        if title.startswith(('Solution', 'Hint')) or 'dropdown' in classes:
            return []
        stars = STARS_RE.search(title)
        right = ''
        if stars and stars.group(1) in ctx.times:
            right = f'approx.\\ {ctx.times[stars.group(1)]} min'
        # an exercise stays on one page unless it is too long for a page
        environment = 'aufgabe'
        if len(content) > MAX_UNBROKEN_LINES:
            environment = 'aufgabelang'
            ctx.warn(f'{title} has more than {MAX_UNBROKEN_LINES} lines and '
                     'may be split across pages')
        # every exercise starts on a new page
        return ['\\clearpage',
                f'\\begin{{{environment}}}{{{inline(title)}}}{{{right}}}',
                *parse_blocks(content, ctx), f'\\end{{{environment}}}', '']
    if info == 'python':
        return box('code', body)
    if info == 'text':
        return box('ausgabe', body)
    ctx.warn(f'skipped unsupported block ```{info}')
    return []


def collect_list(lines, i, marker_re):
    """Return the items of the list starting at lines[i] and the next index."""
    items = []
    while i < len(lines):
        m = marker_re.match(lines[i])
        if not m:
            break
        width = len(lines[i]) - len(m.group(2))
        item = [m.group(2)]
        i += 1
        while i < len(lines):
            line = lines[i]
            if line.strip() and indent_of(line) >= width:
                item.append(line)
            elif not line.strip() and i + 1 < len(lines) \
                    and indent_of(lines[i + 1]) >= width and lines[i + 1].strip():
                item.append('')
            else:
                break
            i += 1
        items.append([item[0]] + dedent(item[1:], width))
        while i < len(lines) and not lines[i].strip() \
                and i + 1 < len(lines) and marker_re.match(lines[i + 1]):
            i += 1
    return items, i


def block_start(line):
    return (FENCE_RE.match(line) or HEADING_RE.match(line)
            or BULLET_RE.match(line) or NUMBER_RE.match(line)
            or line.strip().startswith(('$$', '|')))


def parse_blocks(lines, ctx):
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        fence = FENCE_RE.match(line)
        if fence:
            width, ticks, info = len(fence.group(1)), fence.group(2), fence.group(3).strip()
            j = i + 1
            while j < len(lines) and lines[j].strip() != ticks:
                j += 1
            out += convert_fence(info, dedent(lines[i + 1:j], width), ctx)
            i = j + 1
            continue

        heading = HEADING_RE.match(line)
        if heading:
            out += [f'\\subsection*{{{inline(heading.group(2))}}}', '']
            i += 1
            continue

        if stripped.startswith('$$'):
            math = [stripped[2:]]
            j = i
            # one line $$ ... $$ or several lines up to a line ending in $$
            while not (math[-1].endswith('$$') and (j > i or len(stripped) >= 4)):
                j += 1
                math.append(lines[j].strip())
            math[-1] = math[-1][:-2]
            out += ['\\[', *[m for m in math if m.strip()], '\\]', '']
            i = j + 1
            continue

        if stripped.startswith('|'):
            ctx.warn('skipped a table')
            while i < len(lines) and lines[i].strip().startswith('|'):
                i += 1
            continue

        for marker_re, environment in ((BULLET_RE, 'itemize'), (NUMBER_RE, 'enumerate')):
            if marker_re.match(line):
                items, i = collect_list(lines, i, marker_re)
                out.append(f'\\begin{{{environment}}}')
                for item in items:
                    content = parse_blocks(item, ctx)
                    out.append('  \\item ' + '\n'.join(content).strip())
                out += [f'\\end{{{environment}}}', '']
                break
        else:
            paragraph = []
            while i < len(lines) and lines[i].strip() and \
                    (not paragraph or not block_start(lines[i])):
                paragraph.append(lines[i].strip())
                i += 1
            out += [inline(' '.join(paragraph)), '']
    return out


# ── Document ──────────────────────────────────────────────────────────────────

def convert(source, target):
    lines = source.read_text(encoding='utf-8').split('\n')
    if lines and lines[0].strip() == '---':
        end = lines.index('---', 1)
        lines = lines[end + 1:]

    ctx = Context(source)
    for line in lines:
        m = BULLET_RE.match(line)
        if m and TIME_RE.match(m.group(2)):
            stars, minutes = TIME_RE.match(m.group(2)).groups()
            ctx.times[stars] = minutes

    h1 = next((i for i, line in enumerate(lines) if H1_RE.match(line)), None)
    if h1 is None:
        sys.exit(f'{source}: no heading "# N.M Exercises" found')
    chapter, section = H1_RE.match(lines[h1]).groups()
    body = parse_blocks(lines[h1 + 1:], ctx)

    rel_preamble = os.path.relpath(PREAMBLE.with_suffix(''), target.resolve().parent)
    tex = [
        f'% Generated by convert_myst_to_latex.py from {source}.',
        '% Change the master and convert again instead of editing this file.',
        r'\RequirePackage[l2tabu, orthodox, abort]{nag}',
        r'\documentclass[paper=a4, fontsize=11pt, parskip=half]{scrartcl}',
        '',
        f'\\input{{{rel_preamble}}}',
        '',
        r'\begin{document}',
        f'\\section*{{{chapter}.{section} Exercises}}',
        '',
        PRACTICE,
        r'\subsection*{Exercises}',
        '',
        *body,
        r'\end{document}',
        '',
    ]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(re.sub(r'\n{3,}', '\n\n', '\n'.join(tex)), encoding='utf-8')
    for message in ctx.warnings:
        print(f'note {source}: {message}')
    print(f'Wrote {target}')


def compile_pdf(target):
    with tempfile.TemporaryDirectory() as build_dir:
        for _ in range(2):
            result = subprocess.run(
                ['lualatex', '-interaction=nonstopmode', '-halt-on-error',
                 f'-output-directory={build_dir}', target.name],
                cwd=target.resolve().parent, capture_output=True, text=True)
            if result.returncode != 0:
                print(result.stdout[-3000:])
                sys.exit(f'lualatex failed for {target}')
        pdf = Path(build_dir) / target.with_suffix('.pdf').name
        shutil.copy(pdf, target.with_suffix('.pdf'))
    print(f'Wrote {target.with_suffix(".pdf")}')


if __name__ == '__main__':
    args = parse_command_line_arguments()
    convert(args.source, args.target)
    if args.pdf:
        compile_pdf(args.target)
