# 附录 A　符号表

全书符号尽量统一，但有两套坐标和两组反照率容易混，这里集中列一次。

## A.1 几何与方向

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| $x$ | 介质内的位置 | mm |
| $x_i,x_o$ | 入射点、出射点 | mm |
| $\omega,\omega_i,\omega_o$ | 方向（单位向量） | — |
| $n$ | 表面外法线 | — |
| $z$ | 竖直坐标，$+z$ 指向介质外部 | mm |
| $d=-z$ | 深度，向内为正 | mm |
| $r$ | 两点间距离 | mm |
| $\theta$ | 与法线的夹角 | rad |
| $d\omega$ | 立体角元 | sr |
| $dA$ | 面积元 | mm² |

## A.2 辐射度量

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| $L$ | 辐亮度 | $\mathrm{W\,mm^{-2}\,sr^{-1}}$ |
| $\Phi$ | 辐射通量 | W |
| $E,M$ | 辐照度、出射度 | $\mathrm{W\,mm^{-2}}$ |
| $\phi$ | 光通量密度（fluence rate） | $\mathrm{W\,mm^{-2}}$ |
| $\mathbf{E}$ | 通量矢量 | $\mathrm{W\,mm^{-2}}$ |
| $S$ | BSSRDF | $\mathrm{mm^{-2}\,sr^{-1}}$ |
| $f_r$ | BRDF | $\mathrm{sr^{-1}}$ |

## A.3 介质参数

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| $\sigma_a$ | 吸收系数 | $\mathrm{mm^{-1}}$ |
| $\sigma_s$ | 散射系数 | $\mathrm{mm^{-1}}$ |
| $\sigma_t=\sigma_a+\sigma_s$ | 消光系数 | $\mathrm{mm^{-1}}$ |
| $g$ | 相函数的平均余弦 | — |
| $p(\cos\theta)$ | 相函数 | $\mathrm{sr^{-1}}$ |
| $\alpha=\sigma_s/\sigma_t$ | 单次散射反照率 | — |
| $\sigma_s'=(1-g)\sigma_s$ | 约化散射系数 | $\mathrm{mm^{-1}}$ |
| $\sigma_t'=\sigma_a+\sigma_s'$ | 约化消光系数 | $\mathrm{mm^{-1}}$ |
| $\alpha'=\sigma_s'/\sigma_t'$ | 输运反照率 | — |
| $\ell=1/\sigma_t$ | 平均自由程 | mm |
| $\ell^*=1/\sigma_t'$ | 输运平均自由程 | mm |

## A.4 扩散理论的量

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| $D=1/(3\sigma_t')$ | 扩散系数 | mm |
| $\mu_{\text{eff}}=\sqrt{\sigma_a/D}$ | 有效衰减系数 | $\mathrm{mm^{-1}}$ |
| $\delta=1/\mu_{\text{eff}}$ | 扩散长度 | mm |
| $F_{dr}$ | 内部漫反射率 | — |
| $A=(1+F_{dr})/(1-F_{dr})$ | 反射参数 | — |
| $z_b=2AD$ | 外推边界距离 | mm |
| $z_r=1/\sigma_t'$ | 正源深度 | mm |
| $z_v=z_r+2z_b$ | 负源距离 | mm |
| $R_d(r)$ | 径向反射剖面 | $\mathrm{mm^{-2}}$ |
| $T_d(r)$ | 径向透射剖面 | $\mathrm{mm^{-2}}$ |
| $F_t=1-F_r$ | 界面透射率 | — |

## A.5 容易混的两组

**两套坐标。** 光学文献常用 $z$ 指向介质内部，本书用 $z$ 指向外部、$d=-z$ 指向内部。原因是渲染的几何里"外法线"是常用量，而深度的正方向在推导中更自然。读数时注意公式里用的是哪一个：$\partial\varphi/\partial z$ 与 $\partial\varphi/\partial d$ 差一个负号。

**两组反照率。** $\alpha$ 是单次散射反照率（一次事件是散射的概率），$\alpha'$ 是输运反照率（把前向散射当成没散射之后的概率）。前者用于判断"光会不会被吸收"，后者用于扩散理论。$\alpha'\ge\alpha$，$g$ 大时差距明显，皮肤上两者分别是 0.99 与 0.995。
