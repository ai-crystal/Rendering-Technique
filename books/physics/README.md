# 从初高中物理到麦克斯韦方程组

**专业级渲染技术 · 基础篇**　·　一步一步推出电磁场

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/v11-physics.pdf)

---

这本书假设你只记得中学物理：速度、力、欧姆定律、左手定则。从这些出发，一步一步推到麦克斯韦方程组，中间不跳步，每引入一个新量都先说清它要解决什么问题。
路线是：运动与力、功与能、电荷与库仑定律、电场与电势、电流与电路、磁场与安培环路、电磁感应与电感，然后补上矢量分析（梯度、散度、旋度与两个积分定理），最后用位移电流把四个方程补齐，并从中解出电磁波。

## 目录

**第一篇　运动与能量**

- [第 1 章 物理量、单位与量纲](#/books/physics/chapters/ch01)
- [第 2 章 运动的描述：位置、速度、加速度](#/books/physics/chapters/ch02)
- [第 3 章 牛顿三定律与受力分析](#/books/physics/chapters/ch03)
- [第 4 章 功、能量与动量](#/books/physics/chapters/ch04)

**第二篇　电荷与电场**

- [第 5 章 电荷、库仑定律与叠加原理](#/books/physics/chapters/ch05)
- [第 6 章 电场强度、电场线与电偶极子](#/books/physics/chapters/ch06)
- [第 7 章 电通量与高斯定理](#/books/physics/chapters/ch07)
- [第 8 章 电势能、电势与等势面](#/books/physics/chapters/ch08)
- [第 9 章 电势与场强的微分关系](#/books/physics/chapters/ch09)
- [第 10 章 电容、电容器与电场能量](#/books/physics/chapters/ch10)

**第三篇　电流**

- [第 11 章 电流、电阻与欧姆定律的微观图像](#/books/physics/chapters/ch11)
- [第 12 章 电动势、电路与基尔霍夫定律](#/books/physics/chapters/ch12)
- [第 13 章 焦耳热、电功率与能量转换](#/books/physics/chapters/ch13)

**第四篇　磁场**

- [第 14 章 磁现象、磁感应强度与磁通量](#/books/physics/chapters/ch14)
- [第 15 章 电流的磁场：毕奥–萨伐尔定律](#/books/physics/chapters/ch15)
- [第 16 章 安培环路定理](#/books/physics/chapters/ch16)
- [第 17 章 磁场对电流与运动电荷的作用](#/books/physics/chapters/ch17)
- [第 18 章 磁介质、磁化与磁场强度 H](#/books/physics/chapters/ch18)

**第五篇　电磁感应**

- [第 19 章 法拉第电磁感应定律](#/books/physics/chapters/ch19)
- [第 20 章 楞次定律、涡流与能量](#/books/physics/chapters/ch20)
- [第 21 章 自感、互感与磁场能量](#/books/physics/chapters/ch21)

**第六篇　场与方程**

- [第 22 章 矢量场：通量、环量与两个积分定理](#/books/physics/chapters/ch22)
- [第 23 章 梯度、散度、旋度](#/books/physics/chapters/ch23)
- [第 24 章 微分形式的电磁定律](#/books/physics/chapters/ch24)
- [第 25 章 位移电流](#/books/physics/chapters/ch25)
- [第 26 章 麦克斯韦方程组](#/books/physics/chapters/ch26)
- [第 27 章 电磁波、光速与能流](#/books/physics/chapters/ch27)
- [第 28 章 单位制、边界条件与总结](#/books/physics/chapters/ch28)

## 重新生成

双击仓库根目录的 `build-physics.bat`，或运行：

```text
python books/build/build.py --book physics
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
