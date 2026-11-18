# 附录 C　参考文献

按作者姓氏首字母排序。这一册的核心推导全部来自下面这些工作，文中的模型名称与年份与这里一致。

**Chandrasekhar, S. 1950.** *Radiative Transfer.* Oxford University Press.
（辐射传输方程的经典处理，H 函数与离散纵标的源头。）

**Chiang, M. J., Kutz, P., Burley, B. 2016.** "Practical and Controllable Subsurface Scattering for Production Path Tracing." ACM SIGGRAPH 2016 Talks.
（把随机游走型次表面散射集成进生产级路径追踪的做法。）

**Christensen, P. H., Burley, B. 2015.** "Approximate Reflectance Profiles for Efficient Subsurface Scattering." Pixar Technical Memo 15-04.
（归一化扩散剖面，$e^{-r/d}$ 与 $e^{-r/(3d)}$ 的组合形式，以及它与蒙特卡洛的拟合。）

**d'Eon, E., Irving, G. 2011.** "A Quantized-Diffusion Model for Rendering Translucent Materials." ACM Transactions on Graphics 30(4)（SIGGRAPH 2011）.
（量化扩散：把扩散方程按边界条件展开成离散模式，保留部分方向信息。）

**Donner, C., Jensen, H. W. 2005.** "Light Diffusion in Multi-Layered Translucent Materials." ACM Transactions on Graphics 24(3)（SIGGRAPH 2005）.
（多极子：用无穷镜像序列处理有限厚度平板与多层介质；文中给出的反射率与透射率对比表是本册第 16 章图 16-2 的数据来源。）

**Egan, W. G., Hilgeman, T. 1973.** 漫射反射率的多项式拟合。本册第 12 章式 12.9 里的拟合系数转引自 Donner 与 Jensen 2005 的论文（其式 8），原文注明出自这一工作。需要核对原式时请以 Donner 与 Jensen 2005 为直接出处。

**Farrell, T. J., Patterson, M. S., Wilson, B. 1992.** "A Diffusion Theory Model of Spatially Resolved, Steady-State Diffuse Reflectance for the Noninvasive Determination of Tissue Optical Properties in Vivo." *Medical Physics* 19(4).
（扩散偶极子在生物医学光学里的原型，$z_b=2AD$ 与外推边界的来源。）

**Frisvad, J. R., Habel, R., Jensen, H. W., Christensen, P. H. 2014.** "A Directional Dipole Model for Subsurface Scattering." ACM Transactions on Graphics 34(1).
（方向偶极子：把各向同性点源换成沿入射方向的小偶极，修正近场的方向性。）

**Habel, R., Christensen, P. H., Jarosz, W. 2013.** "Photon Beam Diffusion: A Hybrid Monte Carlo Method for Subsurface Scattering." *Computer Graphics Forum* 32(4)（EGSR 2013）.
（光子束扩散：把入射光当成有限宽的光束，用扩散解求辐射度，解决了点源近似在近场的奇性。）

**Ishimaru, A. 1978.** *Wave Propagation and Scattering in Random Media.* Academic Press.
（P1 近似、Fick 定律与扩散方程的标准推导，本册第 9、10 章的组织方式来自这里。）

**Jensen, H. W., Marschner, S. R., Levoy, M., Hanrahan, P. 2001.** "A Practical Model for Subsurface Light Transport." ACM SIGGRAPH 2001.
（偶极子 BSSRDF 与单次散射项的完整模型，本册第 13、14 章的核心。）

**Jensen, H. W., Buhler, J. 2002.** "A Rapid Hierarchical Rendering Technique for Translucent Materials." ACM Transactions on Graphics 21(3)（SIGGRAPH 2002）.
（层次化积分：把 BSSRDF 的面积分加速，是第一次让次表面散射进入实用渲染的工作。）

**Jimenez, J., Zsolnai, K., Jarabo, A., et al. 2015.** "Separable Subsurface Scattering." *Computer Graphics Forum* 34(6).
（可分离卷积：把径向剖面拟合成若干个高斯，用多次一维卷积实现实时次表面散射。）

**Kajiya, J. T., Kay, T. L. 1989.** "Rendering Fur with Three Dimensional Textures." ACM SIGGRAPH 1989.
（毛发散射的早期模型，圆柱几何里几个散射模态的来源。）

**Jacques, S. L. 2013.** "Optical Properties of Biological Tissues: A Review." *Physics in Medicine and Biology* 58(11).
（生物组织光学参数的综述，黑色素的幂律吸收与组织的典型参数范围取自这里。）

**Marschner, S. R., Jensen, H. W., Cammarano, M., Worley, S., Hanrahan, P. 2003.** "Light Scattering from Human Hair Fibers." ACM Transactions on Graphics 22(3)（SIGGRAPH 2003）.
（毛发纤维的 R / TT / TRT 模态模型。）

**Patterson, M. S., Chance, B., Wilson, B. C. 1989.** "Time Resolved Reflectance and Transmittance for the Non-Invasive Measurement of Tissue Optical Properties." *Applied Optics* 28(12).
（把准直入射换成埋在一个自由程深处的点源的做法。）

## 说明

正文里提到"某年某作者"时，指的就是上面对应的条目。文中出现的具体数值（总反射率、剖面对比、散射次数分布等）如果标注了"蒙特卡洛"，含义是用本书附带的脚本在给定参数下算出来的，脚本在 `books/code/sss/` 下，可以复现。标注了来源表格的数据（第 16 章图 16-2）取自 Donner 与 Jensen 2005 的论文。

关于血红蛋白的吸收谱：正文只用了它的两条吸收带位置（542 与 577 纳米，氧合态），没有给解析式，因为完整的谱是实验编译数据（常用的编译表由 Prahl 维护），不能用简单函数准确表示。需要精确数值时应当查表，不要用高斯近似。
