# A5ED052A B32A 可参考原理图 VCC / SmartVID 方案汇总

日期：2026-05-11

目标器件：`A5ED052AB32AE2V`

本文只汇总目前本地可参考原理图里的 `VCC/VCCP/SmartVID` 相关方案，不替代最终电源完整设计。

## 1. 参考资料

| 优先级 | 文件 | 用途 |
|---:|---|---|
| 1 | `sources/reference_schematic/agilex-5e-mdevkit-som-sch-v2p1.pdf` | Altera 官方 Agilex 5 E-Series 065B B32A SOM 原理图，最高优先级实物参考 |
| 2 | `sources/vendor_reference/keim-a5esom_sch_rev1.10.pdf` | KEIm A5E SOM Rev1.10 原理图，供应商实际 SOM 参考 |
| 3 | `sources/vendor_reference/keim-a5esom_bom_rev1.10-.xlsx` | KEIm Rev1.10 BOM，用于确认器件料号 |
| 4 | `sources/vendor_reference/sulfur_type-a_sch_rev1.00.pdf` | Sulfur Type-A carrier 原理图，只能参考 SOM 供电入口和 PMBus 暴露方式 |
| 5 | `sources/official_pinouts/a5ed052a/a5ed052A.xlsx` | A5ED052A B32A 官方 pinout，用于确认本项目 ball/pin |

## 2. 总体结论

目前可参考原理图都支持同一个核心判断：

- `VCC/VCCP` 不是普通固定 0.8V buck 方案。
- 应设计成 SmartVID / PMBus 可调核心电源 rail。
- `VCCLSENSE` 和 `GNDSENSE` 要接入 regulator sense 网络，不能悬空。
- PMBus 要能被 Agilex SDM 或外部板级控制器访问。

对本项目建议的 rail 命名：

```text
A5E_VCC_VID
```

并把 A5ED052A B32A 的所有 `VCC` 和 `VCCP` balls 接到该 rail。

## 3. KEIm A5E SOM Rev1.10 方案

原理图位置：

- `keim-a5esom_sch_rev1.10.pdf`
- Sheet 13: `Power VID`
- Sheet 14: `Power 0.8V, 1.0V`
- Sheet 15: `Power 3.3V, 1.8V, 1.2V, 1.1V`

器件与封装：

- Hardware manual 标注 device：`A5ED065BB32AE5SR0`
- BOM 标注 FPGA package：`A5ED065BB32A` / `BGA1591`
- 因此 KEIm Rev1.10 是 `A5ED065B`、`B32A`、1591-ball BGA，不是 `A5ED052A`，但封装代码同为 `B32A`。

核心方案：

| 项目 | KEIm Rev1.10 做法 |
|---|---|
| SmartVID rail 名称 | `VCC_VID` |
| VID 控制器 | `LTC7883AY#PBF` |
| VCC_VID 功率级 | `NCP302035MNTWG` |
| VCC_VID 电流标注 | `27A/41A` |
| VCC/VCCP | 接到 `VCC_VID` |
| 远端采样 | `VCCLSENSE_AV72`、`GNDSENSE_AU72` 通过 0R 接入 `VID_VSNSA_P/N` |
| PMBus | 同时有 `SDM_PWRMGT_*_3V3` 和 `SOM_PMBUS_*_3V3` 路径，部分 0R 为可选/NoMount |
| 固定辅助低压 | 同一颗 `LTC7883` 的另一组通道还生成 `1.0V` 和 `0.8V` |

KEIm 的关键特征：

- 这是一个 SOM 设计，不是最小独立板设计。
- 它把 PMBus 暴露到 SOM 连接器，便于 carrier / 外部控制器管理。
- 它不是简单的“SDM 直接连 regulator PMBus”的最小方案。
- `LTC7883` 在这个设计中既做 `VCC_VID`，也参与固定 `1.0V/0.8V` rail。

因此，KEIm 方案对 `B32A` 封装下的 VCC/SmartVID 原理图拓扑参考价值很高；只是因为它的实际器件是 `A5ED065B` 而不是本项目的 `A5ED052A`，且它是 SOM 架构，所以不能直接照抄电流容量、PMBus 主控分工和所有辅助 rail 共轨方式。

## 4. Altera 官方 065B SOM 方案

原理图位置：

- `agilex-5e-mdevkit-som-sch-v2p1.pdf`
- Sheet 52/53: `POWER-LTC7883-CONTROLLER`
- Sheet 54: `POWER-VCCP_VID`
- Sheet 55: `POWER - +V1P0, +V0P8`

核心方案：

