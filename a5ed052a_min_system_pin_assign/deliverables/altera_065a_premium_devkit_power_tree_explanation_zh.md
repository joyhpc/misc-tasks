# Altera 065A Premium Devkit 电源树分析

日期：2026-05-11

参考原理图：

- 在线文档：`Agilex 5 FPGA E-Series 065A Premium Development Kit DK-A5E065AB32AEA Board Schematic`
- 本地文件：`sources/reference_schematic/065a_premium/agilex5e-065a-premium-devkit-b0-a3-altera.pdf`
- PDF 标题：`AGILEX5E_065A_PREMIUM_DEVKIT_B0`
- 原理图版本：`A3`
- 日期：`Monday, February 09, 2026`
- 板上器件：`A5ED065AB32AE1V`

## 1. 先纠正参考对象

前面分析的 `agilex-5e-mdevkit-som-sch-v2p1.pdf` 是 **065B Modular Dev Kit SOM**。

你现在看的 `agilex5e-065a-premium-devkit-b0-a3-altera.pdf` 是 **065A Premium Dev Kit**。

这两份原理图不是同一块板：

| 项目 | 065A Premium Dev Kit | 065B Modular Dev Kit SOM |
|---|---|---|
| 板级形态 | 完整 premium demo board | SOM module |
| 板上 FPGA | `A5ED065AB32AE1V` | `A5ED065B B32A` |
| 原理图页数 | 67 页 | 62 页 |
| 电源复杂度 | 很高，面向完整开发板和遥测验证 | SOM 内部电源，结构较集中 |
| LTC7883 使用范围 | 覆盖 VCCcore、HSSI、VCCERT、VCCPT、多个 VCCIO rail | 主要覆盖 VCCP_VID、+V1P0、+V0P8 |

对 `A5ED052AB32AE2V` 来说，065A Premium Dev Kit 的参考价值很高，因为它同为 `065A/052A` 这一侧的 premium 参考板，并且是 Altera 官方生产版原理图。

## 2. 结论

065A Premium Devkit 里，很多 FPGA rail 确实都采用了：

```text
LTC7883AY#PBF + LTC7050AV#PBF
```

但仍然不是“所有电源”都用这套方案。

准确说：

- FPGA 大电流 / 可遥测 / 需要严格时序管理的 rail，大量使用 `LTC7883 + LTC7050`。
- 小电流 rail、standby rail、DDR VTT/VREF、外设电源仍然用其它 regulator / load switch。

## 3. Power Sequence Group

原理图 Power Tree 页把电源分成几个 group：

| Group | 主要 rail | 说明 |
|---|---|---|
| Group 0 | `12V_SYS`, `12V_HPS` | 输入/前级电源 |
| Group 1 | `FPGA_VCC`, `VCC_HSSI`, `VCCERT_UX`, `VCCPLLDIG_HPS`, `VCCPLLDIG_SDM` | 核心和高速相关 rail |
| Group 2 | `VCCPT`, `VCCPLL12_HPS`, `VCCPLL_SDM`, `VCCEHT_UX`, `88E2110_ENET1_AVDD` | PLL / pre-driver / EHT / 模拟相关 rail |
| Group 3 | `VCCIO_3B_B`, `VCCIO_2B3A3B_T`, `VCCIO_HVIO`, `2V5_SYS`, `VCCIO_2A`, `1V8_HVIO_6D`, `1V8_HPS`, `1V8_LPDDR4`, `0V6_DDR4_VTT`, `0V6_DDR4_VREF` | IO / DDR / 辅助低压 rail |
| Other | QSFP/SFP/FMC/PHY 外设电源 | 外设专用电源 |

原理图 Power Tree 页还有一句关键建议：

```text
Dev Kit power tree design are for reference.
Recommend customer to scale power solution based on design requirements.
```

也就是说，Altera 明确提示：开发板电源树是参考，客户产品要按实际需求缩放。

## 4. LTC7883 Controller 1

Controller 1 对应 Sheet 57/58：

- Sheet 57: `ADI7883 CONTROLLER1 1/2`
- Sheet 58: `ADI7883 CONTROLLER1 2/2`

