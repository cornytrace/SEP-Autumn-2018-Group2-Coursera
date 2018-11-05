#!/usr/bin/env python
import sys

import pytest


class MyPlugin:
    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.collected.append((item.nodeid, item._obj.__doc__))


my_plugin = MyPlugin()
pytest.main(["--collect-only", "-p", "no:terminal"], plugins=[my_plugin])

file = open("test-coursera.tex", "w+")
currentname = ""

file.write("\\documentclass[preview]{standalone}\n \\begin{document}\n")
for nodeid, docstring in my_plugin.collected:

    id = nodeid.split("::")
    filename = id[0].replace("_", "\\_")
    functionname = id[1].replace("_", " ").replace("[", " ").replace("]", "")
    if filename != currentname:
        if currentname != "":
            file.write("\\end{itemize}\n")
        currentname = filename
        file.write("\\subsection{" + filename + "}\n\\begin{itemize}\n")
    file.write("\\item " + functionname + "\n")
    itemize = False
    for line in docstring.splitlines(keepends=True):
        if line.startswith("    -") and not itemize:
            itemize = True
            file.write("    \\begin{itemize}\n")
        elif not line.startswith("    -") and itemize:
            itemize = False
            file.write("    \\end{itemize}\n")
        if line.startswith("    -"):
            line = line.replace("    - ", "    \\item ")
        file.write(line.replace("_", "\\_"))
    if itemize:
        file.write("    \\end{itemize}\n")
    file.write("\n")
    print(nodeid)
    print(docstring)
file.write("\\end{itemize}\n\\end{document}\n")
