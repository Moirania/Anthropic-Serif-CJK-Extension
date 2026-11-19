# Using the font

## Files

Two independent builds are shipped. Pick one; see
[../fonts/README.md](../fonts/README.md) for the full comparison.

| Version | TTF | WOFF2 | Glyphs |
| --- | --- | --- | --- |
| 1.0.0 cjk-only | `fonts/cjk-only/AnthropicSerifWebText-CJK-Only.ttf` (15.3 MB) | `fonts/cjk-only/AnthropicSerifWebText-CJK-Only.woff2` (6.9 MB) | 31,724 |
| 1.1.0 multilingual | `fonts/multilingual/AnthropicSerifWebText-Multilingual.ttf` (15.6 MB) | `fonts/multilingual/AnthropicSerifWebText-Multilingual.woff2` (7.0 MB) | 33,897 |

The examples below use **1.1.0 multilingual**. Swap in the `cjk-only`
filenames if you only need Chinese; every command and CSS declaration is
otherwise identical. WOFF2 is brotli compressed and is the right choice
for the web; TTF is convenient for installing on an operating system or
embedding in a document.

## Desktop installation

- **Windows**: double click the TTF and choose Install, or copy it into
  `%WINDIR%\Fonts`.
- **macOS**: open the TTF with Font Book and click Install Font.
- **Linux**: copy to `~/.local/share/fonts/`, then run `fc-cache -fv`.

The internal family name is `Anthropic Serif Web Text` in **both** builds.
Do not install both versions at once, and remove the original upstream
Latin font first if it is already present; otherwise the font cache will
resolve unpredictably. For a renamed build, see [BUILD.md](BUILD.md).

Verify with:

```bash
fc-match "Anthropic Serif Web Text"
```

## Web embedding

```css
@font-face {
  font-family: "Anthropic Serif Web Text";
  src: url("/fonts/AnthropicSerifWebText-Multilingual.woff2") format("woff2");
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

Because CJK, Greek and Cyrillic live in the same file, no fallback stack is
needed for those scripts. A fallback family is still useful for glyphs the
font does not cover, such as emoji, Hangul or mathematical operators.

## Multilingual example

```html
<p lang="zh">《庄子》曰：「天地与我并生，而万物与我为一。」</p>
<p lang="el">Ἀπὸ τὴν ἀρχὴ ἦν ὁ λόγος, καὶ ὁ λόγος ἦν πρὸς τὸν θεόν.</p>
<p lang="ru">В начале было Слово, и Слово было у Бога.</p>
<p lang="la">Ā ā Ă ă Æ æ Ø ø Ł ł Ș Ț ẞ — ﬁde et amōre.</p>
<p>Typography 排版設計 Ελληνικά Кириллица ﬁ 123</p>
```

Polytonic Greek (U+1F00–U+1FFF) and Cyrillic Extended-A/B/C are covered,
so classical Greek and older Slavic orthographies render without tofu
boxes. Combining marks (U+0300–U+036F) are included for decomposed accents.

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

These features were authored for the upstream Latin glyphs. Greek and
Cyrillic glyphs are correctly shaped and spaced but are not included in the
Latin kerning pairs or language-specific substitutions.

## Subsetting for production

The full WOFF2 is 6.9 MB. Shipping it to every visitor is wasteful. Use
`pyftsubset` to keep only the characters a page actually needs:

```bash
pyftsubset fonts/multilingual/AnthropicSerifWebText-Multilingual.ttf \
  --text-file=content.txt \
  --output-file=subset.woff2 \
  --flavor=woff2 \
  --layout-features='*' \
  --no-hinting
```

Notes:

- `--text-file` should contain every character that can appear on the
  page, including punctuation, digits, Greek accents and Cyrillic letters.
- `--layout-features='*'` keeps the ligature and kerning tables. Without
  it, `fi` and kerning pairs may be dropped.
- For dynamic user-generated content, either generate subsets per page
  build, or use a `unicode-range` split: one small Latin subset plus CJK
  chunks of a few thousand code points each, and separate Greek/Cyrillic
  chunks if those languages are used.
- Do not drop the format 12 cmap subtable if your content uses rare CJK
  characters from Extensions B through I or Latin Extended-F/G.

A minimal example for a single multilingual article:

```bash
printf '%s' 'Typography 排版设计 Ελληνικά Кириллица 2026' > content.txt
pyftsubset fonts/multilingual/AnthropicSerifWebText-Multilingual.ttf \
  --text-file=content.txt --flavor=woff2 \
  --output-file=article.woff2 --layout-features='*'
```

## Rendering notes

- The font uses 2000 units per em with ascender 1985 and descender -515.
  Very tight line-height values can clip CJK glyph tops and polytonic Greek
  accents; 1.6 or greater is comfortable for mixed text.
- Chinese glyphs are full width (2000 units). Latin, Greek and Cyrillic
  glyphs keep proportional advances, so mixed paragraphs need no special
  letter-spacing.
- CFF hinting was lost during conversion, and LGC composites were
  decomposed. At very small sizes on low-density screens, text may appear
  slightly softer than a native hinted font.
- CJK vertical typesetting features are not added. The vertical forms
  block is covered as characters, not as a full vertical layout
  implementation.
- The global `head` bounding box is wider than the vertical metrics because
  a few combining marks extend far above or below the em box. This does not
  change `hhea` ascent/descent, so line height stays stable.

## PDF and document embedding

The TTF can be embedded in PDF, EPUB and office documents. Embedding rules
for the upstream proprietary Latin outlines still apply; read
[COMPLIANCE.md](COMPLIANCE.md) before distributing files that contain the
font.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Chinese still shows boxes | Original font still selected | Remove the old font or clear the font cache |
| Greek accents or Cyrillic letters missing | Client ignores format 12 cmap | Use a modern browser or include the range in a subset |
| `fi` no longer joins | Subset dropped layout features | Rebuild subset with `--layout-features='*'` |
| Very large page weight | Full WOFF2 served | Generate a subset as shown above |
| Polytonic Greek accents clipped | Line height too tight | Raise `line-height` to 1.6 or more |
