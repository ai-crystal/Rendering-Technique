# 符号距离场与渲染

**专业级渲染技术 · 专题九**　·　从距离函数到光线步进与全局光照

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/rendering-09-sdf.pdf)

---

距离场把几何换成一个标量函数：每个点存到最近表面的距离，符号表示在里还是在外。这个替换让求交变成求零点、让布尔运算变成取最小值、让圆角与变形变成一次加法。
这本书从距离函数的定义讲起，经解析 SDF、布尔与平滑组合、光线步进与法线、软阴影与环境光遮蔽，到体积渲染与锥追踪全局光照，最后讲网格怎么转成 SDF、怎么压缩与怎么接进路径追踪器。

## 目录

**第一篇　距离是什么**

- [第 1 章 从几何到函数](#/books/sdf/chapters/ch01)
- [第 2 章 有符号距离的定义与性质](#/books/sdf/chapters/ch02)
- [第 3 章 常见形状的解析 SDF](#/books/sdf/chapters/ch03)
- [第 4 章 导数：法线、曲率与有限差分](#/books/sdf/chapters/ch04)

**第二篇　用距离做造型**

- [第 5 章 布尔运算](#/books/sdf/chapters/ch05)
- [第 6 章 平滑并集](#/books/sdf/chapters/ch06)
- [第 7 章 域变换](#/books/sdf/chapters/ch07)
- [第 8 章 圆角、倒角与壳体](#/books/sdf/chapters/ch08)
- [第 9 章 精确与近似](#/books/sdf/chapters/ch09)

**第三篇　渲染**

- [第 10 章 光线步进](#/books/sdf/chapters/ch10)
- [第 11 章 法线、环境光遮蔽与软阴影](#/books/sdf/chapters/ch11)
- [第 12 章 SDF 与体积渲染](#/books/sdf/chapters/ch12)
- [第 13 章 锥追踪与全局光照](#/books/sdf/chapters/ch13)

**第四篇　数据**

- [第 14 章 从网格生成 SDF](#/books/sdf/chapters/ch14)
- [第 15 章 数据结构与压缩](#/books/sdf/chapters/ch15)
- [第 16 章 接进路径追踪](#/books/sdf/chapters/ch16)

**第五篇　边界**

- [第 17 章 神经 SDF 与可微表示](#/books/sdf/chapters/ch17)
- [第 18 章 表示的选择](#/books/sdf/chapters/ch18)

## 重新生成

双击仓库根目录的 `build-sdf.bat`，或运行：

```text
python books/build/build.py --book sdf
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
