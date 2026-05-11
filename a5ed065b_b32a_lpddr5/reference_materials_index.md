# LPDDR5 Reference Materials Index

## Best-Match Reference Design

Source: https://github.com/antmicro/lpddr5-testbed

Local path:
`/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/reference_designs/antmicro_lpddr5_testbed/`

This is the closest complete public reference for the current memory-side direction:

- LPDDR5 x32
- Micron `MT62F1G32D4DR-031 WT:B`
- 315-ball WFBGA / TFBGA
- 12.4 mm x 15.0 mm
- KiCad 9 project

Important files:

- Complete KiCad project:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/reference_designs/antmicro_lpddr5_testbed/lpddr5-testbed.kicad_pro`
- Complete schematic PDF:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/reference_designs/antmicro_lpddr5_testbed/doc/lpddr5-testbed.pdf`
- LPDDR5 schematic sheet and symbol definition:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/reference_designs/antmicro_lpddr5_testbed/lpddr5.kicad_sch`
- PCB with 315-ball footprint and routing:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/reference_designs/antmicro_lpddr5_testbed/lpddr5-testbed.kicad_pcb`
- Power reference sheet:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/reference_designs/antmicro_lpddr5_testbed/power_supply.kicad_sch`

Extracted ECAD facts from the KiCad design:

- Symbol: `antmicroMemory:MT62F1G32D4DR-031`
- Footprint: `antmicro-footprints:BGA-315_12.4x15mm_Layout15x21_P0.8x0.7mm`
- Description: `DRAM LPDDR5 32G X32 TFBGA`

## Current Project Pin Tables

- FPGA-side OrCAD table:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/fpga_side/fpga_pin_assign_orcad_format_hsio2b_3a_lpddr5.xlsx`
- Memory-side 315-ball x32 table:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/memory_side/lpddr5_memory_pin_net_by_package_orcad_order.xlsx`
  - Sheet: `315_DR_DS_valid_x32`
- U0 memory TSV:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/memory_side/lpddr5_315_DR_DS_U0_Bank2B_pin_net.tsv`
- U1 memory TSV:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/memory_side/lpddr5_315_DR_DS_U1_Bank3A_pin_net.tsv`

## OrCAD / Allegro ECAD

- OrCAD/Allegro ECAD notes and download sources:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/orcad_ecad/README.md`
- OrCAD Capture pin-list CSV:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/orcad_ecad/lpddr5_315_tfbga_symbol_pinlist_for_orcad.csv`
- Allegro 315-ball footprint checklist:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/orcad_ecad/lpddr5_315_tfbga_footprint_spec.md`

## Datasheets And PCN

- Micron 315/441/561 Y62P LPDDR5X datasheet:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/datasheets_pcn/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- Micron Y6CP LPDDR5X datasheet:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/datasheets_pcn/315b-441b-561b-y6cp-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- Samsung 245FBGA LPDDR5X datasheet:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/datasheets_pcn/[Datasheet]LP5X_32Gb_D_245F_8.2x12.4_K3KL8L80DM-TGCT_Rev0.0.pdf`
- Micron PCN 36290:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/datasheets_pcn/PCN 36290.pdf`

## Agilex 5 Reference Documents

- Altera Agilex 5 EMIF IP user guide, LPDDR5 sections:
  https://docs.altera.com/r/docs/817467/current
- Altera Agilex 5E 065B SOM complete schematic:
  `/home/ubuntu/misc-tasks/a5ed052a_min_system_pin_assign/sources/reference_schematic/agilex-5e-mdevkit-som-sch-v2p1.pdf`

Note: the Altera 065B SOM schematic is useful for FPGA power, SDM, JTAG, configuration, and board structure, but its memory reference is not the current 315-ball LPDDR5 x32 memory-side design.
