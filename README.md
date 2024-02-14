# Documentation

## Locally

Run `tasker.sh` to set up the pipenv and run mkdocs, e.g. `tasker.sh serve`.

### Generating Python documentation

1. Navigate to the relevant folder where the Python bindings are installed, e.g. `/home/crabotin/Workspace/nyx-space/anise/anise-py`
2. Install `pdoc3` with pipx if not available yet: `pipx install pdoc3`
3. Run pdoc with the `--pdf` flag, which generates a markdown actually: `pdoc3 anise.astro --pdf > /home/crabotin/Workspace/nyx-space/docs/docs/anise/reference/api/python/astro2.md`. Keep in mind that there are TWO `docs` folders here!
4. This will create a mostly ready Markdown, but you'll need to clean it up by removing all occurance of ` {#id}` (search and replace with nothing) and then removing extra new lines with `sed`: `sed '/^$/N;/\n$/D' docs/anise/reference/api/python/astro/index.md > docs/anise/reference/api/python/astro/index2.md`. **Importantly**, you must specify a different output than input or the file will be empty.

A few manual edits are typically required. Check on the staging server first.