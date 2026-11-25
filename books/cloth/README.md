# 布料渲染

> 纤维散射、纱线模型、sheen 与薄织物透射

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/rendering-01-cloth.pdf)

织物不是一种材质，而是纤维、纱线、编织三级结构共同产生的结果。单看一根纤维是圆柱散射，单看一根纱线是带绒毛的粗糙表面，放大到织物又出现编织方向与透光。 这本书沿着这三级结构往上走：从圆柱散射讲到 Karis 的纱线级模型，再讲 sheen、绒面、薄织物透射和染色，最后给出一个能放进路径追踪器、能量对得上的实现。

共 12 章 · 79 页

[从第 1 章开始](chapters/ch01.md)　·　<a href="../../output/rendering-01-cloth.pdf" target="_blank" rel="noopener" data-router-ignore>下载本册 PDF</a>

## 目录

- [前言](front/preface.md)
- [第 1 章　一块布为什么不能用一个 BRDF](chapters/ch01.md)
- [第 2 章　织物的几何](chapters/ch02.md)
- [第 3 章　圆柱散射与 Kajiya–Kay 模型](chapters/ch03.md)
- [第 4 章　Marschner 模型搬到布料上](chapters/ch04.md)
- [第 5 章　纱线级散射与 micro-flake](chapters/ch05.md)
- [第 6 章　编织感知的 BRDF 与 sheen](chapters/ch06.md)
- [第 7 章　绒面与天鹅绒](chapters/ch07.md)
- [第 8 章　薄织物透射](chapters/ch08.md)
- [第 9 章　染色与 Kubelka–Munk](chapters/ch09.md)
- [第 10 章　实时近似与能量补偿](chapters/ch10.md)
- [第 11 章　参数标定与资产](chapters/ch11.md)
- [第 12 章　验证与对比](chapters/ch12.md)

### 附录

- [附录 A　符号表](appendix/app_a.md)
- [附录 B　布料参数速查](appendix/app_b.md)
- [附录 C　参考文献](appendix/app_c.md)

---

[返回系列首页](../../README.md)
