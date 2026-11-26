# 基于储蓄池的渲染

**专业级渲染技术 · 专题八**　·　从 RIS 到 ReSTIR

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/v9-reservoir.pdf)

---

光源采样在多灯场景里会失效：随机挑一盏，大多数时候挑中的那盏对着色点毫无贡献。蓄水池采样换了个思路——多试几个候选，只留下最好的那个，并记住它被选中的概率。
这本书从 MIS 与带权蓄水池讲起，经 Talbot 的 RIS 走到 ReSTIR 的时空复用、路径复用与 GRIS 理论，每一步都给出无偏性成立的条件，也给出破坏它之后偏差会有多大。

## 目录

**第一篇　从重要性采样到重采样**

- [第 1 章 一百盏灯，一次采样](#/books/reservoir/chapters/ch01)
- [第 2 章 MIS：把多个采样器合起来](#/books/reservoir/chapters/ch02)
- [第 3 章 带权蓄水池：一遍流过完](#/books/reservoir/chapters/ch03)
- [第 4 章 RIS：廉价评估换昂贵评估](#/books/reservoir/chapters/ch04)

**第二篇　ReSTIR**

- [第 5 章 ReSTIR DI：把蓄水池放进像素](#/books/reservoir/chapters/ch05)
- [第 6 章 ReSTIR 的数学](#/books/reservoir/chapters/ch06)
- [第 7 章 偏差从哪里来](#/books/reservoir/chapters/ch07)
- [第 8 章 时空复用与可见性复用](#/books/reservoir/chapters/ch08)

**第三篇　路径与体积**

- [第 9 章 ReSTIR GI：把路径放进蓄水池](#/books/reservoir/chapters/ch09)
- [第 10 章 体积重采样](#/books/reservoir/chapters/ch10)
- [第 11 章 GRIS：重采样与多重重要性采样的统一](#/books/reservoir/chapters/ch11)

**第四篇　工程与前沿**

- [第 12 章 实现细节](#/books/reservoir/chapters/ch12)
- [第 13 章 参数、收敛与稳定性](#/books/reservoir/chapters/ch13)
- [第 14 章 验证与调试](#/books/reservoir/chapters/ch14)
- [第 15 章 SIGGRAPH 2025 的生产现状](#/books/reservoir/chapters/ch15)

## 重新生成

双击仓库根目录的 `build-reservoir.bat`，或运行：

```text
python books/build/build.py --book reservoir
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