| 项目 | Altera 官方 SOM 做法 |
|---|---|
| SmartVID rail 名称 | `+V0P8_VCCP_VID` |
| VID 控制器 | `LTC7883` |
| VCCP_VID 功率级 | `LTC7050AV#PBF` |
| VCC/VCCP | 接到 `+V0P8_VCCP_VID` |
| 远端采样 | `VCCLSENSE/GNDSENSE` 接到 `VCCL_SENSE_R_P/N` sense 网络 |
| SDM PMBus SCL | `CF109 / SDM_IO14 / PWRMGT_SCL` -> `PMBUS_SCL_C2M_1V8` |
| SDM PMBus SDA | `CF99 / SDM_IO11 / PWRMGT_SDA` -> `PMBUS_SDA_C2M_1V8` |
| PMBus 电平 | 1.8V 侧经电平转换到 3.3V PMBus |
| PMBus 总线 | 同时连接多个 PMBus regulator / power IC |

官方方案的价值：

- 它是 Altera 官方开发套件 SOM 原理图，参考优先级最高。
- 它证明 `LTC7883` 在 Agilex 5 官方参考板上确实被采用。
- 但这不等于 `LTC7883` 是 Altera SmartVID 页面里的 fully validated 器件；官方页面仍把它归为 `API validated only`。

## 5. Sulfur Type-A Carrier 方案

原理图位置：

- `sulfur_type-a_sch_rev1.00.pdf`

它不是 FPGA VCC/SmartVID regulator 的核心参考。它主要提供：

- SOM 输入电源。
- carrier 到 SOM 的 PMBus 访问路径：
  - `SOM_PMBUS_SCL_3V3`
  - `SOM_PMBUS_SDA_3V3`
- 外设和 carrier 侧电源。

使用方式：

- 可以参考它如何把 PMBus 暴露到 carrier。
- 不应从它推导 A5ED052A 的 `VCC/VCCP` regulator 拓扑。

## 6. 方案对比

| 参考设计 | VCC/SmartVID rail | 控制器 | 功率级 | PMBus 主控倾向 | 对本项目价值 |
|---|---|---|---|---|---|
| Altera 065B SOM | `+V0P8_VCCP_VID` | `LTC7883` | `LTC7050AV#PBF` | FPGA SDM / C2M PMBus 体系 | 最高优先级参考 |
| KEIm A5E SOM Rev1.10 | `VCC_VID` | `LTC7883AY#PBF` | `NCP302035MNTWG` | SOM / carrier 可访问，SDM 路径可选 | 有实际 SOM 设计价值，但需确认 PMBus 架构 |
| Sulfur Type-A carrier | 不生成 FPGA `VCC_VID` | 不适用 | 不适用 | 暴露 `SOM_PMBUS_*` | 只参考 carrier 访问和输入电源 |

## 7. 对 A5ED052AB32AE2V 的建议

推荐把本项目先按以下方式画：

```text
PMBus-capable SmartVID regulator
  -> +A5E_VCC_VID
  -> A5ED052A VCC balls
  -> A5ED052A VCCP balls

CF109 / SDM_IO14 / PWRMGT_SCL -> regulator PMBus SCL
CF99  / SDM_IO11 / PWRMGT_SDA -> regulator PMBus SDA

AV72 / VCCLSENSE -> regulator remote sense+
AU72 / GNDSENSE  -> regulator remote sense-
```

器件选择有两条路线：

1. 低供应/支持风险路线：优先让 FAE 推荐 `TPS53676`、`LTC3882-1` 或 `ISL68223` 这类 Altera fully validated SmartVID regulator。
2. 参考设计复制路线：采用 `LTC7883`，但需要 FAE 明确确认本项目 Quartus 版本、PMBus 配置、PAGE/address、初始电压、NVM 配置和 power-up 时序。

当前我更建议：

- 原理图结构参考 Altera 官方 065B SOM。
- KEIm Rev1.10 作为第二交叉验证，尤其验证 `VCC/VCCP -> VCC_VID`、remote sense 和 `LTC7883` 实际使用方式。
- 最终 regulator 料号让 Altera/代理商 FAE 确认后冻结。

## 8. 需要继续确认的点

- `A5ED052AB32AE2V` 在当前采购渠道下是否明确按 SmartVID `-V/-E` 规则处理。
- 目标 Quartus 版本对所选 regulator 的支持状态。
- PMBus master 是 FPGA SDM 还是外部 MCU / carrier 控制器。
- `VCC/VCCP` 以外的其它 0.8V 类 rail 是否允许与 `A5E_VCC_VID` 共轨。
- `A5E_VCC_VID` 电流能力应由 Quartus Power Analyzer / EPE 重新计算，不能直接照抄 KEIm 的 `27A/41A` 或官方 SOM 的功率级容量。
