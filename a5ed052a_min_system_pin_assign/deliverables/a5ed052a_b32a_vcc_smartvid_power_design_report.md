# A5ED052A B32A VCC / SmartVID Power Design Report

Date: 2026-05-11

Target device: `A5ED052AB32AE2V`

Package: `B32A`

Design status: schematic-design recommendation, not release-frozen until FAE / Quartus / PDN checks close.

## 1. Executive Conclusion

For `A5ED052AB32AE2V`, the VCC core supply must be designed as a SmartVID-controlled supply, not as a plain fixed 0.8 V regulator.

Recommended board-level architecture:

- Use one SmartVID rail named `A5E_VCC_VID`.
- Connect FPGA `VCC` and `VCCP` pins to `A5E_VCC_VID`.
- Regulator initial/NVM output: `0.80 V`.
- Use PMBus Master Mode unless a system power controller is intentionally responsible for VID.
- Connect Agilex SDM PMBus pins:
  - `CF109 / SDM_IO14 / PWRMGT_SCL` -> regulator PMBus SCL.
  - `CF99 / SDM_IO11 / PWRMGT_SDA` -> regulator PMBus SDA.
- Connect remote sense:
  - `AV72 / VCCLSENSE` -> regulator sense positive at FPGA load point.
  - `AU72 / GNDSENSE` -> regulator sense negative / ground sense at FPGA load point.
- Keep `BP102 / SDM_IO16` as `CONF_DONE`.
- Keep `CA99 / SDM_IO0` as `INIT_DONE`.
- Keep `BR99 / SDM_IO12` as optional `PWRMGT_ALERT` / status / DNP until PMBus mode is frozen.

Preferred regulator path:

1. Product-first recommendation: use an Intel/Altera fully validated Agilex 5 SmartVID regulator, such as `TPS53676`, `LTC3882-1`, or `ISL68223`.
2. Reference-copy path: use the KEIm reference topology `LTC7883AY#PBF + NCP302035MNTWG` only if FAE confirms it for this exact project, because Altera lists `LTC7883` as API-validated only for Agilex 5.

## 2. Source Hierarchy

Use sources in this order:

1. Intel/Altera official power-management documentation.
2. Intel/Altera official A5ED052A B32A pinout.
3. Intel/Altera official 065B B32A SOM reference schematic.
4. KEIm A5E SOM vendor reference schematic and BOM.
5. Local derived workbooks and notes.

Local source files reviewed:

- `sources/official_pinouts/a5ed052a/a5ed052A.xlsx`
- `sources/reference_schematic/agilex-5e-mdevkit-som-sch-v2p1.pdf`
- `sources/vendor_reference/keim-a5esom_sch_rev1.10.pdf`
- `sources/vendor_reference/keim-a5esom_bom_rev1.10-.xlsx`
- `sources/vendor_reference/keim-a5esom_hardware_manual_EN_v1.1.pdf`

Official online sources:

- Altera Power Management User Guide: Agilex 5 FPGAs and SoCs, SmartVID / PMBus sections.
- Altera FPGA SmartVID regulator page.
- Altera Pin Connection Guidelines: Agilex 5 FPGAs and SoCs.
- Altera A5ED052A pin information document 830449.

## 3. Official Requirement Summary

The official Agilex 5 power-management guidance states that Agilex 5 `-V` / `-E` SmartVID devices require a PMBus-compliant voltage regulator for `VCC` and `VCCP`. The SDM Power Manager reads the device-specific VID fuse and sets the regulator through PMBus before FPGA configuration.

Important interpretation for this project:

- `A5ED052AB32AE2V` includes a `-2V` speed/power suffix.
- Treat it as a SmartVID part unless FAE explicitly proves otherwise.
- Do not design `VCC/VCCP` as a fixed-output 0.8 V regulator with no PMBus path.
- PMBus and VID behavior must be configured both in hardware and Quartus.

The Altera SmartVID page lists Agilex 5 recommended PMBus-compliant regulators:

- Fully validated for Agilex 5:
  - `TPS53676`
  - `LTC3882-1`
  - `ISL68223`
- API validated only:
  - `LTC7883`

This is why `TPS53676 / LTC3882-1 / ISL68223` are lower-risk choices for a new product, while `LTC7883` is useful as a reference-design datapoint.

## 4. A5ED052A B32A Relevant Pins

From the official A5ED052A B32A pinout:

