# VCC / SmartVID Power Reference Analysis

## Scope

This note reviews the VCC/SmartVID-related power implementation in the vendor reference files placed under:

`sources/vendor_reference/`

Primary files reviewed:

- `keim-a5esom_sch_rev1.10.pdf`
- `keim-a5esom_bom_rev1.10-.xlsx`
- `keim-a5esom_hardware_manual_EN_v1.1.pdf`
- Existing official Altera 065B B32A SOM schematic under `sources/reference_schematic/`

## Key Finding

The KEIm A5E SOM reference does not use a plain fixed 0.8 V buck for the Agilex 5 core rail. It implements a dedicated `VCC_VID` rail using a PMBus-capable controller.

Observed topology:

- Main VID controller: `LTC7883AY#PBF`
- Power stages for `VCC_VID`: `NCP302035MNTWG`
- `VCC_VID` current annotation: `27A/41A`
- Reference voltage note on schematic:
  - `-1, -2, -3: VID`
  - `-4: 0.8V`
  - `-5: 0.78V`
  - `-6: 0.75V`

This supports the conclusion that `-2V` SmartVID designs must preserve a PMBus/VID-capable core regulator path.

## Rails Powered by VCC_VID in the KEIm Reference

The A5E power sheet clearly connects `VCC_VID` to `VCC` and `VCCP`, and routes `VCCLSENSE/GNDSENSE` into the VID regulator sense network.

The same power page also contains several 0.8 V-class low-voltage rails such as:

- `VCC`
- `VCCP`
- `VCCL_ADC_SDM`
- `VCCL_SDM`
- `VCCL_HPS`
- `VCCL_HPS_CORE0_CORE1`
- `VCCL_HPS_CORE2`
- `VCCL_HPS_CORE3`
- `VCCPLLDIG1_HPS`
- `VCCPLLDIG2_HPS`
- `VCCPLLDIG_SDM`

Do not infer from the reference schematic alone that every 0.8 V-class rail must be tied to `VCC_VID` on a new design. The hard official SmartVID requirement is for `VCC` and `VCCP`; the sharing of other low-voltage rails must be closed against the current Pin Connection Guidelines and FAE guidance.

## PMBus Topology Observed

The KEIm reference exposes two PMBus-related paths:

1. SDM PMBus path from Agilex 5:
   - `SDM_PWRMGT_SCL_1V8`
   - `SDM_PWRMGT_SDA_1V8`
   - level-shifted to 3.3 V

2. SOM/carrier PMBus path:
   - `SOM_PMBUS_SCL_3V3`
   - `SOM_PMBUS_SDA_3V3`

The BOM population indicates some SDM-to-PMBus links are optional / not mounted, while the SOM PMBus links are populated. This means the KEIm design is not a simple direct copy of the recommended minimal SDM-PMBus-master topology; it is a module design with carrier-accessible power management.

For a standalone board without a separate power-management controller, use the simpler direct SDM PMBus master topology.

## Sense Connection

The KEIm reference connects Agilex 5 sense pins into the VID regulator feedback/sense network:

- `VCCLSENSE_AV72`
- `GNDSENSE_AU72`

They are routed through 0-ohm links to the VID sense nets:

- `VID_VSNSA_P`
- `VID_VSNSA_N`

There is also local filtering/decoupling around the sense path.

Recommended interpretation for the new design:

- Do not leave `VCCLSENSE` / `GNDSENSE` floating.
- Use Kelvin-style remote sense from the regulator to the FPGA load point.
- Put any 0-ohm sense-selection resistors deliberately: load-sense near FPGA, local-sense near regulator only as a bring-up fallback.

## Recommended Direction for A5ED052AB32AE2V

For the target `A5ED052AB32AE2V`, use:

- One SmartVID-controlled rail, named for example `A5E_VCC_VID`.
- Initial regulator output: `0.80 V`.
- PMBus Master Mode from Agilex SDM.
- `PWRMGT_SCL = SDM_IO14 / CF109`.
- `PWRMGT_SDA = SDM_IO11 / CF99`.
- Keep `CONF_DONE = SDM_IO16 / BP102`.
- Keep `INIT_DONE = SDM_IO0 / CA99`.
- Keep `SDM_IO12 / BR99` as optional `PWRMGT_ALERT` / status / DNP until the final PMBus mode is frozen.

The regulator choice can follow either:

1. Intel/Altera fully validated SmartVID regulator list, such as `TPS53676`, `LTC3882-1`, or `ISL68223`.
2. The KEIm-style reference topology using `LTC7883AY#PBF` plus external power stages, if the FAE confirms Quartus/firmware compatibility and PMBus setup.

For the first production-oriented board, the lower-risk path is to use an Intel/Altera fully validated SmartVID regulator unless there is a strong reason to copy the KEIm LTC7883 implementation.

## Design Review Checks

Before releasing the schematic:

- Confirm the exact target order code is a `-2V` SmartVID part.
- Confirm which rails must be tied to the SmartVID rail from the current Intel pin connection guideline.
- Confirm PMBus Master vs external PMBus controller architecture.
- Confirm regulator part number, PMBus address, voltage format, PAGE setting, and initial NVM voltage.
- Confirm current rating using Quartus Power Analyzer or Intel EPE, not by copying the reference design current.
- Confirm remote sense routing and fallback resistor population.
- Confirm power-good and enable sequencing versus Agilex 5 power sequencing requirements.
