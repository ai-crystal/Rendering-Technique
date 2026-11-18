# 基于储蓄池的渲染

**专业级渲染技术 · 专题八**　·　从 RIS 到 ReSTIR

作者：Dr. Dezeming　　在线阅读 <https://dezeming.github.io/RenderingSeries/>　　下载：[整本 PDF](../../output/rendering-08-reservoir.pdf)

---

光源采样在有很多灯的场景里会失效：随机挑一盏灯，大多数时候挑中的那盏对当前着色点毫无贡献。蓄水池采样换了个思路——多试几个候选，只留下最好的那个，并记住它被选中的概率。
这本书从蓄水池采样讲到 RIS，再到 ReSTIR 的时空复用、路径复用与 GRIS 理论，重点是那些让结果仍然无偏的细节。

## 目录

**第一篇　为什么要重采样**

- [第 1 章 一百盏灯，一次采样](#/books/reservoir/chapters/ch01)
- [第 2 章 蓄水池：只留一个，但记住它怎么被选中](#/books/reservoir/chapters/ch02)

**第二篇　ReSTIR 家族**

- [第 3 章 ReSTIR DI：把蓄水池放进像素](#/books/reservoir/chapters/ch03)
- [第 4 章 偏差从哪里来](#/books/reservoir/chapters/ch04)
- [第 5 章 ReSTIR GI：把路径也放进蓄水池](#/books/reservoir/chapters/ch05)
- [第 6 章 GRIS：重采样与多重重要性采样的统一](#/books/reservoir/chapters/ch06)

**第三篇　工程**

- [第 7 章 实现细节](#/books/reservoir/chapters/ch07)
- [第 8 章 参数与收敛](#/books/reservoir/chapters/ch08)
- [第 9 章 验证与调试](#/books/reservoir/chapters/ch09)
- [附录 A　符号与文献](#/books/reservoir/appendix/app_a)
- [后记](#/books/reservoir/front/afterword)
- [backcover](#/books/reservoir/front/backcover)

## 重新生成

双击仓库根目录的 `build-reservoir.bat`，或运行：

```text
python books/build/build.py --book reservoir
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
