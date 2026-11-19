# Contributing

Thanks for taking the time to improve this project.

## Before you start

Read [docs/COMPLIANCE.md](docs/COMPLIANCE.md). The font files in `fonts/`
combine proprietary upstream Latin outlines with outlines from two SIL OFL
1.1 sources (Noto Serif CJK SC for Chinese, kana, Hangul and CJK symbols;
Noto Serif for Latin Extended, Greek and Cyrillic). Any contribution that
adds or replaces glyph outlines must state which source was used, which
instance weight, and under which license the outlines are available.
Without that information a pull request cannot be merged.

## Good first contributions

- Report a missing character with its Unicode code point, the rendering
  engine and a screenshot.
- Fix a typo, a broken relative link, or an unclear sentence in `docs/`.
- Improve `scripts/build_cjk.py`: better error handling, faster outline
  conversion, extra command line options.
- Add a specimen image or a reading sample for a language not shown yet
  (polytonic Greek, Old Church Slavonic, Vietnamese, IPA transcription,
  classical Japanese kana orthography, older Hangul orthography).
- Add a subsetting recipe to [docs/USAGE.md](docs/USAGE.md).
- Propose an additional Unicode range, with the source font and its license.
- Improve the kana or Hangul preview sheets under `assets/`; keep the
  print-specimen style (hard rules, crop marks, left alignment, no rounded
  corners, no glass, no gradient buttons).

## Pull request process

1. Fork the repository and create a branch from `main`.
2. Keep the change focused. Rebuild the font only when the change actually
   affects outlines or metrics.
3. If you changed the build script, rebuild with
   `python3 scripts/build_cjk.py --help` documented parameters and verify
   the result with the checks in [docs/BUILD.md](docs/BUILD.md).
4. Confirm that the README, `fonts/README.md` and the docs still describe
   the real output: glyph count, code point count, file sizes.
5. Do not commit binary files other than the six font files in the three
   `fonts/` subdirectories and the specimen images under `assets/`. Do not
   commit credentials, local paths, or generated caches.
6. **Never overwrite an existing build.** A new version goes into its own
   `fonts/` subdirectory with its own filenames, its own README row and
   its own GitHub Release. All three of 1.0.0, 1.1.0 and 1.2.0 must stay
   downloadable.
7. Open a pull request describing what changed and how you verified it.

## Reporting problems

Use the GitHub issue tracker and include:

- which build you used (`cjk-only` 1.0.0, `multilingual` 1.1.0 or
  `full` 1.2.0);
- operating system and application, browser, or rendering engine version;
- the exact text or Unicode code points involved;
- what you expected and what you saw;
- a screenshot when the problem is visual.

## Code of conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
