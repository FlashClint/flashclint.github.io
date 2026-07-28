---
layout: post
title: "Calcein-containing Liposome Leakage Assay Protocol"
date: 2026-07-28
tags: [protocols, research-notes, liposome, membrane]
mathjax: true
comments: true
---

<div class="callout callout-note" markdown="1" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 - Reference</p>
  1. Hausig‐Punke, F., Richter, F., Hoernke, M., Brendel, J. C. & Traeger, A. Tracking the Endosomal Escape: A Closer Look at Calcein and Related Reporters. _Macromolecular Bioscience_ **22**, 2200167 (2022).
1
</div>

## 写在前面
liposome leakage assay 有一些常用的[荧光组合](https://www.thermofisher.cn/cn/zh/home/references/molecular-probes-the-handbook/technical-notes-and-product-highlights/assays-of-volume-change-membrane-fusion-and-membrane-permeability.html?utm_source=chatgpt.com)，包括：
- ANTS / DPX
- Tb<sup>3+</sup> / DPA
- fluorescein derivatives (比如calcein, carboxyfluorescein) (可搭配二价金属离子使用)

## Calcein 基本信息
- calcein  = fluorescein + iminodiacetic acid (EDTA的关键部分)，所以calcein同时具有荧光和螯合作用 (Ref.1)
![calcein_synthesis.png](/assets/img/protocols/calcein-leakage/calcein_synthesis.png)
- 其激发/发射谱如[下图](https://assets.thermofisher.cn/TFS-Assets/LSG/manuals/MAN0019058_CalceinAM_UG.pdf)：激发495 nm，发射515 nm
![calcein_spectrum.png](/assets/img/protocols/calcein-leakage/calcein_spectrum.png)
- calcein AM是一种能穿透细胞膜进入细胞、并在细胞内形成calcein的变体
### 影响calcein 发光的因素
(Ref.1)
![influencing_factor_of_calcein_fluorescence.png](/assets/img/protocols/calcein-leakage/influencing_factor_of_calcein_fluorescence.png)
#### 浓度
- 通常认为，calcein在浓度大于70 mM时会完全自淬灭（但不同条件下、不同文章给出的不尽相同）(Ref.1)
![calcein_quenching_concentration_table.png](/assets/img/protocols/calcein-leakage/calcein_quenching_concentration_table.png)
- 荧光强度随浓度的变化如下图 ([A](https://www.nature.com/articles/s41598-023-43813-4), [B](http://dx.doi.org/10.1023/a:1016832027325), [C](https://linkinghub.elsevier.com/retrieve/pii/S0731708598002295))
![calcein_fluorescence-intensity_vs_concentration.png](/assets/img/protocols/calcein-leakage/calcein_fluorescence-intensity_vs_concentration.png)
#### pH
荧光强度随pH变化的变化幅度：6-carboxyfluorescein > calcein >sulforhodamine B
calcain在pH4.5~10之间都能保持高荧光强度

#### 阳离子
- 碱土金属离子（Mg<sup>2+</sup>, Ca<sup>2+</sup>等）在碱性pH下会增强calcein的荧光，而在中性pH下只影响吸收谱、不影响荧光强度
- 过渡金属离子（Co<sup>2+</sup>, Ni<sup>2+</sup>等）在中性pH下会淬灭calcein荧光（[图片来源：ThermoFisher](https://www.thermofisher.cn/cn/zh/home/references/molecular-probes-the-handbook/indicators-for-ca2-mg2-zn2-and-other-metal-ions/fluorescent-indicators-for-zn2-and-other-metal-ions.html)）
<img src="/assets/img/protocols/calcein-leakage/calcein_quenched_by_metal-ions.png" alt="calcein_quenched_by_metal-ions.png" width="500" style="max-width:100%;height:auto;">
- 在高pH下，Na<sup>+</sup>离子会提高荧光强度，而K<sup>+</sup>几乎不会改变calcein荧光性质

## Protocol
概览(Ref.1)：
![calcein-containing_liposome_preparation.png](/assets/img/protocols/calcein-leakage/calcein-containing_liposome_preparation.png)

1. 将所需组分lipid吹制成膜，抽真空
2. 加入含~70 mM calcein 或者 1 mM calcein + 1 mM Co<sup>2+</sup> 的溶液，充分振荡使lipid完全溶解
<div class="callout callout-tip" markdown="1" style="background: #fffbeb; border-left: 4px solid #d97706; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #d97706;">💡 - 配制calcein 母液</p>
  - calcein酸性较强且在酸性条件下溶解性很低，因此需要用NaOH调pH、增加溶解度。实验上需要用pH计持续监测调pH的过程
- 在没有缓冲体系存在下，稀释calcein母液，体系pH会明显降低。如果想维持pH稳定，则需要过量的缓冲物质（比如HEPES、Tris等）
</div>

3. （可选项：在振荡后，先进行>5次的freeze-thaw cycle，据说可以提高calcein的包埋率）用extruder反复推拉>20次 或者 用超声处理
<div class="callout callout-note" markdown="1" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 - extrusion 和 sonication 的对比</p>
  extrusion是最常见的方法，且是控制liposome尺寸最好的方法，但有[文献](https://doi.org/10.3390/ma6083294)指出：由于shape relaxation，extrusion得到的liposome尺寸随时间（以天为单位）的增加会显著减少，并且lipid的流动性会在9天后显著降低，而sonication没有这种情况。但sonication的问题在于liposome size distribution较难控制。
</div>

4. 配制liposome外相溶液，尽量使内外等渗（[70 mM calcein和110 mM NaCl大致等渗](https://www.sciencedirect.com/science/article/pii/S0006349522006063)），对于包埋Co<sup>2+</sup>-calcein的liposome，外相中需要含有>1 mM EDTA
5. 用外相buffer过SEC柱 或 离心 或 超滤，来分离游离的calcein或者Co<sup>2+</sup>-calcein和包裹了染料的liposome
<div class="callout callout-note" markdown="1" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 - 分离方法对比</p>
  [文献](http://www.doi.org/10.26538/tjnpr/v6i9.6)指出：SEC会损失约40%的liposome，而1kD超滤几乎不会损失liposome；超滤会略微减小liposome的平均尺寸
</div>

6. 预实验确定合适的liposome稀释倍数：将liposome用外相buffer稀释成不同倍数后加入96孔板（黑色、低吸附），用荧光酶标仪测加入~0.2% (v/v) Triton X-100前后的荧光强度。比较合适的情况是，加入后强度为加入前的4~5倍。通常liposome的浓度在**1~100 μg/mL**
7. 预实验确定所研究蛋白/分子对荧光强度的影响：设计四组对照（无liposome存在）：<u>外相buffer</u>；<u>外相buffer + 蛋白/分子</u>；<u>外相buffer + calcein/Co<sup>2+</sup>-calcein</u>；<u>外相buffer + calcein/Co<sup>2+</sup>-calcein + 蛋白/分子</u>。并且最终都加入0.2% (v/v) Triton X-100。如果有显著影响，则需考虑优化浓度、降低影响，或者更换染料。
8. 正式实验：每组至少3个对照：<u>外相buffer</u>；<u>外相buffer+liposome</u>；<u>外相buffer+liposome+蛋白/分子</u>。最终均加入0.2% (v/v) Triton X-100
9. 数据处理：对荧光强度做归一化，荧光强度最大值可以用外相buffer+liposome加Triton X-100后得到的，也可以用外相buffer+liposome+蛋白/分子加Triton X-100后得到的

若干文章方案参考：

|                                 文献                                 |                                                 内相                                                  |                                         外相                                          |                        制备liposome                         |                                             分离                                             |
| :----------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------: | :-------------------------------------------------------: | :----------------------------------------------------------------------------------------: |
|                [a](https://bio-protocol.org/e3690)                 |                                           103 mM calcein                                            |                                          -                                          |                         extrusion                         |                                     Sephadex G -50 SEC                                     |
|    [b](https://www.tjnpr.org/index.php/home/article/view/1254)     |                                    HEPES pH7.4<br>107 mM calcein                                    |                                     HEPES pH7.4                                     | 5 cycles 液氮-60℃,<br>sonication 30min,<br>extrusion 200 nm | Sephadex G -25 SEC<br>or<br>1kD-ultrafiltration 4000 rpm for 15 min (total dilution: 4096) |
|            [c](https://doi.org/10.1074/jbc.M200429200)             |                                        HBS<br>90 mM calcein                                         |                                         HBS                                         |                    extrusion 50~600 nm                    |                     100,000g-centrifugation of 1 mL solution 45 min ×2                     |
|         [d](https://doi.org/10.1016/0005-2736(95)80035-E)          | 150 mM H<sub>2</sub>BO<sub>3</sub> <br>pH 9<br>5 mM EDTA<br>5 mM KOH<br>20 mM NaCl<br>80 mM calcein | 150 mM H<sub>2</sub>BO<sub>3</sub> <br>pH 9<br>5 mM EDTA<br>5 mM KOH<br>140 mM NaCl |                     extrusion 100 nm                      |                                     Sephadex G -50 SEC                                     |
|      [e](https://www.nature.com/articles/s41598-023-43813-4)       |                                       pH 7.7<br>30 mM calcein                                       |                               borate buffer<br>pH8.5                                |           sonication 2 min<br>extrusion 200 nm            |                             3000rpm-centrifugation 1h of 1 mL                              |
|            [f](https://doi.org/10.1073/pnas.0606129103)            |                                            60 mM calcein                                            |                        10 mM HEPES<br>pH 7.4<br>150 mM NaCl                         |                             -                             |                                     Sephadex G -50 SEC                                     |
| [g](https://www.embopress.org/doi/full/10.1038/s44318-024-00190-6) |                                       pH 7.0<br>80 mM calcein                                       |                  20 mM HEPES<br>pH 7.0<br>140 mM NaCl<br>1 mM EDTA                  |                         extrusion                         |                                     Sephadex G -50 SEC                                     |
|      [h](https://www.nature.com/articles/s41467-023-39726-5)       |             50 mM phosphate buffer<br>pH 7.0<br>1 mM CoCl<sub>2</sub><br>0.8 mM calcein             |                   35 mM phosphate buffer<br>pH 7.0<br>10 mM EDTA                    |            5 cycles 液氮-温水<br>extrusion 400 nm             |                   Sephadex G -75 SEC,<br>444,000g-centrifugation 25 min                    |
|        [i](https://doi.org/10.1021/acsbiomedchemau.5c00084)        |                                       pH 7.4<br>80 mM calcein                                       |                 50 mM HEPES<br>pH 7.4<br>100 mM NaCl<br>0.3 mM EDTA                 |         3 cycles freeze-thaw<br>extrusion 100 nm          |                                     Sephadex G -50 SEC                                     |

## Additional Notes
### 关于DMSO
在liposome leakage assay中，如果需要用DMSO作为外相，**最好做无DMSO存在时的对照**。根据经验，4% DMSO下DOPC GUV无法透过FITC （MW: 389 Da）。[文献](https://doi.org/10.3389/fmicb.2021.669709)指出：DMSO ≤5%时不会影响他们研究的peptide引起的liposome leakage

### 关于calcein释放后浓度的估算
假设溶液中lipid的浓度为\(C_{lipid}\)，liposome内包埋的calcein浓度为\(C_0\)，溶液体积为\(V\)，liposome上每个lipid分子平均占据的面积为\(A\)，liposome的平均半径为\(R\)，最终全部释放后的calcein浓度 为\(C_f\)，则
$$
\begin{align}
C_f &=C_0 \cdot N_{liposome}\cdot \frac{4}{3}\pi R^3/V\\
&= C_0 \cdot \frac{N_A ~ C_{lipid} ~ V}{2\cdot 4\pi R^2/A} \cdot \frac{\frac{4}{3}\pi R^3}{V}\\
&= C_0 \cdot \frac{1}{6} N_A ~ C_{lipid} ~ A ~ R \tag{1}
\end{align}
$$
[已知](https://doi.org/10.1016/j.bbamem.2012.05.006)\(A \approx 0.6 ~\mathrm{nm^2}\)，设：
$$
C_{lipid} = x~\mathrm{mM}, ~~~ C_0=y~\mathrm{mM}, ~~~R=r\times 10^2 ~ \mathrm{nm}
$$
代入公式(1)，得：
$$
\begin{align}
C_f &= y~\mathrm{mM}\cdot \frac{1}{6}\cdot 6.02\times10^{23}\cdot x\times 10^{-3} ~\mathrm{mol/L} \cdot 0.6\times10^{-16} ~\mathrm{dm^2} \cdot r\times10^{-6}~\mathrm{dm}\\
&=6.02\times10^{-3}\cdot x\cdot y \cdot r~\mathrm{mM}
\end{align}
$$

