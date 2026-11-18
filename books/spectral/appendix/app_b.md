# 附录 B　数值速查

## B.1 配色函数的多瓣拟合

由 Wyman、Sloan、Shirley（2013）给出，$$\overline{c}(\lambda)=\sum_i\alpha_i\exp\left(-\frac{1}{2}\left[(\lambda-\beta_i)S(\lambda-\beta_i,\gamma_i,\delta_i)\right]^2\right)$$，其中 $S$ 在自变量为负时取 $\gamma_i$，否则取 $\delta_i$。

| 曲线 | $\alpha_i$ | $\beta_i$ (nm) | $\gamma_i$ (1/nm) | $\delta_i$ (1/nm) |
|:---|:---|:---|:---|:---|
| $\overline{x}$ | 0.362 | 442.0 | 0.0624 | 0.0374 |
| $\overline{x}$ | 1.056 | 599.8 | 0.0264 | 0.0323 |
| $\overline{x}$ | $-0.065$ | 501.1 | 0.0490 | 0.0382 |
| $\overline{y}$ | 0.821 | 568.8 | 0.0213 | 0.0247 |
| $\overline{y}$ | 0.286 | 530.9 | 0.0613 | 0.0322 |
| $\overline{z}$ | 1.217 | 437.0 | 0.0845 | 0.0278 |
| $\overline{z}$ | 0.681 | 459.0 | 0.0385 | 0.0725 |

注意 $\gamma$、$\delta$ 是宽度的倒数，例如 $\overline{y}$ 第一瓣在短波侧的标准差是 $1/0.0213\approx46.9$ nm。

## B.2 sRGB 矩阵

线性 sRGB 到 XYZ（D65，IEC 61966-2-1）：

$$\begin{pmatrix}X\\Y\\Z\end{pmatrix}=
\begin{pmatrix}
0.4124 & 0.3576 & 0.1805\\
0.2126 & 0.7152 & 0.0722\\
0.0193 & 0.1192 & 0.9505
\end{pmatrix}
\begin{pmatrix}R\\G\\B\end{pmatrix}$$

XYZ 到线性 sRGB：

$$\begin{pmatrix}R\\G\\B\end{pmatrix}=
\begin{pmatrix}
3.2406 & -1.5372 & -0.4986\\
-0.9689 & 1.8758 & 0.0415\\
0.0557 & -0.2040 & 1.0570
\end{pmatrix}
\begin{pmatrix}X\\Y\\Z\end{pmatrix}$$

原色色度 R(0.640,0.330)、G(0.300,0.600)、B(0.150,0.060)，白点 D65 (0.3127,0.3290)，白点 XYZ $(0.95047,1.00000,1.08883)$。

sRGB 传递函数：$v\le0.0031308$ 时 $12.92v$，否则 $1.055v^{1/2.4}-0.055$。

## B.3 CIE 1931 RGB 到 XYZ

$$\begin{pmatrix}X\\Y\\Z\end{pmatrix}=
\begin{pmatrix}
2.7689 & 1.7517 & 1.1302\\
1.0000 & 4.5907 & 0.0601\\
0.0000 & 0.0565 & 5.5943
\end{pmatrix}
\begin{pmatrix}R\\G\\B\end{pmatrix}$$

原色取 700 nm、546.1 nm、435.8 nm。

## B.4 Sellmeier 系数

$n^2(\lambda)=1+\sum_{i=1}^{3}B_i\lambda^2/(\lambda^2-C_i)$，$\lambda$ 以微米为单位。

| 玻璃 | $B_1$ | $B_2$ | $B_3$ | $C_1$ | $C_2$ | $C_3$ |
|:---|:---|:---|:---|:---|:---|:---|
| N-BK7 | 1.03961212 | 0.231792344 | 1.01046945 | 0.00600069867 | 0.0200179144 | 103.560653 |
| F2 | 1.34533359 | 0.209073176 | 0.937357162 | 0.00997743871 | 0.0470450767 | 111.886764 |
| SF11 | 1.73759695 | 0.313747346 | 1.89878101 | 0.013188707 | 0.0623068142 | 155.23629 |
| 熔石英 | 0.6961663 | 0.4079426 | 0.8974794 | 0.004679148 | 0.01351206 | 97.9340025 |

验证值（$n_d$ / $V_d$）：N-BK7 1.51680 / 64.17，F2 1.62004 / 36.37，SF11 1.78472 / 25.68，熔石英 1.45846 / 67.82。

## B.5 常用波长

| 名称 | 波长 (nm) |
|:---|:---|
| 氢 F 线 | 486.1327 |
| 氦 d 线 | 587.5618 |
| 氢 C 线 | 656.2725 |
| 钠 D 双线 | 589.0 / 589.6 |
| 汞 e 线 | 546.074 |
| 汞 g 线 | 435.833 |

阿贝数 $V_d=(n_d-1)/(n_F-n_C)$ 用的就是 F、d、C 三条线。

## B.6 常用公式

辐照度与辐亮度的关系：$E=\int_{H^2}L_i\cos\theta_i\,d\omega_i$。

渲染方程：$L_o=L_e+\int_{H^2}f_rL_i\cos\theta_i\,d\omega_i$。

BSDF 的能量守恒：$\int_{H^2}f_r(\omega_i,\omega_o,\lambda)\cos\theta_o\,d\omega_o\le1$。

Beer–Lambert：$T_r(\lambda)=\exp(-\sigma_t(\lambda)d)$。

球透镜焦距（从球心量起）：$f=nR/(2(n-1))$。

等边棱镜最小偏向角：$\delta_{\min}=2\arcsin(n\sin30°)-60°$。

圆盘光源轴向辐照度：$E(d)=L\pi R^2/(R^2+d^2)$。

XYZ 的像素估计（每条路径 $n$ 个波长）：

$$X=\frac{1}{n}\sum_{i=0}^{n-1}\frac{L(\lambda_i)\overline{x}(\lambda_i)}{p(\lambda_i)}$$