器件：

```text
LTC7883AY#PBF
```

它控制的 rail：

| Channel | Rail | Power stage 页 |
|---|---|---|
| `A0` | `FPGA_VCC` phase 1 | Sheet 59 `VCCcore PHASE1` |
| `A1` | `FPGA_VCC` phase 2 | Sheet 60 `VCCcore PHASE2` |
| `B0` | `VCC_HSSI` | Sheet 61 `VCC_HSSI, VCCERT_UX` |
| `B1` | `VCCERT_UX` | Sheet 61 `VCC_HSSI, VCCERT_UX` |

特征：

- `FPGA_VCC` 用两相：`PWMA0_FPGA_VCC`、`PWMA1_FPGA_VCC`。
- `VCC_HSSI` 用 `PWMB0_VCC_HSSI`。
- `VCCERT_UX` 用 `PWMB1_VCCERT_UX`。
- 每个 rail 都有对应的 current sense、voltage sense、temperature/fault/PG。
- `FPGA_VCC` controller 页连接 `FPGA_3V3_SVID_SCL/SDA`，也就是和 FPGA SmartVID/PMBus 管理相关。

## 5. LTC7883 Controller 2

Controller 2 对应 Sheet 62/63：

- Sheet 62: `ADI7883 CONTROLLER2 1/2`
- Sheet 63: `ADI7883 CONTROLLER2 2/2`

器件：

```text
LTC7883AY#PBF
```

它控制的 rail：

| Channel | Rail | Power stage 页 |
|---|---|---|
| `A0` | `VCCPT` | Sheet 64 `VCCPT, VCCIO_3B_B` |
| `A1` | `VCCIO_3B_B` | Sheet 64 `VCCPT, VCCIO_3B_B` |
| `B0` | `VCCIO_2B3A3B_T` | Sheet 65 `HSIO_2B3A3B_T, VCCIO_HVIO` |
| `B1` | `VCCIO_HVIO` | Sheet 65 `HSIO_2B3A3B_T, VCCIO_HVIO` |

特征：

- 这些 rail 不是 VCCcore，但仍然采用 `LTC7883 + LTC7050`。
- 原因是它们在 premium devkit 上电流不小、需要监控、需要 power-good/fault 进 MAX10/系统管理。
- 这更像开发板级“可观测、可调试、可验证”的电源架构，不是最低成本产品架构。

## 6. LTC7050 Power Stage 分布

使用的 power stage：

```text
LTC7050AV#PBF
```

分布：

| Sheet | Rail | 说明 |
|---|---|---|
| 59 | `FPGA_VCC` phase 1 | VCCcore 第一相 |
| 60 | `FPGA_VCC` phase 2 | VCCcore 第二相 |
| 61 | `VCC_HSSI`, `VCCERT_UX` | 一颗 LTC7050 内两个 channel |
| 64 | `VCCPT`, `VCCIO_3B_B` | 一颗 LTC7050 内两个 channel |
| 65 | `VCCIO_2B3A3B_T`, `VCCIO_HVIO` | 一颗 LTC7050 内两个 channel |

所以 065A Premium Devkit 的理解应该是：

```text
两个 LTC7883 controller
  -> 多个 PWM channel
  -> 多颗 LTC7050 smart power stage
  -> 覆盖 FPGA core / HSSI / VCCERT / VCCPT / VCCIO rails
```

## 7. 非 LTC7883 + LTC7050 的 rail

Sheet 66/67 仍然有其它电源方案：

| Rail | 器件 | 说明 |
|---|---|---|
| `VCCIO_2A` | `LTC3312SAAV#PBF` | 1.1V +/-3%，独立 buck |
| `2V5_SYS` | `LTC3312SAAV#PBF` | 2.5V +/-3%，同一双路 buck 的第二路 |
| `1V8_HVIO_6D` / `1V8_LPDDR4` | `MAX25302B` | 从 `VCCIO_HVIO` 生成 1.8V，LDO/低 dropout 类结构 |
| `0V6_DDR4_VTT_COMP1` / `0V6_DDR4_VTT_COMP` | `TPS51200DRCR` | DDR4 VTT |
| `0V6_DDR4_VREF_COMP1` / `0V6_DDR4_VREF_COMP` | `TPS51200DRCR` | DDR4 VREF |

