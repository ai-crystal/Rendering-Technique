# 专业级渲染技术

**一套写给渲染实现者的材质专题书**　·　Dr. Dezeming

在线阅读：<https://dezeming.github.io/RenderingSeries/>

---

这套书假设你已经写过一个能跑的光线追踪器，知道射线求交、着色和蒙特卡洛积分怎么工作，也见过 BRDF 和渲染方程。它不打算再教一遍怎么打第一条光线，而是集中在“材质”这一层最容易含糊的地方：一个材质为什么长成那个公式，公式里的每一项在物理上对应什么，换到另一种材料上哪些假设会碎掉。

入门篇把后面几册共用的骨架搭起来：Fresnel、微表面三段式、能量补偿、分层、采样与验证。各专题册再各自深入一种材料或一种光学现象，彼此独立，可以从任意一本读起。

光谱那一册从普朗克讲起，把量子描述、相干性、辐亮度、光谱渲染、RGB 看成层层收紧的近似；蓄水池那一册从 MIS 与带权蓄水池讲起，前半本是可以独立读的采样理论。

## 分册

| 册 | 书名 | 一句话 | 页数 | 阅读 | PDF |
| --- | --- | --- | --- | --- | --- |
| 00 | 材质渲染的骨架 | 微表面、Fresnel、能量补偿、分层与采样 | 77 | [阅读](books/beginner/README.md) | [下载](output/rendering-00-beginner.pdf) |
| 01 | 布料渲染 | 纤维散射、纱线模型、sheen 与薄织物透射 | 79 | [阅读](books/cloth/README.md) | [下载](output/rendering-01-cloth.pdf) |
| 02 | 毛发渲染 | Marschner 模型、双散射、远距离 LOD 与采样 | 64 | [阅读](books/hair/README.md) | [下载](output/rendering-02-hair.pdf) |
| 03 | 次表面散射与 BSSRDF | 辐射传输、扩散近似、偶极子、随机游走 | 111 | [阅读](books/sss/README.md) | [下载](output/rendering-03-sss.pdf) |
| 04 | 光谱渲染 | 光子与相干、上采样、神经基底、色散与荧光 | 125 | [阅读](books/spectral/README.md) | [下载](output/rendering-04-spectral.pdf) |
| 05 | 各向异性金属 | 复折射率、各向异性 GGX、拉丝与氧化层 | 59 | [阅读](books/aniso-metal/README.md) | [下载](output/rendering-05-aniso-metal.pdf) |
| 06 | 体素渲染 | 稀疏体素、体素化、锥追踪与体素光照 | 58 | [阅读](books/voxel/README.md) | [下载](output/rendering-06-voxel.pdf) |
| 07 | 波动光学渲染 | 衍射、薄膜干涉、结构色与偏振 | 71 | [阅读](books/wave-optics/README.md) | [下载](output/rendering-07-wave-optics.pdf) |
| 08 | 基于储蓄池的渲染 | MIS、带权蓄水池、RIS、ReSTIR 与 GRIS | 94 | [阅读](books/reservoir/README.md) | [下载](output/rendering-08-reservoir.pdf) |

## 怎么读

入门篇建议按顺序读完，它是后面所有册的公共语言。专题册之间没有依赖，做布料就读布料那一册，做毛发就读毛发那一册，需要的微表面结论在入门篇第 4 到第 7 章。

系列内的符号、参数名和代码约定保持一致：$σ_t$ 始终表示消光系数，$α$ 始终是粗糙度，$f_r$ 始终是 BSDF，不随分册换写法。

## 仓库结构

```text
books/
  build/          构建脚本，全系列共用
  code/           插图脚本，按册、按章分目录
  common/         共用样式与封面生成
  <册名>/
    book.json     这一册的元数据
    structure.json  章节顺序
    chapters/     正文
    front/        封面、扉页、前言、篇首、后记
    images/       插图，按章分目录
output/           各册 PDF
```

## 重新生成

双击 `build-<册名>.bat` 只编那一册；`build.bat` 编译全部；`build.bat figures` 只重画插图。

## 关于插图

所有插图由 `books/code/` 下的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比曲线一律由书中给出的公式算出。
