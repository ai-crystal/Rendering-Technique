# 附录 C　参考文献

按作者姓氏的字母顺序排列。后面标出这本书里用到它的地方。

Akenine-Möller, T. "Fast 3D Triangle-Box Overlap Testing." *Journal of Graphics Tools*, 6(1), 2001.
第 3 章的保守覆盖用到的分离轴测试。文章给了三角形与轴对齐方盒之间需要检查的十三根轴，以及提前退出的写法。

Amanatides, J., Woo, A. "A Fast Voxel Traversal Algorithm for Ray Tracing." *Eurographics*, 1987.
第 2 章与第 9 章的 DDA 遍历。每一格只做一次比较和一次加法，是稠密网格求交的标准做法。

Crassin, C., Neyret, F., Lefebvre, S., Eisemann, E. "GigaVoxels: Ray-Guided Streaming for Efficient and Detailed Voxel Rendering." *I3D*, 2009.
第 8 章的按需加载。射线驱动流式的原始出处，也给出了"每一帧用现有数据做到最好"的渐进策略。

Crassin, C., Neyret, F., Sainz, M., Green, S., Eisemann, E. "Interactive Indirect Illumination Using Voxel Cone Tracing." *Pacific Graphics*（*Computer Graphics Forum* 30(7)）, 2011.
第 4 章的锥追踪。锥的半径、mip 层级的选择、六条锥覆盖半球的做法都来自这篇。

Gibson, S. F. F. "Constrained Elastic Surface Nets: Generating Smooth Surfaces from Binary Volumetric Data." *MICCAI*, 1998.
第 7 章的 surface nets。每个格子一个顶点，顶点位置取边交点的平均。

Greger, G., Shirley, P., Hubbard, P. M., Greenberg, D. P. "The Irradiance Volume." *IEEE Computer Graphics and Applications*, 18(2), 1998.
第 5 章的辐照度体积。文中明确指出单标量会在方向性光下失效，需要用球谐。

Hart, J. C. "Sphere Tracing: A Geometric Method for the Antialiased Ray Tracing of Implicit Surfaces." *The Visual Computer*, 12(10), 1996.
第 6 章的球体步进。步长等于距离场值，保证不跳过表面。

Hoetzlein, R. K. "GVDB: Raytracing Sparse Voxel Database Structures on the GPU." *High Performance Graphics*, 2016.
第 2 章与第 8 章的砖块池。树的上半部分是稀疏指针，下半部分是自由分配的 $8^3$ 砖块。

Ju, T., Losasso, F., Schaefer, S., Warren, J. "Dual Contouring of Hermite Data." *SIGGRAPH*, 2002.
第 7 章的对偶方法。用二次误差函数把顶点拉向特征，恢复 surface nets 磨掉的锐利边缘。

Kämpe, V., Sintorn, E., Assarsson, U. "High Resolution Sparse Voxel DAGs." *SIGGRAPH*（*ACM Transactions on Graphics* 32(4)）, 2013.
第 2 章与第 8 章的 DAG 压缩。相同子树合并，节点用哈希去重，建筑场景常有一个数量级的压缩。

Laine, S., Karras, T. "Efficient Sparse Voxel Octrees." *I3D*, 2010；扩展版 *IEEE Transactions on Visualization and Computer Graphics*, 17(8), 2011.
第 2 章的节点编码。每个节点两个 32 位字，整个结构可以完全用整数数组表示。

Lorensen, W. E., Cline, H. E. "Marching Cubes: A High Resolution 3D Surface Construction Algorithm." *SIGGRAPH*, 1987.
第 7 章的等值面提取。八位模式查表，十五种基本构型。

Ramamoorthi, R., Hanrahan, P. "An Efficient Representation for Irradiance Environment Maps." *SIGGRAPH*, 2001.
第 5 章的球谐系数。clamped cosine 在球谐域是对角的，前三个卷积系数为 $\pi$、$2\pi/3$ 与 $\pi/4$，可以直接用来由辐亮度重建辐照度。

Villanueva, A. J., Marton, F., Gobbetti, E. "SSVDAGs: Symmetry-Aware Sparse Voxel DAGs." *I3D*, 2016.
第 2 章提到的对称性压缩。把镜像和旋转等价的子树也合并，比单纯去重再省一截。

## 说明

书里还有几处提到别人的工作但没有单列条目，比如 GPU 硬件光栅化器做体素化的做法（第 3 章），因为原始材料是厂商文档与会议演讲，没有可引的期刊版本。这类内容只写成"工业实现常用"，不给具体出处。

插图全部由书中脚本按公式计算，没有引用外部数据。正文里出现的实测数字（比如噪声曲线、锥追踪的步数）都是脚本跑出来的，脚本在 `books/code/voxel/` 下，参数写在脚本里。

有几种常见的说法这本书没有采用，理由一并写在这里，免得读者以为遗漏。一是"体素分辨率每翻一倍，内存涨八倍"，这句话对稠密网格成立，对表面稀疏结构是四倍，对 DAG 更少，笼统地说八倍会误导。二是"锥追踪没有噪点"，它确实没有随机噪点，但有系统性偏差，这本书把它当作偏差来讨论而不是当作优点。三是"距离场一定比体素准"，这只在距离场是精确距离时成立，从占据率算出来的距离场精度受限于占据率。
