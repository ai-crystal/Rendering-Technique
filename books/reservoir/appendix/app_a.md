# 附录 A　符号与文献

## A.1 符号表

| 符号 | 含义 | 首次出现 |
|------|------|----------|
| $N$ | 场景中光源的数量 | 1.2 |
| $f_k$ | 第 $k$ 盏灯对一个着色点的真实贡献，含可见性 | 1.1 |
| $b_k$ | 第 $k$ 盏灯的无阴影贡献 | 1.10 |
| $I$ | 直接光照积分，$\sum_k f_k$ | 1.2 |
| $N_{\text{eff}}$ | 有效灯数，$I^2/\sum_k f_k^2$ | 1.8 |
| $p$ | 候选分布（可以抽样的那个） | 2.3 |
| $\hat p$ | 目标函数（想抽但抽不出来的那个） | 2.3 |
| $w$ | 权重，$w=\hat p/p$ | 2.3 |
| $M$ | 候选数 | 2.3 |
| $\hat W$ | 权重和，$\sum_{k}w(x_k)$ | 2.3 |
| $y$ | 蓄水池里选中的样本 | 2.3 |
| $F$ | 估计量 | 2.5 |
| $M_{\max}$ | 候选数上限 | 3.4 |
| $m_i$ | 多重重要性采样的技术权重 | 6.1 |

## A.2 三个核心公式

无偏的 RIS 估计量，对任意正整数 $M$ 成立：

$$F=\left(\frac{1}{M}\sum_{k=1}^{M}w(x_k)\right)\frac{f(y)}{p(y)\,w(y)} , \qquad
w=\frac{\hat p}{p} . \tag{A.1}$$

合并两个蓄水池时的权重换算，$y_j$ 是来源蓄水池的样本：

$$\hat W'=\hat W_j\cdot\frac{\hat p_i(y_j)}{\hat p_j(y_j)} . \tag{A.2}$$

技术合并时的份额校正，$M_i$ 是技术 $i$ 出的候选数：

$$w_i(x)=\frac{M}{M_i}\,m_i(x)\,\frac{\hat p_i(x)}{p_i(x)} . \tag{A.3}$$

## A.3 四条不能破的条件

候选分布与目标函数必须在同一处求值；$M$ 必须是最初抽的候选数；$\hat p>0$ 必须成立在 $f\neq 0$ 的地方；合并时的比值必须用被合并蓄水池自己的样本算。这四条里任何一条被破坏，偏差都会回来，而且不会随样本数消失。

## A.4 文献

Vitter, J. S. 1985. Random Sampling with a Reservoir. *ACM Transactions on Mathematical Software*, 11(1), 37–57.

抽一个长度未知的流中的等概率样本，是蓄水池采样的原始文献。

Chao, M.-T. 1982. A General Purpose Unequal Probability Sampling Plan. *Biometrika*, 69(3), 653–656.

把蓄水池采样推广到加权情形，按权重比例保留元素。

Veach, E. 1997. *Robust Monte Carlo Methods for Light Transport Simulation*. PhD thesis, Stanford University.

多重重要性采样与技术权重 $m_i$ 的来源，第 6 章 (6.1) 与 (6.2) 的基础。

Talbot, J. F., Cline, D., Egbert, P. 2005. Importance Resampling for Global Illumination. *Eurographics Symposium on Rendering*.

把蓄水池采样引入渲染，给出 RIS 的估计量与候选数 $M$ 的作用，第 2 章的主要依据。

Bitterli, B., Wyman, C., Pharr, M., Shirley, P., Lefohn, A., Jarosz, W. 2020. Spatiotemporal Reservoir Resampling for Real-Time Ray Tracing with Dynamic Direct Lighting. *ACM Transactions on Graphics*, 39(4).

ReSTIR DI 的原始工作，时间复用、空间复用与候选数上限的做法出自这里。

Ouyang, Y., Liu, S., Kettunen, M., Pharr, M., Pantaleoni, J. 2021. ReSTIR GI: Path Resampling for Real-Time Path Tracing. *Computer Graphics Forum*, 40(8).

把蓄水池推广到路径空间，第 5 章的主要依据。

Lin, D., Kettunen, M., Bitterli, B., Pantaleoni, J., Yuksel, C., Wyman, C. 2022. Generalized Resampled Importance Sampling: Foundations of ReSTIR. *ACM Transactions on Graphics*, 41(4).

把重采样与多重重要性采样放进同一个框架，第 6 章的份额校正与无偏条件出自这里。

Ruppert, L., Wronski, B., Major, D. 2020. Robust Fitting of Parallax-Aware Mixtures for Path Guiding. *ACM Transactions on Graphics*, 39(4).

路径引导里的样本复用与鲁棒拟合，第 5 章讨论路径空间复用时的参考工作之一。

## A.5 关于数值实验

书中所有曲线与数字由 `books/code/reservoir/` 下的脚本生成，只依赖 NumPy 与 Matplotlib。每个脚本开头导入一个共用模块，里面定义了玩具场景：一片像素、若干点光源、随时间平滑变化的可见性。所有"真值"都是对同一个玩具场景直接求和的解析结果，不是另一套渲染器算出来的。

这个设置的好处是每个数字都能复算：改动任何一个参数，偏差与方差的变化都能在几秒内看到。坏处是它比真实场景简单——没有多次弹射，没有复杂的遮挡，可见性是随机游走而不是几何求交。用一个简单模型验证偏差，用一个真实场景验证性能，这两件事不能互相替代。
