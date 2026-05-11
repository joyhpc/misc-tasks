# A38 / DF108 LPDDR5 采购寻样内部决策报告

日期：2026-05-08
范围：Gmail 转发邮件，时间窗口 2026-05-07 至 2026-05-08
项目：A38 / DF108 Agilex 5
用途：内部项目决策、采购下一步动作、硬件/逻辑侧可行性输入

## 1. 结论摘要

本轮邮件没有找到完全匹配原始需求的料号：`单颗 2GB / 16Gb、x32、LPDDR5、商业级、未来 5-8 年无 EOL`。

当前唯一可继续推进的主候选是美光 LPDDR5X：

| 项目 | 内容 |
| --- | --- |
| 推荐料号 | `MT62F1G32D2DS-020 WT:D` |
| 厂商 | Micron / 美光 |
| 类型 | LPDDR5X，兼容 LPDDR5/LPDDR5X data interface |
| 容量 | 4GB / 32Gb |
| 位宽 | x32 |
| 速率 | 9600 Mb/s per pin |
| 封装 | 315-ball TFBGA，package code DS |
| 当前判断 | 可作为 primary candidate，但不是原始 2GB 方案 |

建议决策：接受“4GB x32 LPDDR5X 降频使用”作为主线评估方向，同时把“2GB x32 长生命周期 LPDDR5”标记为供应链高风险或当前不可满足。

## 2. 原始需求基线

采购寻样的原始需求如下：

| 需求项 | 原始要求 |
| --- | --- |
| 核心规格 | LPDDR5，Standard BGA Package |
| 位宽 | 单颗 x32 |
| 容量 | 单颗 2GB / 16Gb |
| 主控支持上限 | 3733 MT/s |
| 寻源建议 | 市面主流 5500 MT/s 或 6400 MT/s 料号，硬件设计降频使用 |
| 温度等级 | 商业级即可 |
| 生命周期 | 未来 5-8 年无 EOL 风险 |
| 目标品牌 | 美光、三星、海力士等一线大厂 |

本轮供应商反馈暴露出的核心矛盾是：主流一线厂商 x32 LPDDR5/LPDDR5X 已经向更高容量、更高速率产品迁移，2GB / 16Gb x32 长生命周期料号不可得或存在 EOL 风险。

## 3. 供应商反馈结论

### 3.1 美光路线

来源邮件：

- `19e065cdbd67077e`：Kun Cao / WT Microelectronics，2026-05-08 08:59
- `19e065df94f3cfec`：Vince Huo / WPI，2026-05-07 17:13

关键事实：

- 美光 x32 LPDDR5/LPDDR5X 当前从 4GB 起步。
- 推荐 4GB LPDDR5X Y62P：`MT62F1G32D2DS-020 WT:D`。
- 美光后续主推 9600 MT/s 产品。
- 原 8533 速率型号将停产；7500 以下已停产。
- 供应商要求补充：终端客户、项目名称、应用、试产时间、量产时间、主芯片、年用量、每片用几颗。

判断：

- 美光是唯一给出明确候选料号和 datasheet/PCN 资料的路线。
- 但推荐料号容量为 4GB，不满足原始 2GB 要求。
- 由于旧代 2GB x32 料号存在 EOL 信息，强行坚持 2GB 会显著增加供应风险。

### 3.2 三星路线

来源邮件：

- `19e065c771a63d06`：Link Liu / Golden Supreme，2026-05-08 14:18

关键事实：

- 三星渠道明确反馈：目前出货 LP5X 产品从容量和生命周期看都没有能匹配需求的产品。
- 提到的最小容量产品为消费类 245ball，预计 2026 年 5 月底或 6 月中出样品。
- 附件料号：`K3KL8L80DM-TGCT`。
- Datasheet 字段：32Gb / x32 / 245FBGA / 7500 Mbps / Tc -25 to 85 C。
- 供应商明确说明消费类生命周期通常 2-3 年。

判断：

- 不适合作为 A38 当前主推料号。
- 可保留为备选调研项，但不满足 5-8 年生命周期要求。

### 3.3 南亚路线

来源邮件：

- `19e065d03c1d5052`：Fifi Lin / WT Microelectronics，2026-05-07 23:56

关键事实：

- Nanya 没有 LPDDR5。

判断：

- 关闭南亚路线。

### 3.4 Henry / HSRP 路线

来源邮件：

- `19e065c87163f67f`：采购在 2026-05-08 10:10 发出需求。

关键事实：

- 当前 Gmail 搜索范围内只看到发出的寻样需求，没有看到 Henry 回复。

判断：

- 采购可催一次，但不能把 Henry 路线计入当前可用候选。

## 4. 候选方案对比

