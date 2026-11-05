import re, sys
src, dst = sys.argv[1], sys.argv[2]
lines = open(src).read().split("\n")

UNI = {"≈": r"$\approx$", "→": r"$\to$", "×": r"$\times$", "÷": r"$\div$", "✓": r"\cmark{}", "✗": r"\xmark{}",
       "⇔": r"$\Leftrightarrow$", "·": r"$\cdot$", "…": r"\ldots{}", "≤": r"$\le$"}

def esc_code(s):
    out = ""
    for ch in s:
        if ch in "\\": out += r"\textbackslash{}"
        elif ch in "{}_&%#$": out += "\\" + ch
        elif ch == "^": out += r"\^{}"
        elif ch == "~": out += r"\~{}"
        elif ch == "…": out += r"\ldots{}"
        else: out += ch
    return out

def inline(s):
    """Convert one line of markdown text (with $math$, `code`, **bold**) to LaTeX."""
    keep = []
    def stash(x):
        keep.append(x); return f"\x00{len(keep)-1}\x00"
    s = re.sub(r"`([^`]+)`", lambda m: stash(r"\texttt{" + esc_code(m.group(1)) + "}"), s)
    s = re.sub(r"\$([^$]+)\$", lambda m: stash("$" + m.group(1) + "$"), s)
    # straight double quotes -> TeX quotes
    s = re.sub(r'"([^"]*)"', r"``\1''", s)
    for ch in "&%#_":
        s = s.replace(ch, "\\" + ch)
    for k, v in UNI.items():
        s = s.replace(k, v)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], s)
    return s

out = []
i = 0
state = None          # 'box' while inside a formula box
def close_box():
    global state
    if state == "box":
        out.append(r"\end{formulabox}")
    elif state == "note":
        out.append(r"\end{notebox}")
    state = None

while i < len(lines):
    L = lines[i]
    if L.startswith("# "):
        out.append(r"\sheettitle{" + inline(L[2:]) + "}")
    elif L.startswith("## "):
        close_box()
        out.append(r"\week{" + inline(L[3:]) + "}")
    elif L.strip() == "---" or L.strip() == "":
        pass
    elif re.match(r"\*\*\d+\.\d+ ", L):
        close_box()
        m = re.match(r"\*\*(\d+\.\d+) (.*?)\*\*(.*)$", L)
        num, title, rest = m.group(1), m.group(2), m.group(3).strip()
        t = inline(title) + ((r" \normalfont\small " + inline(rest)) if rest else "")
        out.append(r"\begin{formulabox}{" + num + "}{" + t + "}")
        state = "box"
    elif L.startswith("$$"):
        body = L.strip()[2:-2]
        out.append(r"\[" + body + r"\]")
    elif L.startswith(">"):
        para = []
        while i < len(lines) and lines[i].startswith(">"):
            para.append(inline(lines[i][1:].strip())); i += 1
        i -= 1
        txt = " ".join(para)
        if state == "box":
            out.append(r"\meaningline{" + txt + "}")
        elif state == "note":
            out.append(txt)
        else:
            out.append(r"\intro{" + txt + "}")
    elif L.startswith("**e.g.**"):
        # Example block: runs until the next bold heading, rule or section.
        out.append(r"\tcblower" + "\n" + r"\egline{" + inline(L[len("**e.g.**"):].strip()) + "}")
        out.append(r"\begin{egbody}")
        in_list = False
        i += 1
        while i < len(lines) and not (re.match(r"\*\*(\d+\.\d+ |Remember\*\*)", lines[i]) or lines[i].strip() == "---" or lines[i].startswith("#")):
            E = lines[i]
            if E.startswith("- "):
                if not in_list:
                    out.append(r"\begin{itemize}"); in_list = True
                out.append(r"\item " + inline(E[2:]).replace(r"\frac", r"\dfrac"))
            elif E.strip():
                if in_list:
                    out.append(r"\end{itemize}"); in_list = False
                edge = re.match(r"\*\*(Edge case[^*]*)\*\*\s*(.*)$", E.strip())
                if E.startswith("$$"):
                    out.append(r"\[" + E.strip()[2:-2] + r"\]")
                elif edge:
                    out.append(r"\edgesub{" + inline(edge.group(1)) + "}{" + inline(edge.group(2)).replace(r"\frac", r"\dfrac") + "}")
                else:
                    out.append(r"\egsub{" + inline(E.strip()).replace(r"\frac", r"\dfrac") + "}")
            i += 1
        if in_list:
            out.append(r"\end{itemize}")
        out.append(r"\end{egbody}")
        i -= 1
    elif L.strip() == "**Remember**":
        close_box()
        out.append(r"\begin{rembox}")
        i += 1
        items, table = [], []
        while i < len(lines) and (lines[i].startswith("- ") or lines[i].startswith("|") or lines[i].strip() == ""):
            if lines[i].startswith("- "): items.append(inline(lines[i][2:]))
            elif lines[i].startswith("|"): table.append(lines[i])
            i += 1
        i -= 1
        if table:
            rows = [r for r in table if not re.match(r"\|\s*-", r)]
            cells = [[inline(c.strip()) for c in r.strip("|").split("|")] for r in rows]
            out.append(r"\begin{center}\begin{tabular}{" + "l" + "c" * (len(cells[0]) - 1) + r"}\toprule")
            out.append(" & ".join(r"\textbf{" + c + "}" for c in cells[0]) + r"\\\midrule")
            for r in cells[1:]: out.append(" & ".join(r) + r"\\")
            out.append(r"\bottomrule\end{tabular}\end{center}")
        if items:
            out.append(r"\begin{itemize}")
            out += [r"\item " + it for it in items]
            out.append(r"\end{itemize}")
        out.append(r"\end{rembox}")
    elif L.startswith("**"):
        close_box()
        m = re.match(r"\*\*(.*?)\*\*(.*)$", L)
        out.append(r"\begin{notebox}{" + inline(m.group(1)) + (" " + inline(m.group(2).strip()) if m.group(2).strip() else "") + "}")
        state = "note"
    else:
        raise SystemExit(f"unhandled line {i+1}: {L}")
    i += 1
