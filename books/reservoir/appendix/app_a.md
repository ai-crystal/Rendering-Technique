# 附录 A　符号、公式与文献

## A.1 符号表

| 符号 | 含义 | 首次出现 |
|------|------|----------|
| $I$ | 待求的积分 | 1.2 |
| $f$ | 真实贡献（含可见性） | 1.1 |
| $\hat p$ | 目标函数，不必归一化 | 4.1 |
| $p$ | 候选密度，可抽样、已归一化 | 4.1 |
| $w$ | 权重 $w=\hat p/p$ | 4.1 |
| $M$ | 候选数 | 4.2 |
| $\hat W$ | 权重和 $\sum_k w_k$ | 4.2 |
| $y$ | 蓄水池里选中的样本 | 4.2 |
| $q$ | 重采样之后样本的实际分布 | 6.2 |
| $w_i$ 或 $m_i$ | 技术 $i$ 的份额（MIS 权重） | 2.3 |
| $T_i$ | 技术 $i$ 的移位映射 | 11.1 |
| $J$ | 移位映射的雅可比 | 9.4 |
| $M_0$ | 每帧的初始候选数 | 5.2 |
| $M_{\max}$ | 候选数上限 | 5.5 |
| $\sigma_t$ | 消光系数 | 10.2 |
| $\sigma_s$ | 散射系数 | 10.1 |
| $T(t)$ | 透射率 | 10.1 |

## A.2 五个核心式子

RIS 的估计量，对任意正整数 $M$ 成立：

$$F=\frac{f(y)}{\hat p(y)}\cdot\frac{1}{M}\sum_{i=1}^{M}\frac{\hat p(x_i)}{p(x_i)} . \tag{A.1}$$

两个蓄水池合并：按权重和之比抽签，乘上目标函数之比。

$$\hat W'=\hat W_j\cdot\frac{\hat p_i(y_j)}{\hat p_j(y_j)} ,\qquad
\Pr[\text{选 } j]=\frac{\hat W'}{\hat W_a+\hat W'} . \tag{A.2}$$

MIS 的份额必须和为一：

$$\sum_i w_i(x)=1 \qquad \text{对所有 } f(x)\neq 0 \text{ 的 } x . \tag{A.3}$$

GRIS 的通用权重：

$$w_i(x)=m_i\big(T_i(x)\big)\cdot\frac{M}{M_i}\cdot\frac{\hat p_i\big(T_i(x)\big)}{p_i(x)}\cdot\left|\frac{\mathrm{d}T_i}{\mathrm{d}x}\right| . \tag{A.4}$$

着色：

$$\langle L\rangle=\frac{f_i(y)}{\hat p_i(y)}\cdot\frac{\hat W}{M} . \tag{A.5}$$

## A.3 五条不能破的条件

移位映射必须双射且雅可比不为零；目标函数必须在映射后的域求值；密度必须是技术在自己域里的真实密度；份额之和必须为一；$\hat W$ 与 $M$ 必须描述同一批候选。

前三条出错时偏差随几何变化，后两条出错时偏差是一个常数比例。两种症状在图像上的样子不同，第 14 章给了一套区分它们的测量流程。

## A.4 文献

Vitter, J. S. 1985. Random Sampling with a Reservoir. *ACM Transactions on Mathematical Software*, 11(1), 37–57.

抽一个长度未知的流中的等概率样本，是蓄水池采样的原始文献。

Chao, M.-T. 1982. A General Purpose Unequal Probability Sampling Plan. *Biometrika*, 69(3), 653–656.

把蓄水池采样推广到加权情形，按权重比例保留元素。

Veach, E. 1997. *Robust Monte Carlo Methods for Light Transport Simulation*. PhD thesis, Stanford University.

多重重要性采样与技术权重的来源，第 2 章的平衡启发式与单样本 MIS 出自这里。

Talbot, J. F., Cline, D., Egbert, P. 2005. Importance Resampling for Global Illumination. *Eurographics Symposium on Rendering*.

把蓄水池采样引入渲染，给出 RIS 的估计量与候选数 $M$ 的作用，第 4 章的主要依据。

Efraimidis, P. S., Spirakis, P. G. 2006. Weighted Random Sampling with a Reservoir. *Information Processing Letters*, 97(5), 181–185.

提出 $k=u^{1/w}$ 的 key 构造（A-Res）与跳步版本（A-ExpJ），第 3 章的主要依据。

Bitterli, B., Wyman, C., Pharr, M., Shirley, P., Lefohn, A., Jarosz, W. 2020. Spatiotemporal Reservoir Resampling for Real-Time Ray Tracing with Dynamic Direct Lighting. *ACM Transactions on Graphics*, 39(4).

ReSTIR DI 的原始工作，时间复用、空间复用、可见性复用与候选数上限的做法出自这里。

Ouyang, Y., Liu, S., Kettunen, M., Pharr, M., Pantaleoni, J. 2021. ReSTIR GI: Path Resampling for Real-Time Path Tracing. *Computer Graphics Forum*, 40(8).

把蓄水池推广到路径空间，重连接与雅可比的处理是第 9 章的依据。

Lin, D., Kettunen, M., Bitterli, B., Pantaleoni, J., Yuksel, C., Wyman, C. 2022. Generalized Resampled Importance Sampling: Foundations of ReSTIR. *ACM Transactions on Graphics*, 41(4).

把重采样与 MIS 放进同一个框架，$M/M_i$ 修正与五条无偏条件出自这里。

Ruppert, L., Wronski, B., Major, D. 2020. Robust Fitting of Parallax-Aware Mixtures for Path Guiding. *ACM Transactions on Graphics*, 39(4).

路径引导里的样本复用与鲁棒拟合，讨论路径空间复用时的参考工作。

SIGGRAPH 2025, *Advances in Real-Time Rendering in Games*（课程报告）。

课程里对随机直接光与重采样方案的讨论，是第 15 章关于生产现状的主要依据。具体演讲人、场次与页码未逐一核实，本章只引用其中可以确认的方法轮廓。

Utah Graphics Lab 的 volumetric ReSTIR 工作，论文题为《Volumetric ReSTIR》。

第 10 章关于体积重采样的框架参考了这份工作。除团队与标题外，作者名单、发表年份与具体实现细节在撰写时未能核实，因此正文只讨论它公开的方法框架，不涉及其工程选择。

## A.5 关于数值实验

书中所有曲线与数字由 `books/code/reservoir/` 下的脚本生成，只依赖 NumPy 与 Matplotlib。共用模块 `ris.py` 提供玩具场景（一片像素、若干点光源、随时间平滑变化的可见性），`lab.py` 提供本章后半部分用的实验台（MIS 的半球积分、加权蓄水池、ReSTIR 模拟器、体积与 GRIS 的小实验），`pathlab.py` 提供第 9 到 11 章那个二维路径场景。

所有真值都是对同一个玩具场景直接求和或数值积分得到的解析结果，不是另一套渲染器算出来的。偏差的测量一律采用多随机种子重复，报告均值与标准误；凡是文中出现"在统计误差内"的说法，都可以在脚本的输出里找到对应的数字。

这个设置的好处是每个数字都能复算：改动任何一个参数，偏差与方差的变化都能在几秒内看到。坏处是它比真实场景简单——没有多次弹射，没有复杂的遮挡，可见性是随机游走而不是几何求交，灯的位置是随机撒的而不是美术摆的。用一个简单模型验证偏差，用一个真实场景验证性能，这两件事不能互相替代。
