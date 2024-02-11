# enscroll

Convert source code to PDF. Similar to GNU `enscript`, but you are supposed to
glue the ends of each page over the header of the next page so it looks like a
very long piece of paper containing source code, kind of like a continuous feed
computer paper, but with regular A4/letter paper.

## Usage

```sh
pdm install

pdm run enscroll [options...] [--] <input file name> >output.tex && latexmk -xelatex output.tex
```

Options:

- `--paper=<string>`: Paper size as defined by the CTAN `geometry` package.
  Defaults to `a4paper`.
- `--a4`: Equivalent to `--paper=a4paper`.
- `--a5`: Equivalent to `--paper=a5paper`.
- `--b5`: Equivalent to `--paper=b5paper`.
- `--executive`: Equivalent to `--paper=executivepaper`.
- `--legal`: Equivalent to `--paper=legalpaper`.
- `--letter`: Equivalent to `--paper=letterpaper`.
- `--top=<dimension>`: The top margin. Defaults to `1.5cm`.
- `--bottom=<dimension>`: The bottom margin. Defaults to `1.5cm`.
- `--left=<dimension>`: The left margin. Defaults to `1.5cm`.
- `--right=<dimension>`: The right margin. Defaults to `1.5cm`.
- `--vertical=<dimension>`: Equivalent to `--top=<dimension> --bottom=<dimension>`.
- `--horizontal=<dimension>`: Equivalent to `--left=<dimension> --right=<dimension>`.
- `--margin=<dimension>`: Equivalent to `--vertical=<dimension> --horizontal=<dimension>`.
- `--family=<string>`: The font family. Defaults to `JetBrains Mono`.
- `--features=<options>`: The font features as defined by the CTAN
  `fontspec` package. Defaults to `Scale=0.9`.
- `--linechunks=<int>`: Number of lines per page. Defaults to `60`.
- `--tabsize=<int>`: Width of horizontal tab columns. Defaults to `4`.
- `--linenospace=<dimension>`: Space between the line number and the content. Defaults to `1.5em`.