close_box()

preamble = r"""\documentclass[10pt,a4paper]{article}
\usepackage[a4paper,margin=1.5cm,top=1.4cm,bottom=1.6cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{fontspec}
\usepackage{pifont}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{extramarks}
\usepackage{needspace}
\setlength{\parindent}{0pt}
\definecolor{accent}{HTML}{1D4E89}
\definecolor{accentlight}{HTML}{EAF1FA}
\definecolor{eg}{HTML}{F4F6F8}
\definecolor{muted}{HTML}{4A5560}
\definecolor{rem}{HTML}{8A5A00}
\definecolor{remlight}{HTML}{FFF7E6}
\newcommand{\cmark}{\textcolor{green!50!black}{\ding{51}}}
\newcommand{\xmark}{\textcolor{red!70!black}{\ding{55}}}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\color{muted}MXB103 Formula Sheet}
\fancyhead[R]{\small\color{muted}\ifx\topleftxmark\empty\firstleftxmark\else\topleftxmark\fi}
\fancyfoot[C]{\small\color{muted}\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\newcommand{\sheettitle}[1]{{\color{accent}\LARGE\bfseries #1\par}\vspace{4pt}}
\newcommand{\intro}[1]{{\small\color{muted}#1\par}\vspace{6pt}}
\newcommand{\week}[1]{\needspace{6\baselineskip}\vspace{8pt}\extramarks{#1}{#1}{\color{accent}\large\bfseries #1\par}\vspace{-2pt}{\color{accent}\rule{\linewidth}{0.8pt}}\par\vspace{4pt}}
\newcommand{\meaningline}[1]{{\small\color{muted}\textit{Meaning:} #1\par}}
\newcommand{\egline}[1]{{\small\textbf{e.g.}\ #1\par}}
\newcommand{\egsub}[1]{{\vspace{3pt}\small #1\par}}
\definecolor{edge}{HTML}{B03A2E}
\newcommand{\edgesub}[2]{{\vspace{5pt}\small\textcolor{edge}{\textbf{\ding{115}\ #1}}\ #2\par}}
\newenvironment{egbody}{\small\setlist[itemize]{leftmargin=16pt,itemsep=4pt,topsep=3pt,label=\textcolor{accent}{\textbullet}}}{}
\newtcolorbox{formulabox}[2]{enhanced,breakable=false,colback=white,colframe=accent!60,colbacktitle=accentlight,
  coltitle=accent,fonttitle=\bfseries,title={#1\quad #2},boxrule=0.5pt,arc=2pt,left=6pt,right=6pt,top=2pt,bottom=4pt,
  colbacklower=eg,segmentation style={solid,draw=accent!25},lower separated=true,before skip=5pt,after skip=5pt}
\newtcolorbox{rembox}{enhanced,colback=remlight,colframe=rem!50,boxrule=0.4pt,arc=2pt,left=6pt,right=6pt,top=3pt,bottom=3pt,
  fontupper=\small,before upper={{\color{rem}\bfseries Remember}\par},before skip=5pt,after skip=5pt}
\newtcolorbox{notebox}[1]{enhanced,colback=white,colframe=rem!50,colbacktitle=remlight,coltitle=rem,fonttitle=\bfseries,
  title={#1},boxrule=0.4pt,arc=2pt,fontupper=\small,before skip=5pt,after skip=5pt}
\setlist[itemize]{leftmargin=14pt,itemsep=1pt,topsep=2pt}
\allowdisplaybreaks
\begin{document}
\thispagestyle{plain}
"""
open(dst, "w").write(preamble + "\n".join(out) + "\n\\end{document}\n")
print("ok", len(out), "lines")
