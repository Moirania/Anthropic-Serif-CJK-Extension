# Licensing and compliance

This is the most important document in the repository. It explains why the
font files in `fonts/` cannot be treated as a normal open source font.

## Summary

The composite font is made of two parts with incompatible licensing
situations:

| Part | Source | Status |
| --- | --- | --- |
| Latin outlines, OpenType tables, metrics, internal name | Anthropic Serif Web Text Regular | Proprietary brand typeface, no public license |
| Chinese outlines | Noto Serif CJK SC Medium | SIL Open Font License 1.1 |
| Latin Extended, Greek, Cyrillic and shared marks | Noto Serif, wght=500 | SIL Open Font License 1.1 |

The SIL OFL applies to both added portions. It does not, and cannot,
relicense the proprietary Latin outlines that are stored in the same file.

## 1. Upstream Latin font

Anthropic Serif Web Text is a proprietary brand typeface used by Anthropic
on its own products. Public reporting describes it as "a proprietary
brand typeface and is not available to license". Third-party repositories
that host extracted copies of these fonts typically add an explicit notice
that the files are included for personal use only and are **not** covered
by the repository's MIT license, with all rights remaining with Anthropic.
See also the Anthropic Trademark Guidelines, which state that Anthropic
trademarks may not be used in a way that implies sponsorship or
endorsement.

Consequences for this repository:

- Publishing `fonts/` in a public repository redistributes the complete
  Latin outline set. That may require permission from the rights holder.
- Applying an MIT or OFL license to the whole file is not possible. The
  [LICENSE](../LICENSE) file therefore splits the rights by component.
- Repository and font names are used only to identify what was extended.
  There is no affiliation, sponsorship or endorsement by Anthropic.

The maintainer of this repository explicitly chose the "public repository,
full files" publication mode and takes responsibility for that choice.
No rights to the upstream font are granted by this repository, and no
representation is made that upstream permission has been obtained. If you
plan to use the files in a commercial product, a client deliverable or
any further redistribution, obtain your own legal confirmation.

## 2. Added outlines under SIL OFL 1.1

Two sources supply the added outlines, both under the SIL Open Font
License 1.1:

- Noto Serif CJK SC (Source Han Serif), copyright (c) 2014-2022 Adobe and
  other contributors, for the Chinese glyphs, and (in 1.2.0 only) for kana,
  Hangul syllables, Jamo and the CJK enclosed / squared / box-drawing
  symbols. Builds 1.0.0 and 1.1.0 take only its Chinese-related subset;
  1.2.0 takes essentially its entire remaining character set.
- Noto Serif from [notofonts/latin-greek-cyrillic](https://github.com/notofonts/latin-greek-cyrillic),
  Copyright 2022 The Noto Project Authors, for Latin Extended, Greek,
  Cyrillic and the shared marks. It was instanced at wght=500 before use.
  All three builds use the same two sources; no third font was introduced
  for the kana and Hangul coverage.

The OFL permits use, study, modification, embedding and redistribution,
including commercial use, subject to these conditions:

1. The copyright notice and the license text must accompany every copy.
   This repository ships [OFL.txt](../OFL.txt) with both copyright lines,
   and records them in [FONTLOG.txt](../FONTLOG.txt) and in the font
   `name` table.
2. Modified versions must be distributed only under the OFL. All added
   outlines in this font are therefore OFL 1.1.
3. The font software may not be sold by itself. Bundling it with software
   is allowed, but the file alone may not be the product.
4. Reserved Font Names, where declared, must not be used by a modified
   version. The composite family name uses neither "Noto" nor
   "Source Han".
5. The original authors' names may not be used to promote a modified
   version. Credit is given as attribution, not as endorsement.

The OFL applies to font software, not to documents made with it. The
specimen images in `assets/` and the PDF or web pages you design are not
subject to the OFL.

## 3. What the SIL OFL does not fix

A common mistake is to assume that because the added components are OFL,
the whole composite becomes open source. It does not. The OFL requires
derivative versions of the OFL fonts to stay under the OFL, but the
upstream Latin outlines are a separate work with a separate rights holder.
Combining them in one file does not grant a license for the Latin outlines.

Conversely, the proprietary upstream font does not remove the OFL
obligations attached to either added source: the copyright notices, the
license text and the share-alike condition still apply to those portions.
Having two OFL sources does not dilute either one; each copyright line must
be preserved.

## 4. Internal font names

The files in `fonts/` currently keep `Anthropic Serif Web Text` in the
`name` table so that the composite can replace the original font in an
existing document. This creates two risks:

- Trademark and branding confusion with the upstream typeface.
- A potential Reserved Font Name conflict if the upstream font ever
  declares one.

A conservative redistribution should rename the internal family, full
name and PostScript name. [BUILD.md](BUILD.md) gives the exact fontTools
snippet, and `scripts/build_cjk.py --family-name` applies it during the
build. The specimen images and the repository name can stay as they are,
because they describe the extension rather than the font family.

## 5. Conservative publication path

If you want an unambiguously compliant public repository, follow this
pattern instead of shipping the binary files:

1. Publish the build script, all documentation, the specimen images, the
   OFL text and FONTLOG.
2. Do not commit `fonts/*/*.ttf` or `fonts/*/*.woff2`. Add them to
   `.gitignore` and remove them from the git history.
3. In the README, instruct readers to supply their own legally obtained
   copy of the upstream Latin font and to run
   `scripts/build_cjk.py` locally to produce the composite.
4. Keep the generated font in a private repository, a local build
   artifact, or a release asset whose access is controlled.

This path still shares the entire method and the OFL-derived contribution,
while avoiding public redistribution of the proprietary outlines. The
maintainer of this repository chose not to use it, after being informed
of the risk.

## 6. Checklist before reusing this work

- [ ] I have confirmed the rights for the upstream Latin outlines for my
      intended use.
- [ ] I keep OFL.txt, the copyright notices and FONTLOG.txt with any copy.
- [ ] I do not sell the font file by itself.
- [ ] I do not imply Anthropic or Adobe endorsement.
- [ ] I renamed the internal family if redistribution is public.
- [ ] I subset the web font rather than shipping the full 6.9 MB.

## References

- SIL Open Font License 1.1, official text: https://openfontlicense.org/
- OFL FAQ, modifying and redistributing OFL fonts:
  https://openfontlicense.org/how-to-modify-ofl-fonts
- Noto Serif (Latin-Greek-Cyrillic) source project:
  https://github.com/notofonts/latin-greek-cyrillic
- Noto Serif CJK / Source Han Serif:
  https://github.com/notofonts/noto-cjk
- Anthropic Trademark Guidelines: https://www.anthropic.com/brand
- GitHub Docs, About READMEs:
  https://docs.github.com/repos/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

These references are provided for orientation. This repository does not
provide legal advice.
