# 光谱渲染

**专业级渲染技术 · 专题四**　·　从波长到图像

作者：Dr. Dezeming　　在线阅读 <https://dezeming.github.io/RenderingSeries/>　　下载：[整本 PDF](../../output/rendering-04-spectral.pdf)

---

有一些场景，任何 RGB 渲染器都会答错：两条窄谱线混出的洋红，穿过棱镜后的一条彩带，荧光材料在紫外下的发光。它们错在同一个地方——把连续的光谱压成了三个数。
这本书把波长放回渲染方程，讲清楚光谱表示、波长采样、hero wavelength、光谱上采样、色散、介质与荧光，最后给出一个能跑的最小实现和一个完整的色散玻璃场景。

## 目录

**第一篇　颜色不是光**

- [第 1 章 一个错误的颜色](#/books/spectral/chapters/ch01)
- [第 2 章 光、波长与辐亮度](#/books/spectral/chapters/ch02)
- [第 3 章 人眼与色匹配函数](#/books/spectral/chapters/ch03)
- [第 4 章 RGB 渲染到底假设了什么](#/books/spectral/chapters/ch04)

**第二篇　把波长放进渲染方程**

- [第 5 章 光谱光传输](#/books/spectral/chapters/ch05)
- [第 6 章 波长作为随机变量](#/books/spectral/chapters/ch06)
- [第 7 章 Hero Wavelength 采样](#/books/spectral/chapters/ch07)
- [第 8 章 从 RGB 到光谱：上采样与基分解](#/books/spectral/chapters/ch08)

**第三篇　色散、介质与荧光**

- [第 9 章 色散](#/books/spectral/chapters/ch09)
- [第 10 章 介质中的光谱传输](#/books/spectral/chapters/ch10)
- [第 11 章 荧光与波长变换](#/books/spectral/chapters/ch11)
- [第 12 章 偏振接口](#/books/spectral/chapters/ch12)

**第四篇　实现与验证**

- [第 13 章 一个最小的光谱路径追踪器](#/books/spectral/chapters/ch13)
- [第 14 章 验证、性能与完整场景](#/books/spectral/chapters/ch14)
- [附录 A　符号与单位](#/books/spectral/appendix/app_a)
- [附录 B　数值速查](#/books/spectral/appendix/app_b)
- [附录 C　参考文献](#/books/spectral/appendix/app_c)
- [后记](#/books/spectral/front/afterword)
- [backcover](#/books/spectral/front/backcover)

## 重新生成

双击仓库根目录的 `build-spectral.bat`，或运行：

```text
python books/build/build.py --book spectral
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