| Rail / Pin | Ball count | B32A balls |
|---|---:|---|
| `VCC` | 41 | `BA61, AY75, AY68, AY64, AY57, AY53, AW79, AW72, AW68, AW61, AW57, AV86, AV83, AV75, AV64, AV61, AV53, AU79, AU75, AU68, AU64, AU57, AU53, AT79, AT72, AT68, AT61, AT57, AR83, AR75, AR72, AR64, AR61, AR53, AP86, AP79, AP75, AP68, AP64, AN79, AN72` |
| `VCCP` | 14 | `BB72, BB68, BB61, BB57, BB50, BA64, BA53, AN68, AN57, AM75, AM72, AM64, AM61, AM53` |
| `VCCLSENSE` | 1 | `AV72` |
| `GNDSENSE` | 1 | `AU72` |
| `PWRMGT_SCL` | 1 | `CF109 / SDM_IO14` |
| `PWRMGT_SDA` | 1 | `CF99 / SDM_IO11` |
| optional `PWRMGT_ALERT` | 1 | `BR99 / SDM_IO12` or other supported SDM option depending Quartus selection |

Do not automatically tie every 0.8 V-looking rail to `A5E_VCC_VID`. For non-`VCC/VCCP` low-voltage rails, follow the current Pin Connection Guidelines and final power-tree decision.

## 5. Reference Design Findings

### 5.1 Intel/Altera 065B B32A SOM Reference

The official 065B B32A SOM reference uses the same SDM/JTAG/config ballout for the relevant B32A pins. It confirms:

- `CF109 = PMBus SCL` option.
- `CF99 = PMBus SDA` option.
- `BP102 = CONF_DONE` option.
- `CA99 = INIT_DONE` option.
- SmartVID-style core rail is present in the power design.

Use this as the strongest real-board reference because it is an official Altera development-kit schematic.

### 5.2 KEIm A5E SOM Reference

The vendor package contains `keim-a5esom_sch_rev1.10.pdf` and BOM files. Relevant findings:

- The power page is explicitly named `Power VID`.
- The main VID controller is `LTC7883AY#PBF`.
- The power stage is `NCP302035MNTWG`.
- The generated rail is named `VCC_VID`.
- The schematic annotates `VCC_VID` current as `27A/41A`.
- The schematic voltage note indicates `-1, -2, -3` power grades use `VID`; lower speed grades use fixed voltages.
- `VCC` and `VCCP` are connected to `VCC_VID`.
- `VCCLSENSE_AV72` and `GNDSENSE_AU72` are routed to VID sense nets through 0-ohm links.
- PMBus is exposed both through SDM PMBus nets and SOM/carrier PMBus nets.

Important caveat:

The KEIm design is a module design. Its PMBus architecture includes carrier/system management access, so it is not a simple one-to-one template for a standalone board. Copy the topology only after deciding who owns PMBus at boot: Agilex SDM, external system controller, or both with a controlled multi-master policy.

## 6. Recommended Schematic Design

### 6.1 Core Rail Naming

Use:

```text
A5E_VCC_VID
```

Connect to:

```text
FPGA VCC pins
FPGA VCCP pins
```

Do not name this simply `+0V8` in the schematic. `A5E_VCC_VID` makes it clear that the rail is VID-adjustable and PMBus-controlled.

### 6.2 Regulator Architecture

Recommended block:

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

Regulator selection:

- Prefer `TPS53676`, `LTC3882-1`, or `ISL68223` unless FAE recommends otherwise.
- Size current from Quartus Power Analyzer / EPE.
- Do not copy KEIm's `27A/41A` current blindly. That board uses `A5ED065B`, and your `A5ED052A` resource usage and thermal target may differ.

### 6.3 PMBus Electrical Connection

If regulator PMBus supports 1.8 V:

```text
CF109 / PWRMGT_SCL ---- regulator SCL
CF99  / PWRMGT_SDA ---- regulator SDA
pull-up both lines to VCCIO_SDM / 1.8 V
```

If regulator PMBus is 3.3 V only:

```text
CF109 / CF99 at 1.8 V
  -> bidirectional level shifter
  -> regulator PMBus at 3.3 V
```

Requirements:

- Use open-drain compatible PMBus/I2C-style level shifting.
- Pull-ups on Agilex side: `5.1 kΩ` to `10 kΩ` to `VCCIO_SDM`.
- Pull-ups on regulator side: per regulator datasheet, commonly `3.3 V`.
- Avoid uncontrolled back-powering before `VCCIO_SDM` is valid.
- If using a level shifter with OE, define OE default state explicitly.

