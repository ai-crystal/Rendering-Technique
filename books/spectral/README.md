# 光谱渲染

**专业级渲染技术 · 专题四**　·　从光子到图像

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/v5-spectral.pdf)

---

从普朗克把能量换成一份一份开始，这本书把光从量子描述一路放回渲染方程：光子与相干性怎么变成辐亮度，辐亮度又怎么被压成三个通道。中间每一层近似都标出成立条件，也标出它碎掉的样子。
后面讲光谱表示、波长采样、hero wavelength、光谱上采样、色散、介质与荧光，再用两章讲神经光谱：怎样用一个张量积把 RGB 变成一条谱线，训练时要造什么数据、会学到什么，以及接进渲染器要付多少代价。

## 目录

**第一篇　光的量子描述**

- [第 1 章 黑体辐射与普朗克的量子假设](#/books/spectral/chapters/ch01)
- [第 2 章 光子：能量、动量与吸收发射](#/books/spectral/chapters/ch02)
- [第 3 章 相干性：从单光子到激光](#/books/spectral/chapters/ch03)
- [第 4 章 从光子到辐亮度：渲染为什么能用经典量](#/books/spectral/chapters/ch04)

**第二篇　颜色不是光**

- [第 5 章 一个错误的颜色](#/books/spectral/chapters/ch05)
- [第 6 章 光、波长与辐亮度](#/books/spectral/chapters/ch06)
- [第 7 章 人眼与色匹配函数](#/books/spectral/chapters/ch07)
- [第 8 章 RGB 渲染到底假设了什么](#/books/spectral/chapters/ch08)

**第三篇　把波长放进渲染方程**

- [第 9 章 光谱光传输](#/books/spectral/chapters/ch09)
- [第 10 章 波长作为随机变量](#/books/spectral/chapters/ch10)
- [第 11 章 Hero Wavelength 采样](#/books/spectral/chapters/ch11)
- [第 12 章 从 RGB 到光谱：上采样与基分解](#/books/spectral/chapters/ch12)

**第四篇　色散、介质与荧光**

- [第 13 章 色散](#/books/spectral/chapters/ch13)
- [第 14 章 介质中的光谱传输](#/books/spectral/chapters/ch14)
- [第 15 章 荧光与波长变换](#/books/spectral/chapters/ch15)
- [第 16 章 偏振接口](#/books/spectral/chapters/ch16)

**第五篇　实现与验证**

- [第 17 章 一个最小的光谱路径追踪器](#/books/spectral/chapters/ch17)
- [第 18 章 验证、性能与完整场景](#/books/spectral/chapters/ch18)

**第六篇　神经光谱**

- [第 19 章 神经基底：把 RGB 映射成一条谱线](#/books/spectral/chapters/ch19)
- [第 20 章 训练、验证与接进渲染器](#/books/spectral/chapters/ch20)

## 重新生成

双击仓库根目录的 `build-spectral.bat`，或运行：

```text
python books/build/build.py --book spectral
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
