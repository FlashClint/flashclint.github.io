---
layout: post
title: "PeakForce Tapping AFM Protocol"
date: 2026-07-28
tags: [protocols, research-notes, AFM, biophysics]
mathjax: true
comments: true
---

## 探针选择
- k 要接近或者大于样品模量对应的“劲度系数”，使得探针能够在样品表面产生形变
	- 对于生物样品，一般选择 0.01~0.5 N/m (from <span style="background:rgba(240, 107, 5, 0.2)">Dufrene & Muller, Nat. Methods (2013)</span>)
	- 对于生物样品，在不知道样品模量时，可先尝试0.1N/m (from <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne</span> & <span style="background:rgba(240, 107, 5, 0.2)">Muller, Nat. Protoc (2014)</span>)
- 液相f (一般为气相的1/3)要显著大于 (大于5倍(<span style="background:rgba(240, 107, 5, 0.2)">Dufrene & Muller, Nat. Methods (2013)</span>)) PFT的工作频率(1~2kHz)，防止工作时因为接近探针共振频率、探针被激励，产生inertia effect &  hydrodynamic drgging，对成像产生影响
	- 因为$Q \sim f/\Delta f$，low Q 意味着，$\Delta f$较大，悬臂梁在远离共振频率较远时也能被激励
	- 对于快速成像，需要用$f>100~kHz$的悬臂梁
- force sensitivity尽量高，但存在tradeoff，即 high force sensitivity 往往对应 high Q-factor，而high Q-factor对快速成像不利(from <span style="background:rgba(240, 107, 5, 0.2)">Dufrene & Muller, Nat. Methods (2013)</span>)
- 有金属镀层的探针可能会有较大的drift，影响力控制的精度
- **钝针通常不会变尖，但尖针会逐渐变尖** (from <span style="background:rgba(240, 107, 5, 0.2)">Muller, Nat. Protoc (2014)</span>)
	- In any case, achieving high-resolution FD-based AFM topographs and images takes patience. The operator **needs to wait for the stylus to get sufficiently sharp** to contour structural details of the proteins. (from <span style="background:rgba(240, 107, 5, 0.2)">Muller, Nat. Protoc (2014)</span>)
- 同一批次的探针可能会有相同的污染情况，如果遇到状态不好的针可以换一批探针

## 探针校准
- 在扫描前&扫描后、或者 改变激光照射位置后，都用一些硬基底(如：mica、glass等)来校针的deflection sensitivity
<div class="callout callout-tip" style="background: #fffbeb; border-left: 4px solid #d97706; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #d97706;">💡 测量sensitivity的方法</p>
  <div style="margin: 0;">一般说的deflection sensitivity又被称为 z scan sensitivity
- 对于z scan sensitivity，用ramp，设置：trigger mode: relative; trig threshold: <0.5V
- 对于PeakForce QNM，还需校准 Drive3 Amplitude Sensitivity (校准流程参见b站BrukerAFM课)
- 若Drive3设置正确，则high-speed capture里height sensor的振幅与设置的peakforce amplitude应该会相同</div>
</div>
<div class="callout callout-note" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 探针的deflection sensitivity 在扫描过程中可能会发生变化，其可能原因为：</p>
  <div style="margin: 0;">- 温度变化导致的激光位置偏移
- 探针表面反光度 因为沾染东西 或 涂层脱落等原因 发生变化

**在几个小时的扫描后，探针deflection sensitivity变化5~8%是可接受的**
*from:  Muller, Nat. Protoc (2014)*</div>
</div>
- 测 k 需要让探针远离基底至少100μm
	- 测得的 k 通常可能会与 nominal k 相差较大（可能会相差到3倍）


## 成像参数
#### 进针
- 按照每次增加~10 pN的方法从小engage setpoint开始进针，直到找到最小的进针engage setpoint
- 进针时的gain值不能太大，否则容易伤针，推荐值：10 (from <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne, Chromosome Architecture (2022)</span>)
- 增大engage setpoint 或 增大gain值都可以提高进针的速率
- 如果不使用ScanAsyst Auto Setpoint，进针后系统会把setpoint设置成peak force setpoint

#### Sync Distance
- 进针后要<font color="#ff0000">立即</font>设定 sync distance， 否则容易伤针
	- 可以用 autoconfig 来设置该值，但对于小力情况(the peak force will be barely discernible above the noise)，则需要手动调
<div class="callout callout-note" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 Note</p>
  <div style="margin: 0;">- Bruker Multimode 8的Force Monitor里，蓝线为approach，红线为retract
- autoconfig的另一用处：分析并消除parasitic deflection (即ringing at the pulling-off point，一般包括：探针脱离表面的自由振荡、piezo周期变化带来的探针形变、粘滞力影响)</div>
</div>
<div class="callout callout-tip" style="background: #fffbeb; border-left: 4px solid #d97706; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #d97706;">💡 Auto Config for small peak force setpoint (< ~20mV)</p>
  <div style="margin: 0;">小setpoint情况下用auto config可能会导致探针直接脱离表面，因此需要先设置一个较大的setpoint，然后用auto config，之后再调回小的setpoint</div>
