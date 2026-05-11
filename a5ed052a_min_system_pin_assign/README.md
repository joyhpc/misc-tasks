# A5ED052A B32A Minimum-System Pin Assign

This folder is the canonical delivery package for the A5ED052A B32A minimum-system schematic pin assignment work.

## Open This First

- Final working workbook: `deliverables/a5ed052a_b32a_min_system_pin_assign_draft_v2.xlsx`
- Altera 065A Premium Devkit power tree explanation, Chinese: `deliverables/altera_065a_premium_devkit_power_tree_explanation_zh.md`
- Altera 065B SOM demo power tree explanation, Chinese: `deliverables/altera_065b_som_power_tree_explanation_zh.md`
- VCC / SmartVID reference schematic summary, Chinese: `deliverables/a5ed052a_b32a_vcc_reference_schematic_summary_zh.md`
- VCC / SmartVID power design report, Chinese: `deliverables/a5ed052a_b32a_vcc_smartvid_power_design_report_zh.md`
- VCC / SmartVID power design report, English: `deliverables/a5ed052a_b32a_vcc_smartvid_power_design_report.md`
- Older draft, do not use unless comparing history: `deliverables/archive/a5ed052a_b32a_min_system_pin_assign_draft_v1.xlsx`

## Source Structure

- `sources/official_pinouts/a5ed052a/`
  - Official Altera A5ED052A pinout package, used as the primary source for A5ED052A B32A ball/function mapping.
- `sources/official_pinouts/a5ed065b_reference/`
  - Official Altera A5ED065B pinout package, used only to verify that the reference board's B32A SDM/config pins are pin-to-pin compatible with A5ED052A B32A.
- `sources/reference_schematic/`
  - Official Altera Agilex 5 E-Series 065B Modular Development Kit SOM schematic, used as the real schematic reference for JTAG, AS boot, MSEL, CONF_DONE, INIT_DONE, PMBus, OSC_CLK_1, and RREF_SDM connections.

## Current Status

- The workbook is a source-backed draft for schematic drawing, not a release-frozen design.
- Ball numbers and SDM/JTAG/config pin functions are backed by official A5ED052A pinout.
- Board-level connection style is cross-checked against the official A5ED065B B32A reference schematic.
- Items still requiring project decisions are marked `TBD-source` in `Mechanical_Checks`.

## Recommended Next Inputs

- QSPI flash part and topology.
- Power tree and SmartVID/PMBus regulator plan.
- HPS usage decision and boot medium.
- Quartus project pin report or generated SDM_IO report.
- OrCAD FPGA symbol order if the workbook must be reordered exactly as the schematic symbol.
