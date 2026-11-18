# 附录 A　数学工具箱

## A.1 立体角

球面上的面积元 $dA$ 除以半径平方，得到立体角

$$d\omega=\frac{dA}{r^2} . \tag{A.1}$$

用球坐标 $(\theta,\phi)$ 表示，单位球面上

$$d\omega=\sin\theta\,d\theta\,d\phi . \tag{A.2}$$

半球的立体角是 $2\pi$，整个球是 $4\pi$。

投影立体角是另一个常用量：一个面元从某个方向看过去的有效面积，等于它的面积乘上看的方向与法线的余弦。半球上的积分经常写成

$$\int_\Omega \cos\theta\,d\omega=\pi . \tag{A.3}$$

这个 $\pi$ 在漫反射的归一化里反复出现。

## A.2 方向向量与角度

单位方向 $\omega$ 与法线 $n$ 的夹角为 $\theta$，于是

$$\cos\theta=\omega\cdot n . \tag{A.4}$$

给定两个方向 $\omega_1,\omega_2$，它们的夹角余弦是内积。半程向量定义为

$$h=\frac{\omega_1+\omega_2}{\|\omega_1+\omega_2\|} , \tag{A.5}$$

它平分两个方向的夹角。

球坐标到笛卡尔坐标的换算是

$$\omega=(\sin\theta\cos\phi,\;\sin\theta\sin\phi,\;\cos\theta) . \tag{A.6}$$

## A.3 立体角的映射与雅可比

从一套坐标换到另一套时，密度要乘雅可比。反射与透射各有一个常用的映射。

镜面反射把微面法线映射到出射方向：

$$\omega_o=2(\omega_i\cdot h)h-\omega_i , \tag{A.7}$$

对应的雅可比是

$$\frac{d\omega_o}{d\omega_h}=4\,|\omega_i\cdot h| . \tag{A.8}$$

这个 4 是第 6 章那个分母的来源。

折射的映射复杂一些，雅可比是

$$\frac{d\omega_o}{d\omega_h}=\frac{\eta_o^2\,|\omega_o\cdot h|}{\eta_i^2\,|\omega_i\cdot h|^2} . \tag{A.9}$$

## A.4 Delta 函数

理想镜面的 BRDF 是一个 delta 函数：

$$f_r(\omega_i,\omega_o)=F(\omega_i)\,\delta\big(\omega_o-R(\omega_i)\big) , \tag{A.10}$$

其中 $R$ 是镜面反射算子。delta 函数的作用是在积分里把方向固定住：

$$\int_\Omega g(\omega_o)\,\delta\big(\omega_o-\omega_0\big)\,d\omega_o=g(\omega_0) . \tag{A.11}$$

在球面上，delta 函数用立体角定义，所以积分不需要额外的 $\sin\theta$ 因子。这一点在写代码时容易搞错，因为离散化之后面积元里确实有 $\sin\theta$。

## A.5 常用积分

几个在推导里反复出现的积分，列在这里方便查阅。

$$\int_0^{\pi/2}\sin\theta\cos\theta\,d\theta=\frac{1}{2} , \tag{A.12}$$

$$\int_0^{2\pi}\cos^2\phi\,d\phi=\pi , \tag{A.13}$$

$$\int_0^1 x^n\,dx=\frac{1}{n+1} , \tag{A.14}$$

$$\int_\Omega (\omega\cdot n)^n\,d\omega=\frac{2\pi}{n+1} . \tag{A.15}$$

最后这个在计算 Fresnel 平均、方向反照率的时候会用到。

## A.6 数值积分的做法

本书所有积分类的插图都是用同一个方法算的：在半球上按 $(\theta,\phi)$ 均匀划分网格，取每个小格的中心点，乘以对应的面积元。

$$\int_\Omega f(\omega)\,d\omega\approx\sum_{i,j}f(\theta_i,\phi_j)\,\sin\theta_i\,\Delta\theta\,\Delta\phi . \tag{A.16}$$

网格密度取 $180\times360$ 就足够，误差在 $10^{-4}$ 量级。如果要算的函数据在掠射角附近有尖峰，需要加密 $\theta$ 方向的网格，或者在 $\cos\theta$ 上均匀划分。

代码在 `books/common/bsdf.py` 的 `integrate_hemisphere` 里，直接调用即可。
