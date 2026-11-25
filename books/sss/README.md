# 次表面散射与 BSSRDF

> 辐射传输、扩散近似、偶极子、随机游走

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/rendering-03-sss.pdf)

从一束照在蜡上的光开始，这本书把次表面散射拆成可以逐步推导的问题：光在介质里怎样被吸收与散射，辐射传输方程为什么解不动，扩散近似在什么条件下成立，偶极子公式又是怎样从一次求导里长出来的。 读完可以自己从方程推到代码，也能判断一个模型在什么物体上不再适用。

共 22 章 · 112 页

[从第 1 章开始](chapters/ch01.md)　·　<a href="../../output/rendering-03-sss.pdf" target="_blank" rel="noopener" data-router-ignore>下载本册 PDF</a>

## 目录

- [前言](front/preface.md)
- [第 1 章　为什么 BRDF 不够用](chapters/ch01.md)
- [第 2 章　辐射度量学：把"多少光"说清楚](chapters/ch02.md)
- [第 3 章　BSSRDF 的定义、量纲与渲染方程](chapters/ch03.md)
- [第 4 章　吸收、散射与 Beer–Lambert](chapters/ch04.md)
- [第 5 章　相函数与相似关系](chapters/ch05.md)
- [第 6 章　辐射传输方程](chapters/ch06.md)
- [第 7 章　单次散射](chapters/ch07.md)
- [第 8 章　多次散射与扩散理论的出场](chapters/ch08.md)
- [第 9 章　球谐展开与 P1 近似](chapters/ch09.md)
- [第 10 章　Fick 定律与扩散方程](chapters/ch10.md)
- [第 11 章　Green 函数](chapters/ch11.md)
- [第 12 章　边界条件与外推边界](chapters/ch12.md)
- [第 13 章　偶极子](chapters/ch13.md)
- [第 14 章　从径向剖面到完整 BSSRDF](chapters/ch14.md)
- [第 15 章　扩散在哪里失效](chapters/ch15.md)
- [第 16 章　多极子与薄层](chapters/ch16.md)
- [第 17 章　量化扩散与归一化剖面](chapters/ch17.md)
- [第 18 章　方向偶极子](chapters/ch18.md)
- [第 19 章　随机游走：不做近似的做法](chapters/ch19.md)
- [第 20 章　表面积分与采样器](chapters/ch20.md)
- [第 21 章　从旋钮到参数：多层皮肤、光谱与毛发](chapters/ch21.md)
- [第 22 章　实时近似、验证与调试](chapters/ch22.md)

### 附录

- [附录 A　符号表](appendix/app_a.md)
- [附录 B　公式速查](appendix/app_b.md)
- [附录 C　参考文献](appendix/app_c.md)
- [附录 D　术语对照](appendix/app_d.md)

---

[返回系列首页](../../README.md)
