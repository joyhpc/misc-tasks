# LPDDR5 采购寻样邮件处理结论

处理时间：2026-05-08
搜索范围：Gmail `purehpc@gmail.com`，`in:anywhere after:2026/05/06 before:2026/05/09`，关键词 `LPDDR5 / LPDDR / 采购 / 寻样 / 存储颗粒 / 美光 / 三星 / 南亚 / Henry`。

## 结论

当前邮件没有找到完全匹配“单颗 2GB / 16Gb、x32、LPDDR5、商业级、未来 5-8 年无 EOL”的现货/可推荐料号。

最接近的可推进候选是美光 LPDDR5X 4GB x32：

- 推荐料号：`MT62F1G32D2DS-020 WT:D`
- 类型：LPDDR5X / LPDDR5 data interface
- 容量：4GB / 32Gb
- 位宽：x32
- 速率：9600 Mb/s per pin，设计可降频到主控 3733 MT/s 使用
- 附件：`attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x.pdf`

但它不满足原始“2GB / 16Gb”容量要求，是容量上浮方案；需要硬件/系统确认容量上浮、BOM 成本、封装尺寸、pinout、供电和 Agilex 5 EMIF 兼容性是否接受。

## 供应商反馈摘要

### 美光 / WPG / WT Microelectronics

邮件链路：

- `19e065cdbd67077e`：Kun Cao / WT Microelectronics，2026-05-08 08:59
- `19e065df94f3cfec`：Vince Huo / WPI，2026-05-07 17:13

关键反馈：

- 美光 x32 LPDDR5/LPDDR5X 已经从 4GB 起步。
- 推荐 4GB LPDDR5X Y62P：`MT62F1G32D2DS-020 WT:D`。
- 美光后续主推 9600 MT/s 产品。
- 原 8533 速率型号将停产；7500 以下已经停产。
- 美光要求补充项目背景信息：终端客户、项目名称、应用、试产时间、量产时间、主芯片、年用量、每片用几颗。

EOL/PCN 风险：

- 附件 `PCN 36290.pdf`：Y52P specific 315b packages EOL，Published 2026-02-04，Last Order Date 2026-08-04，Last Ship Date 2027-02-04，NCNR Date 2026-05-06。
- 邮件正文还引用 PCN_36383：Y52Q 315b x32 2GB SDP 等 EOL，Published 2026-04-22，Last Order Date 2026-10-23，Last Ship Date 2028-12-31，NCNR Date 2026-07-25。
- 这说明 2GB x32 旧代料号不适合作为 5-8 年生命周期方案。

建议动作：

1. 把美光 4GB x32 Y62P 作为 primary candidate 继续推进。
2. 补齐项目/用量信息给美光代理，要求正式确认生命周期、供货年限、商业级/温度等级、sample/MP lead time、价格、推荐替代路线。
3. 让硬件/逻辑确认 `MT62F1G32D2DS-020 WT:D` 的封装、pinout、供电、初始化参数和 Agilex 5 EMIF 降频兼容性。

### 三星 / Golden Supreme

邮件链路：

- `19e065c771a63d06`：Link Liu / Golden Supreme，2026-05-08 14:18

关键反馈：

- 三星目前出货的 LP5X 产品，从容量和生命周期看都没有能匹配需求的产品。
- 三星 LP5X 最小容量是 5 月底或 6 月中才出样品的消费类 245ball 产品。
- 附件料号：`K3KL8L80DM-TGCT`
- 附件显示：32Gb / x32 / 245FBGA / 7500 Mbps / Tc -25 to 85 C。
- 供应商明确说明消费类生命周期通常 2-3 年。

建议动作：

- 不作为 A38 当前主推料号。
- 仅保留为备选调研项；除非项目可以接受消费类、样品等待、2-3 年生命周期和 245FBGA 封装，否则不要推进。

### 南亚 / Nanya

邮件链路：

- `19e065d03c1d5052`：Fifi Lin / WT Microelectronics，2026-05-07 23:56

关键反馈：

- Nanya 没有 LPDDR5。

建议动作：

- 关闭 Nanya 路线，不再投入时间。

### Henry / HSRP

邮件链路：

- `19e065c87163f67f`：采购 2026-05-08 10:10 发给 Henry

关键反馈：

- 当前 Gmail 搜索范围内只看到发出的寻样需求，没有看到 Henry 回复。

建议动作：

- 如果 Henry 是必须覆盖的渠道，建议采购单独催一次，并明确问是否有 2GB x32 长生命周期 LPDDR5/LPDDR5X 可供。

## 推荐决策

推荐先按“美光 4GB x32 LPDDR5X Y62P 降频使用”推进可行性评估，同时把“2GB x32 长生命周期”标记为当前供应链不可满足或高风险。

理由：

- 美光是唯一给出明确可推进料号和资料的路线。
- 三星明确不匹配，南亚明确无 LPDDR5。
- 原 2GB x32 相关美光旧料号存在 EOL/停产风险，不满足 5-8 年目标。

需要你确认的工程取舍：

- 是否接受单颗容量从 2GB 上浮到 4GB。
- 是否接受 LPDDR5X 料号按 LPDDR5/LPDDR5X 接口降频使用。
- 是否先让逻辑侧用 `MT62F1G32D2DS-020 WT:D` 参数进入 Quartus EMIF / Pin Planner / Fitter 验证。

## 当前目录附件

- `attachments/PCN 36290.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x_19e065df94f3cfec.pdf`
- `attachments/315b-441b-561b-y6cp-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/[Datasheet]LP5X_32Gb_D_245F_8.2x12.4_K3KL8L80DM-TGCT_Rev0.0.pdf`