### 6.4 PMBus Mode

Recommended mode:

```text
PMBus Master Mode
```

Reason:

- Simpler minimum system.
- Agilex SDM can directly set the core VID regulator.
- No external MCU/PMIC firmware is required during the critical boot window.

Do not choose PMBus Slave/Target mode unless:

- An external controller is guaranteed to be alive before Agilex configuration.
- That controller implements the required VID/PMBus flow.
- `PWRMGT_ALERT` is connected and Quartus is configured accordingly.

### 6.5 Sense Connection

Connect:

```text
AV72 / VCCLSENSE -> regulator remote sense positive
AU72 / GNDSENSE  -> regulator remote sense negative / ground sense
```

Recommended implementation:

- Route as Kelvin sense pair to FPGA load point.
- Add 0-ohm options:
  - load sense near FPGA: default populate.
  - local sense near regulator: DNP fallback.
- Add small sense filtering only if recommended by regulator datasheet / reference design.
- Keep sense traces away from noisy switching nodes.

### 6.6 Related Status Pins

Keep these pins in the minimum-system page:

| FPGA ball | Pin / function | Recommended net | Purpose |
|---|---|---|---|
| `BP102` | `SDM_IO16 / CONF_DONE` | `A5E_CONF_DONE` | Configuration complete monitor |
| `CA99` | `SDM_IO0 / INIT_DONE` | `A5E_INIT_DONE` | User-mode / init-done monitor |
| `BR99` | `SDM_IO12 / PWRMGT_ALERT option` | `A5E_PWRMGT_ALERT_DNP` or `A5E_CAT_TRIP_N` | Reserve until PMBus mode/status policy is frozen |

## 7. Quartus Configuration

Expected direction:

```tcl
set_global_assignment -name VID_OPERATION_MODE "PMBUS MASTER"
set_global_assignment -name USE_PWRMGT_SCL SDM_IO14
set_global_assignment -name USE_PWRMGT_SDA SDM_IO11
set_global_assignment -name PWRMGT_BUS_SPEED_MODE "100 KHZ"
```

Regulator-specific assignments depend on selected regulator:

```tcl
set_global_assignment -name PWRMGT_SLAVE_DEVICE_TYPE <selected_regulator>
set_global_assignment -name PWRMGT_SLAVE_DEVICE0_ADDRESS <7bit_address>
set_global_assignment -name PWRMGT_VOLTAGE_OUTPUT_FORMAT <linear_or_direct>
set_global_assignment -name PWRMGT_LINEAR_FORMAT_N <regulator_specific_N>
```

Useful regulator-format starting points from Altera SmartVID documentation:

| Regulator | Agilex 5 validation status | Voltage format note |
|---|---|---|
| `TPS53676` | Fully validated | Linear, `N = -10` |
| `LTC3882-1` | Fully validated | Linear, `N = -12` |
| `ISL68223` | Fully validated | Direct format family |
| `LTC7883` | API validated only | Use only with FAE-confirmed Quartus settings |

Bring-up recommendation:

- Start PMBus at `100 kHz`.
- Enable Diagnostic Boot during first board bring-up.
- Export and archive the Quartus-generated pin/config report.

## 8. Sequencing and Power-Good Requirements

Board-level sequence must ensure:

- `A5E_VCC_VID` initially powers up to `0.80 V`.
- The regulator PMBus interface is alive when SDM attempts VID communication.
- `VCCIO_SDM` is valid before relying on SDM PMBus communication.
- PMBus lines are not held low by an unpowered regulator, level shifter, or external controller.
- Regulator PGOOD is included in the board-level power-good tree.
- FPGA `nSTATUS`, `CONF_DONE`, and `INIT_DONE` are observable during bring-up.

Recommended power-good signals to expose:

- `A5E_VCC_VID_PGOOD`
- `A5E_1V8_SDM_PGOOD`
- `A5E_NSTATUS`
- `A5E_CONF_DONE`
- `A5E_INIT_DONE`
- PMBus test header or accessible debug pads

## 9. Layout Requirements

For the regulator:

- Keep power stages close to regulator/controller and current path compact.
- Put high-frequency input/output capacitors close to the power stage.
- Follow regulator vendor layout guide for switching nodes and current sense.
- Avoid routing PMBus and sense lines near SW nodes.

For FPGA load:

