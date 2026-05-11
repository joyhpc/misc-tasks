# Altera 065B SOM Demo 电源树说明

日期：2026-05-11

参考原理图：

- `sources/reference_schematic/agilex-5e-mdevkit-som-sch-v2p1.pdf`
- Sheet 52/53: `POWER-LTC7883-CONTROLLER`
- Sheet 54: `POWER-VCCP_VID`
- Sheet 55: `POWER - +V1P0, +V0P8`
- Sheet 56: `POWER - +V1P8`
- Sheet 57: `POWER - +V1P2`
- Sheet 58: `POWER - +V5P0, +V2P5, +V3P3, +V1P8 - STBY`
- Sheet 59: `POWER - MP5087 LOAD SWITCH`
- Sheet 60: `POWER - +V0P6_DDR4_VTT`

## 1. 结论

Altera 065B SOM demo 不是所有 FPGA 电源都用 `LTC7883 + LTC7050`。

准确说：

- `LTC7883AY#PBF + LTC7050AV#PBF` 用在几路**大电流、低电压、高管理需求**的 rail 上：
  - `+V0P8_VCCP_VID`
  - `+V1P0`
  - `+V0P8`
- 其它 rail 由不同 regulator / load switch 生成：
  - `+V1P8`：`MP8870GL-0012`
  - `+V1P2`：`MP8796BGVT-0023`
  - standby rails：`MPM54304GMN-0044`、`MPM3804GG`
  - `+V2P5` / `+V3P3`：`MP5087GG-Z` load switch
  - DDR VTT：`MP20075DH`

所以你在 demo 里看到很多 PMBus 和 power monitor，不代表全都是同一套 `LTC7883 + LTC7050`。

## 2. Rail 对应关系

| Rail | Demo 标注能力 | 主要器件 | 类型 | 作用 |
|---|---:|---|---|---|
| `+V0P8_VCCP_VID` | `0.8V @ 36A` | `LTC7883AY#PBF + LTC7050AV#PBF` | SmartVID / 大电流 buck | FPGA `VCC/VCCP` 等核心 SmartVID rail |
| `+V1P0` | `1.0V @ 14A` | `LTC7883AY#PBF + LTC7050AV#PBF` | 大电流 buck | 固定 1.0V FPGA rail / transceiver 类 rail |
| `+V0P8` | `0.8V @ 17A` | `LTC7883AY#PBF + LTC7050AV#PBF` | 大电流 buck | 固定 0.8V FPGA low-voltage rail |
| `+V1P8` / `+V1P8_AUX` | `1.8V @ 8.2A` | `MP8870GL-0012` | PMBus buck | 1.8V system / FPGA IO / AUX 类 rail |
| `+V1P2` | `1.2V @ 12.5A` | `MP8796BGVT-0023` | PMBus buck | 1.2V FPGA rail / IO pre-driver / board rail |
| `+V5P0_STBY` | `5V @ 2.3A` | `MPM54304GMN-0044` | 多路 PMBus module | standby power tree |
| `+V3P3_STBY` | `3.3V @ 3.7A` | `MPM54304GMN-0044` | 多路 PMBus module | standby / control / load-switch source |
| `+V2P5_STBY` | `2.5V @ 0.3A` | `MPM54304GMN-0044` | 多路 PMBus module | standby / bias |
| `+V1P8_STBY` | `1.8V @ 0.1A` | `MPM3804GG` | small buck / module | standby 1.8V |
| `+V2P5` | `2.5V @ 0.3A` | `MP5087GG-Z` | load switch | 从 `+V2P5_STBY` 受控输出 |
| `+V3P3` / `+V3P3_AUX` | `3.3V @ 2.6A` | `MP5087GG-Z` | load switch | 从 `+V3P3_STBY` 受控输出 |
| `+V0P6_DDR4_VTT_[1:3]` | `0.6V @ 0.5A` each | `MP20075DH` | DDR VTT regulator | DDR termination |

## 3. `LTC7883 + LTC7050` 为什么这样用

`LTC7883` 是控制器，不是大电流输出芯片。它负责：

- PMBus 通信。
- SmartVID 电压调整。
- PWM 控制。
- 软启动、故障保护、遥测。
- NVM 默认配置。

`LTC7050` 是功率级，负责：

- high-side / low-side MOSFET 开关。
- driver。
- 电流检测。
- 温度 / fault 反馈。
- 真正把输入电源转换成大电流低压 rail。

