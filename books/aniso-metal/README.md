# 各向异性金属

**专业级渲染技术 · 专题五**　·　从复折射率到拉丝高光

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/rendering-05-aniso-metal.pdf)

---

金属的反射率随波长变化，这不是调色能还原的：铜偏红、金偏黄、铝几乎中性，原因是自由电子对不同频率的响应不同。更麻烦的是拉丝表面——高光被拉成一条线，而不是一个圆斑。
这本书从复折射率与导体 Fresnel 出发，把微表面理论推广到各向异性，再讲拉丝、锤纹、氧化层与薄膜，最后落到实时管线里能用的近似。

## 目录

**第一篇　界面**

- [第 1 章 金属的光学](#/books/aniso-metal/chapters/ch01)
- [第 2 章 导体 Fresnel 与 F0](#/books/aniso-metal/chapters/ch02)

**第二篇　微表面**

- [第 3 章 各向异性微表面](#/books/aniso-metal/chapters/ch03)
- [第 4 章 切线空间与拉伸的高光](#/books/aniso-metal/chapters/ch04)
- [第 5 章 多次散射下的各向异性](#/books/aniso-metal/chapters/ch05)

**第三篇　工艺、薄膜与实现**

- [第 6 章 拉丝、锤纹与测量](#/books/aniso-metal/chapters/ch06)
- [第 7 章 氧化层与薄膜](#/books/aniso-metal/chapters/ch07)
- [第 8 章 实时近似](#/books/aniso-metal/chapters/ch08)
- [第 9 章 验证](#/books/aniso-metal/chapters/ch09)

## 重新生成

双击仓库根目录的 `build-aniso-metal.bat`，或运行：

```text
python books/build/build.py --book aniso-metal
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