</div>
- Sync Distance QNM是通过硬样品校准后得到的（之后不需要修改），而Sync Distance New则是用于feedback，需要在扫描时调节
- Alice Pyne的观点：(from <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne, Chromosome Architecture (2022)</span>)：先优化Sync Distance New，使小圆点在Force-Time曲线的peak force处，再把Sync Distance QNM设置成与Sync Distance New相同的值，并检查Force-Z曲线是否关于小圆点”对称“ <font color="#548dd4">(这也可以作为一种检查Sync Distance New是否被调得正确的方法，即：如果将Sync Distance QNM设得和Sync Distance New一致后Force-Z曲线关于小圆点对称，则设置正确)</font>
- 当PeakForce Frequency改变时，Sync Distance也要相应地变化，一般frequency double时sync distance要减小为1/3(from <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne, Chromosome Architecture (2022)</span>)
	- <u>个人认为，这个建议可能是针对以μs为单位的sync distance，而不是MM8上以%为单位的sync distance</u>
- 

#### Amplitude
**小振幅是为了让针尖处于短程力区、实现高衬度(high contrast)，同时也能减少流体力的扰动，但振幅不能过小，防止样品损伤**
- large oscillation amplitudes <font color="#ff0000">(~10–100 nm)</font> are desirable for measuring long-range interactions (e.g., **electrostatic and hydrophobic**), whereas small oscillation amplitudes (<<font color="#ff0000">3 nm</font>) are suitable for sensing short-range interactions (e.g., **Pauli repulsion and van der Waals**) (from <span style="background:rgba(240, 107, 5, 0.2)">Dufrene & Muller, Nat. Methods (2013)</span>)
- amplitude可以调整到与蛋白突起高度差不多 (对于膜蛋白：4~15 nm) (from <span style="background:rgba(240, 107, 5, 0.2)">Muller, Nat. Protoc (2014)</span>)，或 突起高度的~2倍(from <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne, Chromosome Architecture (2022)</span>)
- at too-high amplitudes the force feedback may be impaired and the biological sample may be damaged (from <span style="background:rgba(240, 107, 5, 0.2)">Muller, Nat. Protoc (2014)</span>)
- 

#### Lift height
- 定义为：针尖与样品不再发生作用的抬针高度，对应力曲线上开始变平缓的点，是做auto config时的抬针高度
- lift height 是与 auto config捆绑的：点击<u>auto config按钮</u>时会自动计算lift height，然后在该lift height上做auto config操作；手动改变lift height后会触发auto config在所指定的lift height上做
- 如果手动设置，可以观察力曲线，将其设置为力曲线开始变平缓的点（lift height应该要比 感兴趣的分子的突起更高）
- 即使是在小振幅、小力下，通过调整lift height可以使基线变得平整(from <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne, Chromosome Architecture (2022)</span>)

#### Setpoint
- 小力可能会导致力曲线噪声较大，此时可以提高力来提高信噪比
- **开始扫描后一定要修改 approach setpoint，使其$\le$ imaging setpoint**，因为当改变peak force amplitude, lift height, sync distance或者用autoconfig时，都会触发tip engage

#### Gain
**目标：找到系统的那个最优ratio between I gain and P gain**
- 调gain流程：(from<span style="background:rgba(240, 107, 5, 0.2)"> Atomic Force Microscopy for Life Sciences  ~~ by Bruker</span>)
	1. 增大I gain直到信号开始振荡后 适当减小
	2. 增大P gain直到信号开始出现振荡后 适当减小
	3. 重复1, 2直到稍微增大gain后不出现振荡
- 一般需要先把力调到最小，再优化feedback gain和scan rate
- 最佳的gain：刚好在信号出现振荡 或者说 形貌图上噪声明显增加 之前的gain

