# Building the font from source

Everything in `fonts/` can be regenerated with one command. This document
explains what the script does, why each step is needed, and how to verify
the result.

## Prerequisites

| Requirement | Version used | Notes |
| --- | --- | --- |
| Python | 3.10 | Any 3.8+ should work |
| fontTools | 4.65.0 | `ttLib`, `Cu2QuPen`, `varLib.instancer`, `DecomposingRecordingPen` |
| brotli | 1.2.1 | Only needed for WOFF2 output |
| Noto Serif CJK | 2.004 | `NotoSerifCJK-Medium.ttc`, SC face index 2 |
| Noto Serif | 2025.04 | `NotoSerif[wdth,wght].ttf`, variable font |
| Upstream Latin font | Anthropic Serif Web Text Regular | Supply your own legally obtained copy |

```bash
pip install fonttools brotli
```

On Debian or Ubuntu the CJK source can be installed with
`apt install fonts-noto-cjk`. The Noto Serif variable font ships with
`fonts-noto` packages or can be obtained from the
[notofonts/latin-greek-cyrillic](https://github.com/notofonts/latin-greek-cyrillic)
repository. Both are under the SIL Open Font License 1.1.

## Full rebuild

```bash
python3 scripts/build_cjk.py \
  --latin /path/to/AnthropicSerifWebText.ttf \
  --cjk-ttc /path/to/NotoSerifCJK-Medium.ttc \
  --lgc-font "/path/to/NotoSerif[wdth,wght].ttf" \
  --lgc-weight 500 \
  --out ./AnthropicSerifWebText-CJK.ttf
```

Useful options:

| Option | Default | Meaning |
| --- | --- | --- |
| `--latin` | required | Path to the upstream Latin TTF |
| `--cjk-ttc` | optional | Noto Serif CJK TTC or single-face OTF |
| `--cjk-face` | 2 | Face index inside the TTC; 2 is Simplified Chinese |
| `--lgc-font` | optional | Noto Serif variable font for Latin/Greek/Cyrillic |
| `--lgc-weight` | 500 | Instance `wght` value; `wdth` stays at its default |
| `--out` | required | Output TTF path |
| `--max-err` | 0.5 | cu2qu maximum error in source units |
| `--family-name` | keep upstream name | Replace internal family and PostScript names |
| `--no-cjk` | off | Skip the CJK source |
| `--no-lgc` | off | Skip the LGC source (CJK-only build) |
| `--limit` | 0 | Convert only a small sample, for debugging |

A `WOFF2` can then be produced with:

```bash
python3 - <<'PY'
from fontTools.ttLib import TTFont
f = TTFont("AnthropicSerifWebText-CJK.ttf")
f.flavor = "woff2"
f.save("AnthropicSerifWebText-CJK.woff2")
PY
```

## What the script does

1. **Baseline.** Load the Latin font and record its glyph order, cmap and
   vertical metrics. It reads `unitsPerEm == 2000` and never alters
   `hhea`, `OS/2` typographic metrics or the cap/x heights.
2. **CJK selection.** Walk the CJK source cmap and keep only Chinese-related
   ranges (see [CHARACTER-SET.md](CHARACTER-SET.md)), excluding code points
   already mapped by the Latin base.
3. **CJK outline conversion.** The CJK source is a CFF font with cubic
   charstrings. `Cu2QuPen` converts each to quadratic curves
   (`max_err=0.5`, `reverse_direction=True`) while a `TransformPen` scales
   coordinates by 2 to reach 2000 UPM. The result is a `glyf` glyph.
4. **LGC instance.** The Latin/Greek/Cyrillic source is a variable TrueType
   font. `instantiateVariableFont` pins `wght=500` and the default `wdth`,
   producing a static instance whose `hmtx` advances already include the
   `HVAR` deltas.
5. **LGC outline conversion.** `DecomposingRecordingPen` expands composite
   glyphs into plain contours, then a `TransformPen` scales every coordinate
   by 2 and `TTGlyphPen` rebuilds the glyph. Decomposing is essential: a
   composite copied without its component glyphs would render as a blank
   box. Expanding also removes the dependency on source glyph names, so
   CJK `uniXXXX` names and LGC `lgcXXXX` names never collide.
6. **Metrics.** Chinese advances are set to full-width 2000 units. Latin,
   Greek and Cyrillic advances are taken from the instanced source and
   scaled by 2. The original Latin advances, side bearings, baseline,
   ascender and descender are untouched.
7. **Append only.** New glyphs are appended after the original 720 glyphs.
   This is the critical detail: every existing glyph id stays valid, so all
   `GSUB` and `GPOS` lookups (ligatures, kerning, mark positioning) keep
   working without being rewritten.
8. **cmap.** BMP characters are added to the existing format 4 subtables,
   and a new (3,10) format 12 subtable carries the complete mapping so
   non-BMP CJK Extensions B–I and Latin Extended-F/G resolve correctly.
   The Macintosh (1,0,6) subtable is left untouched; see
   [CHARACTER-SET.md](CHARACTER-SET.md) for the 37 code points that live
   only there.
9. **Metadata.** `maxp`, `hhea`, `head` bounding box, `OS/2` Unicode range
   fields and the `name` table are updated. The Adobe, Noto Project and
   project-maintainer copyright lines plus the SIL OFL 1.1 reference are
   written into nameIDs 0, 5, 13 and 14.

## Choosing the weight

The default is `wght=500` for both sources. The upstream Latin is a Text
optical size with a fairly heavy vertical stem. At 2000 UPM the Latin `H`
stem measures about 227 units; Noto Serif CJK Regular at 1000 UPM measures
about 68 units (136 after scaling), Medium about 85 (170 after scaling),
and SemiBold about 104 (208 after scaling). Medium is the closest visual
match, and pinning the Noto Serif variable font to the same 500 keeps the
Greek and Cyrillic stems consistent with the Chinese. To compare, change
`--lgc-weight` or point `--cjk-ttc` at
`NotoSerifCJK-Light.ttc`, `NotoSerifCJK-Bold.ttc` and so on.

## Verification checklist

```bash
python3 - <<'PY'
from fontTools.ttLib import TTFont
f = TTFont("AnthropicSerifWebText-CJK.ttf")
print("tables:", sorted(f.keys()))
print("numGlyphs:", f["maxp"].numGlyphs)
print("GSUB features:", len(f["GSUB"].table.FeatureList.FeatureRecord))
print("GPOS features:", len(f["GPOS"].table.FeatureList.FeatureRecord))
print("cmap:", [(t.platformID, t.platEncID, t.format, len(t.cmap))
                for t in f["cmap"].tables])
cm = f.getBestCmap()
for cp in (0x4E00, 0x2000B, 0x0180, 0x03B1, 0x1F00, 0x0416, 0xA640):
    print("U+%05X" % cp, cm.get(cp, "MISSING"))
print("unique glyph names:", len(set(f.getGlyphOrder())) == len(f.getGlyphOrder()))
PY
```

Expected: 33,897 glyphs, 19 GSUB features, 2 GPOS features, four cmap
subtables including a format 12 table with 33,768 entries, and 33,897
unique glyph names. Render a mixed string such as
`Typography 排版设计 Ελληνικά Кириллица ﬁ 123` and confirm that `fi`
still forms a ligature and no tofu boxes appear.

## Renaming the internal family name

The shipped files keep the upstream family name so that they can replace
the original font in an existing document. For a more conservative
redistribution, rename the internal names before publishing:

```python
from fontTools.ttLib import TTFont

f = TTFont("AnthropicSerifWebText-CJK.ttf")
n = f["name"]
for nid, value in (
    (1, "Serif CJK Extension"),
    (4, "Serif CJK Extension Regular"),
    (6, "SerifCJKExtension-Regular"),
    (16, "Serif CJK Extension"),
    (17, "Regular"),
):
    for rec in list(n.names):
        if rec.nameID == nid:
            n.names.remove(rec)
    n.setName(value, nid, 3, 1, 0x409)
    n.setName(value, nid, 1, 0, 0)
f.save("SerifCJKExtension-Regular.ttf")
```

Or pass `--family-name "Serif CJK Extension"` to the build script, which
applies the same change while generating the font. Renaming also helps
avoid any Reserved Font Name or trademark conflict; see
[COMPLIANCE.md](COMPLIANCE.md).

## Known trade-offs

- CFF to TrueType conversion drops native CFF hinting; decomposing LGC
  composites drops their hinting instructions too. Very small screen sizes
  may look slightly softer.
- Greek, Cyrillic and Latin Extended outlines come from Noto Serif, while
  Chinese comes from Source Han Serif. They share the Noto/Source serif
  design language and the same wght=500, but they are not redrawn stroke by
  stroke to imitate the Anthropic Latin letterforms.
- The original GSUB/GPOS lookups cover Latin only. Greek and Cyrillic get
  correct glyphs and advances but do not inherit Latin kerning pairs or
  language-specific substitutions.
- The full font is large. Subset for the web; see [USAGE.md](USAGE.md).
