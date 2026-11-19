# Font files

Four independent builds live side by side. None overwrites another.
Pick one; do not install two at once, because they share the same internal
family name and would conflict in the operating system font cache.

| Directory | Version | Glyphs | Code points | Files |
| --- | --- | --- | --- | --- |
| `cjk-only/` | 1.0.0 | 31,724 | 31,595 | `AnthropicSerifWebText-CJK-Only.ttf` (15.3 MB), `.woff2` (6.9 MB) |
| `cjk-only-bold/` | 1.0.0-bold | 31,724 | 31,595 | `AnthropicSerifWebText-CJK-Only-Bold.ttf` (15.3 MB), `.woff2` (7.2 MB) |
| `multilingual/` | 1.1.0 | 33,897 | 33,768 | `AnthropicSerifWebText-Multilingual.ttf` (15.6 MB), `.woff2` (7.0 MB) |
| `full/` | 1.2.0 | 47,092 | 46,963 | `AnthropicSerifWebText-Full.ttf` (23.6 MB), `.woff2` (8.4 MB) |

## cjk-only (1.0.0)

The original release. Adds 31,004 CJK-related code points to the upstream
Latin font: CJK Unified Ideographs, Extension A, Extensions B through I,
compatibility ideographs, punctuation, bopomofo, radicals, strokes and
fullwidth forms. Chinese outlines come from Noto Serif CJK SC **Medium**
(wght 500). No kana, no Hangul, no Greek, no Cyrillic, no Latin Extended
beyond what the upstream font already had.

Use this when you only need Chinese and want the smallest file.

## cjk-only-bold (1.0.0-bold)

**Same coverage, heavier Chinese.** This build exists because the Medium
Chinese in 1.0.0 can look thin and pale next to the upstream Latin. It has
the **exact same 31,595 code points, 31,724 glyphs, 2000 UPM advances,
720 Latin outlines and 19 GSUB / 2 GPOS features** as 1.0.0. The only
difference is the CJK source weight: Noto Serif CJK SC **Bold** (wght 700)
instead of Medium.

Measured on the same paragraph at the same size:

| | 1.0.0 Medium | 1.0.0-bold Bold |
| --- | --- | --- |
| Ink pixels | 21,178 | 28,082 (+32.6%) |
| `中` stem width | 54.5 px | 70.7 px |
| Western `H` stem | 61.4 px | 61.4 px (unchanged) |

The Latin stem is 61.4 px. Medium Chinese at 54.5 px is about 11% lighter,
SemiBold at 60.7 px would be an almost exact optical match, and Bold at
70.7 px is deliberately about 15% heavier than the Latin. Bold was chosen
because the brief was to fix Chinese that looked thin and pale, not merely
to equalise stems. If you want the tighter match instead, rebuild with
`--cjk-ttc NotoSerifCJK-SemiBold.ttc`; see
[../docs/BUILD.md](../docs/BUILD.md#choosing-the-weight).

The side-by-side sheet is
[`../assets/cjk-weight-comparison.png`](../assets/cjk-weight-comparison.png).

Note that `OS/2.usWeightClass` and `name` ID 2 still read **Regular** in
this build. The Western outlines are Regular and the family is unchanged,
so this is a Regular font with heavier Chinese, not a synthetic bold face.
Do not install it together with `cjk-only/`; the two have identical family
and subfamily names.

## multilingual (1.1.0)

Everything in 1.0.0 plus 2,173 further code points: Latin Extended (IPA,
phonetic, Ext-B through G), Greek including polytonic Greek Extended,
Cyrillic including Supplement and Ext-A/B/C, and the combining marks,
punctuation, currency and number forms needed to typeset them. Chinese
outlines remain Medium (wght 500).

Use this for mixed CJK / Greek / Cyrillic / Latin text without Japanese or
Korean.

## full (1.2.0)

The complete build. Everything in 1.1.0 plus **13,195 further code
points** taken from the remaining character set of Noto Serif CJK SC
Medium: Hangul Syllables (11,172), Jamo (451), kana (221), enclosed CJK
and squared compatibility forms (735), enclosed alphanumerics and box
drawing (312), and assorted arrows, math and misc symbols (304).

Japanese and Korean specimens for this build are in
[`../assets/kana-preview.png`](../assets/kana-preview.png) and
[`../assets/hangul-preview.png`](../assets/hangul-preview.png).

Use this when you need Japanese kana, Korean Hangul, or CJK enclosed and
squared symbols. It is the largest build; subsetting for the web is
strongly recommended. See [../docs/USAGE.md](../docs/USAGE.md).

## Shared properties

All four builds keep the complete upstream Latin outlines, all 720
original glyph ids, 19 GSUB features, 2 GPOS features, 2000 units per em,
and the original vertical metrics (ascender 1985, descender -515). Chinese
and kana glyphs are full width 1em; Hangul syllables are proportional at
1932 units. All four are built from the same script; see
[../docs/BUILD.md](../docs/BUILD.md).

## Licensing

The upstream Latin outlines are proprietary. All added outlines are under
the SIL Open Font License 1.1. See [../LICENSE](../LICENSE) and
[../docs/COMPLIANCE.md](../docs/COMPLIANCE.md).

## Releases

Pre-built binaries are also attached to the GitHub Releases
`v1.0.0-cjk-only`, `v1.0.0-cjk-bold`, `v1.1.0-multilingual` and
`v1.2.0-full`, so any version can be downloaded without checking out a
historical commit.
