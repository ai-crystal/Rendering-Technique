# 基于储蓄池的渲染

> MIS、带权蓄水池、RIS、ReSTIR 与 GRIS

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/rendering-08-reservoir.pdf)

光源采样在多灯场景里会失效：随机挑一盏，大多数时候挑中的那盏对着色点毫无贡献。蓄水池采样换了个思路——多试几个候选，只留下最好的那个，并记住它被选中的概率。 这本书从 MIS 与带权蓄水池讲起，经 Talbot 的 RIS 走到 ReSTIR 的时空复用、路径复用与 GRIS 理论，每一步都给出无偏性成立的条件，也给出破坏它之后偏差会有多大。

共 15 章 · 94 页

[从第 1 章开始](chapters/ch01.md)　·　<a href="../../output/rendering-08-reservoir.pdf" target="_blank" rel="noopener" data-router-ignore>下载本册 PDF</a>

## 目录

- [前言](front/preface.md)
- [第 1 章　一百盏灯，一次采样](chapters/ch01.md)
- [第 2 章　MIS：把多个采样器合起来](chapters/ch02.md)
- [第 3 章　带权蓄水池：一遍流过完](chapters/ch03.md)
- [第 4 章　RIS：廉价评估换昂贵评估](chapters/ch04.md)
- [第 5 章　ReSTIR DI：把蓄水池放进像素](chapters/ch05.md)
- [第 6 章　ReSTIR 的数学](chapters/ch06.md)
- [第 7 章　偏差从哪里来](chapters/ch07.md)
- [第 8 章　时空复用与可见性复用](chapters/ch08.md)
- [第 9 章　ReSTIR GI：把路径放进蓄水池](chapters/ch09.md)
- [第 10 章　体积重采样](chapters/ch10.md)
- [第 11 章　GRIS：重采样与多重重要性采样的统一](chapters/ch11.md)
- [第 12 章　实现细节](chapters/ch12.md)
- [第 13 章　参数、收敛与稳定性](chapters/ch13.md)
- [第 14 章　验证与调试](chapters/ch14.md)
- [第 15 章　SIGGRAPH 2025 的生产现状](chapters/ch15.md)

### 附录

- [附录 A　符号、公式与文献](appendix/app_a.md)

---

[返回系列首页](../../README.md)
