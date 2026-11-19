# Character set coverage

This document lists exactly which Unicode ranges were added to the
original Latin font. Numbers were counted from the two source fonts, minus
code points the Latin base font already covered.

It describes the **1.2.0 full** build, the most complete of the three.
Earlier builds are strict subsets:

| Build | Added | Glyphs | Code points | Excludes |
| --- | --- | --- | --- | --- |
| 1.0.0 cjk-only | 31,004 | 31,724 | 31,595 | all LGC, kana, Hangul, CJK extra symbols |
| 1.0.0-bold cjk-only-bold | 31,004 | 31,724 | 31,595 | same as 1.0.0 (weight variant only) |
| 1.1.0 multilingual | 33,177 | 33,897 | 33,768 | kana, Hangul, CJK extra symbols |
| 1.2.0 full | 46,372 | 47,092 | 46,963 | nothing from either source |

**1.0.0-bold has exactly the same cmap as 1.0.0**, glyph for glyph and code
point for code point; every range table below applies identically to both.
The only difference is the CJK outline source weight (Bold wght 700 instead
of Medium wght 500). See [../fonts/README.md](../fonts/README.md) for the
stem and ink-density measurements.

See [../fonts/README.md](../fonts/README.md) for the side-by-side
comparison.

## Totals

| Metric | Value |
| --- | --- |
| Code points added | 46,372 |
| Glyphs in the composite font | 47,092 |
| Addressable code points (best cmap) | 46,963 |
| Highest code point | U+3106C |
| Non-BMP code points via format 12 cmap | 2,619 |
| Original Latin code points retained | 628 |
| GSUB / GPOS features retained | 19 / 2 |

The format 12 subtable is built from the upstream Unicode BMP subtables
(591 code points) plus the 46,372 added code points, giving 46,963 entries.
The upstream font also has 37 code points that exist only in its Macintosh
(1,0,6) subtable; those are deliberately left in that subtable so Mac
applications keep resolving them to the original glyphs. All four original
subtables are preserved untouched.

The 2,619 non-BMP code points break down as 2,248 CJK Extensions B–F,
55 compatibility supplement, 3 CJK Extensions G–I, 57 Latin Extended-F,
31 Latin Extended-G, 167 Enclosed Alphanumeric Supplement (U+1F100–U+1F1FF)
and 58 Enclosed Ideographic Supplement (U+1F200–U+1F2FF).

### By group

| Group | Added | Source |
| --- | --- | --- |
| CJK Unified Ideographs, basic block | 20,971 | Noto Serif CJK SC Medium |
| CJK Extension A | 6,582 | Noto Serif CJK SC Medium |
| CJK Extensions B–I plus compatibility supplement | 2,306 | Noto Serif CJK SC Medium |
| CJK compatibility ideographs (BMP) | 366 | Noto Serif CJK SC Medium |
| CJK punctuation, radicals, bopomofo, strokes, forms | 779 | Noto Serif CJK SC Medium |
| Hangul Syllables | 11,172 | Noto Serif CJK SC Medium |
| Hangul Jamo, Compatibility Jamo, Ext-A, Ext-B | 451 | Noto Serif CJK SC Medium |
| Hiragana, Katakana, Katakana Phonetic Ext, Kanbun | 221 | Noto Serif CJK SC Medium |
| Enclosed CJK, squared compatibility, enclosed ideographs | 735 | Noto Serif CJK SC Medium |
| Enclosed alphanumerics, Roman numerals, box drawing | 312 | Noto Serif CJK SC Medium |
| Arrows, math, geometric, misc symbols, dingbats, small forms | 304 | Noto Serif CJK SC Medium |
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

These are not scripts themselves, but without them the six writing systems
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

## Kana ranges (1.2.0 only)

| Unicode range | Block | Added |
| --- | --- | --- |
| U+3040–U+309F | Hiragana | 93 |
| U+30A0–U+30FF | Katakana | 96 |
| U+31F0–U+31FF | Katakana Phonetic Extensions | 16 |
| U+3190–U+319F | Kanbun | 16 |

Halfwidth Katakana (U+FF61–U+FF9F, 63 code points) and the CJK
punctuation used in Japanese were already covered by the Halfwidth and
Fullwidth Forms / CJK Symbols and Punctuation rows of the 1.0.0 build.

## Hangul ranges (1.2.0 only)

