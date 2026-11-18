#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extend a Latin TrueType font with a complete CJK character set.

The Latin font is used as the base: every original glyph id, advance,
metric and OpenType layout lookup is preserved. CJK outlines are taken
from a Noto Serif CJK SC face, converted from CFF cubic curves to
TrueType quadratic curves, scaled to the Latin font's units per em, and
appended at the end of the glyph order.

Typical use:

    python3 scripts/build_cjk.py \
        --latin /path/to/AnthropicSerifWebText.ttf \
        --cjk-ttc /path/to/NotoSerifCJK-Medium.ttc \
        --out ./AnthropicSerifWebText-CJK.ttf

Requires: fontTools (and brotli only if you also produce a WOFF2).
The CJK source is licensed under the SIL Open Font License 1.1; see
OFL.txt and FONTLOG.txt. The upstream Latin font is proprietary and is
not relicensed by this script. See docs/COMPLIANCE.md.
"""
import argparse
import os
import sys
import time

from fontTools.ttLib import TTCollection, TTFont, newTable
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable


# Chinese-related Unicode ranges. Kana, Hangul, Cyrillic and Greek are
# intentionally excluded: this is a Chinese extension of a Latin font.
CJK_RANGES = (
    (0x2E80, 0x2FDF),    # CJK radicals supplement, Kangxi radicals
    (0x2FF0, 0x2FFF),    # ideographic description characters
    (0x3000, 0x303F),    # CJK symbols and punctuation
    (0x3100, 0x312F),    # bopomofo
    (0x31A0, 0x31BF),    # bopomofo extended
    (0x31C0, 0x31EF),    # CJK strokes
    (0x3400, 0x4DBF),    # extension A
    (0x4E00, 0x9FFF),    # unified ideographs, basic block
    (0xF900, 0xFAFF),    # compatibility ideographs
    (0xFE10, 0xFE1F),    # vertical forms
    (0xFE30, 0xFE4F),    # CJK compatibility forms
    (0xFF00, 0xFFEF),    # halfwidth and fullwidth forms
    (0x20000, 0x2EBEF),  # extensions B through F
    (0x2F800, 0x2FA1F),  # compatibility ideographs supplement
    (0x30000, 0x323AF),  # extensions G through I
)

DEBUG_SAMPLE = (
    0x4E00, 0x4E2D, 0x6587, 0x5B57, 0x6392, 0x7248, 0x8BBE, 0x8BA1,
    0x4E16, 0x754C, 0x4F60, 0x597D, 0x3002, 0xFF0C, 0x3001, 0xFF1A,
)


def is_cjk(cp):
    return any(lo <= cp <= hi for lo, hi in CJK_RANGES)


def glyph_name(cp, used):
    name = ("uni%04X" % cp) if cp <= 0xFFFF else ("u%X" % cp)
    if name in used:
        name = "cjk%X" % cp
    return name


def set_name(font, name_id, value):
    """Replace every record of a name ID with a single bilingual value."""
    table = font["name"]
    for rec in list(table.names):
        if rec.nameID == name_id:
            table.names.remove(rec)
    table.setName(value, name_id, 3, 1, 0x409)
    table.setName(value, name_id, 1, 0, 0)


def rename_family(font, family):
    sub = font["name"].getDebugName(2) or "Regular"
    ps = family.replace(" ", "") + "-" + sub.replace(" ", "")
    for nid, value in ((1, family), (4, family + " " + sub),
                       (6, ps), (16, family), (17, sub)):
        set_name(font, nid, value)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--latin", required=True, help="upstream Latin TTF")
    ap.add_argument("--cjk-ttc", required=True, help="Noto Serif CJK TTC or OTF")
    ap.add_argument("--cjk-face", type=int, default=2,
                    help="TTC face index, 2 = Simplified Chinese (default)")
    ap.add_argument("--out", required=True, help="output TTF path")
    ap.add_argument("--max-err", type=float, default=0.5,
                    help="cu2qu maximum error in source units (default 0.5)")
    ap.add_argument("--family-name", default=None,
                    help="replace internal family names (conservative builds)")
    ap.add_argument("--limit", type=int, default=0,
                    help="convert only a small sample, for debugging")
    args = ap.parse_args()

    for path in (args.latin, args.cjk_ttc):
        if not os.path.isfile(path):
            sys.exit("input file not found: %s" % path)

    t0 = time.time()
    base = TTFont(args.latin)
    upem = base["head"].unitsPerEm
    orig_order = list(base.getGlyphOrder())
    orig_cps = set(cp for t in base["cmap"].tables for cp in t.cmap.keys())
    print("Latin base: %s | upem %d | glyphs %d | code points %d" %
          (base["name"].getDebugName(1) or "(unnamed)", upem,
           len(orig_order), len(orig_cps)))

    if args.cjk_ttc.lower().endswith(".ttc"):
        cjk = TTCollection(args.cjk_ttc, lazy=False).fonts[args.cjk_face]
    else:
        cjk = TTFont(args.cjk_ttc)
    cjk_upem = cjk["head"].unitsPerEm
    scale = upem / cjk_upem
    cjk_cmap = cjk.getBestCmap()
    charstrings = cjk["CFF "].cff.topDictIndex[0].CharStrings
    print("CJK source: %s | upem %d | scale %.3f" %
          (cjk["name"].getDebugName(1) or "(unnamed)", cjk_upem, scale))

    todo = sorted(cp for cp in cjk_cmap if is_cjk(cp) and cp not in orig_cps)
    if args.limit:
        todo = [cp for cp in DEBUG_SAMPLE if cp in cjk_cmap and cp not in orig_cps]
    print("CJK code points to add: %d" % len(todo))

    glyf = base["glyf"]
    hmtx = base["hmtx"]
    for name in orig_order:
        _ = glyf[name]  # force decoding of lazy glyph data
    used = set(orig_order)
    new_names, new_cps, failed = [], {}, []

    for i, cp in enumerate(todo):
        cjk_name = cjk_cmap[cp]
        pen = TTGlyphPen(None)
        cu = Cu2QuPen(TransformPen(pen, (scale, 0, 0, scale, 0, 0)),
                      max_err=args.max_err, reverse_direction=True)
        try:
            charstrings[cjk_name].draw(cu)
            glyph = pen.glyph()
            glyph.recalcBounds(None)
        except Exception as exc:
            failed.append((hex(cp), type(exc).__name__, str(exc)[:80]))
            continue
        name = glyph_name(cp, used)
        used.add(name)
        glyf.glyphs[name] = glyph
        advance = int(round(cjk["hmtx"][cjk_name][0] * scale))
        lsb = glyph.xMin if glyph.numberOfContours > 0 else 0
        hmtx.metrics[name] = (advance, lsb)
        new_names.append(name)
        new_cps[cp] = name
        if (i + 1) % 5000 == 0:
            print("  converted %d / %d (%.1fs)" %
                  (i + 1, len(todo), time.time() - t0))
    print("converted %d, failed %d %s" %
          (len(new_names), len(failed), failed[:5]))
    if not new_names:
        sys.exit("no glyphs produced")

    # Append only: all original glyph ids stay valid, so GSUB/GPOS survive.
    base.setGlyphOrder(orig_order + new_names)
    total = len(orig_order) + len(new_names)
    base["maxp"].numGlyphs = total
    base["hhea"].numberOfHMetrics = total

    # BMP characters go into the existing format 4 subtables.
    for sub in base["cmap"].tables:
        if sub.format in (4, 6) and sub.platformID in (0, 3):
            for cp, name in new_cps.items():
                if cp <= 0xFFFF:
                    sub.cmap[cp] = name

    # A format 12 subtable is required for non-BMP extensions B through I.
    full = {}
    for sub in base["cmap"].tables:
        if sub.platformID in (0, 3) and not (sub.platformID == 3 and sub.platEncID == 10):
            full.update(sub.cmap)
    full.update(new_cps)
    sub12 = CmapSubtable.newSubtable(12)
    sub12.platformID, sub12.platEncID = 3, 10
    sub12.format, sub12.language = 12, 0
    sub12.cmap = dict(sorted(full.items()))
    base["cmap"].tables.append(sub12)

    os2 = base["OS/2"]
    os2.usFirstCharIndex = min(full)
    os2.usLastCharIndex = 0xFFFF
    for i in range(1, 5):
        setattr(os2, "usUnicodeRange%d" % i, 0xFFFFFFFF)

    xmin = ymin = 10 ** 9
    xmax = ymax = -10 ** 9
    for name in base.getGlyphOrder():
        g = glyf[name]
        if g.numberOfContours > 0:
            xmin, ymin = min(xmin, g.xMin), min(ymin, g.yMin)
            xmax, ymax = max(xmax, g.xMax), max(ymax, g.yMax)
    head = base["head"]
    head.xMin, head.yMin, head.xMax, head.yMax = xmin, ymin, xmax, ymax
    base["maxp"].recalc(base)
    try:
        base["hhea"].recalc(base)
    except Exception as exc:
        print("hhea recalc skipped:", exc)

    # OFL attribution for the CJK-derived outlines.
    copyright_cjk = str(cjk["name"].getDebugName(0) or "")
    license_desc = str(cjk["name"].getDebugName(13) or
                       "SIL Open Font License, Version 1.1")
    license_url = str(cjk["name"].getDebugName(14) or
                      "https://openfontlicense.org/")
    set_name(base, 0,
             "CJK glyph outlines: " + copyright_cjk +
             " Licensed under the SIL Open Font License, Version 1.1. "
             "This font is a modified composite; the Reserved Font Name "
             "'Noto' is not used. Upstream Latin outlines are proprietary "
             "and are not relicensed.")
    set_name(base, 5, "Version 1.001 CJK")
    set_name(base, 13, license_desc)
    set_name(base, 14, license_url)

    if args.family_name:
        rename_family(base, args.family_name)
        print("internal family renamed to: %s" % args.family_name)

    print("saving ... total glyphs %d, code points %d" % (total, len(full)))
    base.save(args.out)
    print("done: %s | %.2f MB | %.1fs" %
          (args.out, os.path.getsize(args.out) / 1048576, time.time() - t0))


if __name__ == "__main__":
    main()
