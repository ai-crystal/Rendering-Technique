# 附录 B　NDF 与遮蔽函数速查

## B.1 法线分布

下表列出本书用到的两种分布。$c=\cos\theta_h=n\cdot h$，$\alpha$ 是粗糙度。

| 分布 | $D(h)$ | 归一化 |
| --- | --- | --- |
| Beckmann | $\dfrac{1}{\pi\alpha^2c^4}\exp\left(-\dfrac{1-c^2}{\alpha^2c^2}\right)$ | $\int D\,c\,d\omega=1$ |
| GGX | $\dfrac{\alpha^2}{\pi\left(c^2(\alpha^2-1)+1\right)^2}$ | $\int D\,c\,d\omega=1$ |

两者的差别在尾部。把 $c$ 趋于 0 看渐近行为，Beckmann 按指数衰减，GGX 按 $c^{-4}$ 衰减。幂律衰减的尾部更重，这就是 GGX 高光有长辉光的原因。

## B.2 遮蔽函数

Smith 模型的形式是

$$G_1(\omega)=\frac{1}{1+\Lambda(\omega)},\qquad G_2=\frac{1}{1+\Lambda(\omega_i)+\Lambda(\omega_o)} . \tag{B.1}$$

$\Lambda$ 对两种分布的表达式：

| 分布 | $\Lambda(\omega)$ |
| --- | --- |
| Beckmann | $\dfrac{1}{2}\left(\operatorname{erf}(a)+\dfrac{e^{-a^2}}{a\sqrt{\pi}}-1\right)$，$a=\dfrac{1}{\alpha\tan\theta}$ |
| GGX | $\dfrac{-1+\sqrt{1+\alpha^2\tan^2\theta}}{2}$ |

Beckmann 的表达式里有误差函数，没有初等闭式，实际实现中常用有理近似或者直接借用 GGX 的 $\Lambda$。

## B.3 可见法线分布的 pdf

用 VNDF 采样时，出射方向的 pdf 是

$$p(\omega_o)=\frac{G_1(\omega_i)\,D(h)}{4\cos\theta_i} . \tag{B.2}$$

用普通 NDF 采样时是

$$p(\omega_o)=\frac{D(h)\,(n\cdot h)}{4\,(\omega_i\cdot h)} . \tag{B.3}$$

两个式子的分母不同，混用会导致能量偏差。判断方法：如果采样代码里对 $h$ 做了"变换到半球"的操作，用 (B.2)；如果直接从 $D$ 采，用 (B.3)。

## B.4 采样公式

GGX 的 NDF 采样：

$$\theta_h=\arctan\left(\frac{\alpha\sqrt{u_1}}{\sqrt{1-u_1}}\right),\qquad \phi_h=2\pi u_2 . \tag{B.4}$$

GGX 的 VNDF 采样需要先把视线变换到椭球空间，步骤见第 10 章的代码。它的核心是把视线方向 $(\omega_x,\omega_y,\omega_z)$ 变成 $(\alpha\omega_x,\alpha\omega_y,\omega_z)$ 再归一化，然后在以该向量为轴的半球上均匀采样，最后变换回来。

## B.5 方向反照率

单次散射的方向反照率（$F=1$）：

$$E(\mu)=\int_\Omega \frac{D(h)\,G_2}{4\cos\theta_i\cos\theta_o}\cos\theta_o\,d\omega_o . \tag{B.5}$$

多次散射补偿项：

$$f_{\text{ms}}=\frac{(1-E(\mu_i))(1-E(\mu_o))}{\pi(1-E_{\text{avg}})} . \tag{B.6}$$

$E_{\text{avg}}=2\int_0^1E(\mu)\mu\,d\mu$。这两个量都可以预先算成表，运行时插值。