| Unicode range | Block | Added |
| --- | --- | --- |
| U+AC00–U+D7A3 | Hangul Syllables | 11,172 |
| U+1100–U+11FF | Hangul Jamo | 256 |
| U+3130–U+318F | Hangul Compatibility Jamo | 94 |
| U+A960–U+A97F | Hangul Jamo Extended-A | 29 |
| U+D7B0–U+D7FF | Hangul Jamo Extended-B | 72 |

Hangul syllables are precomposed glyphs. Conjoining Jamo sequences are
present as individual characters but are not recombined into syllables by
any OpenType lookup; use a shaping engine or precomposed text.

## CJK symbol ranges (1.2.0 only)

These blocks are not scripts, but they appear constantly in Japanese and
Korean typography: circled and parenthesized labels, squared unit words,
box-drawing tables and enclosed ideographs.

| Unicode range | Block | Added |
| --- | --- | --- |
| U+3200–U+32FF | Enclosed CJK Letters and Months | 255 |
| U+3300–U+33FF | CJK Compatibility (squared units) | 255 |
| U+1F100–U+1F1FF | Enclosed Alphanumeric Supplement | 167 |
| U+1F200–U+1F2FF | Enclosed Ideographic Supplement | 58 |
| U+2460–U+24FF | Enclosed Alphanumerics | 160 |
| U+2500–U+257F | Box Drawing | 128 |
| U+2150–U+218F | Roman numerals (Number Forms) | 24 |
| U+2190–U+21FF | Arrows | 17 |
| U+2200–U+22FF | Mathematical Operators | 66 |
| U+2300–U+23FF | Miscellaneous Technical | 25 |
| U+25A0–U+25FF | Geometric Shapes and block elements | 37 |
| U+2600–U+26FF | Miscellaneous Symbols | 50 |
| U+2700–U+27BF | Dingbats | 38 |
| U+FE50–U+FE6F | Small Form Variants | 26 |
| U+20DD–U+20DE | Combining enclosing circle / square | 2 |

The remaining 43 code points are scattered single characters such as
U+2423 OPEN BOX and the U+2580–U+259F block elements.

## What is deliberately not included

The 1.2.0 build takes essentially everything the CJK source offers, but
this is still not a universal pan-Unicode font:

- **Colour emoji and pictographs** are not present. The U+1F200–U+1F2FF
  block contributes monochrome enclosed CJK ideographs, not emoji. Use a
  dedicated emoji font for pictographs.
- **Private Use Area** code points are not added.
- **Hangul composition and vertical kana positioning** are not implemented
  as OpenType features; see [BUILD.md](BUILD.md).
- **Other scripts** such as Arabic, Devanagari, Thai and Hebrew are out of
  scope, as are kana extensions beyond U+31FF that the Source Han Serif
  version used here does not contain.

The 1.0.0, 1.0.0-bold and 1.1.0 builds deliberately stop earlier; see the
table at the top of this document.

## cmap structure

| Subtable | Platform | Encoding | Format | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 (Unicode) | 3 | 4 | BMP, legacy and modern clients |
| 2 | 1 (Macintosh) | 0 | 6 | Mac Roman subset, retained from upstream |
| 3 | 3 (Windows) | 1 | 4 | BMP, primary Windows mapping |
| 4 | 3 (Windows) | 10 | 12 | Full Unicode, including non-BMP extensions |

The format 12 subtable is required for CJK Extensions B through I, Latin
Extended-F/G, and the U+1F100 / U+1F200 enclosed supplements: format 4
subtables cannot encode code points above U+FFFF. Most modern browsers and
applications prefer format 12 when it is present.

## Verifying coverage yourself

```bash
python3 - <<'PY'
from fontTools.ttLib import TTFont
f = TTFont("fonts/full/AnthropicSerifWebText-Full.ttf")
cm = f.getBestCmap()
for cp in (0x4E00, 0x9FFF, 0x3400, 0x2000B, 0x3002, 0xFF0C,
           0x0180, 0x03B1, 0x1F00, 0x0416, 0xA640, 0x20AC,
           0x3042, 0x30A2, 0x31F0, 0xAC00, 0xD7A3, 0x1100,
           0x3131, 0x320E, 0x337F, 0x2160, 0x1F200):
    print("U+%05X" % cp, cm.get(cp, "MISSING"))
print("total", len(cm), "glyphs", f["maxp"].numGlyphs)
PY
```
