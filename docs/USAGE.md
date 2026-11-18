# Using the font

## Files

| File | Size | Use |
| --- | --- | --- |
| `fonts/AnthropicSerifWebText-CJK.ttf` | 15.3 MB | Desktop, print, PDF embedding |
| `fonts/AnthropicSerifWebText-CJK.woff2` | 6.9 MB | Web pages |

Both files contain the same 31,724 glyphs. WOFF2 is brotli compressed and
is the right choice for the web; TTF is convenient for installing on an
operating system or embedding in a document.

## Desktop installation

- **Windows**: double click the TTF and choose Install, or copy it into
  `%WINDIR%\Fonts`.
- **macOS**: open the TTF with Font Book and click Install Font.
- **Linux**: copy to `~/.local/share/fonts/`, then run `fc-cache -fv`.

The internal family name is `Anthropic Serif Web Text`. If the original
Latin font is already installed, installing this composite under the same
name may cause a conflict; remove or replace the original first, or use a
renamed build (see [BUILD.md](BUILD.md)).

Verify with:

```bash
fc-match "Anthropic Serif Web Text"
```

## Web embedding

```css
@font-face {
  font-family: "Anthropic Serif Web Text";
  src: url("/fonts/AnthropicSerifWebText-CJK.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

article {
  font-family: "Anthropic Serif Web Text", Georgia, "Times New Roman", serif;
  font-feature-settings: "kern" 1, "liga" 1;
  line-height: 1.65;
}
```

Because Chinese and Latin live in the same file, no fallback stack is
needed for Chinese text. A fallback family is still useful for glyphs the
font does not cover, such as emoji or Hangul.

## OpenType features preserved

All original GSUB and GPOS lookups survive the extension, because new
glyphs were appended rather than inserted into the existing glyph order.

| Feature | Effect |
| --- | --- |
| `liga`, `dlig` | Standard and discretionary ligatures (`fi`, `ffi`, `ffl`) |
| `kern` | Pair kerning from GPOS |
| `mark` | Mark positioning |
| `onum`, `tnum` | Oldstyle and tabular figures |
| `frac`, `numr`, `dnom` | Fractions, numerators, denominators |
| `sups`, `subs`, `sinf` | Superior, inferior and scientific inferiors |
| `ordn`, `case`, `zero` | Ordinals, case-sensitive forms, slashed zero |
| `ss01`, `aalt`, `calt` | Stylistic set, alternates, contextual alternates |

Example:

```css
.numbers { font-feature-settings: "tnum" 1, "onum" 1; }
.heading { font-feature-settings: "dlig" 1, "case" 1; }
```

## Subsetting for production

The full WOFF2 is 6.9 MB. Shipping it to every visitor is wasteful. Use
`pyftsubset` to keep only the characters a page actually needs:

```bash
pyftsubset fonts/AnthropicSerifWebText-CJK.ttf \
  --text-file=content.txt \
  --output-file=subset.woff2 \
  --flavor=woff2 \
  --layout-features='*' \
  --no-hinting
```

Notes:

- `--text-file` should contain every character that can appear on the
  page, including punctuation and digits.
- `--layout-features='*'` keeps the ligature and kerning tables. Without
  it, `fi` and kerning pairs may be dropped.
- For dynamic user-generated content, either generate subsets per page
  build, or use a unicode-range split: one small Latin subset plus CJK
  chunks of a few thousand code points each.
- Do not drop the format 12 cmap subtable if your content uses rare
  characters from Extensions B through I.

A minimal example for a single article:

```bash
printf '%s' 'Typography 排版设计 — 中文与西文混排 2026' > content.txt
pyftsubset fonts/AnthropicSerifWebText-CJK.ttf \
  --text-file=content.txt --flavor=woff2 \
  --output-file=article.woff2 --layout-features='*'
```

## Rendering notes

- The font uses 2000 units per em with ascender 1985 and descender -515.
  Very tight line-height values can clip CJK glyph tops; 1.5 or greater is
  comfortable for mixed text.
- Chinese glyphs are full width (2000 units). Latin glyphs keep their
  original proportional advances, so mixed paragraphs need no special
  letter-spacing.
- CFF hinting was lost during conversion to TrueType outlines. At very
  small sizes on low-density screens, text may appear slightly softer than
  a native CFF font.
- CJK vertical typesetting features are not added. The vertical forms
  block is covered as characters, not as a full vertical layout
  implementation.

## PDF and document embedding

The TTF can be embedded in PDF, EPUB and office documents. Embedding rules
for the upstream proprietary Latin outlines still apply; read
[COMPLIANCE.md](COMPLIANCE.md) before distributing files that contain the
font.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Chinese still shows boxes | Original font still selected | Remove the old font or clear the font cache |
| `fi` no longer joins | Subset dropped layout features | Rebuild subset with `--layout-features='*'` |
| Rare Extension B characters missing | Client ignores format 12 cmap | Use a modern browser or a subset that includes them |
| Very large page weight | Full WOFF2 served | Generate a subset as shown above |
