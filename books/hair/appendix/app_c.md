# 附录 C　参考文献

只列本册引用过或直接依赖的文献。作者、年份、刊物按原文，页码与 DOI 从略以免出错。

## 毛发散射模型

**Kajiya, J. T., Kay, T. L. (1989).** Rendering Fur with Three Dimensional Textures. *Computer Graphics (SIGGRAPH '89 Proceedings)*, 23(3).

第一个把纤维当成圆柱做着色处理的模型。给出切线空间、$\sin\theta$ 的漫反射项与余弦幂的高光项。第 2 章讨论的全部内容出自这篇。

**Marschner, S. R., Jensen, H. W., Cammarano, M., Worley, S., Hanrahan, P. (2003).** Light Scattering from Human Hair Fibers. *ACM Transactions on Graphics*, 22(3), SIGGRAPH 2003.

把散射分成 R、TT、TRT 三条路径，并引入方位角分布与纵向分布的可分离形式。本册第 3、4 章的基础。

**Zinke, A., Sobottka, G., Magnor, M. (2008).** Dual Scattering Approximation for Fast Multiple Scattering in Hair. *ACM Transactions on Graphics*, 27(3), SIGGRAPH 2008.

提出用二阶项近似多次散射，是第 5 章的主要参考。

**d'Eon, E., Francois, G., Hill, S., Letteri, J., Aubry, M. (2011).** An Energy-Conserving Hair Reflectance Model. *Computer Graphics Forum*, 30(4), EGSR 2011.

把方位角分布写成可以用累积分布采样的解析形式，并处理了能量守恒。第 6 章的采样思路来源于此。

**Yan, L.-Q., Tseng, C.-W., Jensen, H. W., Ramamoorthi, R. (2015).** Physically-Accurate Fur Reflectance: Modeling, Measurement and Rendering. *ACM Transactions on Graphics*, 34(6), SIGGRAPH Asia 2015.

对纤维散射做了系统的测量与建模，包含椭圆截面与多层结构。第 1 章关于截面结构的讨论参考了这篇。

**Pekelis, L., Hsu, D., Burley, B. (2015).** A Data-Driven Light Scattering Model for Hair. Technical report, Disney Research.

用测量数据拟合纵向与方位角分布，把美术可控性放在首位。第 9 章的参数化思路受其影响。

**Chiang, M. J. Y., Bitterli, B., Tappan, C., Burley, B. (2016).** A Practical and Controllable Hair and Fur Model for Production Path Tracing. *Computer Graphics Forum*, 35(2), EGSR 2016.

生产环境下的实用模型，包含双散射的工程实现与参数约定。第 7、8 章多处参考。

## 体积散射与介质

**Kubelka, P., Munk, F. (1931).** Ein Beitrag zur Optik der Farbanstriche. *Zeitschrift für technische Physik*, 12.

双流近似的原始文献。第 7 章的 (7.3)、(7.4) 出自这里。

**Henyey, L. G., Greenstein, J. L. (1941).** Diffuse Radiation in the Galaxy. *Astrophysical Journal*, 93.

各向异性相位函数的常用近似形式，第 7 章用它描述毛发的相位函数。

## 教科书与实现参考

**Pharr, M., Jakob, W., Humphreys, G.** *Physically Based Rendering: From Theory to Implementation*. Morgan Kaufmann.

第 3 版 2016 年，第 4 版 2023 年。本册的黑色素吸收系数取自其中的毛发材质实现；第 8 章的曲线求交与切线插值写法也参照了它。

**Robbins, C. R.** *Chemical and Physical Behavior of Human Hair*. Springer.

毛发学的标准参考，第 1 章关于角质层、皮层、髓质的结构与尺寸数据出自这里。
