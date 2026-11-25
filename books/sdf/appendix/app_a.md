# 附录 A　常用形状 SDF 速查

记号约定：$\mathbf{p}$ 是查询点，$d$ 是返回值，内部为负。$\lvert\mathbf{p}\rvert$ 表示逐分量取绝对值，$\mathbf{p}_{xz}$ 表示 $xz$ 平面上的分量，$\rho=\lVert\mathbf{p}_{xz}\rVert$。

## A.1 基本体

| 形状 | 公式 | 精确性 |
|---|---|---|
| 球，心 $\mathbf{c}$，半径 $r$ | $\lVert\mathbf{p}-\mathbf{c}\rVert-r$ | 内外都精确 |
| 平面，法线 $\mathbf{n}$ | $\mathbf{n}\cdot\mathbf{p}-c$ | 精确 |
| 盒，半尺寸 $\mathbf{b}$ | 令 $\mathbf{q}=\lvert\mathbf{p}\rvert-\mathbf{b}$，则 $\lVert\max(\mathbf{q},0)\rVert+\min(\max_i q_i,0)$ | 内外都精确 |
| 圆环，主半径 $R$，管半径 $r$ | $\big\lVert(\rho-R,\ p_y)\big\rVert-r$ | 内外都精确 |
| 圆柱，半径 $r$，半高 $h$ | 令 $\mathbf{q}=(\rho-r,\ \lvert p_y\rvert-h)$，同盒 | 内外都精确 |
| 胶囊，端点 $\mathbf{a},\mathbf{b}$，半径 $r$ | $\big\lVert\mathbf{p}-\mathbf{a}-\operatorname{clamp}\!\big(\frac{(\mathbf{p}-\mathbf{a})\cdot\mathbf{b}'}{\mathbf{b}'\cdot\mathbf{b}'},0,1\big)\mathbf{b}'\big\rVert-r$，$\mathbf{b}'=\mathbf{b}-\mathbf{a}$ | 精确 |
| 线段，端点 $\mathbf{a},\mathbf{b}$ | 上式去掉半径 | 精确 |
| 圆台，底半径 $r_1$ 在 $y=-h$，顶半径 $r_2$ 在 $y=+h$ | 见 A.2 | 精确 |
| 二维多边形 | 见 A.3 | 精确（凸） |

## A.2 圆台

令 $\mathbf{q}=(\rho,y)$，$\mathbf{k}_1=(r_2,h)$，$\mathbf{k}_2=(r_2-r_1,2h)$，则

$$\mathbf{c}_a=\Big(q_x-\min\big(q_x,\ (q_y<0\,?\,r_1:r_2)\big),\ \lvert q_y\rvert-h\Big) ,$$

$$\mathbf{c}_b=\mathbf{q}-\mathbf{k}_1+\mathbf{k}_2\operatorname{clamp}\!\left(\frac{(\mathbf{k}_1-\mathbf{q})\cdot\mathbf{k}_2}{\mathbf{k}_2\cdot\mathbf{k}_2},0,1\right) ,$$

$$d=s\sqrt{\min(\lVert\mathbf{c}_a\rVert^2,\lVert\mathbf{c}_b\rVert^2)},\qquad s=\begin{cases}-1,&\mathbf{c}_{b,x}<0\ \text{且}\ \mathbf{c}_{a,y}<0\\ +1,&\text{其他}\end{cases}$$

$r_2=0$ 时轴上的点会退化，把 $r_2$ 取一个极小的正数。

## A.3 二维多边形

凸多边形用半平面交，每条边的外侧法线 $\mathbf{n}_i$，$d=\max_i(\mathbf{n}_i\cdot\mathbf{p}-c_i)$。非凸多边形要取所有边的最小距离，符号用绕数或奇偶规则。

## A.4 算子

| 算子 | 公式 | 对 Lipschitz 的影响 |
|---|---|---|
| 并集 | $\min(a,b)$ | 保持 1 |
| 交集 | $\max(a,b)$ | 保持 1 |
| 差集 | $\max(a,-b)$ | 保持 1 |
| 平滑并集 | $b+(a-b)h-kh(1-h)$，$h=\operatorname{clamp}(\tfrac12+\tfrac{b-a}{2k},0,1)$ | 保持 1，接缝处梯度偏小 |
| 壳体 | $\lvert d\rvert-t$ | 保持 1 |
| 圆角 / 外偏移 | $d-r$ | 保持 1 |
| 内偏移 | $d+r$ | 保持 1，$r$ 超过曲率半径时形状自交 |
| 伸长 | 令 $\mathbf{q}=\mathbf{p}-\operatorname{clamp}(\mathbf{p},-\mathbf{h},\mathbf{h})$，取 $d(\mathbf{q})$ | 保持 1 |
| 非均匀缩放 | $s_{\min}\,d(\mathbf{p}\oslash\mathbf{s})$ | 乘因子后保持 1，因子为 $s_{\min}$ |
| 镜像 | $d(\lvert p_x\rvert,p_y,p_z)$ | 保持 1 |
| 重复 | $d((\mathbf{p}+\tfrac12\mathbf{s})\bmod\mathbf{s}-\tfrac12\mathbf{s})$ | 保持 1，物体超出格子时不准 |
| 扭转 | $d(\mathbf{q})$，$\mathbf{q}$ 为绕轴旋转 $\omega x$ 后的坐标 | 上界 $\sqrt{1+(\omega r)^2}$ |

## A.5 步进

步长取 $c\,f$，$c\le1/L$，$L$ 是梯度长度的上界。表 A.4 里"保持 1"的算子取 $c=1$；扭转取 $c=1/\sqrt{1+(\omega r_{\max})^2}$；弯曲取 $c=R/(R+\lvert z\rvert_{\max})$。检测到符号翻转时在区间内二分回退。
