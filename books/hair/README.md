# 毛发渲染

**专业级渲染技术 · 专题二**　·　从一根纤维到一头头发

作者：Dr. Dezeming　　在线阅读 <https://dezeming.github.io/RenderingSeries/>　　下载：[整本 PDF](../../output/rendering-02-hair.pdf)

---

毛发的高光为什么有两道？为什么逆光时整头头发会亮起来？答案在纤维的同心结构里：角质层、皮层、髓质，各自折射率不同，光线在里面走 R、TT、TRT 三条路。
这本书从 Kajiya–Kay 讲到 Marschner，再讲生产里真正用的双散射与远距离 LOD，最后把毛发当成一种极细的参与介质重新看一遍。

## 目录

**第一篇　一根纤维**

- [第 1 章 毛发的结构与光学](#/books/hair/chapters/ch01)
- [第 2 章 Kajiya–Kay：把纤维当一根细圆柱](#/books/hair/chapters/ch02)
- [第 3 章 Marschner 的 R、TT、TRT](#/books/hair/chapters/ch03)
- [第 4 章 方位角分布与纵向粗糙度](#/books/hair/chapters/ch04)

**第二篇　一束纤维**

- [第 5 章 多次散射与双散射](#/books/hair/chapters/ch05)
- [第 6 章 重要性采样](#/books/hair/chapters/ch06)
- [第 7 章 毛发作为介质](#/books/hair/chapters/ch07)

**第三篇　一头头发**

- [第 8 章 路径追踪实现](#/books/hair/chapters/ch08)
- [第 9 章 参数标定与美术控制](#/books/hair/chapters/ch09)
- [第 10 章 验证](#/books/hair/chapters/ch10)
- [附录 A　符号表](#/books/hair/appendix/app_a)
- [附录 B　毛发参数速查](#/books/hair/appendix/app_b)
- [附录 C　参考文献](#/books/hair/appendix/app_c)
- [后记](#/books/hair/front/afterword)
- [backcover](#/books/hair/front/backcover)

## 重新生成

双击仓库根目录的 `build-hair.bat`，或运行：

```text
python books/build/build.py --book hair
```

## 关于插图

所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。