因此即使在 065A Premium Devkit，`LTC7883 + LTC7050` 也没有覆盖所有 rail。

## 8. 为什么 Premium Devkit 这样设计

这块板是 premium development kit，不是成本优化产品板。它的目标是：

1. 支持多种高速接口、DDR4、LPDDR4、FMC+、QSFP/SFP、MIPI、HPS 扩展。
2. 支持 board test system、遥测、margin、fault debug。
3. 覆盖最坏使用场景和大量可选外设。
4. 通过 MAX10 / PMBus 管理电源状态。
5. 给客户一个“强参考”而不是最低 BOM 成本方案。

所以它会把很多 FPGA rail 做成：

```text
PMBus controller + smart power stage + current/voltage/temperature/fault telemetry
```

这对开发板非常合理，因为开发板要能测、能调、能诊断。

对产品板来说，是否照抄要看：

- 实际打开哪些 FPGA bank。
- HSSI/MIPI/DDR/LPDDR/PCIe/QSFP 是否使用。
- 目标功耗。
- 是否需要现场 telemetry。
- 成本、面积、供应风险。
- FAE 对目标器件的推荐 power tree。

## 9. 对 A5ED052AB32AE2V 的判断

对你的 `A5ED052AB32AE2V`，065A Premium Devkit 比 065B SOM 在“器件系列侧”更有参考价值，因为它是 `A5ED065A...`，和 `A5ED052A...` 同属 065A/052A 这一侧的官方 premium 板。

但仍然不能直接照抄：

- 065A 是 656K LE 级别，052A 规模更小。
- Premium devkit 接口非常多，产品板通常不会全用。
- 电流能力和相数必须用 EPE / Quartus Power Analyzer 重新估。
- 哪些 VCCIO rail 需要这么强的 PMBus + smart power stage，要结合实际 bank 电压和负载确认。

建议优先复用的原则：

```text
FPGA_VCC / SmartVID core rail：
  强烈参考 065A Premium 的 LTC7883 + LTC7050 架构。

HSSI / VCCERT / VCCPT / high-current VCCIO rails：
  可以参考，但是否照抄需要 FAE 和功耗评估。

VCCIO_2A / 2V5_SYS / LPDDR4 1V8 / DDR VTT：
  按实际外设和 bank 用法单独设计，不必默认套 LTC7883 + LTC7050。
```

## 10. 给 FAE 的问题

```text
我们参考了 Altera Agilex 5E 065A Premium Dev Kit A3 原理图。
该板 FPGA 为 A5ED065AB32AE1V，使用两颗 LTC7883AY#PBF 配合多颗 LTC7050AV#PBF：

Controller1:
- FPGA_VCC 两相
- VCC_HSSI
- VCCERT_UX

Controller2:
- VCCPT
- VCCIO_3B_B
- VCCIO_2B3A3B_T
- VCCIO_HVIO

我们的目标器件为 A5ED052AB32AE2V。

请确认：
1. A5ED052A 的 FPGA_VCC/VCCP SmartVID rail 是否建议直接参考 065A Premium 的 LTC7883 + LTC7050 架构？
2. 对 A5ED052A，VCC_HSSI、VCCERT_UX、VCCPT、VCCIO_3B_B、VCCIO_2B3A3B_T、VCCIO_HVIO 是否也需要像 065A Premium 一样用 LTC7883 + LTC7050，还是可以按实际功耗简化？
3. 是否有 A5ED052A 推荐 power tree / EPE 输入模板 / rail 电流估算建议？
4. LTC7883 的 PMBus address、PAGE、VOUT_MODE、NVM 初始电压、SmartVID/Quartus 配置是否可按 065A Premium 参考？
5. 如果产品板不需要完整遥测和 margin 功能，哪些 rail 可以改用普通 buck 或 fully validated SmartVID regulator？
```
