# 体素渲染

> 稀疏体素、体素化、锥追踪与体素光照

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/rendering-06-voxel.pdf)

体素是一种取舍：把连续的几何换成离散的格子，换取查询速度和全局光照的可行性。代价是表面变糙、法线丢失、细节被平均掉。 这本书讲体素的表示与存储、体素化怎么做才不漏面、锥追踪怎么估全局光照、体素表面怎么重建法线，以及大规模场景下的流式与压缩。

共 9 章 · 58 页

[从第 1 章开始](chapters/ch01.md)　·　<a href="../../output/rendering-06-voxel.pdf" target="_blank" rel="noopener" data-router-ignore>下载本册 PDF</a>

## 目录

- [前言](front/preface.md)
- [第 1 章　把连续几何切成格子](chapters/ch01.md)
- [第 2 章　体素的存储结构](chapters/ch02.md)
- [第 3 章　体素化](chapters/ch03.md)
- [第 4 章　体素锥追踪](chapters/ch04.md)
- [第 5 章　体素上的光传播](chapters/ch05.md)
- [第 6 章　距离场与体素的混合](chapters/ch06.md)
- [第 7 章　从占据率重建表面](chapters/ch07.md)
- [第 8 章　大规模场景的分块与流式](chapters/ch08.md)
- [第 9 章　体素与路径追踪的接缝](chapters/ch09.md)

### 附录

- [附录 A　符号表](appendix/app_a.md)
- [附录 B　体素方案对比](appendix/app_b.md)
- [附录 C　参考文献](appendix/app_c.md)

---

[返回系列首页](../../README.md)
