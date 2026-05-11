# A5ED052A B32A VCC / SmartVID 供电设计报告

日期：2026-05-11

目标器件：`A5ED052AB32AE2V`

封装：`B32A`

状态：原理图设计建议版。最终 release 前仍需 FAE、Quartus、PDN 分析闭环确认。

## 1. 核心结论

`A5ED052AB32AE2V` 的 `VCC/VCCP` 不应按普通固定 `0.8 V` Buck 设计，而应按 **SmartVID 可调核心电源**设计。

推荐板级架构：

- 建立一个 SmartVID 核心电源轨，命名为 `A5E_VCC_VID`。
- FPGA 的 `VCC` 和 `VCCP` 全部接到 `A5E_VCC_VID`。
- regulator 初始/NVM 输出设为 `0.80 V`。
- 默认采用 `PMBus Master Mode`，除非项目明确有外部系统电源控制器负责 VID。
- Agilex SDM PMBus 管脚连接：
  - `CF109 / SDM_IO14 / PWRMGT_SCL` 接 regulator PMBus `SCL`。
  - `CF99 / SDM_IO11 / PWRMGT_SDA` 接 regulator PMBus `SDA`。
- 远端采样连接：
  - `AV72 / VCCLSENSE` 接 regulator sense positive，采样点靠近 FPGA 负载端。
  - `AU72 / GNDSENSE` 接 regulator sense negative / ground sense，采样点靠近 FPGA 负载端。
- 保留 `BP102 / SDM_IO16` 作为 `CONF_DONE`。
- 保留 `CA99 / SDM_IO0` 作为 `INIT_DONE`。
- `BR99 / SDM_IO12` 先作为可选 `PWRMGT_ALERT` / 状态信号 / DNP 兼容位，等 PMBus 模式冻结后再定。

推荐 regulator 路线：

1. 产品首版优先：选 Intel/Altera 对 Agilex 5 fully validated 的 SmartVID regulator，例如 `TPS53676`、`LTC3882-1` 或 `ISL68223`。
2. 参考设计复制路线：参考 KEIm 的 `LTC7883AY#PBF + NCP302035MNTWG` 拓扑，但仅在 FAE 对本项目和 Quartus 版本确认后采用。原因是 Altera 对 Agilex 5 把 `LTC7883` 标为 API validated only，不是 fully validated。

## 2. 资料优先级

本报告按以下优先级使用资料：

1. Intel/Altera 官方 Power Management 文档。
2. Intel/Altera 官方 A5ED052A B32A pinout。
3. Intel/Altera 官方 065B B32A SOM 参考原理图。
4. KEIm A5E SOM 供应商参考原理图和 BOM。
5. 本地派生 workbook 和 notes。

已核查的本地资料：

- `sources/official_pinouts/a5ed052a/a5ed052A.xlsx`
- `sources/reference_schematic/agilex-5e-mdevkit-som-sch-v2p1.pdf`
- `sources/vendor_reference/keim-a5esom_sch_rev1.10.pdf`
- `sources/vendor_reference/keim-a5esom_bom_rev1.10-.xlsx`
- `sources/vendor_reference/keim-a5esom_hardware_manual_EN_v1.1.pdf`

官方在线资料：

- Altera Power Management User Guide: Agilex 5 FPGAs and SoCs，SmartVID / PMBus 章节。
- Altera FPGA SmartVID regulator 页面。
- Altera Pin Connection Guidelines: Agilex 5 FPGAs and SoCs。
- Altera A5ED052A pin information document 830449。

## 3. 官方要求解读

Agilex 5 官方 Power Management 文档说明：Agilex 5 的 `-V` / `-E` SmartVID 器件，`VCC` 和 `VCCP` 需要由 PMBus-compliant voltage regulator 供电。SDM Power Manager 会读取器件内部的 VID fuse，然后在 FPGA 配置前通过 PMBus 调整 regulator 输出。

对本项目的解释：

