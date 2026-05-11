# A5ED065B B32A LPDDR5 File Index

## Active Pin Assignment

- FPGA side OrCAD table:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/fpga_side/fpga_pin_assign_orcad_format_hsio2b_3a_lpddr5.xlsx`
- Pin characteristics summary workbook:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/pin_characteristics_summary.xlsx`
  - Regenerate with:
    `python3 /home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/build_pin_characteristics_summary.py`
  - Key sheets: `overview`, `net_summary`, `memory_pin_features`, `fpga_pin_features`, `count_by_class`, `shared_net_detail`, `validation_rules`
- Memory side 315-ball x32 table:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/memory_side/lpddr5_memory_pin_net_by_package_orcad_order.xlsx`
  - Use sheet: `315_DR_DS_valid_x32`
- Memory side U0 TSV:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/memory_side/lpddr5_315_DR_DS_U0_Bank2B_pin_net.tsv`
- Memory side U1 TSV:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/memory_side/lpddr5_315_DR_DS_U1_Bank3A_pin_net.tsv`

## Mapping

- `U0` connects to FPGA `Bank2B`, net prefix `LP5_U0_*`.
- `U1` connects to FPGA `Bank3A`, net prefix `LP5_U1_*`.
- FPGA-only nets `REFCLK_P/N` and `FPGA_RZQ` are not on the LPDDR5 component side.
- Memory-side `ZQ_A_240R_TO_VDDQ` is local 240 ohm to VDDQ, not connected to FPGA.

## Reference Only

- LPDDR5 complete reference materials index:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/reference_materials_index.md`
- Antmicro LPDDR5 Testbed reference design:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/reference_designs/antmicro_lpddr5_testbed/`
- 441-ball package reference, not current x32 choice:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/package_reference/441_not_current/`
- Previous FPGA-side working files:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/fpga_side/archive_previous/`

## Sourcing And Evidence

- Sourcing docs:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/sourcing/`
- Datasheets and PCN:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/datasheets_pcn/`

## Cleanup

Deleted generated intermediate files:

- `offpage_*`
- `lpddr5_offpage_sorted_by_class.xlsx`
- `lpddr5_x32_a5ec052a_b32a_*.csv`
- `orcad_hsio2b_lpddr5_x32_*.csv`
- old duplicate Micron Y62P PDF with hash suffix
