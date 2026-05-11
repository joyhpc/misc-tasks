# OrCAD / Allegro ECAD Notes

## Current Status

Native OrCAD/Allegro files are not checked in yet:

- OrCAD Capture library: `.olb`
- OrCAD/Capture design: `.dsn`
- Allegro package symbol: `.dra` / `.psm`
- Allegro padstacks: `.pad`

This machine does not have Cadence OrCAD/Allegro installed, so native binary Cadence libraries cannot be generated locally.

## Exact Download Sources To Use

Priority 1, current 315-ball LPDDR5 candidate:

- Mouser `MT62F1G32D2DS-020 WT:D`:
  https://www.mouser.tw/ProductDetail/Micron/MT62F1G32D2DS-020-WTD?qs=PBDs2xEllI%2FX8sIy9eo6PQ%3D%3D
- Mouser `MT62F1G32D2DS-020 WT:F`:
  https://www.mouser.com/ProductDetail/Micron/MT62F1G32D2DS-020-WTF?qs=IKkN%2F947nfCJEjcMUI%252BN0g%3D%3D

Both Mouser pages expose an `ECAD Model` entry and instruct using Library Loader to convert for the ECAD tool. Select OrCAD/Allegro when downloading/importing.

Priority 2, known LPDDR5 315-ball x32 reference part:

- Mouser `MT62F1G32D4DR-031 WT:B`:
  https://www.mouser.com/ProductDetail/Micron/MT62F1G32D4DR-031-WTB?qs=Wj%2FVkw3K%252BMAQnk0A174vSA%3D%3D
- SnapMagic `MT62F1G32D4DR-031 WT:B`:
  https://www.snapeda.com/parts/MT62F1G32D4DR-031%20WT%3AB/Micron/view-part/

SnapMagic lists OrCAD/Allegro v17/v16 formats, but download requires account/login.

Priority 3, distributor CAD request:

- Arrow `MT62F1G32D2DS-020 WT:F`:
  https://www.arrow.com/en/products/mt62f1g32d2ds-020-wtf/micron-technology

Arrow shows `2D PCB Symbol, Footprint, 3D Model`, but the page routes through a CAD model request flow.

## Local OrCAD Input Files

- Symbol pin list for OrCAD Capture spreadsheet entry:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/orcad_ecad/lpddr5_315_tfbga_symbol_pinlist_for_orcad.csv`
- Footprint package spec:
  `/home/ubuntu/misc-tasks/a5ed065b_b32a_lpddr5/orcad_ecad/lpddr5_315_tfbga_footprint_spec.md`

## Package Target

Use 315-ball TFBGA / WFBGA:

- Body: 12.4 mm x 15.0 mm
- Ball count: 315
- Ball diameter reference: 0.42 mm SMD from Antmicro reference
- Footprint reference name from KiCad source:
  `BGA-315_12.4x15mm_Layout15x21_P0.8x0.7mm`

Before release, verify pad diameter, soldermask, paste, escape via, and courtyard against the final Micron datasheet and PCB factory capability.
