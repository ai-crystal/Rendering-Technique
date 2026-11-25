# 毛发渲染

> Marschner 模型、双散射、远距离 LOD 与采样

作者：Dr. Dezeming　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>　　下载：[整本 PDF](https://github.com/ai-crystal/Rendering-Technique/raw/main/output/rendering-02-hair.pdf)

毛发的高光为什么有两道？为什么逆光时整头头发会亮起来？答案在纤维的同心结构里：角质层、皮层、髓质，各自折射率不同，光线在里面走 R、TT、TRT 三条路。 这本书从 Kajiya–Kay 讲到 Marschner，再讲生产里真正用的双散射与远距离 LOD，最后把毛发当成一种极细的参与介质重新看一遍。

共 10 章 · 64 页

[从第 1 章开始](chapters/ch01.md)　·　<a href="../../output/rendering-02-hair.pdf" target="_blank" rel="noopener" data-router-ignore>下载本册 PDF</a>

## 目录

- [前言](front/preface.md)
- [第 1 章　毛发的结构与光学](chapters/ch01.md)
- [第 2 章　Kajiya–Kay：把纤维当一根细圆柱](chapters/ch02.md)
- [第 3 章　Marschner 的 R、TT、TRT](chapters/ch03.md)
- [第 4 章　方位角分布与纵向粗糙度](chapters/ch04.md)
- [第 5 章　多次散射与双散射](chapters/ch05.md)
- [第 6 章　重要性采样](chapters/ch06.md)
- [第 7 章　毛发作为介质](chapters/ch07.md)
- [第 8 章　路径追踪实现](chapters/ch08.md)
- [第 9 章　参数标定与美术控制](chapters/ch09.md)
- [第 10 章　验证](chapters/ch10.md)

### 附录

- [附录 A　符号表](appendix/app_a.md)
- [附录 B　毛发参数速查](appendix/app_b.md)
- [附录 C　参考文献](appendix/app_c.md)

---

[返回系列首页](../../README.md)
