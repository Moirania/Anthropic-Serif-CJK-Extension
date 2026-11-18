# Anthropic Serif CJK Extension

[![Glyphs](https://img.shields.io/badge/Glyphs-31724-222118)](docs/CHARACTER-SET.md) [![Codepoints](https://img.shields.io/badge/Unicode-31595%20codepoints-222118)](docs/CHARACTER-SET.md) [![UPM](https://img.shields.io/badge/UPM-2000-222118)](docs/BUILD.md) [![CJK outlines](https://img.shields.io/badge/CJK%20outlines-SIL%20OFL%201.1-A62E26)](OFL.txt) [![Upstream](https://img.shields.io/badge/Upstream-proprietary-746F64)](docs/COMPLIANCE.md) [![Formats](https://img.shields.io/badge/Formats-TTF%20%2F%20WOFF2-222118)](docs/USAGE.md)

给 **Anthropic Serif Web Text Regular** 补上一套完整的中文字符集，并把可复现的构建过程、字符集明细与前后对比图一并公开。

原字体是一套用于阅读的西文衬线字体，只有 628 个码位、720 个字形，中文字符一个也没有。在中英混排时，中文会全部退化为缺字方框。本项目在**不改动任何西文字形、不改动原有 OpenType 排版特性、不改动原有字形编号顺序**的前提下，追加 31,004 个中文相关码位，得到 31,724 个字形、31,595 个可用码位的复合字体。中文轮廓取自 Noto Serif CJK SC Medium（思源宋体），统一到 2000 UPM 与全宽 1em 的度量，使「A」与「文」能落在同一条基线上。

仓库提供直接可用的 `TTF` 与 `WOFF2`、一键重建脚本、按 Unicode 分区的覆盖明细、以及两张样张图。文档结构遵循 GitHub 官方 [About READMEs](https://docs.github.com/repos/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) 与 README 结构建议：先回答「这是什么、为什么有用、怎么开始」，深度内容放进 `docs/`。

---

## 授权与风险声明（请先阅读）

这一节不是免责套话，而是使用本仓库前必须确认的事实。

1. **上游拉丁字体是专有品牌字体。** `Anthropic Serif Web Text` 及相关名称属于 Anthropic, PBC，官方未提供公开的字体授权，也**不是** SIL OFL 字体。第三方资料同样将其描述为不公开许可的品牌字体（见 [docs/COMPLIANCE.md](docs/COMPLIANCE.md)）。本仓库中的复合字体文件包含该字体的全部西文轮廓，公开发布与再次分发可能需要权利人授权。
2. **本仓库按「公开仓库全量」发布。** 维护者确认已就公开分发所需权利自行作出判断并承担相应责任。若你打算在公司项目、商业产品或对外分发中使用，请先自行核实权利来源；本仓库不构成任何授权担保。
3. **中文轮廓部分受 SIL OFL 1.1 约束。** Noto Serif CJK SC 的版权归 Adobe 等权利人所有，依 [SIL Open Font License 1.1](OFL.txt) 授权。因此衍生部分必须同许可分发、随附版权声明与协议全文、不得单独售卖字体文件、不得使用原作者的名义为衍生版本背书、且保留名称条款需被尊重。完整说明见 [LICENSE](LICENSE) 与 [docs/COMPLIANCE.md](docs/COMPLIANCE.md)。
4. **字体内部名称仍含上游品牌名。** 为保持与原始字体在系统中可替换，当前 `fonts/` 内文件的 `name` 表沿用 `Anthropic Serif Web Text`。若你要以更保守的方式再分发，可按 [docs/BUILD.md](docs/BUILD.md) 中的改名步骤修改内部家族名。
5. **本项目与 Anthropic 无 affiliation。** 仓库名与字体名仅用于描述被扩展的对象，不代表 Anthropic 的赞助、背书或参与。

---

## 为什么有用

- **一处解决中英混排缺字**：不必为一段中文单独指定回退字体，也不必在 CSS 里拼一长串 `font-family`，西文与中文由同一个字体文件渲染。
- **西文质量不被稀释**：原字体的 `GSUB` 特性（连字 `fi`/`ffi`、小型大写、旧式数字、分数、序号、样式集等）与 `GPOS` 字距全部保留，因为新增字形只追加在字形表末尾，原有 glyph id 未变。
- **中文覆盖足够深**：不只是常用字，CJK 扩展 A、扩展 B 至 I、兼容表意文字、中文标点、注音符号、部首、全角与半角形式都在同一个文件里。
- **可直接上网页**：同时提供 15.3 MB 的 TTF 与 6.9 MB 的 WOFF2，附带子集化建议，避免把整套字库压给访问者。
- **过程完全可复现**：构建脚本、依赖版本、轮廓转换参数与度量处理全部公开，可自行替换中文来源字重或收窄字符集。

## 核心特性

| 项目 | 数值 |
| --- | --- |
| 追加中文码位 | 31,004 |
| 总字形数 | 31,724 |
| cmap 可用码位 | 31,595（含扩展区非 BMP 字符） |
| 基本区 U+4E00–U+9FFF | 20,971 字 |
| 扩展 A / 扩展 B–I | 6,582 / 2,306 字 |
| 标点、注音、部首、全角等 | 1,145 个码位 |
| 单位度量 | 2000 UPM，中文全宽 1em，西文度量原样保留 |
| 轮廓转换 | CFF 三次贝塞尔转 TrueType 二次贝塞尔（cu2qu，`max_err=0.5`） |

## 效果对比

同一段文字、同一字号、同一基线。上半为补全后，下半为原字体，中文显示为缺字方框。

![补全前后同文对照](assets/before-after.png)

完整的双语排版样张（含标点、注音、部首、扩展区生僻字与简繁对照）：

![中英混排样张](assets/type-specimen-sheet.png)

## 快速开始

最短路径是直接取用已构建好的字体文件，无需安装任何依赖。

```bash
git clone https://github.com/Moirania/Anthropic-Serif-CJK-Extension.git
cd Anthropic-Serif-CJK-Extension
ls fonts/
# AnthropicSerifWebText-CJK.ttf   AnthropicSerifWebText-CJK.woff2
```

桌面使用：双击 `fonts/AnthropicSerifWebText-CJK.ttf`（Windows 选择「安装」；macOS 用「字体册」导入；Linux 复制到 `~/.local/share/fonts/` 后执行 `fc-cache -fv`）。安装后在应用里选择 `Anthropic Serif Web Text` 即可，中英文都会由它渲染。

网页使用，把 WOFF2 放到静态目录并声明 `@font-face`：

```css
@font-face {
  font-family: "Anthropic Serif Web Text";
  src: url("/fonts/AnthropicSerifWebText-CJK.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

body {
  font-family: "Anthropic Serif Web Text", Georgia, serif;
  font-feature-settings: "liga" 1, "kern" 1;
}
```

打开 `docs/USAGE.md` 可看到完整的排版示例、OpenType 特性清单、子集化命令与常见注意事项。

## 从源码构建

如果你想换中文来源字重、调整字面大小或收窄字符集，可以重建字体。完整步骤、依赖与参数说明见 [docs/BUILD.md](docs/BUILD.md)。

```bash
pip install fonttools brotli
python3 scripts/build_cjk.py \
  --latin /path/to/AnthropicSerifWebText.ttf \
  --cjk-ttc /path/to/NotoSerifCJK-Medium.ttc \
  --out ./AnthropicSerifWebText-CJK.ttf
```

脚本默认使用思源宋体 SC 面的 Medium 字重。选它是因为原西文属于 Text 光学尺寸、竖干偏粗，Medium 在缩放到 2000 UPM 后视觉重量最接近；若你偏好更轻或更重，替换 `--cjk-ttc` 即可。

## 文档导航

| 文档 | 内容 |
| --- | --- |
| [docs/USAGE.md](docs/USAGE.md) | 安装、CSS、OpenType 特性、子集化、渲染注意事项 |
| [docs/BUILD.md](docs/BUILD.md) | 构建原理、依赖、参数、校验方法与改名步骤 |
| [docs/CHARACTER-SET.md](docs/CHARACTER-SET.md) | 按 Unicode 分区的逐段覆盖明细 |
| [docs/COMPLIANCE.md](docs/COMPLIANCE.md) | 上游授权、OFL 义务、商标与再分发风险 |
| [FONTLOG.txt](FONTLOG.txt) | 逐项修改记录（遵循 OFL 惯例） |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献方式 |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | 社区行为准则 |

## 项目结构

```
.
├── fonts/          构建产物：TTF 与 WOFF2
├── assets/         前后对比图与排版样张
├── scripts/        build_cjk.py，可复现构建脚本
├── docs/           使用、构建、字符集与合规文档
├── README.md       本文件
├── LICENSE         文档与脚本许可，以及字体文件的分层授权说明
├── OFL.txt         SIL Open Font License 1.1 全文
├── FONTLOG.txt     修改记录
└── CITATION.cff    引用信息
```

## 获取帮助

- 使用与构建问题：先查 [docs/](docs/)，再到 [Issues](https://github.com/Moirania/Anthropic-Serif-CJK-Extension/issues) 提问。
- 缺字、字形错位、行高异常等具体缺陷：请附上字符码位、操作系统、浏览器或渲染引擎版本，以及一张截图。
- 授权相关问题：请先阅读 [docs/COMPLIANCE.md](docs/COMPLIANCE.md)；本仓库无法代替权利人给出授权结论。

## 贡献与维护

欢迎提交缺字报告、字符集扩展、构建脚本改进与文档修正，流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。仓库由 [Moirania](https://github.com/Moirania) 维护。请注意：由于上游字体的授权状态，涉及**新增或替换字形轮廓**的 PR 需要同时说明来源与许可，否则无法合并。

## 许可证

- 仓库中的文档、脚本与样张图：见 [LICENSE](LICENSE)。
- 中文轮廓及其衍生部分：[SIL Open Font License 1.1](OFL.txt)，版权与条件详见 [LICENSE](LICENSE) 与 [FONTLOG.txt](FONTLOG.txt)。
- 上游西文轮廓：专有字体，权利归 Anthropic, PBC 所有，**不适用**上述任何开源许可。完整说明见 [docs/COMPLIANCE.md](docs/COMPLIANCE.md)。

## 致谢

- 西文原始字体：Anthropic Serif Web Text Regular。
- 中文轮廓：Noto Serif CJK SC / 思源宋体，Adobe 与 Google 等贡献者，SIL OFL 1.1。
- 构建工具：fontTools（`cu2qu`、`feaLib`、`ttLib`、`varLib`）。
