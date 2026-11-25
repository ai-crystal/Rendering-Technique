# 材质渲染的骨架

**专业级渲染技术 · 入门篇**　·　从光线追踪器到可用的材质系统

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/rendering-00-beginner.pdf)

---

一个材质为什么长成那个公式，公式里每一项在物理上对应什么，换一种材料时哪一条假设先碎——这是后面八册反复要问的三个问题。
入门篇把公共语言搭起来：Fresnel、微表面三段式、丢失的能量、分层界面、采样与验证。读完能自己写出一个能量守恒、能被采样的 BSDF，也知道怎么证明它是对的。

## 目录

**第一篇　材质的语言**

- [第 1 章 从光线追踪器到材质系统](#/books/beginner/chapters/ch01)
- [第 2 章 BSDF、渲染方程与互易性](#/books/beginner/chapters/ch02)
- [第 3 章 Fresnel：界面上的第一道门](#/books/beginner/chapters/ch03)

**第二篇　微表面**

- [第 4 章 微表面理论（一）：把粗糙表面拆成小镜子](#/books/beginner/chapters/ch04)
- [第 5 章 微表面理论（二）：遮蔽与 Smith 模型](#/books/beginner/chapters/ch05)
- [第 6 章 微表面理论（三）：Cook–Torrance 完整形式](#/books/beginner/chapters/ch06)
- [第 7 章 掉下去的能量：多重散射微表面](#/books/beginner/chapters/ch07)

**第三篇　界面之间**

- [第 8 章 折射、透射与粗糙界面](#/books/beginner/chapters/ch08)
- [第 9 章 分层材质：涂层、清漆与薄膜](#/books/beginner/chapters/ch09)

**第四篇　落到代码**

- [第 10 章 采样 BSDF：把积分变成代码](#/books/beginner/chapters/ch10)
- [第 11 章 参数化：从美术旋钮到物理量](#/books/beginner/chapters/ch11)
- [第 12 章 验证：白炉、互易性与参考对比](#/books/beginner/chapters/ch12)

**第五篇　边界**

- [第 13 章 光谱与偏振：材质的另外两个维度](#/books/beginner/chapters/ch13)
- [第 14 章 材质系统：把公式组织起来](#/books/beginner/chapters/ch14)

## 重新生成

双击仓库根目录的 `build-beginner.bat`，或运行：

```text
python books/build/build.py --book beginner
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