- `A5ED052AB32AE2V` 包含 `-2V` speed/power suffix。
- 除非 FAE 明确证明不是 SmartVID 器件，否则应按 SmartVID 器件处理。
- 不应把 `VCC/VCCP` 设计成没有 PMBus 控制路径的固定 `0.8 V` 输出。
- SmartVID 不只是硬件问题，也必须在 Quartus 中配置。

Altera SmartVID 页面列出的 Agilex 5 推荐 PMBus regulator：

- Agilex 5 fully validated：
  - `TPS53676`
  - `LTC3882-1`
  - `ISL68223`
- API validated only：
  - `LTC7883`

因此，对新产品而言，`TPS53676 / LTC3882-1 / ISL68223` 风险更低；`LTC7883` 有参考价值，但更适合作为已有参考设计的佐证，而不是默认首选。

## 4. A5ED052A B32A 相关 pin

来自 A5ED052A B32A 官方 pinout：

| Rail / Pin | Ball 数量 | B32A ball |
|---|---:|---|
| `VCC` | 41 | `BA61, AY75, AY68, AY64, AY57, AY53, AW79, AW72, AW68, AW61, AW57, AV86, AV83, AV75, AV64, AV61, AV53, AU79, AU75, AU68, AU64, AU57, AU53, AT79, AT72, AT68, AT61, AT57, AR83, AR75, AR72, AR64, AR61, AR53, AP86, AP79, AP75, AP68, AP64, AN79, AN72` |
| `VCCP` | 14 | `BB72, BB68, BB61, BB57, BB50, BA64, BA53, AN68, AN57, AM75, AM72, AM64, AM61, AM53` |
| `VCCLSENSE` | 1 | `AV72` |
| `GNDSENSE` | 1 | `AU72` |
| `PWRMGT_SCL` | 1 | `CF109 / SDM_IO14` |
| `PWRMGT_SDA` | 1 | `CF99 / SDM_IO11` |
| 可选 `PWRMGT_ALERT` | 1 | `BR99 / SDM_IO12`，或其它 Quartus 支持的 SDM 选项 |

注意：不要看到某个 rail 是 `0.8 V` 就自动接到 `A5E_VCC_VID`。官方强制 SmartVID 的核心对象是 `VCC/VCCP`；其它低压 rail 必须根据当前 Pin Connection Guidelines 和 FAE 反馈单独确认。

## 5. 参考设计分析

### 5.1 Intel/Altera 065B B32A SOM 官方参考

官方 065B B32A SOM 参考设计使用的 SDM/JTAG/config ballout 与本项目相关 pin 一致。它确认了：

- `CF109` 可作为 PMBus `SCL`。
- `CF99` 可作为 PMBus `SDA`。
- `BP102` 可作为 `CONF_DONE`。
- `CA99` 可作为 `INIT_DONE`。
- 供电设计中存在 SmartVID 风格核心 rail。

这是最强的真实板级参考，因为它来自 Altera 官方开发板原理图。

### 5.2 KEIm A5E SOM 参考

供应商资料中包含 `keim-a5esom_sch_rev1.10.pdf` 和 BOM。与 VCC/SmartVID 相关的发现：

- 电源页明确命名为 `Power VID`。
- 主 VID controller 是 `LTC7883AY#PBF`。
- 功率级是 `NCP302035MNTWG`。
- 输出 rail 命名为 `VCC_VID`。
- 原理图标注 `VCC_VID` 电流能力为 `27A/41A`。
- 电压注释显示 `-1, -2, -3` power grade 使用 `VID`，更低 speed grade 使用固定电压。
- `VCC` 和 `VCCP` 接到 `VCC_VID`。
- `VCCLSENSE_AV72` 和 `GNDSENSE_AU72` 通过 0R 接到 VID sense 网络。
- PMBus 同时暴露了 SDM PMBus 路径和 SOM/carrier PMBus 路径。

重要限制：

KEIm 是模块设计，PMBus 架构包含 carrier / 系统管理访问，不是“独立最小系统板”的一比一模板。是否能直接复制，取决于启动时到底谁拥有 PMBus：Agilex SDM、外部系统控制器，还是带严格仲裁的多主系统。

## 6. 推荐原理图设计

### 6.1 核心电源命名

建议命名：

