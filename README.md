# Documentation

## Locally

+ Run `tasker.sh` to set up the pipenv and run mkdocs, e.g. `tasker.sh serve`.
+ Or with [`uv`](https://github.com/astral-sh/uv):
    + `uv venv` to create the environment
    + `source .venv/bin/activate` to jump into it
    + `uv pip install -r reqs.txt` to install the requirements
    + `mkdocs serve` to launch the server

### Generating Python documentation

1. Navigate to the relevant folder where the Python bindings are installed, e.g. `/home/$USER/Workspace/nyx-space/anise/anise-py`
2. Install `pdoc3` with pipx if not available yet: `pipx install pdoc3`
3. Run pdoc with the `--pdf` flag, which generates a markdown actually: `pdoc3 anise.astro --pdf > /home/$USER/Workspace/nyx-space/docs/docs/anise/reference/api/python/astro2.md`. Keep in mind that there are TWO `docs` folders here!
4. This will create a mostly ready Markdown, but you'll need to clean it up by removing all occurrence of ` {#id}` (search and replace with nothing) and then removing extra new lines with `sed`: `sed '/^$/N;/\n$/D' /home/$USER/Workspace/nyx-space/docs/docs/anise/reference/api/python/astro/index2.md > /home/$USER/Workspace/nyx-space/docs/docs/anise/reference/api/python/astro/index.md`. **Importantly**, you must specify a different output than input or the file will be empty.

A few manual edits are typically required. Check on the staging server first.