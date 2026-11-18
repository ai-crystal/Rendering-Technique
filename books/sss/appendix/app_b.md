# 附录 B　公式速查

按推导顺序排列，每一行给出编号与用途。

## B.1 介质的三个参数

$$\sigma_t=\sigma_a+\sigma_s,\qquad \sigma_s'=(1-g)\sigma_s,\qquad \sigma_t'=\sigma_a+\sigma_s' . \tag{B.1}$$

$$\alpha=\frac{\sigma_s}{\sigma_t},\qquad \alpha'=\frac{\sigma_s'}{\sigma_t'} . \tag{B.2}$$

Beer–Lambert 与平均自由程：

$$L(d)=L_0e^{-\sigma_t d},\qquad \ell=\frac{1}{\sigma_t},\qquad p(s)=\sigma_te^{-\sigma_t s} . \tag{B.3}$$

Henyey–Greenstein 相函数：

$$p(\cos\theta)=\frac{1}{4\pi}\frac{1-g^2}{\left(1+g^2-2g\cos\theta\right)^{3/2}} . \tag{B.4}$$

采样：

$$\cos\theta=\frac{1}{2g}\left[1+g^2-\left(\frac{1-g^2}{1-g+2gu}\right)^2\right] . \tag{B.5}$$

## B.2 辐射传输与扩散

辐射传输方程：

$$\omega\cdot\nabla L=-\sigma_tL+\sigma_s\int_{4\pi}p(\omega'\cdot\omega)L\,d\omega' . \tag{B.6}$$

P1 近似与两个矩方程：

$$L=\frac{\phi}{4\pi}+\frac{3}{4\pi}\mathbf{E}\cdot\omega,\qquad \nabla\cdot\mathbf{E}=-\sigma_a\phi,\qquad \frac{1}{3}\nabla\phi=-\sigma_t'\mathbf{E} . \tag{B.7}$$

Fick 定律与扩散方程：

$$\mathbf{E}=-D\nabla\phi,\qquad D=\frac{1}{3\sigma_t'},\qquad \nabla^2\phi=\mu_{\text{eff}}^2\phi , \tag{B.8}$$

$$\mu_{\text{eff}}=\sqrt{3\sigma_a\sigma_t'} ,\qquad \delta=\frac{1}{\mu_{\text{eff}}} . \tag{B.9}$$

点源 Green 函数（三维）：

$$\phi(r)=\frac{P}{4\pi D}\frac{e^{-\mu_{\text{eff}}r}}{r} . \tag{B.10}$$

线源（二维）：

$$\phi(\rho)=\frac{P}{2\pi D}K_0(\mu_{\text{eff}}\rho) . \tag{B.11}$$

## B.3 边界

$$F_{dr}=2\int_0^{\pi/2}F(\theta)\cos\theta\sin\theta\,d\theta , \tag{B.12}$$

$$A=\frac{1+F_{dr}}{1-F_{dr}},\qquad z_b=2AD , \tag{B.13}$$

$$\varphi=2AD\frac{\partial\varphi}{\partial n}\quad\Longleftrightarrow\quad\varphi(-z_b)=0 . \tag{B.14}$$

$F_{dr}$ 的多项式拟合（Egan 等，1973）：

$$F_{dr}\approx\begin{cases}-0.4399+0.7099\eta^{-1}-0.3319\eta^{-2}+0.0636\eta^{-3}, & \eta<1\\ -1.4399\eta^{-2}+0.7099\eta^{-1}+0.6681+0.0636\eta, & \eta>1\end{cases} \tag{B.15}$$

## B.4 偶极子

$$R_d(r)=\frac{\alpha'}{4\pi}\left[\frac{z_r\left(1+\mu_{\text{eff}}d_r\right)e^{-\mu_{\text{eff}}d_r}}{d_r^3}+\frac{z_v\left(1+\mu_{\text{eff}}d_v\right)e^{-\mu_{\text{eff}}d_v}}{d_v^3}\right] , \tag{B.16}$$

$$d_r=\sqrt{r^2+z_r^2},\quad d_v=\sqrt{r^2+z_v^2},\quad z_r=\frac{1}{\sigma_t'},\quad z_v=z_r+2z_b .$$

多极子（板厚 $L$）：

$$R_d(r)=\sum_{i}\left[\frac{\alpha'z_{r,i}(1+\mu d_{r,i})e^{-\mu d_{r,i}}}{4\pi d_{r,i}^3}-\frac{\alpha'z_{v,i}(1+\mu d_{v,i})e^{-\mu d_{v,i}}}{4\pi d_{v,i}^3}\right] , \tag{B.17}$$

$$z_{r,i}=2i(L+2z_b)+z_r,\qquad z_{v,i}=2i(L+2z_b)-z_r-2z_b .$$

## B.5 BSSRDF

可分离形式：

$$S_d=\frac{1}{\pi}F_t(\omega_i)\,R_d(r)\,F_t(\omega_o) . \tag{B.18}$$

单次散射的光程（正弦定理）：

$$s_i+s_o=r\,\frac{\sin\theta_i+\sin\theta_o}{\sin(\theta_i+\theta_o)} . \tag{B.19}$$

单次散射的总反射率（各向同性相函数）：

$$R_{\text{ss}}=0.153\,\alpha . \tag{B.20}$$

归一化剖面：

$$\tilde R(r)=A\,\frac{e^{-r/d}+e^{-r/(3d)}}{8\pi d\,r} . \tag{B.21}$$

## B.6 采样

径向 pdf 与面积 pdf：

$$p(r)=2\pi rR_d(r),\qquad \text{pdf}(x_i)=\frac{R_d(r)}{R_{\text{tot}}} . \tag{B.22}$$

半球上 P1 场给出的出射通量：

$$J_{\text{out}}=\frac{\phi}{4}+\frac{E_n}{2} . \tag{B.23}$$
