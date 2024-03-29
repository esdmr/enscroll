import itertools
import posixpath
import sys
import typing

import pygments
import pygments.lexers
import pygments.token

type TranslationTable = dict[int, str | int | None]

latex_encoded: TranslationTable = {
    ord("%"): r"\%",
    ord("~"): r"\NSCRt{}",
    ord("_"): r"\NSCRu{}",
    ord("&"): r"\&",
    ord("\\"): r"\NSCRb{}",
    ord("{"): r"\{",
    ord("}"): r"\}",
    ord("^"): r"\NSCRc{}",
    ord("$"): r"\NSCRd{}",
    ord("#"): r"\#",
}

latex_encoded_verbatim: TranslationTable = {
    **latex_encoded,
    ord("~"): r"\NSCRt ",
    ord("_"): r"\NSCRu ",
    ord("\\"): r"\NSCRb ",
    ord("^"): r"\NSCRc ",
    ord("$"): r"\NSCRd ",
    ord(" "): r"\NSCRs ",
}


options: dict[str, str] = {
    "paper": "a4paper",
    "top": "1.5cm",
    "bottom": "1.5cm",
    "left": "1.5cm",
    "right": "1.5cm",
    "family": "JetBrains Mono",
    "features": "Scale=0.9",
    "linechunks": "60",
    "tabsize": "4",
    "linenospace": "1.5em",
}


def format_token(type: typing.Any, content: str):
    content = content.translate(latex_encoded_verbatim)

    if type in pygments.token.String:
        return rf"\textbf{{{content}}}"
    elif type in pygments.token.Comment:
        return rf"\textit{{{content}}}"
    elif type in pygments.token.Keyword:
        return rf"\textbf{{{content}}}"
    elif type in pygments.token.Name:
        return rf"\textit{{{content}}}"
    else:
        return content


def main():
    is_options = True
    path = ""

    # This should use argparse instead.
    for i in sys.argv[1:]:
        try:
            name, value = i[2:].split("=", 1)
        except ValueError:
            name = i[2:]
            value = ""

        if not is_options or not i.startswith("-"):
            path = i
        elif i == "--":
            is_options = False
        elif i in {"--a4", "--a5", "--b5", "--executive", "--legal", "--letter"}:
            options["paper"] = f"{name}paper"
        elif i.startswith("--margin="):
            options["top"] = value
            options["bottom"] = value
            options["left"] = value
            options["right"] = value
        elif i.startswith("--vertical="):
            options["top"] = value
            options["bottom"] = value
        elif i.startswith("--horizontal="):
            options["left"] = value
            options["right"] = value
        elif i.startswith("--") and name in options:
            options[name] = value
        else:
            raise Exception(f"Unknown option {i}")

    assert path, f"No input path"

    options["dir"] = posixpath.dirname(path) or "."
    options["name"] = posixpath.basename(path)

    with open(path, "r") as f:
        source = f.read().rstrip("\n")

    source_lines: list[list[str]] = [[]]

    for type, content in pygments.lex(
        source,
        pygments.lexers.get_lexer_for_filename(
            path,
            source,
            tabsize=int(options["tabsize"]),
        ),
    ):
        i, *lines = content.split("\n")

        if i:
            source_lines[-1].append(format_token(type, i))

        for i in lines:
            source_lines.append([])

            if i:
                source_lines[-1].append(format_token(type, i))

    with open(posixpath.join(posixpath.dirname(__file__), "template.tex"), "r") as f:
        preamble = f.read()

    lines = [rf"\NSCRline{{{"".join(i)}}}" for i in source_lines]

    options["lines"] = str(len(lines))
    options["linenolen"] = str(len(options["lines"]))

    pages = [
        [r"\begin{NSCRpage}", *i, r"\end{NSCRpage}"]
        for i in itertools.batched(lines, int(options["linechunks"]))
    ]

    options["pages"] = str(len(pages))

    body = [j for i in pages for j in i]

    variables = [
        rf"\def\NSCR{k}{{{v.translate(latex_encoded)}}}" for k, v in options.items()
    ]

    content = [
        *variables,
        preamble,
        r"\begin{document}",
        *body,
        r"\end{document}",
    ]

    print("\n".join(content))
