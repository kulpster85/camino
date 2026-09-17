# Converting a notebook to Markdown for the docs site

This project expects docs content to be written as Markdown files in the docs tree, even when the source material starts as a notebook.

## Recommended workflow

1. Open the notebook you want to convert.
2. In VS Code, use the notebook export flow or a local Jupyter conversion command to export it to Markdown.
3. Save the output into a docs page such as `docs/examples/` or another relevant section.
4. Check the generated Markdown for any broken relative links, image paths, or code fences.
5. Update `mkdocs.yml` if you want the page to appear in the nav.

## Command line example

From the repo root, run:

```bash
jupyter nbconvert --to markdown --output-dir docs/examples path/to/notebook.ipynb
```

This will create a `.md` file alongside the notebook output in `docs/examples/`.

## Notes for Shrish

- Prefer writing a short, polished narrative page rather than dumping the raw notebook cells as-is.
- Keep headings concise and explain the workflow in plain language.
- Move any large code blocks into a stable documentation section if they are central to the example.
- If the notebook includes images, ensure they are copied into the docs tree or referenced via stable relative paths.
- After conversion, review the final Markdown and keep the structure consistent with the rest of the docs site.

## Typical final file pattern

For example:

```text
docs/
  examples/
    worked_example.md
```

The Markdown page can then be linked from the docs navigation in `mkdocs.yml`.
