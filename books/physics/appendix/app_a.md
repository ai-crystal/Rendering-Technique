# 附录 A　数学工具

正文里用到数学的地方，凡是第一次出现都解释过。这一份附录把用到的工具集中列一遍，方便回头查。

## A.1 矢量

一个矢量同时有大小和方向。本书用粗体字母表示，比如 $\mathbf{E}$、$\mathbf{B}$、$\mathbf{v}$，手写时在上面加箭头。矢量的长度记作 $|\mathbf{E}|$，正文的公式里为了简洁常写成 $E$。

在直角坐标系里把一个矢量写成分量：

$$\mathbf{A}=A_x\,\hat{\mathbf{x}}+A_y\,\hat{\mathbf{y}}+A_z\,\hat{\mathbf{z}} . \tag{A.1}$$

$\hat{\mathbf{x}}$、$\hat{\mathbf{y}}$、$\hat{\mathbf{z}}$ 是三个互相垂直的单位矢量，长度为一。上式读作"沿 $x$ 方向走 $A_x$，沿 $y$ 方向走 $A_y$，沿 $z$ 方向走 $A_z$"，三者合成就是 $\mathbf{A}$。矢量相加就是分量相加：

$$\mathbf{A}+\mathbf{B}=(A_x+B_x)\hat{\mathbf{x}}+(A_y+B_y)\hat{\mathbf{y}}+(A_z+B_z)\hat{\mathbf{z}} . \tag{A.2}$$

一个矢量乘一个数，等于每个分量乘这个数。乘正数不改变方向，乘负数把方向反过来。

### A.1.1 点乘

两个矢量的点乘是一个数：

$$\mathbf{A}\cdot\mathbf{B}=A_xB_x+A_yB_y+A_zB_z=|\mathbf{A}||\mathbf{B}|\cos\theta , \tag{A.3}$$

$\theta$ 是两者之间的夹角。第二个等号是几何意义，说明点乘测量的是"一个矢量在另一个矢量方向上的投影"。两个矢量垂直时点乘为零，这是判断垂直最方便的办法。

正文里点乘出现在两个地方：功 $W=\int\mathbf{F}\cdot d\mathbf{l}$，通量 $\Phi=\int\mathbf{B}\cdot d\mathbf{S}$。两处的物理含义不同，数学操作一样：把矢量分解成"沿着面法线的那一份"和"平行于面的那一份"，只有前一份对结果有贡献。

### A.1.2 叉乘

两个矢量的叉乘是一个矢量：

$$\mathbf{A}\times\mathbf{B}=(A_yB_z-A_zB_y)\hat{\mathbf{x}}+(A_zB_x-A_xB_z)\hat{\mathbf{y}}+(A_xB_y-A_yB_x)\hat{\mathbf{z}} . \tag{A.4}$$

这个式子不好记，用行列式写：

$$\mathbf{A}\times\mathbf{B}=\begin{vmatrix}\hat{\mathbf{x}}&\hat{\mathbf{y}}&\hat{\mathbf{z}}\\ A_x&A_y&A_z\\ B_x&B_y&B_z\end{vmatrix} . \tag{A.5}$$

按第一行展开，每一项是"单位矢量乘以剩下两行两列构成的行列式"，中间那一项要变号。大小是

$$|\mathbf{A}\times\mathbf{B}|=|\mathbf{A}||\mathbf{B}|\sin\theta , \tag{A.6}$$

方向由右手定则给出：四指从 $\mathbf{A}$ 弯向 $\mathbf{B}$，拇指指向叉乘结果。叉乘不满足交换律，$\mathbf{B}\times\mathbf{A}=-\mathbf{A}\times\mathbf{B}$。

叉乘的几何意义是平行四边形的面积。$|\mathbf{A}\times\mathbf{B}|$ 等于以 $\mathbf{A}$、$\mathbf{B}$ 为邻边的平行四边形面积，方向垂直于这个平面。安培力 $\mathbf{F}=I\mathbf{L}\times\mathbf{B}$、洛伦兹力 $\mathbf{F}=q\mathbf{v}\times\mathbf{B}$、坡印廷矢量 $\mathbf{S}=\mathbf{E}\times\mathbf{B}/\mu_0$ 都用到它。

## A.2 导数

导数描述的是"变化得有多快"。函数 $f(t)$ 在 $t$ 处的导数定义为

$$\frac{df}{dt}=\lim_{\Delta t\to 0}\frac{f(t+\Delta t)-f(t)}{\Delta t} . \tag{A.7}$$

分子是函数值的改变量，分母是自变量的改变量，两者相除是平均变化率，取极限得到瞬时变化率。

几个反复用到的结果：

$$\frac{d}{dt}t^n=nt^{n-1},\qquad \frac{d}{dt}\sin\omega t=\omega\cos\omega t,\qquad \frac{d}{dt}\cos\omega t=-\omega\sin\omega t , \tag{A.8}$$

$$\frac{d}{dt}e^{at}=ae^{at},\qquad \frac{d}{dt}\ln t=\frac{1}{t} . \tag{A.9}$$

复合函数要链式求导。设 $y=f(u)$，$u=g(t)$，则

$$\frac{dy}{dt}=\frac{dy}{du}\frac{du}{dt} . \tag{A.10}$$

第二章算加速度时用的就是这一条：$a=dv/dt=(dv/dx)(dx/dt)=v\,dv/dx$。乘积的导数是

