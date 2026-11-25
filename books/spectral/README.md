# 光谱渲染

> 光子与相干、上采样、神经基底、色散与荧光

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/rendering-04-spectral.pdf)

从普朗克把能量换成一份一份开始，这本书把光从量子描述一路放回渲染方程：光子与相干性怎么变成辐亮度，辐亮度又怎么被压成三个通道。中间每一层近似都标出成立条件，也标出它碎掉的样子。 后面讲光谱表示、波长采样、hero wavelength、光谱上采样、色散、介质与荧光，再用两章讲神经光谱：怎样用一个张量积把 RGB 变成一条谱线，训练时要造什么数据、会学到什么，以及接进渲染器要付多少代价。

共 20 章 · 126 页

[从第 1 章开始](chapters/ch01.md)　·　<a href="../../output/rendering-04-spectral.pdf" target="_blank" rel="noopener" data-router-ignore>下载本册 PDF</a>

## 目录

- [前言](front/preface.md)
- [第 1 章　黑体辐射与普朗克的量子假设](chapters/ch01.md)
- [第 2 章　光子：能量、动量与吸收发射](chapters/ch02.md)
- [第 3 章　相干性：从单光子到激光](chapters/ch03.md)
- [第 4 章　从光子到辐亮度：渲染为什么能用经典量](chapters/ch04.md)
- [第 5 章　一个错误的颜色](chapters/ch05.md)
- [第 6 章　光、波长与辐亮度](chapters/ch06.md)
- [第 7 章　人眼与色匹配函数](chapters/ch07.md)
- [第 8 章　RGB 渲染到底假设了什么](chapters/ch08.md)
- [第 9 章　光谱光传输](chapters/ch09.md)
- [第 10 章　波长作为随机变量](chapters/ch10.md)
- [第 11 章　Hero Wavelength 采样](chapters/ch11.md)
- [第 12 章　从 RGB 到光谱：上采样与基分解](chapters/ch12.md)
- [第 13 章　色散](chapters/ch13.md)
- [第 14 章　介质中的光谱传输](chapters/ch14.md)
- [第 15 章　荧光与波长变换](chapters/ch15.md)
- [第 16 章　偏振接口](chapters/ch16.md)
- [第 17 章　一个最小的光谱路径追踪器](chapters/ch17.md)
- [第 18 章　验证、性能与完整场景](chapters/ch18.md)
- [第 19 章　神经基底：把 RGB 映射成一条谱线](chapters/ch19.md)
- [第 20 章　训练、验证与接进渲染器](chapters/ch20.md)

### 附录

- [附录 A　符号与单位](appendix/app_a.md)
- [附录 B　数值速查](appendix/app_b.md)
- [附录 C　参考文献](appendix/app_c.md)

---

[返回系列首页](../../README.md)
