# 布料渲染

**专业级渲染技术 · 专题一**　·　从纤维、纱线到织物

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/v2-cloth.pdf)

---

织物不是一种材质，而是纤维、纱线、编织三级结构共同产生的结果。单看一根纤维是圆柱散射，单看一根纱线是带绒毛的粗糙表面，放大到织物又出现编织方向与透光。
这本书沿着这三级结构往上走：从圆柱散射讲到 Karis 的纱线级模型，再讲 sheen、绒面、薄织物透射和染色，最后给出一个能放进路径追踪器、能量对得上的实现。

## 目录

**第一篇　三个尺度**

- [第 1 章 一块布为什么不能用一个 BRDF](#/books/cloth/chapters/ch01)
- [第 2 章 织物的几何](#/books/cloth/chapters/ch02)
- [第 3 章 圆柱散射与 Kajiya–Kay 模型](#/books/cloth/chapters/ch03)

**第二篇　纱线与编织**

- [第 4 章 Marschner 模型搬到布料上](#/books/cloth/chapters/ch04)
- [第 5 章 纱线级散射与 micro-flake](#/books/cloth/chapters/ch05)
- [第 6 章 编织感知的 BRDF 与 sheen](#/books/cloth/chapters/ch06)

**第三篇　厚度与颜色**

- [第 7 章 绒面与天鹅绒](#/books/cloth/chapters/ch07)
- [第 8 章 薄织物透射](#/books/cloth/chapters/ch08)
- [第 9 章 染色与 Kubelka–Munk](#/books/cloth/chapters/ch09)

**第四篇　实现与验证**

- [第 10 章 实时近似与能量补偿](#/books/cloth/chapters/ch10)
- [第 11 章 参数标定与资产](#/books/cloth/chapters/ch11)
- [第 12 章 验证与对比](#/books/cloth/chapters/ch12)

## 重新生成

双击仓库根目录的 `build-cloth.bat`，或运行：

```text
python books/build/build.py --book cloth
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
