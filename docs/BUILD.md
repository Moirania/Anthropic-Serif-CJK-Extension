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

The same script produces all four independent builds. Run it with
different output paths; no run touches another build's files.

```bash
# 1.0.0 cjk-only (skip the LGC source)
python3 scripts/build_cjk.py \
  --latin /path/to/AnthropicSerifWebText.ttf \
  --cjk-ttc /path/to/NotoSerifCJK-Medium.ttc \
  --no-lgc \
  --out ./fonts/cjk-only/AnthropicSerifWebText-CJK-Only.ttf

# 1.0.0-bold cjk-only-bold (same coverage, heavier Chinese)
python3 scripts/build_cjk.py \
  --latin /path/to/AnthropicSerifWebText.ttf \
  --cjk-ttc /path/to/NotoSerifCJK-Bold.ttc \
  --no-lgc \
  --version-string "Version 1.000 CJK Bold" \
  --out ./fonts/cjk-only-bold/AnthropicSerifWebText-CJK-Only-Bold.ttf

# 1.1.0 multilingual (default, both sources)
python3 scripts/build_cjk.py \
  --latin /path/to/AnthropicSerifWebText.ttf \
  --cjk-ttc /path/to/NotoSerifCJK-Medium.ttc \
  --lgc-font "/path/to/NotoSerif[wdth,wght].ttf" \
  --lgc-weight 500 \
  --out ./fonts/multilingual/AnthropicSerifWebText-Multilingual.ttf

# 1.2.0 full (also take every remaining CJK source character)
python3 scripts/build_cjk.py \
  --latin /path/to/AnthropicSerifWebText.ttf \
  --cjk-ttc /path/to/NotoSerifCJK-Medium.ttc \
  --lgc-font "/path/to/NotoSerif[wdth,wght].ttf" \
  --full \
  --out ./fonts/full/AnthropicSerifWebText-Full.ttf
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
| `--version-string` | auto | Override nameID 5, e.g. `Version 1.000 CJK Bold` |
| `--no-cjk` | off | Skip the CJK source |
| `--no-lgc` | off | Skip the LGC source (CJK-only build) |
| `--full` | off | Add every remaining CJK source code point: kana, Hangul and CJK symbols (1.2.0) |
| `--limit` | 0 | Convert only a small sample, for debugging |

A `WOFF2` can then be produced for each TTF:

```bash
python3 - <<'PY'
from fontTools.ttLib import TTFont
pairs = [
    ("fonts/cjk-only/AnthropicSerifWebText-CJK-Only.ttf",
     "fonts/cjk-only/AnthropicSerifWebText-CJK-Only.woff2"),
    ("fonts/cjk-only-bold/AnthropicSerifWebText-CJK-Only-Bold.ttf",
     "fonts/cjk-only-bold/AnthropicSerifWebText-CJK-Only-Bold.woff2"),
    ("fonts/multilingual/AnthropicSerifWebText-Multilingual.ttf",
     "fonts/multilingual/AnthropicSerifWebText-Multilingual.woff2"),
    ("fonts/full/AnthropicSerifWebText-Full.ttf",
     "fonts/full/AnthropicSerifWebText-Full.woff2"),
]
for src, dst in pairs:
    f = TTFont(src)
    f.flavor = "woff2"
    f.save(dst)
PY
```

Keep each pair in its own `fonts/` subdirectory. See
[../fonts/README.md](../fonts/README.md) for the version comparison and
for the rule that a new version must never overwrite an existing one.

## What the script does

1. **Baseline.** Load the Latin font and record its glyph order, cmap and
   vertical metrics. It reads `unitsPerEm == 2000` and never alters
   `hhea`, `OS/2` typographic metrics or the cap/x heights.
2. **CJK selection.** By default, walk the CJK source cmap and keep only
   Chinese-related ranges (see [CHARACTER-SET.md](CHARACTER-SET.md)),
   excluding code points already mapped by the Latin base. With `--full`,
   keep **every** remaining code point of the CJK source instead, which
   adds kana, Hangul syllables and Jamo, enclosed CJK, squared
   compatibility forms, box drawing and other CJK-adjacent symbols. In
   that mode the exclusion set is the LGC source's **actual** cmap, not
   its nominal ranges: characters such as U+2160 ROMAN NUMERAL ONE are
   present in the CJK source but absent from Noto Serif, so they must not
   be excluded or the full build would silently lose them.
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

Two independent weight decisions are involved.

**CJK source weight** is controlled by which `--cjk-ttc` file you pass.
All seven weights ship as TTCs with identical cmap coverage (44,746 code
points), so switching weight never changes which characters you get.
Measured by rendering `H` and `中` at the same pixel size (FreeType
normalises by unitsPerEm, so 1000 UPM CJK and 2000 UPM Latin are directly
comparable):

| CJK source | `usWeightClass` | `中` stem | vs. Western `H` (61.4 px) | Sample ink |
| --- | --- | --- | --- | --- |
| Regular | 400 | 47.5 px | -22.7% | 17,931 px |
| Medium (default) | 500 | 54.5 px | -11.1% | 21,178 px |
| SemiBold | 600 | 60.7 px | -1.0% | 23,744 px |
| **Bold (1.0.0-bold)** | **700** | **70.7 px** | **+15.1%** | **28,082 px** |
| Heavy | 900 | 82.3 px | +34.1% | 33,346 px |

Medium is the default for 1.0.0, 1.1.0 and 1.2.0 because it sits reasonably
close to the Latin without darkening dense Chinese text. **SemiBold is the
near-exact optical match** (-1.0%). **Bold is deliberately heavier** and is
what `cjk-only-bold` uses, because its purpose is to fix Chinese that reads
as thin and pale, not merely to equalise stem widths. To produce a tighter
match, point `--cjk-ttc` at `NotoSerifCJK-SemiBold.ttc` and change the
output name; no other parameter needs to change.

`cjk-only-bold` keeps `OS/2.usWeightClass = 400` and `name` ID 2 =
`Regular`. The Western outlines are Regular and the internal family is
unchanged, so the file is a Regular font with heavier Chinese, not a
synthetic bold. Do not install it alongside `cjk-only`: the two have
identical family and subfamily names and the font cache cannot tell them
apart.

**LGC source weight** is controlled by `--lgc-weight` (default 500).
Pinning the Noto Serif variable font to the same 500 keeps Greek and
Cyrillic stems consistent with the Medium Chinese used in 1.1.0 and 1.2.0.
The 1.0.0 builds do not use the LGC source at all (`--no-lgc`).

## Verification checklist

Run the same checks on all four builds; only the counts differ.

```bash
python3 - <<'PY'
from fontTools.ttLib import TTFont

