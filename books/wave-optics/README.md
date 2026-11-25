# 波动光学渲染

**专业级渲染技术 · 专题七**　·　从衍射到结构色

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](../../output/rendering-07-wave-optics.pdf)

---

肥皂泡的彩色、孔雀羽毛的蓝、CD 背面的彩虹，都不是颜料造成的。它们的颜色来自干涉与衍射——光的相位在起作用，而几何光学里没有相位这个量。
这本书从标量衍射讲到多层膜传输矩阵，从光栅讲到结构色，再把偏振与 Mueller 矩阵接进 BSDF，最后讨论波动光学怎么和路径追踪结合。

## 目录

**第一篇　几何光学的边界**

- [第 1 章 当尺度接近波长](#/books/wave-optics/chapters/ch01)
- [第 2 章 相位、相干与干涉](#/books/wave-optics/chapters/ch02)
- [第 3 章 标量衍射与 Kirchhoff 近似](#/books/wave-optics/chapters/ch03)

**第二篇　薄膜与结构色**

- [第 4 章 单层薄膜干涉与 Airy 公式](#/books/wave-optics/chapters/ch04)
- [第 5 章 多层膜传输矩阵](#/books/wave-optics/chapters/ch05)
- [第 6 章 衍射光栅与结构色](#/books/wave-optics/chapters/ch06)
- [第 7 章 微表面与衍射的结合](#/books/wave-optics/chapters/ch07)

**第三篇　偏振与实现**

- [第 8 章 偏振、Stokes 向量与 Mueller 矩阵](#/books/wave-optics/chapters/ch08)
- [第 9 章 BSDF 的 Mueller 形式与偏振路径追踪](#/books/wave-optics/chapters/ch09)
- [第 10 章 实现、验证与性能](#/books/wave-optics/chapters/ch10)
- [附录 A　符号与公式速查](#/books/wave-optics/appendix/app_a)
- [附录 B　参考文献](#/books/wave-optics/appendix/app_b)
- [后记](#/books/wave-optics/front/afterword)
- [backcover](#/books/wave-optics/front/backcover)

## 重新生成

双击仓库根目录的 `build-wave-optics.bat`，或运行：

```text
python books/build/build.py --book wave-optics
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
