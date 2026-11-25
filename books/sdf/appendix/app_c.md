# 附录 C　参考文献

按作者姓氏的字母顺序排列，每条后面标出这本书里用到它的地方。

Bærentzen, J. A., Aanæs, H. "Signed Distance Computation Using the Angle Weighted Pseudonormal." *IEEE Transactions on Visualization and Computer Graphics*, 11(3), 2005.
第 14 章的符号判定。用角度加权的伪法线决定内外，比射线奇偶稳，对噪声网格更宽容。

Crassin, C., Neyret, F., Sainz, M., Green, S., Eisemann, E. "Interactive Indirect Illumination Using Voxel Cone Tracing." *Pacific Graphics*（*Computer Graphics Forum* 30(7)）, 2011.
第 13 章的锥追踪。锥的半径、层级的选择、六条锥覆盖半球的做法都来自这篇。

Felzenszwalb, P. F., Huttenlocher, D. P. "Distance Transforms of Sampled Functions." *Theory of Computing*, 8(19), 2012.
第 14 章的精确欧氏距离变换。可分离的一维变换与下包络的线性算法。

Gropp, A., Lempitsky, V., Vedaldi, A., Umetani, N. "Implicit Geometric Regularization for Learning Shapes." *ICML*, 2020.
第 17 章的 Eikonal 正则。用梯度长度为 1 的惩罚项在无真值时约束网络，是这一族方法的核心技巧。

Hart, J. C. "Sphere Tracing: A Geometric Method for the Antialiased Ray Tracing of Implicit Surfaces." *The Visual Computer*, 12(10), 1996.
第 10 章的球体追踪。步长等于距离场值，保证不跳过表面，这个算法的原始出处。

Jacobson, A., Kavan, L., Sorkine-Hornung, O. "Robust Inside-Outside Segmentation using Generalized Winding Numbers." *ACM Transactions on Graphics*（*SIGGRAPH*）, 32(4), 2013.
第 14 章的绕数判定。对自交与开口网格给出连续的内外划分。

Jones, M. W., Bærentzen, J. A., Srámek, M. "3D Distance Fields: A Survey of Techniques and Applications." *IEEE Transactions on Visualization and Computer Graphics*, 12(4), 2006.
第 1 章与第 14 章的整体框架。距离场的生成、存储与应用的一份综述。

Ju, T., Losasso, F., Schaefer, S., Warren, J. "Dual Contouring of Hermite Data." *ACM Transactions on Graphics*（*SIGGRAPH*）, 21(3), 2002.
第 17 章提取网格时的对照方法。用二次误差函数把顶点拉向特征，恢复 marching cubes 磨掉的锐边。

Laine, S., Karras, T. "Efficient Sparse Voxel Octrees." *I3D*, 2010；扩展版 *IEEE Transactions on Visualization and Computer Graphics*, 17(8), 2011.
第 15 章的八叉树编码。每个节点两个 32 位字，整个结构可以用整数数组表示。

Lorensen, W. E., Cline, H. E. "Marching Cubes: A High Resolution 3D Surface Construction Algorithm." *SIGGRAPH*, 1987.
第 17 章的等值面提取。八位模式查表，十五种基本构型。

Museth, K. "VDB: High-Resolution Sparse Volumes with Dynamic Topology." *ACM Transactions on Graphics*, 32(3), 2013.
第 15 章的稀疏体数据。树的上层是稀疏索引，下层是统一分辨率的叶节点，兼顾稀疏与缓存友好。

Park, J. J., Florence, P., Straub, J., Newcombe, R., Lovegrove, S. "DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation." *CVPR*, 2019.
第 17 章的神经距离场。自编码器式的训练与潜码表示。

Quilez, I. "Modeling with Distance Functions" 与 "Soft Shadows" 系列文章, iquilezles.org, 2008–2020.
第 3 章的解析形状、第 6 章的平滑最小值、第 8 章的算子、第 11 章的软阴影与环境光遮蔽近似，都参考了这些文章里的写法。

Wang, P., Liu, L., Liu, Y., Theobalt, C., Komura, T., Wang, W. "NeuS: Learning Neural Implicit Surfaces by Volume Rendering for Multi-view Reconstruction." *NeurIPS*, 2021.
第 17 章的无真值训练。把距离转成密度再用体积渲染，配合退火的过渡宽度。