- Place bulk and high-frequency decoupling per PDN tool result.
- Connect all `VCC` and `VCCP` balls to low-impedance planes.
- Route `VCCLSENSE/GNDSENSE` as quiet Kelvin sense traces.
- Do not share sense return with high-current ground path.
- Add test point on `A5E_VCC_VID`, but do not stub into sensitive sense path.

## 10. Do / Do Not

Do:

- Use a PMBus-compliant SmartVID regulator.
- Keep the PMBus path available from SDM to regulator.
- Use `A5E_VCC_VID` naming.
- Make the regulator PMBus address explicit in the schematic.
- Add DNP/0-ohm options for sense fallback and PMBus debug.
- Archive FAE confirmation and Quartus reports.

Do not:

- Use a fixed-output non-PMBus 0.8 V buck for `VCC/VCCP`.
- Assume `20 MHz` or other unrelated configuration choices solve SmartVID.
- Tie `PWRMGT_SDA/SCL` to a busy system I2C bus without multi-master analysis.
- Copy the KEIm carrier-access PMBus topology unless the same system-management architecture is intended.
- Copy `27A/41A` current rating without EPE / Quartus Power Analyzer.

## 11. Concrete Recommended Implementation

If the board is a standalone minimum system:

```text
Regulator:
  TPS53676 or LTC3882-1 or ISL68223

Rail:
  +A5E_VCC_VID
  default/NVM output = 0.80 V

Loads:
  A5ED052A VCC
  A5ED052A VCCP
  other low-voltage rails only as allowed by current Pin Connection Guidelines

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

If the board already has a system controller or PMIC supervisor:

- Decide whether Agilex SDM is still the PMBus master.
- If external controller owns PMBus, analyze PMBus Slave/Target mode and connect `PWRMGT_ALERT`.
- Confirm boot-time firmware availability before relying on external PMBus control.

## 12. Items Requiring FAE / Tool Closure

These are not optional before schematic release:

1. Confirm `A5ED052AB32AE2V` is definitely a SmartVID `-2V` device and must use PMBus for `VCC/VCCP`.
2. Confirm chosen regulator is supported by the Quartus version used by the project.
3. Confirm regulator voltage format, PMBus address, PAGE settings, and initial NVM voltage.
4. Confirm exact rail-sharing rules for `VCCL_*`, `VCCPLLDIG_*`, HSSI and PLL rails.
5. Run Intel/Altera EPE or Quartus Power Analyzer for current budget.
6. Run PDN analysis for decoupling and plane impedance.
7. Confirm sequencing against Agilex 5 POR requirements.
8. Generate Quartus `.pin` / configuration report and compare against schematic.

## 13. Review Checklist

Schematic checks:

- [ ] `VCC` and `VCCP` connected to `A5E_VCC_VID`.
- [ ] `A5E_VCC_VID` regulator is PMBus-compliant.
- [ ] Regulator default output is `0.80 V`.
- [ ] `PWRMGT_SCL` uses `CF109 / SDM_IO14`.
- [ ] `PWRMGT_SDA` uses `CF99 / SDM_IO11`.
- [ ] PMBus voltage domain is correct or level shifted.
- [ ] `VCCLSENSE / GNDSENSE` connected correctly.
- [ ] PMBus address straps documented.
- [ ] Regulator PGOOD connected to power-good tree.
- [ ] `nSTATUS`, `CONF_DONE`, `INIT_DONE` visible at test pads or supervisor.
- [ ] FAE confirmation attached to schematic review package.

Layout checks:

- [ ] Sense routing is Kelvin and quiet.
- [ ] PMBus traces are not near switch nodes.
- [ ] Decoupling follows PDN result.
- [ ] Power-stage thermal path is reviewed.
- [ ] Test points do not disturb sense loop.

Bring-up checks:

- [ ] Measure `A5E_VCC_VID` initial voltage before programming.
- [ ] Verify PMBus idle high and no stuck-low condition.
- [ ] Confirm regulator ACK at selected address.
- [ ] Configure with Diagnostic Boot enabled.
- [ ] Log `nSTATUS`, `CONF_DONE`, `INIT_DONE`.
- [ ] Read PMBus output voltage after SDM VID adjustment.

## 14. Final Recommendation

For this project, freeze the schematic direction as:

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

Use the KEIm `LTC7883 + NCP302035` schematic as a reference for topology and sizing style, not as the default component choice, unless FAE explicitly approves it for `A5ED052AB32AE2V` and the selected Quartus version.