builds = [
    ("fonts/cjk-only/AnthropicSerifWebText-CJK-Only.ttf", 31724, 31595),
    ("fonts/cjk-only-bold/AnthropicSerifWebText-CJK-Only-Bold.ttf", 31724, 31595),
    ("fonts/multilingual/AnthropicSerifWebText-Multilingual.ttf", 33897, 33768),
    ("fonts/full/AnthropicSerifWebText-Full.ttf", 47092, 46963),
]
for path, want_glyphs, want_codes in builds:
    f = TTFont(path)
    cm = f.getBestCmap()
    print(path)
    print("  glyphs", f["maxp"].numGlyphs, "(expected", want_glyphs, ")")
    print("  codes ", len(cm), "(expected", want_codes, ")")
    print("  GSUB", len(f["GSUB"].table.FeatureList.FeatureRecord),
          "| GPOS", len(f["GPOS"].table.FeatureList.FeatureRecord))
    print("  cmap", [(t.platformID, t.platEncID, t.format, len(t.cmap))
                     for t in f["cmap"].tables])
    print("  unique names", len(set(f.getGlyphOrder())) == len(f.getGlyphOrder()))
    print("  U+4E00", cm.get(0x4E00), "| U+2000B", cm.get(0x2000B),
          "| U+03B1", cm.get(0x03B1), "| U+3042", cm.get(0x3042),
          "| U+AC00", cm.get(0xAC00))
PY
```

Expected for 1.0.0 and 1.0.0-bold: 31,724 glyphs, 31,595 code points,
Greek / kana / Hangul `MISSING`. The two must have **identical** cmap
dictionaries; only the Chinese outlines differ. Verify that directly:

```python
a = TTFont("fonts/cjk-only/AnthropicSerifWebText-CJK-Only.ttf")
b = TTFont("fonts/cjk-only-bold/AnthropicSerifWebText-CJK-Only-Bold.ttf")
print("cmap identical:", a.getBestCmap() == b.getBestCmap())
western = a.getGlyphOrder()[:720]
print("western glyphs identical:",
      all(a["glyf"][g] == b["glyf"][g] for g in western))
print("Chinese differs:",
      a["glyf"][a.getBestCmap()[0x4E00]] != b["glyf"][b.getBestCmap()[0x4E00]])
```

For 1.1.0: 33,897 glyphs, 33,768 code points, Greek resolved, kana /
Hangul still `MISSING`. For 1.2.0: 47,092 glyphs,
46,963 code points, all six scripts resolved. All three retain 19 GSUB
features, 2 GPOS features and four cmap subtables including a format 12
table. Render a mixed string such as
`A 文 あ 한 α Ж Typography 排版設計 かな 한글 Ελληνικά Кириллица ﬁ 123`
with 1.2.0 and confirm that `fi` still forms a ligature and no tofu boxes
appear.

## Renaming the internal family name

The shipped files keep the upstream family name so that they can replace
the original font in an existing document. For a more conservative
redistribution, rename the internal names before publishing:

```python
from fontTools.ttLib import TTFont

f = TTFont("fonts/multilingual/AnthropicSerifWebText-Multilingual.ttf")
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
  Chinese, kana, Hangul and CJK symbols come from Source Han Serif. They
  share the Noto/Source serif design language and the same wght=500, but
  they are not redrawn stroke by stroke to imitate the Anthropic Latin
  letterforms. Kana and Hangul were taken from the SC face: all five faces
  of the TTC have identical cmap coverage, and the shared glyph library
  gives kana and Hangul the same outlines regardless of regional face.
- The original GSUB/GPOS lookups cover Latin only. Greek, Cyrillic, kana
  and Hangul get correct glyphs and advances but do not inherit Latin
  kerning pairs, kana positioning or Hangul composition rules. Hangul
  syllables are supplied as precomposed U+AC00–U+D7A3 glyphs; composing
  arbitrary Jamo sequences at render time is not supported.
- The 1.2.0 build is 23.6 MB as TTF and 8.4 MB as WOFF2. Subset for the
  web; see [USAGE.md](USAGE.md).
- `cjk-only-bold` is heavier only in its Chinese outlines. It is not a
  true Bold weight of the whole family: Western glyphs, kerning and all
  OpenType features are identical to 1.0.0, and the OS/2 weight class
  still reads 400. Applying `font-weight: 700` in CSS on top of it will
  trigger synthetic emboldening of the Latin, which is usually not wanted.