组合关系是：

```text
PMBus / SDM
  -> LTC7883 controller
  -> PWM / sense / fault
  -> LTC7050 power stage
  -> inductor
  -> output capacitor
  -> FPGA rail
```

这种架构的核心原因：

1. `VCC/VCCP` 是 SmartVID rail，需要 PMBus 可调。
2. FPGA core rail 是低电压大电流，单颗普通 regulator 不合适。
3. demo board 需要遥测、fault、margin、sequencing，方便调试和验证。
4. `LTC7883` 有多路输出能力，demo 顺手把 `+V1P0`、`+V0P8` 这类大电流 rail 也纳入同一颗 controller 体系。
5. `LTC7050` 这种 smart power stage 让功率部分更紧凑，电流/温度反馈也更完整。

## 4. 为什么其它 rail 不用 LTC7883 + LTC7050

因为不是所有 rail 都需要 SmartVID，也不是所有 rail 都是几十安培。

例如：

- `+V1P8` 是 `8.2A` 级别，demo 用 `MP8870GL-0012`，它本身就是 PMBus buck。
- `+V1P2` 是 `12.5A` 级别，demo 用 `MP8796BGVT-0023`。
- `+V3P3`、`+V2P5` 很多时候只是从 standby rail 经 load switch 受控打开，没必要再用大控制器。
- DDR VTT 是专用半压终端电源，用 `MP20075DH` 这种 VTT regulator 更合理。

也就是说，demo 的设计原则不是“所有电源统一用 LTC7883”，而是：

```text
SmartVID / 大电流 / 强管理 rail -> LTC7883 + LTC7050
普通 PMBus buck rail            -> 独立 PMBus regulator
standby / bias rail             -> 多路 module 或小 buck
受控 3.3V/2.5V rail             -> load switch
DDR termination                 -> 专用 VTT regulator
```

## 5. 对 A5ED052A 项目的启发

对 `A5ED052AB32AE2V`，不能直接照抄 demo 的电流能力。

原因：

- demo 是 `A5ED065B B32A`，资源规模大于 `A5ED052A`。
- demo 需要覆盖开发板最大扩展能力，通常比产品板保守。
- 你的板上 HSSI、HPS、DDR、MIPI、IO bank 使用情况会改变电流需求。

可复用的部分：

- `VCC/VCCP` 按 SmartVID rail 设计。
- `PWRMGT_SCL/SDA` 接 PMBus regulator。
- `VCCLSENSE/GNDSENSE` 做 remote sense。
- 大电流 core rail 用 controller + smart power stage 的思路是合理的。

不能直接复用的部分：

- `+V0P8_VCCP_VID 36A` 这个电流值。
- `+V1P0 14A`、`+V0P8 17A` 的容量。
- 是否需要 demo 里所有 PMBus regulator。
- 是否需要全部 standby/load-switch 结构。

## 6. 建议给 FAE 的问题

```text
我们看到 Altera Agilex 5E 065B SOM demo 里：

1. +V0P8_VCCP_VID 使用 LTC7883AY#PBF + LTC7050AV#PBF，标注 0.8V @ 36A；
2. +V1P0 使用 LTC7883AY#PBF + LTC7050AV#PBF，标注 1.0V @ 14A；
3. +V0P8 使用 LTC7883AY#PBF + LTC7050AV#PBF，标注 0.8V @ 17A；
4. +V1P8 使用 MP8870GL-0012；
5. +V1P2 使用 MP8796BGVT-0023；
6. standby rails 使用 MPM54304GMN-0044 / MPM3804GG，3.3V/2.5V 经过 MP5087 load switch。

我们的目标器件是 A5ED052AB32AE2V，B32A 封装。

请帮忙确认：
- 对 A5ED052A，哪些 rail 必须参考 demo 保持 PMBus 可管理？
- VCC/VCCP 是否推荐继续使用 LTC7883 + LTC7050？
- +V1P0 / +V0P8 是否需要继续用 LTC7883 + LTC7050，还是可以按实际功耗简化？
- A5ED052A 的 VCC/VCCP、+V1P0、+V0P8、+V1P8、+V1P2 推荐电流能力如何估算？
- 是否有针对 A5ED052A 的 power tree / EPE / Quartus Power Analyzer 推荐输入条件？
```
