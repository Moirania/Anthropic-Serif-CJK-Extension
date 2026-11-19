# Character set coverage

This document lists exactly which Unicode ranges were added to the
original Latin font. Numbers were counted from the two source fonts, minus
code points the Latin base font already covered.

It describes **1.1.0 multilingual**. The **1.0.0 cjk-only** build contains
only the CJK rows below: 31,004 added code points, 31,724 glyphs, 31,595
addressable code points, and 2,306 non-BMP code points. It has no Greek,
no Cyrillic, no Latin Extended beyond the upstream font's own Latin-1 and
Latin Extended-A, and no shared LGC marks. See
[../fonts/README.md](../fonts/README.md) for the side-by-side comparison.

## Totals

| Metric | Value |
| --- | --- |
| Code points added | 33,177 |
| Glyphs in the composite font | 33,897 |
| Addressable code points (best cmap) | 33,768 |
| Highest code point | U+3106C |
| Non-BMP code points via format 12 cmap | 2,394 |
| Original Latin code points retained | 628 |
| GSUB / GPOS features retained | 19 / 2 |

The format 12 subtable is built from the upstream Unicode BMP subtables
(591 code points) plus the 33,177 added code points, giving 33,768 entries.
The upstream font also has 37 code points that exist only in its Macintosh
(1,0,6) subtable; those are deliberately left in that subtable so Mac
applications keep resolving them to the original glyphs. All four original
subtables are preserved untouched.

The 2,394 non-BMP code points break down as 2,248 CJK Extensions B–F,
55 compatibility supplement, 3 CJK Extensions G–I, 57 Latin Extended-F
and 31 Latin Extended-G.

### By group

| Group | Added | Source |
| --- | --- | --- |
| CJK Unified Ideographs, basic block | 20,971 | Noto Serif CJK SC Medium |
| CJK Extension A | 6,582 | Noto Serif CJK SC Medium |
| CJK Extensions B–I plus compatibility supplement | 2,306 | Noto Serif CJK SC Medium |
| CJK compatibility ideographs (BMP) | 366 | Noto Serif CJK SC Medium |
| CJK punctuation, radicals, bopomofo, strokes, forms | 779 | Noto Serif CJK SC Medium |
| Latin Extended (including IPA and phonetic) | 1,018 | Noto Serif wght=500 |
| Greek (including Greek Extended) | 354 | Noto Serif wght=500 |
| Cyrillic (including Ext-A/B/C) | 441 | Noto Serif wght=500 |
| Shared marks, punctuation, currency, number forms | 360 | Noto Serif wght=500 |

## CJK ranges

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

## Latin Extended ranges

| Unicode range | Block | Added |
| --- | --- | --- |
| U+0080–U+00FF | Latin-1 Supplement | 1 |
| U+0100–U+017F | Latin Extended-A | 0 |
| U+0180–U+024F | Latin Extended-B | 176 |
| U+0250–U+02AF | IPA Extensions | 94 |
| U+1D00–U+1D7F | Phonetic Extensions | 114 |
| U+1D80–U+1DBF | Phonetic Extensions Supplement | 61 |
| U+1E00–U+1EFF | Latin Extended Additional | 199 |
| U+2C60–U+2C7F | Latin Extended-C | 32 |
| U+A720–U+A7FF | Latin Extended-D | 193 |
| U+AB30–U+AB6F | Latin Extended-E | 60 |
| U+10780–U+107BF | Latin Extended-F | 57 |
| U+1DF00–U+1DFFF | Latin Extended-G | 31 |

Latin-1 Supplement and Latin Extended-A show 0 or 1 added code point
because the upstream font already ships both blocks almost in full. Their
glyphs are the original Anthropic outlines, not Noto Serif outlines.

## Greek ranges

| Unicode range | Block | Added |
| --- | --- | --- |
| U+0370–U+03FF | Greek and Coptic | 121 |
| U+1F00–U+1FFF | Greek Extended | 233 |

Greek Extended covers polytonic Greek: breathings, accents, iota subscript
and their combinations, needed for classical and liturgical texts.

## Cyrillic ranges

| Unicode range | Block | Added |
| --- | --- | --- |
| U+0400–U+04FF | Cyrillic | 256 |
| U+0500–U+052F | Cyrillic Supplement | 48 |
| U+2DE0–U+2DFF | Cyrillic Extended-A | 32 |
| U+A640–U+A69F | Cyrillic Extended-B | 96 |
| U+1C80–U+1C8F | Cyrillic Extended-C | 9 |

## Shared supporting ranges

These are not scripts themselves, but without them the four writing systems
cannot be typeset properly: accented letters need combining marks,
polytonic Greek needs spacing modifiers, and multilingual text needs matching
punctuation and symbols.

| Unicode range | Block | Added |
| --- | --- | --- |
| U+02B0–U+02FF | Spacing Modifier Letters | 61 |
| U+0300–U+036F | Combining Diacritical Marks | 92 |
| U+2000–U+206F | General Punctuation | 77 |
| U+2070–U+209F | Superscripts and Subscripts | 13 |
| U+20A0–U+20CF | Currency Symbols | 32 |
| U+2100–U+214F | Letterlike Symbols | 79 |
| U+2150–U+218F | Number Forms | 6 |

## What is deliberately not included

The CJK source also contains kana, Hangul and a large set of general
symbols. The LGC source contains arrows, mathematical operators and
geometric shapes. Neither is added here. The goal is a focused extension of
an existing Latin typeface to CJK, Greek and Cyrillic, not a universal
pan-Unicode font. Adding everything would enlarge the file substantially
and would clash with the Latin design. Emoji, in particular, should always
come from a dedicated emoji font.

## cmap structure

| Subtable | Platform | Encoding | Format | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 (Unicode) | 3 | 4 | BMP, legacy and modern clients |
| 2 | 1 (Macintosh) | 0 | 6 | Mac Roman subset, retained from upstream |
| 3 | 3 (Windows) | 1 | 4 | BMP, primary Windows mapping |
| 4 | 3 (Windows) | 10 | 12 | Full Unicode, including non-BMP extensions |

The format 12 subtable is required for CJK Extensions B through I and for
Latin Extended-F/G: format 4 subtables cannot encode code points above
U+FFFF. Most modern browsers and applications prefer format 12 when it is
present.

## Verifying coverage yourself

```bash
python3 - <<'PY'
from fontTools.ttLib import TTFont
f = TTFont("fonts/multilingual/AnthropicSerifWebText-Multilingual.ttf")
cm = f.getBestCmap()
for cp in (0x4E00, 0x9FFF, 0x3400, 0x2000B, 0x3002, 0xFF0C,
           0x0180, 0x03B1, 0x1F00, 0x0416, 0xA640, 0x20AC):
    print("U+%05X" % cp, cm.get(cp, "MISSING"))
print("total", len(cm), "glyphs", f["maxp"].numGlyphs)
PY
```
