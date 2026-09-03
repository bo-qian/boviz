# Changelog

## 0.3.4 — 2026-09-03

### Added

- Phased automatic curve markers, configurable spacing, and marker groups
  independent of color groups, including dual-axis CSV plots.
- Regression tests for marker helpers, public plotting APIs, exports, and
  positional argument compatibility; isolated headless test output.
- Linux/Windows test matrix for Python 3.10–3.13 and package/documentation builds.
- Test, documentation, and development dependency extras.

### Fixed

- Preserve the positional order of existing plotting parameters by appending
  new marker/line-style options after them.
- Apply dual-axis line-style options even when markers are disabled.
- Make local tests import repository source rather than an older installed copy.
- Centralize packaging metadata and correct the Python requirement to >=3.10
  (the source already used Python 3.10 syntax).
- Remove pytest and standard-library backports from runtime dependencies.
- Require successful tests before publishing tags to PyPI.
- Correct README coverage claims and replace the placeholder documentation home.

### Limitations

- Automatic marker placement approximates linear display coordinates and uses
  existing samples. Logarithmic axes, sparse sampling, and complex curves may
  require explicit marker settings.
- The tests are targeted regressions, not full coverage of all plotting APIs.

## 0.3.3 — 2026-01-18

- Updated project README descriptions and examples.
- See the [historical releases](https://github.com/bo-qian/boviz/releases)
  for earlier versions.
