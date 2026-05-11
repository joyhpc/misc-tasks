# LPDDR5 315-Ball TFBGA Footprint Spec For OrCAD/Allegro

## Target

Use this as the Allegro package symbol creation checklist for the current LPDDR5 x32 memory-side route.

## Package

- Package type: 315-ball TFBGA / WFBGA
- Body size: 12.4 mm x 15.0 mm
- Ball count: 315
- Reference ball diameter: 0.42 mm SMD
- Reference pattern: `Layout15x21_P0.8x0.7mm`
- Reference footprint name from public KiCad design:
  `BGA-315_12.4x15mm_Layout15x21_P0.8x0.7mm`

## Important Checks

- Do not use a 200-ball or 245-ball LPDDR package for this design.
- Do not use the 441-ball x64 reference package.
- Pin numbering must use LPDDR5 ball coordinates such as `A4`, `D1`, `H1`, `T5`, `AA12`.
- `CA/CK/WCK/CS` are shared A/B T-line nets on the memory side.
- `ZQ_A` is local 240 ohm to VDDQ and does not connect to FPGA.
- FPGA `RZQ` and `REFCLK_P/N` are FPGA-side only and must not be added as LPDDR5 component pins.

## Local Pin Source

Canonical memory-side pin list:

`/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/pin_assign/memory_side/lpddr5_memory_pin_net_by_package_orcad_order.xlsx`

Use sheet:

`315_DR_DS_valid_x32`

OrCAD Capture pin-list CSV:

`/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/orcad_ecad/lpddr5_315_tfbga_symbol_pinlist_for_orcad.csv`

## Final Verification Required

Before library release:

- Compare every ball name against final selected Micron datasheet.
- Run OrCAD Capture package pin count check.
- Run Allegro symbol pin count check.
- Cross-probe symbol pin number to Allegro pad number.
- Check BGA orientation: A1 mark, top view vs bottom view.
- Confirm padstack with PCB supplier for HDI process.
