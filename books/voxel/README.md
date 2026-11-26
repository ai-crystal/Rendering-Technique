# 体素渲染

**专业级渲染技术 · 专题六**　·　从稀疏体素到锥追踪

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/v7-voxel.pdf)

---

体素是一种取舍：把连续的几何换成离散的格子，换取查询速度和全局光照的可行性。代价是表面变糙、法线丢失、细节被平均掉。
这本书讲体素的表示与存储、体素化怎么做才不漏面、锥追踪怎么估全局光照、体素表面怎么重建法线，以及大规模场景下的流式与压缩。

## 目录

**第一篇　格子里的世界**

- [第 1 章 把连续几何切成格子](#/books/voxel/chapters/ch01)
- [第 2 章 体素的存储结构](#/books/voxel/chapters/ch02)
- [第 3 章 体素化](#/books/voxel/chapters/ch03)

**第二篇　把光摊在格子上**

- [第 4 章 体素锥追踪](#/books/voxel/chapters/ch04)
- [第 5 章 体素上的光传播](#/books/voxel/chapters/ch05)
- [第 6 章 距离场与体素的混合](#/books/voxel/chapters/ch06)

**第三篇　回到表面与规模**

- [第 7 章 从占据率重建表面](#/books/voxel/chapters/ch07)
- [第 8 章 大规模场景的分块与流式](#/books/voxel/chapters/ch08)
- [第 9 章 体素与路径追踪的接缝](#/books/voxel/chapters/ch09)

## 重新生成

双击仓库根目录的 `build-voxel.bat`，或运行：

```text
python books/build/build.py --book voxel
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
