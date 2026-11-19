# Font files

Three independent builds live side by side. None overwrites another.
Pick one; do not install two at once, because they share the same internal
family name and would conflict in the operating system font cache.

| Directory | Version | Glyphs | Code points | Files |
| --- | --- | --- | --- | --- |
| `cjk-only/` | 1.0.0 | 31,724 | 31,595 | `AnthropicSerifWebText-CJK-Only.ttf` (15.3 MB), `.woff2` (6.9 MB) |
| `multilingual/` | 1.1.0 | 33,897 | 33,768 | `AnthropicSerifWebText-Multilingual.ttf` (15.6 MB), `.woff2` (7.0 MB) |
| `full/` | 1.2.0 | 47,092 | 46,963 | `AnthropicSerifWebText-Full.ttf` (23.6 MB), `.woff2` (8.4 MB) |

## cjk-only (1.0.0)

The original release. Adds 31,004 CJK-related code points to the upstream
Latin font: CJK Unified Ideographs, Extension A, Extensions B through I,
compatibility ideographs, punctuation, bopomofo, radicals, strokes and
fullwidth forms. No kana, no Hangul, no Greek, no Cyrillic, no Latin
Extended beyond what the upstream font already had.

Use this when you only need Chinese and want the smallest file.

## multilingual (1.1.0)

Everything in 1.0.0 plus 2,173 further code points: Latin Extended (IPA,
phonetic, Ext-B through G), Greek including polytonic Greek Extended,
Cyrillic including Supplement and Ext-A/B/C, and the combining marks,
punctuation, currency and number forms needed to typeset them.

Use this for mixed CJK / Greek / Cyrillic / Latin text without Japanese or
Korean.

## full (1.2.0)

The complete build. Everything in 1.1.0 plus **13,195 further code
points** taken from the remaining character set of Noto Serif CJK SC
Medium:

| Group | Added |
| --- | --- |
| Hangul Syllables U+AC00–U+D7A3 | 11,172 |
| Hangul Jamo, Compatibility Jamo, Ext-A, Ext-B | 451 |
| Hiragana, Katakana, Katakana Phonetic Ext, Kanbun | 221 |
| Enclosed CJK, squared CJK compatibility, enclosed ideographs | 735 |
| Enclosed alphanumerics, Roman numerals, box drawing | 312 |
| Arrows, math, geometric, misc symbols, dingbats, small forms | 304 |

Japanese and Korean specimens for this build are in
[`../assets/kana-preview.png`](../assets/kana-preview.png) and
[`../assets/hangul-preview.png`](../assets/hangul-preview.png).

Use this when you need Japanese kana, Korean Hangul, or CJK enclosed and
squared symbols. It is the largest build; subsetting for the web is
strongly recommended. See [../docs/USAGE.md](../docs/USAGE.md).

## Shared properties

All three builds keep the complete upstream Latin outlines, all 720
original glyph ids, 19 GSUB features, 2 GPOS features, 2000 units per em,
and the original vertical metrics (ascender 1985, descender -515). Chinese
and kana glyphs are full width 1em; Hangul syllables are proportional at
1932 units. All three are built from the same script; see
[../docs/BUILD.md](../docs/BUILD.md).

## Licensing

The upstream Latin outlines are proprietary. All added outlines are under
the SIL Open Font License 1.1. See [../LICENSE](../LICENSE) and
[../docs/COMPLIANCE.md](../docs/COMPLIANCE.md).

## Releases

Pre-built binaries are also attached to the GitHub Releases
`v1.0.0-cjk-only`, `v1.1.0-multilingual` and `v1.2.0-full`, so any version
can be downloaded without checking out a historical commit.
