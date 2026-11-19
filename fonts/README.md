# Font files

Two independent builds live side by side. Neither overwrites the other.
Pick one; do not install both, because they share the same internal family
name and would conflict in the operating system font cache.

| Directory | Version | Glyphs | Code points | Files |
| --- | --- | --- | --- | --- |
| `cjk-only/` | 1.0.0 | 31,724 | 31,595 | `AnthropicSerifWebText-CJK-Only.ttf` (15.3 MB), `.woff2` (6.9 MB) |
| `multilingual/` | 1.1.0 | 33,897 | 33,768 | `AnthropicSerifWebText-Multilingual.ttf` (15.6 MB), `.woff2` (7.0 MB) |

## cjk-only (1.0.0)

The original release. Adds 31,004 CJK-related code points to the upstream
Latin font: CJK Unified Ideographs, Extension A, Extensions B through I,
compatibility ideographs, punctuation, bopomofo, radicals, strokes and
fullwidth forms. No Greek, no Cyrillic, no Latin Extended beyond what the
upstream font already had.

Use this when you only need Chinese and want the smaller file.

## multilingual (1.1.0)

The current release. Everything in 1.0.0 plus 2,173 further code points:
Latin Extended (IPA, phonetic, Ext-B through G), Greek including polytonic
Greek Extended, Cyrillic including Supplement and Ext-A/B/C, and the
combining marks, punctuation, currency and number forms needed to typeset
them.

Use this for mixed CJK / Greek / Cyrillic / Latin text. It is the version
documented in the root README and in `docs/`.

## Shared properties

Both builds keep the complete upstream Latin outlines, all 720 original
glyph ids, 19 GSUB features, 2 GPOS features, 2000 units per em, and the
original vertical metrics (ascender 1985, descender -515). Chinese glyphs
are full width 1em. Both are built from the same script; see
[../docs/BUILD.md](../docs/BUILD.md).

## Licensing

The upstream Latin outlines are proprietary. All added outlines are under
the SIL Open Font License 1.1. See [../LICENSE](../LICENSE) and
[../docs/COMPLIANCE.md](../docs/COMPLIANCE.md).

## Releases

Pre-built binaries are also attached to the GitHub Releases
`v1.0.0-cjk-only` and `v1.1.0-multilingual`, so either version can be
downloaded without checking out a historical commit.
