# Character set coverage

This document lists exactly which Unicode ranges were added to the
original Latin font. Numbers were counted from the source cmap of Noto
Serif CJK SC Medium, minus code points the Latin font already covered.

## Totals

| Metric | Value |
| --- | --- |
| CJK code points added | 31,004 |
| Glyphs in the composite font | 31,724 |
| Addressable code points (best cmap) | 31,595 |
| Highest code point | U+3106C |
| Non-BMP code points via format 12 cmap | 2,306 |
| Original Latin code points retained | 628 |

The difference between added code points (31,004) and addressable code
points (31,595) comes from the original Latin coverage and from a small
number of shared compatibility mappings.

## Breakdown by Unicode range

| Unicode range | Block | Added |
| --- | --- | --- |
| U+2E80–U+2FDF | CJK Radicals Supplement, Kangxi Radicals | 329 |
| U+2FF0–U+2FFF | Ideographic Description Characters | 12 |
| U+3000–U+303F | CJK Symbols and Punctuation | 64 |
| U+3100–U+312F | Bopomofo | 43 |
| U+31A0–U+31BF | Bopomofo Extended | 28 |
| U+31C0–U+31EF | CJK Strokes | 36 |
| U+3400–U+4DBF | CJK Unified Ideographs Extension A | 6,582 |
| U+4E00–U+9FFF | CJK Unified Ideographs (basic block) | 20,971 |
| U+F900–U+FAFF | CJK Compatibility Ideographs | 366 |
| U+FE10–U+FE1F | Vertical Forms | 10 |
| U+FE30–U+FE4F | CJK Compatibility Forms | 32 |
| U+FF00–U+FFEF | Halfwidth and Fullwidth Forms | 225 |
| U+20000–U+2EBEF | CJK Unified Ideographs Extensions B–F | 2,248 |
| U+2F800–U+2FA1F | CJK Compatibility Ideographs Supplement | 55 |
| U+30000–U+323AF | CJK Unified Ideographs Extensions G–I | 3 |

Grouped view:

| Group | Added |
| --- | --- |
| CJK Unified Ideographs, basic block | 20,971 |
| Extension A | 6,582 |
| Extensions B through I plus compatibility supplement | 2,306 |
| Compatibility ideographs (BMP) | 366 |
| Punctuation, radicals, bopomofo, strokes, forms, fullwidth | 779 |

## What is deliberately not included

The source font also contains kana, Hangul, Cyrillic, Greek and a large
set of Latin extended characters. Those are **not** added by this project,
because the goal is a Chinese extension of an existing Latin typeface, not
a universal pan-CJK font. Adding them would also make the file larger and
would risk clashing with the Latin design.

## cmap structure

| Subtable | Platform | Encoding | Format | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 (Unicode) | 3 | 4 | BMP, legacy and modern clients |
| 2 | 1 (Macintosh) | 0 | 6 | Mac Roman subset, retained from upstream |
| 3 | 3 (Windows) | 1 | 4 | BMP, primary Windows mapping |
| 4 | 3 (Windows) | 10 | 12 | Full Unicode, including non-BMP extensions |

The format 12 subtable is required for Extensions B through I: format 4
subtables cannot encode code points above U+FFFF. Most modern browsers
and applications prefer format 12 when it is present.

## Verifying coverage yourself

```bash
python3 - <<'PY'
from fontTools.ttLib import TTFont
f = TTFont("fonts/AnthropicSerifWebText-CJK.ttf")
cm = f.getBestCmap()
for cp in (0x4E00, 0x9FFF, 0x3400, 0x2000B, 0x3002, 0xFF0C, 0x3105):
    print("U+%05X" % cp, cm.get(cp, "MISSING"))
print("total", len(cm), "glyphs", f["maxp"].numGlyphs)
PY
```
