import re
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, Sequence

import nbformat

# Insert line of code
insert = re.compile(r"# INSERT (.+)")
# Remove instructor note from Markdown cell
instructor_note = re.compile(r"\*\*Instructor Note:\*\* (.+)", re.I)
# Remove block of code, leaving blank line
remove_block = re.compile(r"# REMOVE\{(.+?)# REMOVE\}", re.S)
# Remove line of code, leaving blank line
remove_line = re.compile(r"(.+) # REMOVELINE")
# Combines `remove_line` and `insert` to avoid blank line
remove_line_insert = re.compile(r"(.+) # REMOVELINE\n(\s*)# INSERT (.+)")
# Remove right-hand side of var assignment
remove_rhs = re.compile(r"(.+? = )(.+)# REMOVERHS")
# Remove right-hand side of argument
remove_rhs_arg = re.compile(r"(.+=)(.+)# REMOVERHS")
# Remove right-hand side of multi-line var assignment
remove_rhs_block = re.compile(r"# REMOVERHS\{(\s*)(.+? = )(.+?)# REMOVERHS\}", re.S)
# Remove block of SQL code
remove_sql_block = re.compile(r"-- REMOVE\{(.+?)-- REMOVE\}", re.S)


def read_nb(filepath):
    """
    Takes `filepath` to `ipynb` file as input.
    Returns notebook object (JSON).
    """
    with open(filepath, "r") as f:
        nb = nbformat.read(f, as_version=4)
    return nb


def scrub_code(code):
    # Remove lines and blocks of code
    code = re.sub(remove_block, "", code)
    code = remove_rhs_block.sub(r"\2...", code)
    # Insert lines of code
    code = remove_line_insert.sub(r"\2\3", code)  # must go first
    code = re.sub(remove_line, "", code)
    code = insert.sub(r"\1", code)
    # Remove RHS var and arg assignments
    code = remove_rhs.sub(r"\1...", code)
    code = remove_rhs_arg.sub(r"\1...,", code)
    return code


def strip_cells(filepath):
    """
    Takes `filepath` to `ipynb` file as input.
    Removes / adds code according to flags.
    Make MD cells non-editable. Makes all cells non-deletable.
    Returns notebook object (JSON).
    """
    nb = read_nb(filepath)
    for idx, c in enumerate(nb.cells):
        # Scrub SQL cells
        if (c.cell_type == "code") and c["source"].startswith("%%sql"):
            c["source"] = re.sub(remove_sql_block, "", c["source"])
        # Scrub python cells, disable delete
        if c.cell_type == "code":
            # Remove lines and blocks of code
            c["source"] = scrub_code(c["source"])
            # Cannot delete cell
            c["metadata"]["deletable"] = False
        # Lock cells with `# LOCK tag`
        if (c.cell_type == "code") and c["source"].startswith("# LOCK\n"):
            c["source"] = c["source"].replace("# LOCK\n", "")
            c["metadata"]["editable"] = False
        if "# DELETE CELL" in c["source"]:
            nb.cells.pop(idx)
        # Autostart grader import cell
        if "import wqet_grader" in c.source:
            c["metadata"]["init_cell"] = True
        # Autostart Video cells
        if "VimeoVideo" in c.source:
            c["metadata"]["init_cell"] = True
            c["metadata"]["editable"] = False
        # Lock grader cells
        if (c.cell_type == "code") & ("wqet_grader" in c.source):
            c["metadata"]["editable"] = False
        # Scrub Markdown cells, disable editing and delete
        if c.cell_type == "markdown":
            c["source"] = re.sub(instructor_note, "", c["source"])
            c["metadata"]["editable"] = False
            c["metadata"]["deletable"] = False
    return nb


def scrub_notebook(input_fp, test_file=False):
    scrubbed_nb = strip_cells(input_fp)
    print(f"Scrubbed {input_fp}")
    if test_file:
        new_path = input_fp[:-6] + "_test.ipynb"
        nbformat.write(scrubbed_nb, new_path)
        print(f"Saved as {new_path}")
    else:
        nbformat.write(scrubbed_nb, input_fp)


def scrub_file(input_fp, test_file=False):
    with open(input_fp, "r") as f:
        code = f.read()
    code = scrub_code(code)
    print(f"Scrubbed {input_fp}")
    if test_file:
        if ".env" in input_fp:
            new_path = input_fp + "_test"
        else:
            new_path = input_fp[:-3] + "_test.py"
        open(new_path, "w").write(code)
        print(f"Saved as {new_path}")
    else:
        open(input_fp, "w").write(code)


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = ArgumentParser("Remove answer code from notebooks")
    parser.add_argument("filenames", nargs="+", metavar="F", help="notebook filenames")
    parser.add_argument(
        "--test",
        action="store_const",
        const=True,
        help="store notebook w/ new filename `test_`",
    )
    args = parser.parse_args(argv)
    for filename in args.filenames:
        print(filename)
        ext = Path(filename).suffix
        if ext == ".ipynb":
            scrub_notebook(filename, args.test)
        elif (ext == ".py") or (".env" in filename):
            scrub_file(filename, args.test)
        else:
            print(f"Can't scrub {filename}")
            pass


if __name__ == "__main__":
    exit(main())