```text
A5E_VCC_VID
```

连接对象：

```text
FPGA VCC pins
FPGA VCCP pins
```

不建议简单命名为 `+0V8`。`A5E_VCC_VID` 能明确表达这是 VID 可调、PMBus 控制的核心电源。

### 6.2 Regulator 架构

推荐框图：

```text
5V or 12V input
  -> PMBus-capable multiphase regulator/controller
  -> power stage(s)
  -> +A5E_VCC_VID
  -> A5ED052A VCC/VCCP pins

A5ED052A SDM PMBus
  CF109 / PWRMGT_SCL
  CF99  / PWRMGT_SDA
  -> regulator PMBus interface
```

Regulator 选择：

- 优先 `TPS53676`、`LTC3882-1` 或 `ISL68223`，除非 FAE 推荐其它器件。
- 电流能力必须由 Quartus Power Analyzer / EPE 估算。
- 不要直接照抄 KEIm 的 `27A/41A` 电流能力。KEIm 板使用的是 `A5ED065B`，你的 `A5ED052A` 资源使用、频率、温度条件都可能不同。

### 6.3 PMBus 电气连接

如果 regulator PMBus 支持 `1.8 V`：

```text
CF109 / PWRMGT_SCL ---- regulator SCL
CF99  / PWRMGT_SDA ---- regulator SDA
两根线都上拉到 VCCIO_SDM / 1.8 V
```

如果 regulator PMBus 只能工作在 `3.3 V`：

```text
CF109 / CF99 at 1.8 V
  -> bidirectional level shifter
  -> regulator PMBus at 3.3 V
```

要求：

- 使用兼容 open-drain 的 PMBus/I2C 双向电平转换。
- Agilex 侧上拉建议 `5.1 kΩ` 到 `10 kΩ` 到 `VCCIO_SDM`。
- Regulator 侧上拉按 regulator datasheet，常见为 `3.3 V`。
- 避免 `VCCIO_SDM` 未上电时通过 PMBus 反灌电。
- 如果 level shifter 带 OE，必须定义 OE 默认状态。

### 6.4 PMBus 模式

推荐模式：

```text
PMBus Master Mode
```

原因：

- 最小系统更简单。
- Agilex SDM 可以直接设置核心 VID regulator。
- 不依赖外部 MCU/PMIC firmware 在 FPGA 配置早期就已经运行。

不要轻易选 PMBus Slave/Target Mode，除非：

- 外部控制器一定早于 Agilex 配置阶段启动。
- 外部控制器完整实现 VID/PMBus 流程。
- `PWRMGT_ALERT` 已连接，并且 Quartus 配置与之匹配。

### 6.5 Sense 连接

连接：

```text
AV72 / VCCLSENSE -> regulator remote sense positive
AU72 / GNDSENSE  -> regulator remote sense negative / ground sense
```

建议实现：

- 按 Kelvin sense 方式走到 FPGA 负载点。
- 增加 0R 选择：
  - 靠近 FPGA 的 load sense：默认贴。
  - 靠近 regulator 的 local sense：DNP 备选。
- 只有 regulator datasheet 或参考设计要求时，才增加 sense 滤波。
- Sense 走线远离开关节点、功率电感、SW copper。

### 6.6 相关状态 pin

最小系统页建议保留：

| FPGA ball | Pin / function | 推荐 net | 用途 |
|---|---|---|---|
| `BP102` | `SDM_IO16 / CONF_DONE` | `A5E_CONF_DONE` | 配置完成监测 |
| `CA99` | `SDM_IO0 / INIT_DONE` | `A5E_INIT_DONE` | 进入 user mode / 初始化完成监测 |
| `BR99` | `SDM_IO12 / PWRMGT_ALERT option` | `A5E_PWRMGT_ALERT_DNP` 或 `A5E_CAT_TRIP_N` | 等 PMBus 模式和状态策略冻结后再定 |

## 7. Quartus 配置方向

预期方向：

```tcl
set_global_assignment -name VID_OPERATION_MODE "PMBUS MASTER"
set_global_assignment -name USE_PWRMGT_SCL SDM_IO14
set_global_assignment -name USE_PWRMGT_SDA SDM_IO11
set_global_assignment -name PWRMGT_BUS_SPEED_MODE "100 KHZ"
```

