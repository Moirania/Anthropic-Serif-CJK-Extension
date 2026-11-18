# Building the font from source

Everything in `fonts/` can be regenerated. This document explains what the
script does, why each step is needed, and how to verify the result.

## Prerequisites

| Requirement | Version used | Notes |
| --- | --- | --- |
| Python | 3.10 | Any 3.8+ should work |
| fontTools | 4.65.0 | Provides `ttLib`, `Cu2QuPen`, `TTGlyphPen` |
| brotli | 1.2.1 | Only needed for WOFF2 output |
| Noto Serif CJK | 2.004 | `NotoSerifCJK-Medium.ttc`, SC face index 2 |
| Upstream Latin font | Anthropic Serif Web Text Regular | Supply your own legally obtained copy |

```bash
pip install fonttools brotli
```

On Debian or Ubuntu the CJK source can be installed with
`apt install fonts-noto-cjk` (package paths vary by distribution). The
script also accepts a single-face OTF if you extract the SC face from the
TTC first.

## Quick rebuild

```bash
python3 scripts/build_cjk.py \
  --latin /path/to/AnthropicSerifWebText.ttf \
  --cjk-ttc /path/to/NotoSerifCJK-Medium.ttc \
  --out ./AnthropicSerifWebText-CJK.ttf
```

Useful options:

| Option | Default | Meaning |
| --- | --- | --- |
| `--latin` | required | Path to the upstream Latin TTF |
| `--cjk-ttc` | required | Path to the Noto Serif CJK TTC |
| `--cjk-face` | 2 | Face index inside the TTC; 2 is Simplified Chinese |
| `--out` | required | Output TTF path |
| `--family-name` | keep upstream name | Replace internal family and PostScript names |
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
   vertical metrics. It asserts `unitsPerEm == 2000`.
2. **Selection.** Walk the source CJK cmap and keep only Chinese-related
   ranges (see [CHARACTER-SET.md](CHARACTER-SET.md)), excluding code points
   the Latin font already maps.
3. **Outline conversion.** The CJK source is a CFF font with cubic
   charstrings. `Cu2QuPen` converts each charstring to quadratic curves
   (`max_err=0.5`, `reverse_direction=True`) while a `TransformPen` scales
   coordinates by 2 to reach 2000 UPM. The result is a `glyf` glyph.
4. **Metrics.** Chinese advances are set to full-width 2000 units. Latin
   advances and side bearings are untouched. Baseline, ascender and
   descender stay exactly as they were.
5. **Append only.** New glyphs are appended after the original 720 glyphs.
   This is the critical detail: every existing glyph id stays valid, so
   all `GSUB` and `GPOS` lookups (ligatures, kerning, mark positioning)
   keep working without being rewritten.
6. **cmap.** BMP characters are added to the existing format 4 subtables,
   and a new (3,10) format 12 subtable carries the complete mapping so
   non-BMP Extensions B through I resolve correctly.
7. **Metadata.** `maxp`, `hhea`, `head` bounding box, `OS/2` Unicode range
   fields and the `name` table are updated. The Adobe copyright line and
   the SIL OFL 1.1 reference are written into nameIDs 0, 5, 13 and 14.

## Choosing a different CJK weight

The default is Medium because the upstream Latin is a Text optical size
with a fairly heavy vertical stem. At 2000 UPM the Latin `H` stem measures
about 227 units; Noto Serif CJK Regular at 1000 UPM measures about 68
units (136 after scaling), while Medium measures about 85 (170 after
scaling) and SemiBold about 104 (208 after scaling). Medium is the closest
visual match. To compare other weights, point `--cjk-ttc` at
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
print("U+4E00:", cm.get(0x4E00), "| U+2000B:", cm.get(0x2000B))
print("unique glyph names:", len(set(f.getGlyphOrder())) == len(f.getGlyphOrder()))
PY
```

Expected: 31,724 glyphs, 19 GSUB features, 2 GPOS features, four cmap
subtables including a format 12 table, and 31,724 unique glyph names.
Render a mixed string such as `Typography 排版设计，世界。fi 123` and
confirm that `fi` still forms a ligature and no tofu boxes appear.

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

- CFF to TrueType conversion drops native CFF hinting; very small screen
  sizes may look slightly softer.
- The CJK outlines are matched by weight and metrics, not redrawn to
  imitate the Latin letterforms stroke for stroke.
- The full font is large. Subset for the web; see [USAGE.md](USAGE.md).
