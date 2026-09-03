# Contributing to boviz

Bug reports, reproducible scientific plotting examples, documentation improvements,
and pull requests are welcome. Do not include confidential research data; use a
small synthetic dataset that reproduces the issue.

## Development

Use Python 3.10 or newer in a virtual environment:

```sh
python -m pip install -e ".[dev,docs]"
python -m pytest
python -m build
python -m twine check dist/*
python -m sphinx -b html docs/source docs/_build/html
```

Tests use the Agg backend and temporary output directories. Add a regression
test for bug fixes and new behavior. Preserve existing parameter order and
defaults; pass new options by keyword. Update both READMEs for public API changes.
Do not commit generated `_version.py`, build artifacts, or private datasets.

## Pull requests

Explain the scientific use case, expected behavior, and validation performed.
Include a small example for visual changes. Keep unrelated formatting or
refactors separate. A maintainer reviews and merges changes; CI passing alone
does not demonstrate scientific correctness.

## Release checklist (maintainers)

1. Update CHANGELOG.md and verify the documentation and examples.
2. Run local tests and packaging checks, then push the reviewed commit.
3. Wait for every Tests job to pass on that exact commit.
4. Create a new `vX.Y.Z` tag on it and push the tag. Never move a published tag.
5. The publishing workflow reruns tests before PyPI Trusted Publishing.
6. Verify the PyPI version, install the wheel in a clean environment, and create
   a GitHub Release with the corresponding changelog section.
7. Verify the hosted documentation build.

## Near-term priorities

- Broaden regression coverage for residuals, heatmaps, histograms, and CLI output.
- Improve marker placement on logarithmic axes and discontinuous/sparse curves.
- Add small reproducible examples for simulation post-processing workflows.
