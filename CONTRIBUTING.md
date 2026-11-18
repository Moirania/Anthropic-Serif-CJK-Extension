# Contributing

Thanks for taking the time to improve this project.

## Before you start

Read [docs/COMPLIANCE.md](docs/COMPLIANCE.md). The font files in `fonts/`
combine proprietary upstream Latin outlines with SIL OFL 1.1 CJK outlines,
so any contribution that adds or replaces glyph outlines must state where
the outlines came from and under which license they are available. Without
that information a pull request cannot be merged.

## Good first contributions

- Report a missing character with its Unicode code point, the rendering
  engine and a screenshot.
- Fix a typo, a broken relative link, or an unclear sentence in `docs/`.
- Improve `scripts/build_cjk.py`: better error handling, faster outline
  conversion, extra command line options.
- Add a specimen image for a script or a language not shown yet.
- Add a subsetting recipe to [docs/USAGE.md](docs/USAGE.md).

## Pull request process

1. Fork the repository and create a branch from `main`.
2. Keep the change focused. Rebuild the font only when the change actually
   affects outlines or metrics.
3. If you changed the build script, rebuild with
   `python3 scripts/build_cjk.py --help` documented parameters and verify
   the result with the checks in [docs/BUILD.md](docs/BUILD.md).
4. Confirm that the README and the docs still describe the real output:
   glyph count, code point count, file sizes.
5. Do not commit binary files other than the two files under `fonts/` and
   the specimen images under `assets/`. Do not commit credentials, local
   paths, or generated caches.
6. Open a pull request describing what changed and how you verified it.

## Reporting problems

Use the GitHub issue tracker and include:

- operating system and application, browser, or rendering engine version;
- the exact text or Unicode code points involved;
- what you expected and what you saw;
- a screenshot when the problem is visual.

## Code of conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