#### Lowpass filter (似乎与”LP Deflection BW“所控制的东西不同？)
目的：用于减少baseline中在pull off时发生的ringing现象
- 通常设置为peak force frequency的~20倍  (<65 kHz) (from <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne's doctoral thesis (2015)</span>)
- 但如果设置的值过低，会 distort force curve、再分析力学性质时引入误差
<div class="callout callout-note" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 "LP Deflection BW"</p>
  <div style="margin: 0;">This parameter invokes user-programmable low pass filter to remove high frequency noise from the real-time data. The filter operates on the collected data regardless of scan direction. The cutoff frequency can be set from 1~65 kHz
相比之下，Peakforce里的lowpass deflection bandwidth (MM8里没有这个参数)只能设置为10~65.56 kHz</div>
</div>
#### 扫描策略
- 进针后顺序 (from <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne, Chromosome Architecture (2022)</span>)
	1. setpoint (使其稍微超过力噪声，~70 pN)
	2. Sync Distance New & QNM
	3. Lift Height (下策：Auto Config)
	4. 大范围扫描+调gain+可能需要增加setpoint(+ 调gain)
	5. zoom in 到小范围，增加pixel数，使得resolution $\le$ ~0.5 nm
	6. 减小setpoint (+ 调gain)
- 从大范围到小范围：
	- 大范围：scan rate: 1~2 Hz, Peakforce amplitude: 40~60 nm <font color="#245bdb">(compensate for large obstacles and the tilt of the support)</font>
		- 可通过调节scan angle来compensate for the tilt of the support
	- 小范围：从大范围zoom in，调节amplitude使得topographic contrast达到最佳，Peakforce amplitude: membrane proteins, 4~15 nm; protein fibrils, 10~25 nm (from <span style="background:rgba(240, 107, 5, 0.2)">Muller, Nat. Protoc (2014)</span>)
		- 转到小范围扫描，可能需要适当减小setpoint
		- 扫描速度要适当增大，防止一个像素点采很多条力曲线导致样品被破坏
		- 如果在小范围观察到样品”拉伸“”creep“，则需要采用更快的扫描速度、或者让仪器更稳定一些


## 其他方面
#### 仪器的稳定与平衡
**标准：使探针在施加力的精度在a few pN**
- 使用mechanical vibration analyzer检测仪器的机械振动情况，电磁噪声则可以分析AFM的input和output信号。更可行的方法是，通过监测探针在远离基底 和 靠近基底时的振动情况，判断仪器稳定性
- 在制作基底时避免引入气泡
- 避免仪器的各种电线受机械或噪声影响
- 仪器及相关仪器最好在扫描前几个小时就打开，来尽量避免drift；上样后系统达到完全平衡，可能需要1h，可以通过监测deflection通道 或者 看diode信号("VERT", "HORI")来判断
- 对于k较小的探针，热噪声通常是最大的噪声来源
- cantilever drift对应的一般是，探针会呈现出一定程度的持续弯曲
<div class="callout callout-tip" style="background: #fffbeb; border-left: 4px solid #d97706; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #d97706;">💡 如果仪器实在无法稳定，则依次判断：</p>
  <div style="margin: 0;">- 如果仪器在液相和气相都不稳定，则有可能是周围热源影响 或者 仪器本身出问题
- 如果仪器只在液相不稳定，则比较可能是探针的问题

*(from:  Muller, Nat. Protoc (2014))*</div>
</div>
<div class="callout callout-note" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 Possible causes of a large hysteresis between trace and retrace:</p>
  <div style="margin: 0;">- 探针没夹紧
- 基底不稳定（有气泡、胶没粘牢、撕mica时带起了一部分mica但未完全解离后又回落至基底）
- feedback gain 太低

*(from:  Muller, Nat. Protoc (2014))*</div>
</div>
#### 样品的洁净度
**标准：对空mica进行扫描，没有发现杂质**
- 使用nanopure, double-distilled or ultrapure water，而不是deionized water来避免水中的残留离子或有机物
- 用dishwashing detergent和filtered nanopure water依次清洗基底 或者 液池
- 用装有滤网的N<sub>2</sub>枪吹，而不是压缩空气
- buffer一周内用完
- 装样品或buffer的容器需要用nanopure water先清洗一遍

#### 其他
- 基底构造：
	- 直径0.5~1 cm mica放在直径1.5~2 cm Teflon foil上，再固定到铁片上(from <span style="background:rgba(240, 107, 5, 0.2)">Muller, Nat. Protoc (2014)</span>)
- **防止粘针的小妙招**：在buffer里加glycerol (< 30% (v/v))
- 时间管理小妙招：
	- 在制样时，用干净buffer弄个干净mica代替样品，之后放上探针打开激光，让整个系统平衡稳定
- 关于高分辨的一些观点：
	- “Proteins and fibrils that protrude by more than 3 nm from the mica surface may be imaged at a resolution **approaching 2 nm**, because such ‘large’ protrusions are likely to be structurally flexible and their protruding height prevents the proper contouring of the sample surface by the AFM stylus.” (from <span style="background:rgba(240, 107, 5, 0.2)">Muller, Nat. Protoc (2014)</span>)
	- “There are a number of complications that currently prevent AFM from achieving atomic resolutions on biomolecules. These include: The binding of the biomolecule to an appropriate substrate, mobility of the molecule, the presence of contamination, the effect of forces exerted by the tip on the sample, and the difficulties in following the contours of a more complex and highly corrugated molecule using a feedback system, whilst accurately controlling the tip sample interaction and therefore the imaging force.” (from <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne's doctoral thesis (2015)</span>)
- 参数参考：(from <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne's doctoral thesis (2015)</span> & <span style="background:rgba(240, 107, 5, 0.2)">Alice Pyne, Chromosome Architecture (2022)</span>)
	- ![AlicePyne_doctoral_thesis_Table3.1.png](/assets/img/protocols/peakforce-tapping/AlicePyne_doctoral_thesis_Table3.1.png)(AlicePyne_doctoral_thesis_Table3.1.png = 400x)]
	- ![AlicePyne_Chromosome_Architecture(2022).png](/assets/img/protocols/peakforce-tapping/AlicePyne_Chromosome_Architecture(2022).png)(AlicePyne_Chromosome_Architecture(2022).png = 400x)]
- 