| 方案 | 料号/来源 | 匹配度 | 优点 | 主要问题 | 建议 |
| --- | --- | --- | --- | --- | --- |
| A. 美光 4GB x32 LPDDR5X | `MT62F1G32D2DS-020 WT:D` | 部分匹配 | 一线厂商；x32；资料明确；主推 9600 MT/s，可降频评估 | 容量从 2GB 上浮到 4GB；生命周期、温度等级、价格、lead time 待正式确认 | 主线推进 |
| B. 继续坚持 2GB x32 | 旧代美光或其他待寻源 | 当前不可确认 | 满足原始容量目标 | 美光旧代 2GB x32 存在 EOL/停产风险；暂无一线厂商推荐 | 标记高风险，不建议作为唯一方案 |
| C. 三星 245FBGA 消费类 | `K3KL8L80DM-TGCT` | 不推荐 | x32，32Gb，7500 Mbps | 消费类；生命周期 2-3 年；样品未稳定；封装 245FBGA；供应商已说明不匹配 | 不作为主推 |
| D. 南亚 | 无 | 不匹配 | 无 | 没有 LPDDR5 | 关闭 |

## 5. 关键风险

### 5.1 容量上浮风险

美光可推进方案是 4GB，而原始需求是 2GB。

影响：

- 单板内存容量翻倍，可能影响 BOM 成本。
- 初始化参数、地址映射、软件/逻辑配置可能需要调整。
- 如果系统原本只需要 2GB，额外容量是成本换供应安全。

需要确认：

- 系统是否接受单颗 4GB。
- 每板 2 颗 x32 规划下，总容量是否仍在系统和 BOM 可接受范围内。

### 5.2 LPDDR5X 降频使用风险

候选料号是 LPDDR5X 9600 Mb/s per pin，主控端当前按 3733 MT/s 上限评估。

影响：

- 理论上高速料号可低速运行，但仍需供应商确认长期降频使用建议。
- Agilex 5 EMIF 配置、training、ODT、SI 约束不能靠采购邮件冻结。

需要确认：

- 供应商确认是否适合 3733 MT/s 降频运行。
- 逻辑侧用 Quartus EMIF / Pin Planner / Fitter 验证。

### 5.3 生命周期风险

原始要求是未来 5-8 年无 EOL 风险。

已知风险：

- 美光 PCN 显示 Y52P specific 315b packages EOL：Published 2026-02-04，Last Order Date 2026-08-04，Last Ship Date 2027-02-04。
- 邮件正文引用 Y52Q 315b x32 2GB SDP 等 EOL：Published 2026-04-22，Last Order Date 2026-10-23，Last Ship Date 2028-12-31。
- 三星渠道明确说明消费类生命周期通常 2-3 年。

需要确认：

- `MT62F1G32D2DS-020 WT:D` 是否属于美光长期主推 Y62P 路线。
- 是否有正式生命周期承诺或 PCN 风险说明。

### 5.4 封装和 pinout 风险

LPDDR5/LPDDR5X 连接不能只按料号采购决定。

需要确认：

- 315-ball TFBGA DS 封装尺寸和原理图库。
- byte lane、CA、CK、CS、DMI、DQ、DQS、RESET、RZQ、VREF/供电 rail。
- 与 Agilex 5 EMIF bank/pin 规划、MIPI/QSFP 共存资源是否冲突。

## 6. 推荐决策

建议做如下内部决策：

1. 采购侧继续以美光 `MT62F1G32D2DS-020 WT:D` 为主线寻样和确认。
2. 硬件侧接受“容量上浮到 4GB”的评估输入，但在正式冻结前保留成本和系统确认项。
3. 逻辑侧尽快将该料号作为 LPDDR5/LPDDR5X x32 候选参数进入 Quartus EMIF / Pin Planner / Fitter 验证。
4. 三星路线暂不推进，除非后续给出长期生命周期料号。
5. 南亚路线关闭。
6. Henry 路线由采购催一次，作为补充渠道，不影响美光主线推进。

## 7. 下一步行动清单

| Owner | 动作 | 输出物 | 优先级 |
| --- | --- | --- | --- |
| 采购 | 向美光/WT 补充项目信息并询问生命周期、价格、sample/MP lead time、MOQ/MPQ | 供应商正式回复 | P0 |
| 硬件 | 评估 4GB x32 方案对 BOM、封装、原理图页、电源 rail、板级空间的影响 | 硬件可接受性结论 | P0 |
| 逻辑 | 用 `MT62F1G32D2DS-020 WT:D` 方向建最小 Quartus EMIF 验证 | Fitter / Pin Planner / QSF / pin report | P0 |
| 项目负责人 | 决定是否接受容量从 2GB 上浮到 4GB | 需求变更确认 | P0 |
| 采购 | 催 Henry / HSRP 是否有 2GB x32 长生命周期料号 | 补充渠道反馈 | P1 |

## 8. 附件和证据

当前工作目录附件：

- `attachments/PCN 36290.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x_19e065df94f3cfec.pdf`
- `attachments/315b-441b-561b-y6cp-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/[Datasheet]LP5X_32Gb_D_245F_8.2x12.4_K3KL8L80DM-TGCT_Rev0.0.pdf`

关联整理文件：

- `lpddr5_supplier_matrix.csv`
- `lpddr5_reply_drafts.md`
- `lpddr5_mail_summary.md`

