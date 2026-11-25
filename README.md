# 专业级渲染技术

> 一套写给渲染实现者的材质专题书

这套书假设你已经写过一个能跑的光线追踪器，知道射线求交、着色和蒙特卡洛积分怎么工作，也见过 BRDF 和渲染方程。它不再教怎么打第一条光线，而是集中在材质这一层最容易含糊的地方：一个材质为什么长成那个公式，公式里的每一项在物理上对应什么，换到另一种材料上哪些假设会碎掉。

入门篇搭起后面各册共用的骨架：Fresnel、微表面三段式、能量补偿、分层、采样与验证。专题册各自深入一种材料或一种光学现象，彼此独立，可以从任意一本读起。

作者：Dr. Dezeming　·　2026

**在线阅读**：[在线阅读站](https://ai-crystal.github.io/Rendering-Technique/)　·　**仓库**：[GitHub 仓库](https://github.com/ai-crystal/Rendering-Technique)

## 分册

| 册 | 书名 | 一句话 | 页数 | 在线阅读 | PDF |
| --- | --- | --- | ---: | --- | --- |
| 01 | [材质渲染的骨架](books/beginner/README.md) | 微表面、Fresnel、能量补偿、分层与采样 | 77 | [阅读](books/beginner/README.md) | <a href="output/rendering-00-beginner.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 02 | [布料渲染](books/cloth/README.md) | 纤维散射、纱线模型、sheen 与薄织物透射 | 79 | [阅读](books/cloth/README.md) | <a href="output/rendering-01-cloth.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 03 | [毛发渲染](books/hair/README.md) | Marschner 模型、双散射、远距离 LOD 与采样 | 64 | [阅读](books/hair/README.md) | <a href="output/rendering-02-hair.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 04 | [次表面散射与 BSSRDF](books/sss/README.md) | 辐射传输、扩散近似、偶极子、随机游走 | 112 | [阅读](books/sss/README.md) | <a href="output/rendering-03-sss.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 05 | [光谱渲染](books/spectral/README.md) | 光子与相干、上采样、神经基底、色散与荧光 | 126 | [阅读](books/spectral/README.md) | <a href="output/rendering-04-spectral.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 06 | [各向异性金属](books/aniso-metal/README.md) | 复折射率、各向异性 GGX、拉丝与氧化层 | 59 | [阅读](books/aniso-metal/README.md) | <a href="output/rendering-05-aniso-metal.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 07 | [体素渲染](books/voxel/README.md) | 稀疏体素、体素化、锥追踪与体素光照 | 58 | [阅读](books/voxel/README.md) | <a href="output/rendering-06-voxel.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 08 | [波动光学渲染](books/wave-optics/README.md) | 衍射、薄膜干涉、结构色与偏振 | 71 | [阅读](books/wave-optics/README.md) | <a href="output/rendering-07-wave-optics.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 09 | [基于储蓄池的渲染](books/reservoir/README.md) | MIS、带权蓄水池、RIS、ReSTIR 与 GRIS | 94 | [阅读](books/reservoir/README.md) | <a href="output/rendering-08-reservoir.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |

## 怎么读

- 入门篇建议按顺序读完，它是后面所有册的公共语言。
- 做布料就读布料册，做毛发就读毛发册；需要的微表面结论在入门篇第 4 到第 7 章。
- 系列内的符号、参数名和代码约定保持一致：消光系数、粗糙度与 BSDF 不随分册换写法。

## 许可

本系列文字与插图采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可发布，转载请注明作者与出处。书中引用的论文、数据集与模型归各自作者所有。

---

作者：Dr. Dezeming　·　2026