Regulator 相关参数取决于最终选型：

```tcl
set_global_assignment -name PWRMGT_SLAVE_DEVICE_TYPE <selected_regulator>
set_global_assignment -name PWRMGT_SLAVE_DEVICE0_ADDRESS <7bit_address>
set_global_assignment -name PWRMGT_VOLTAGE_OUTPUT_FORMAT <linear_or_direct>
set_global_assignment -name PWRMGT_LINEAR_FORMAT_N <regulator_specific_N>
```

来自 Altera SmartVID 文档的 regulator format 方向：

| Regulator | Agilex 5 验证状态 | Voltage format 说明 |
|---|---|---|
| `TPS53676` | Fully validated | Linear，`N = -10` |
| `LTC3882-1` | Fully validated | Linear，`N = -12` |
| `ISL68223` | Fully validated | Direct format 系列 |
| `LTC7883` | API validated only | 需要 FAE 确认 Quartus 设置 |

Bring-up 建议：

- PMBus 初版用 `100 kHz`。
- 首板打开 Diagnostic Boot。
- 导出并归档 Quartus 生成的 pin/config report。

## 8. 上电时序和 Power-Good 要求

板级时序必须保证：

- `A5E_VCC_VID` 初始输出为 `0.80 V`。
- SDM 尝试 VID 通信时，regulator PMBus 接口已经可用。
- 依赖 SDM PMBus 通信前，`VCCIO_SDM` 已有效。
- PMBus 线不会被未上电 regulator、level shifter 或外部控制器拉低。
- Regulator PGOOD 纳入板级 power-good tree。
- `nSTATUS`、`CONF_DONE`、`INIT_DONE` 在 bring-up 时可观测。

建议暴露的 power-good / debug 信号：

- `A5E_VCC_VID_PGOOD`
- `A5E_1V8_SDM_PGOOD`
- `A5E_NSTATUS`
- `A5E_CONF_DONE`
- `A5E_INIT_DONE`
- PMBus 测试点或调试 header

## 9. Layout 要求

Regulator 区域：

- 功率级靠近 controller，电流环路短。
- 高频输入/输出电容靠近功率级。
- SW 节点面积受控，按 regulator 厂商 layout guide。
- PMBus 和 sense 线远离 SW 节点。

FPGA 负载区域：

- 按 PDN 结果放置 bulk 和高频去耦。
- 所有 `VCC` / `VCCP` ball 接低阻抗电源平面。
- `VCCLSENSE/GNDSENSE` 做安静 Kelvin sense。
- Sense return 不要和大电流地路径混在一起。
- `A5E_VCC_VID` 可以加测试点，但不要在 sense loop 上拉长 stub。

## 10. Do / Do Not

应该做：

- 使用 PMBus-compliant SmartVID regulator。
- 保证 SDM 到 regulator 的 PMBus 路径可用。
- 使用 `A5E_VCC_VID` 这种明确命名。
- 原理图中明确 regulator PMBus address。
- 给 sense fallback、PMBus debug 预留 DNP/0R。
- 归档 FAE 确认和 Quartus 报告。

不要做：

- 用普通 fixed-output 0.8 V Buck 直接供 `VCC/VCCP`。
- 把 `PWRMGT_SDA/SCL` 随意并到繁忙系统 I2C，而不做多主分析。
- 未确认系统管理架构时，直接复制 KEIm carrier-access PMBus 拓扑。
- 不跑 EPE / Quartus Power Analyzer 就照抄 `27A/41A`。
- 把所有 0.8V rail 都无脑接到 `A5E_VCC_VID`。

## 11. 推荐具体实现

如果这是独立最小系统板：

