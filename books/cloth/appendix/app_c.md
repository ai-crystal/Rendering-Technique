# 附录 C　参考文献

下列文献都是真实存在的。引用的具体页码和编号没有写出，因为不同版本差异较大；需要核对时按作者、年份、标题检索即可。

Kajiya, J. T., and Kay, T. L. 1989. Rendering Fur with Three Dimensional Textures. *Proceedings of SIGGRAPH 1989*, Computer Graphics 23(3), 271–280.

圆柱散射的切线模型出自这篇。它的漫反射项 $\sin(T,L)$ 和高光项 $\sin(T,H)^p$ 是本书第 3 章推导的起点，也是所有后续布料模型的原子。

Marschner, S. R., Jensen, H. W., Cammarano, M., Worley, S., and Hanrahan, P. 2003. Light Scattering from Human Hair Fibers. *ACM Transactions on Graphics* 22(3), 780–791.

R、TT、TRT 三条路径的分离、纵向与方位角的乘积形式、$\cos^2\theta_d$ 的 Jacobian，都出自这篇。第 4 章把它的结构搬到布料上。

Irawan, P., and Marschner, S. R. 2012. Specular Reflection from Woven Cloth. *ACM Transactions on Graphics* 31(1), Article 11.

纱线级的解析模型。它把纱线表面看成一组沿轴排列的纤维片段，显式加入纱线之间的遮挡，能复现平纹、斜纹、缎纹的差别。第 5 章的微面片写法与它的思路一致。

Sadeghi, I., Bisker, O., De Deken, J., and Jensen, H. W. 2013. A Micro-Appearance Model for Knitted Cloth. *ACM Transactions on Graphics* 32(4), Article 107.

针织物的显式微几何模型。它把线圈参数化，在每个线圈上撒纤维，用圆柱散射的解析积分合成 BRDF。第 1 章把它列为三条路线中"把几何显式建出来"的那一条。

Schröder, K., Klein, R., and Zinke, A. 2011. A Volumetric Approach to Predictive Rendering of Fabrics. *Computer Graphics Forum* 30(4), 1319–1328（EGSR 2011）.

把织物当成由纤维和空气混合的薄层，用体积散射描述传输。第 1 章和第 7 章的体积式近似与它同源。

Kubelka, P., and Munk, F. 1931. Ein Beitrag zur Optik der Farbanstriche. *Zeitschrift für technische Physik* 12, 593–601.

两流近似的原始文献。第 9 章的所有公式都可以追溯到这里。

Karis, B. 2013. Real Shading in Unreal Engine 4. *SIGGRAPH 2013 Course: Physically Based Shading in Theory and Practice*.

实时管线的布料着色。它的 sheen 项和"一个粗糙的 GGX 底加一个掠射亮层"的结构，是第 6 章和第 10 章讨论实时近似时的参照。

Heitz, E. 2018. Sampling the GGX Distribution of Visible Normals. *Journal of Computer Graphics Techniques* 7(4), 1–13.

可见法线分布采样。第 10 章讲预积分与采样的配合时用到，也是布料窄高光避免 firefly 的标准做法。

Heitz, E. 2014. Understanding the Masking-Shadowing Function in Microfacet-Based BRDFs. *Journal of Computer Graphics Techniques* 3(2), 48–107.

遮蔽-阴影函数的系统梳理。第 5 章关于 Smith 相关形式与不相关形式的差别，依据的是这篇。

Kulla, C., and Conty, A. 2017. Revisiting Physically Based Shading at Imageworks. *SIGGRAPH 2017 Course: Physically Based Shading in Theory and Practice*.

多次散射的能量补偿。第 10 章的 $f_{\mathrm{ms}}$ 出自这里。

Estevez, A., and Kulla, C. 2017. Production Friendly Microfacet Sheen BRDF. *ACM SIGGRAPH 2017 Talks*.

Charlie 法线分布。第 6 章把它列为 sheen 的两种生产写法之一。

Jakob, W., Hašan, M., Yan, L.-Q., Lawrence, J., Yuan, R., and Marschner, S. R. 2014. Discrete Stochastic Microfacet Models. *ACM Transactions on Graphics* 33(4), Article 115.

把微表面当成离散随机过程的框架。第 5 章的面片分布可以看成它的一个特例，想在模型里加入几何层面的统计时可以从这篇入手。

Chiang, M. J.-Y., Bitterli, B., and Burley, B. 2015. A Practical and Controllable Hair and Fur Model for Production Path Tracing. *ACM SIGGRAPH 2015 Talks*.

生产环境里的毛发模型。第 7 章讨论绒面的 strand 几何时参照了它的参数组织方式。

Chandrasekhar, S. 1960. *Radiative Transfer*. Dover Publications.

辐射传输的经典教材。第 7 章的光学厚度与多次散射、第 9 章的两流近似，都能在这里找到更严格的推导。

Bohren, C. F., and Huffman, D. R. 1983. *Absorption and Scattering of Light by Small Particles*. Wiley.

圆柱与球散射的完整理论。第 3 章只用了几何光学近似，需要更严格的结果时查这本。

## 一点说明

布料渲染的文献有一个特点：工程实现往往比论文更早成熟。很多实时管线里的做法（sheen 的经验式、厚度贴图的透射、顶点色的编织近似）没有对应的论文，只存在于引擎的源码和演讲里。本书尽量把这类做法标成"工程近似"，与有出处的模型区分开，因为两者的可信度不同：前者要靠实测验证，后者可以靠推导验证。