$$\frac{d}{dt}(fg)=f\frac{dg}{dt}+g\frac{df}{dt} . \tag{A.11}$$

偏导数是在多元函数里只对一个变量求导，其余变量当常数。$\partial f/\partial x$ 表示把 $y$、$z$ 固定，只看 $f$ 随 $x$ 的变化。第二十三章的梯度、散度、旋度都由偏导数构成。

## A.3 积分

积分是求和的极限。把区间 $[a,b]$ 切成 $n$ 小段，每段长 $\Delta x$，在第 $i$ 段里取一点 $x_i$，算 $f(x_i)\Delta x$，再全部加起来：

$$\int_a^b f(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^{n}f(x_i)\Delta x . \tag{A.12}$$

几何上这是曲线 $y=f(x)$ 与 $x$ 轴之间、从 $a$ 到 $b$ 的面积，在 $x$ 轴下方的部分算负。

积分与导数互为逆运算，这是微积分基本定理：

$$\int_a^b\frac{df}{dx}\,dx=f(b)-f(a) . \tag{A.13}$$

第二章从加速度求速度、从速度求位移，第四章从力求功，用的都是这一条。

常用的不定积分：

$$\int t^n\,dt=\frac{t^{n+1}}{n+1}\ (n\neq-1),\qquad \int\frac{dt}{t}=\ln t , \tag{A.14}$$

$$\int e^{at}dt=\frac{1}{a}e^{at},\qquad \int\sin\omega t\,dt=-\frac{1}{\omega}\cos\omega t,\qquad \int\cos\omega t\,dt=\frac{1}{\omega}\sin\omega t . \tag{A.15}$$

换元法把积分变成查表能查的形式。设 $u=g(x)$，$du=g'(x)dx$，则

$$\int f(g(x))g'(x)\,dx=\int f(u)\,du . \tag{A.16}$$

第十五章算直导线的磁场时用了三角换元，第七、八章算电势时用了 $u=r$ 这种最简单的换元。

分部积分由乘积求导公式移项得到：

$$\int u\,dv=uv-\int v\,du . \tag{A.17}$$

## A.4 几个常用的定积分

下面这几个结果在电磁学的积分里反复出现，直接列出。

$$\int_0^{\infty}\frac{dx}{(x^2+a^2)^{3/2}}=\frac{1}{a^2},\qquad \int_{-\infty}^{\infty}\frac{dx}{(x^2+a^2)^{3/2}}=\frac{2}{a^2} , \tag{A.18}$$

$$\int\frac{dx}{(x^2+a^2)^{3/2}}=\frac{x}{a^2\sqrt{x^2+a^2}} , \tag{A.19}$$

$$\int_0^{\pi}\sin\theta\,d\theta=2,\qquad \int_0^{2\pi}d\phi=2\pi , \tag{A.20}$$

$$\int_0^{\infty}e^{-ax}dx=\frac{1}{a}\ (a>0),\qquad \int_0^{\infty}xe^{-ax}dx=\frac{1}{a^2} . \tag{A.21}$$

(A.18) 的第一个结果用来算有限长直导线的磁场，(A.19) 用来算圆环轴线上的磁场，(A.20) 用来算球面与柱面的通量，(A.21) 在统计物理里出现，本书只在讨论漂移速度的量级时用到。

## A.5 球坐标与立体角

球坐标用三个数确定空间一点：到原点的距离 $r$，与 $z$ 轴的夹角 $\theta$（从 $0$ 到 $\pi$），在 $xy$ 平面上的投影与 $x$ 轴的夹角 $\phi$（从 $0$ 到 $2\pi$）。

$$x=r\sin\theta\cos\phi,\qquad y=r\sin\theta\sin\phi,\qquad z=r\cos\theta . \tag{A.22}$$

球面上的面积元是

$$dS=r^2\sin\theta\,d\theta\,d\phi . \tag{A.23}$$

除以 $r^2$ 得到立体角元

$$d\Omega=\sin\theta\,d\theta\,d\phi . \tag{A.24}$$

整个球面的立体角是 $4\pi$，半个球面是 $2\pi$。立体角的单位是球面度，记作 sr，它是个纯数，量纲为一。

柱坐标用 $(r,\phi,z)$，$r$ 是到 $z$ 轴的距离。柱面的面积元是 $r\,d\phi\,dz$，柱体的体积元是 $r\,dr\,d\phi\,dz$。

## A.6 泰勒展开与近似

把函数在一点附近展开成多项式：

$$f(x)=f(0)+f'(0)x+\frac{f''(0)}{2}x^2+\cdots . \tag{A.25}$$

$|x|\ll 1$ 时只保留前几项。本书用到三个：

$$(1+x)^n\approx 1+nx,\qquad \frac{1}{(1+x)^2}\approx 1-2x,\qquad e^x\approx 1+x . \tag{A.26}$$

第一个在第六章算偶极子远场时用，第二个在第七、八章算远处场强时用，第三个在第二十一章解 LR 电路时用（短时间内的电流增长）。

近似不是随便丢项。丢掉的项要比保留的项小得多，判断标准是展开参数 $|x|\ll1$。第六章算偶极子时，$x=a/r$，要求 $r\gg a$，即观察距离远大于电荷间距。这个条件如果不成立，偶极子近似就失效，必须老老实实算两个点电荷的叠加。