```text
Regulator:
  TPS53676 or LTC3882-1 or ISL68223

Rail:
  +A5E_VCC_VID
  default/NVM output = 0.80 V

Loads:
  A5ED052A VCC
  A5ED052A VCCP
  其它低压 rail 仅在当前 Pin Connection Guidelines 允许时接入

Control:
  PMBus Master Mode from SDM
  CF109 / SDM_IO14 / PWRMGT_SCL
  CF99  / SDM_IO11 / PWRMGT_SDA

Sense:
  AV72 / VCCLSENSE -> sense+
  AU72 / GNDSENSE  -> sense-

Debug:
  VCC_VID test point
  PMBus test pads
  regulator PGOOD
  nSTATUS / CONF_DONE / INIT_DONE
```

如果板上已经有系统控制器或 PMIC supervisor：

- 先决定 Agilex SDM 是否仍然是 PMBus master。
- 如果外部控制器控制 PMBus，则需要分析 PMBus Slave/Target Mode，并连接 `PWRMGT_ALERT`。
- 必须确认外部控制器 firmware 在 Agilex 配置前已可用。

## 12. FAE / 工具闭环项

原理图 release 前必须关闭：

1. 确认 `A5ED052AB32AE2V` 确实是 SmartVID `-2V` 器件，且 `VCC/VCCP` 必须 PMBus 供电。
2. 确认选定 regulator 被项目使用的 Quartus 版本支持。
3. 确认 regulator voltage format、PMBus address、PAGE 设置和初始 NVM voltage。
4. 确认 `VCCL_*`、`VCCPLLDIG_*`、HSSI、PLL 等其它低压 rail 的 rail-sharing 规则。
5. 用 Intel/Altera EPE 或 Quartus Power Analyzer 做电流预算。
6. 做 PDN 分析，确定去耦和电源平面阻抗。
7. 确认上电时序满足 Agilex 5 POR 要求。
8. 生成 Quartus `.pin` / configuration report 并和原理图交叉核对。

## 13. 评审 Checklist

原理图检查：

- [ ] `VCC` 和 `VCCP` 已连接到 `A5E_VCC_VID`。
- [ ] `A5E_VCC_VID` regulator 支持 PMBus。
- [ ] Regulator 默认输出为 `0.80 V`。
- [ ] `PWRMGT_SCL` 使用 `CF109 / SDM_IO14`。
- [ ] `PWRMGT_SDA` 使用 `CF99 / SDM_IO11`。
- [ ] PMBus 电压域正确，必要时已做 level shift。
- [ ] `VCCLSENSE / GNDSENSE` 连接正确。
- [ ] PMBus address strap 已在原理图标注。
- [ ] Regulator PGOOD 接入 power-good tree。
- [ ] `nSTATUS`、`CONF_DONE`、`INIT_DONE` 有测试点或 supervisor 监控。
- [ ] FAE 确认已归档到评审资料。

Layout 检查：

- [ ] Sense 走线是 Kelvin、低噪声路径。
- [ ] PMBus 线远离 SW 节点。
- [ ] 去耦符合 PDN 分析结果。
- [ ] 功率级热路径已评审。
- [ ] 测试点不会破坏 sense loop。

Bring-up 检查：

- [ ] 编程前测量 `A5E_VCC_VID` 初始电压。
- [ ] 确认 PMBus idle high，没有 stuck-low。
- [ ] 确认 regulator 在设定地址 ACK。
- [ ] 首次配置启用 Diagnostic Boot。
- [ ] 记录 `nSTATUS`、`CONF_DONE`、`INIT_DONE`。
- [ ] SDM VID 调压后读取 PMBus 输出电压。

## 14. 最终建议

本项目建议冻结的原理图方向：

```text
A5ED052AB32AE2V
VCC/VCCP = A5E_VCC_VID
SmartVID PMBus Master Mode
PWRMGT_SCL = CF109 / SDM_IO14
PWRMGT_SDA = CF99 / SDM_IO11
VCCLSENSE = AV72
GNDSENSE = AU72
Regulator = TPS53676 / LTC3882-1 / ISL68223 class, FAE-confirmed
```

KEIm `LTC7883 + NCP302035` 原理图可作为拓扑和容量设计参考，但不建议默认照抄为产品首版方案，除非 FAE 明确确认该方案适用于 `A5ED052AB32AE2V` 和项目使用的 Quartus 版本。
