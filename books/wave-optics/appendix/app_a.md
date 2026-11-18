# 附录 A　符号与公式速查

## A.1 符号

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| $\lambda$ | 真空中波长 | nm |
| $k$ | 波数，$2\pi/\lambda$ | nm$^{-1}$ |
| $\tilde U$ | 复振幅 | — |
| $I$ | 强度，$\langle|U|^{2}\rangle$ | — |
| $\delta$ | 相位差 | rad |
| $\Delta L$ | 光程差，$n\times$几何距离 | nm |
| $\gamma$ | 复相干度，$0\le|\gamma|\le1$ | — |
| $l_c$ | 相干长度，$\lambda^{2}/\Delta\lambda$ | nm |
| $n,\ \kappa$ | 折射率的实部与虚部 | — |
| $d$ | 膜厚 | nm |
| $\theta_i,\ \theta_t$ | 入射角、折射角 | rad |
| $\eta$ | 等效导纳，$n\cos\theta$ 或 $n/\cos\theta$ | — |
| $r,\ t$ | 振幅反射、透射系数 | — |
| $R,\ T,\ A$ | 反射率、透射率、吸收率 | — |
| $\varphi$ | 单层的相位厚度，$2\pi nd\cos\theta/\lambda$ | rad |
| $B,\ C$ | 膜系矩阵作用在基底向量上的结果 | — |
| $Y$ | 输入导纳，$C/B$ | — |
| $g$ | 相位方差，$(4\pi\sigma_h\cos\theta/\lambda)^{2}$ | — |
| $\sigma_h$ | 表面高度的标准差 | nm |
| $l$ | 横向相关长度 | nm |
| $d$（光栅） | 光栅周期 | nm |
| $m$ | 衍射级次 | — |
| $J$ | Jones 向量或 Jones 矩阵 | — |
| $S$ | Stokes 向量 $[I,Q,U,V]^{T}$ | — |
| $M$ | Mueller 矩阵 | — |
| $R(\phi)$ | Stokes 空间的坐标旋转 | — |

## A.2 公式速查

单层膜反射率（Airy 公式）：

$$R=\frac{r_{01}^{2}+r_{12}^{2}+2r_{01}r_{12}\cos\delta}{1+r_{01}^{2}r_{12}^{2}+2r_{01}r_{12}\cos\delta},\qquad
\delta=\frac{4\pi n_1d\cos\theta_1}{\lambda}. \tag{A.1}$$

零反射条件（垂直入射）：$n_1^{2}=n_0n_2$，$d=\lambda/(4n_1)$。

多层膜特征矩阵：

$$M_j=\begin{bmatrix}\cos\varphi_j & -\dfrac{i}{\eta_j}\sin\varphi_j\\[6pt]
-i\eta_j\sin\varphi_j & \cos\varphi_j\end{bmatrix},\qquad
\begin{bmatrix}B\\C\end{bmatrix}=\left(\prod_j M_j\right)\begin{bmatrix}1\\ \eta_s\end{bmatrix}. \tag{A.2}$$

$$r=\frac{\eta_0B-C}{\eta_0B+C},\qquad
T=\frac{4\,\mathrm{Re}(\eta_0)\mathrm{Re}(\eta_s)}{|\eta_0B+C|^{2}} . \tag{A.3}$$

光栅方程：$d(\sin\theta_i+\sin\theta_m)=m\lambda$。

N 缝强度：$I=I_0\left[\dfrac{\sin(N\delta/2)}{\sin(\delta/2)}\right]^{2}$，峰宽 $\Delta\theta\approx\lambda/(Nd\cos\theta)$。

Bragg–Snell：$\lambda=2D\sqrt{n_{\mathrm{eff}}^{2}-\sin^{2}\theta}$。

相位方差与相干、漫射分量：

$$g=\left(\frac{4\pi\sigma_h\cos\theta_i}{\lambda}\right)^{2},\qquad
\frac{I_{\mathrm{coh}}}{I_0}=e^{-g},\qquad
\frac{I_{\mathrm{diff}}}{I_0}=1-e^{-g}. \tag{A.4}$$

Fresnel 界面的 Mueller 矩阵：

$$M_F=\frac{1}{2}\begin{bmatrix}
R_p+R_s & R_p-R_s & 0 & 0\\
R_p-R_s & R_p+R_s & 0 & 0\\
0 & 0 & 2u & -2v\\
0 & 0 & 2v & 2u
\end{bmatrix},\qquad u+iv=r_pr_s^{*} . \tag{A.5}$$

Stokes 空间的旋转：

$$R(\phi)=\begin{bmatrix}1&0&0&0\\0&\cos2\phi&-\sin2\phi&0\\0&\sin2\phi&\cos2\phi&0\\0&0&0&1\end{bmatrix}. \tag{A.6}$$

单界面相位差（全反射）：

$$\tan\frac{\delta_s}{2}=-\frac{\sqrt{\sin^{2}\theta_i-(n_2/n_1)^{2}}}{\cos\theta_i},\qquad
\tan\frac{\delta_p}{2}=-\frac{\sqrt{\sin^{2}\theta_i-(n_2/n_1)^{2}}}{(n_2/n_1)^{2}\cos\theta_i}. \tag{A.7}$$

## A.3 数量级备忘

| 量 | 数值 |
| --- | --- |
| 可见光范围 | 380 至 780 nm |
| $\lambda/4$（550 nm） | 137 nm |
| 1 nm 光程差对应的相位 | 0.65 度 |
| 空气到玻璃的垂直反射率 | 4.3% |
| 玻璃的布儒斯特角 | 56.3 度 |
| 玻璃到空气的临界角 | 41.8 度 |
| 单层氟化镁膜的最低反射率 | 1.26% |
| 太阳光的相干长度 | 约 1 微米 |
| 白光 LED 的相干长度 | 约 12 微米 |
| 太阳的相干宽度 | 约 60 微米 |
| CD 轨道间距 | 1.6 微米 |
| Morpho 蝴蝶片层周期 | 约 195 nm |
| 孔雀羽毛黑色素棒周期 | 约 140 nm |
