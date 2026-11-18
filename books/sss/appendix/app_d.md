# 附录 D　术语对照

同一件事在不同圈子里有不同叫法，这里按主题列出。中文译名在正文里保持一致，英文原文放在括号里方便查文献。

## D.1 介质与参数

| 英文 | 中文 | 说明 |
| --- | --- | --- |
| participating medium | 参与介质 | 与光发生吸收、散射作用的介质 |
| absorption coefficient | 吸收系数 | $\sigma_a$ |
| scattering coefficient | 散射系数 | $\sigma_s$ |
| extinction coefficient | 消光系数 | $\sigma_a+\sigma_s$ |
| reduced scattering coefficient | 约化散射系数 | $(1-g)\sigma_s$ |
| albedo | 反照率 | 单次散射反照率 $\alpha$ |
| transport albedo | 输运反照率 | $\alpha'$，约化之后的版本 |
| mean free path | 平均自由程 | $1/\sigma_t$ |
| transport mean free path | 输运平均自由程 | $1/\sigma_t'$ |
| anisotropy parameter | 各向异性参数 | 相函数的平均余弦 $g$ |
| phase function | 相函数 | 散射方向的概率密度 |

## D.2 传输与近似

| 英文 | 中文 | 说明 |
| --- | --- | --- |
| radiative transfer equation | 辐射传输方程 | 缩写 RTE |
| single scattering | 单次散射 | 只散射一次的贡献 |
| multiple scattering | 多次散射 | 两次及以上 |
| diffusion approximation | 扩散近似 | 截断球谐到一阶 |
| P1 approximation | P1 近似 | 同上 |
| quantized diffusion | 量化扩散 | 按边界条件展开的扩散解 |
| fluence (rate) | 光通量密度 | 有的文献译作能流率 |
| vector flux / irradiance | 通量矢量 | 带方向的通量 |
| extrapolated boundary | 外推边界 | 虚构的零值平面 |
| partial current boundary condition | 部分电流边界条件 | 通量与通量密度成比例 |
| diffusion constant | 扩散系数 | $D=1/(3\sigma_t')$ |
| effective attenuation coefficient | 有效衰减系数 | $\mu_{\text{eff}}$ |
| diffusion length | 扩散长度 | $1/\mu_{\text{eff}}$ |

## D.3 表面与模型

| 英文 | 中文 | 说明 |
| --- | --- | --- |
| bidirectional reflectance distribution function | 双向反射分布函数 | BRDF |
| bidirectional surface scattering reflectance distribution function | 双向表面散射反射分布函数 | BSSRDF |
| separable BSSRDF | 可分离 BSSRDF | 方向因子乘径向剖面 |
| dipole | 偶极子 | 一正一负两个点源 |
| multipole | 多极子 | 无穷镜像序列 |
| directional dipole | 方向偶极子 | 沿入射方向排列的偶极 |
| reflectance profile | 反射剖面 | $R_d(r)$ |
| transmission profile | 透射剖面 | $T_d(r)$ |
| reflectance parameter | 反射参数 | $A$ |
| internal diffuse reflectance | 内部漫反射率 | $F_{dr}$ |
| mean cosine | 平均余弦 | $g$ 的另一种叫法 |

## D.4 数值方法

| 英文 | 中文 | 说明 |
| --- | --- | --- |
| Monte Carlo | 蒙特卡洛 | 随机抽样估计积分 |
| random walk | 随机游走 | 光子路径的直接模拟 |
| volumetric path tracing | 体积路径追踪 | 把介质当作散射体参与路径追踪 |
| importance sampling | 重要性采样 | 按被积函数的形状采样 |
| Russian roulette | 俄罗斯轮盘 | 按概率终止低权重路径 |
| next event estimation | 下一事件估计 | 直接连到光源 |
| multiple importance sampling | 多重重要性采样 | 两套 pdf 按权重合成 |
| white furnace test | 白炉测试 | 无吸收介质的能量守恒检验 |

## D.5 生物学相关

| 英文 | 中文 | 说明 |
| --- | --- | --- |
| stratum corneum | 角质层 | 皮肤最外层 |
| epidermis | 表皮 | 含黑色素细胞 |
| dermis | 真皮 | 含胶原与血管 |
| melanin | 黑色素 | 短波吸收强 |
| hemoglobin | 血红蛋白 | 有氧与脱氧两种状态 |
| blood volume fraction | 血容量分数 | 单位体积内的血液比例 |
| collagen | 胶原 | 真皮里的主要散射体 |
