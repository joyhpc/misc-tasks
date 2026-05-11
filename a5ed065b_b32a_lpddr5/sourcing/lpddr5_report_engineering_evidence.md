# A38 / DF108 LPDDR5 采购寻样工程证据报告

日期：2026-05-08
报告类型：工程证据版
用途：设计评审、原理图选型依据、Quartus EMIF / Pin Planner 输入、风险归档

## 1. 证据范围和方法

本报告基于以下本地工作空间证据整理：

- Gmail 只读搜索范围：`purehpc@gmail.com`
- 时间窗口：2026-05-07 至 2026-05-08
- 搜索语句：`in:anywhere after:2026/05/06 before:2026/05/09`
- 关键词：`LPDDR5 / LPDDR / 采购 / 寻样 / 存储颗粒 / Micron / Samsung / Hynix / 美光 / 三星 / 南亚 / Henry`
- 原始需求文件：`LPddr5需求 to 采购工程师 沟通.md`
- 附件目录：`attachments/`

本报告只做技术和供应链证据整理，不代表料号已冻结。LPDDR5/LPDDR5X 最终 pin list、bank 分配和时序配置必须以 Quartus EMIF / Pin Planner / Fitter 结果为准。

## 2. 需求追踪矩阵

| 需求项 | 原始需求 | 当前证据状态 | 工程判断 |
| --- | --- | --- | --- |
| DRAM 类型 | LPDDR5 | 美光和三星反馈均为 LPDDR5X 路线；美光 datasheet 标注 LPDDR5X/LPDDR5 data interface | 可以评估 LPDDR5X 降频/兼容使用，但需 EMIF 验证 |
| 位宽 | 单颗 x32 | 美光 `MT62F1G32D2DS-020 WT:D` 为 x32；三星 `K3KL8L80DM-TGCT` 为 x32 | x32 可满足 |
| 容量 | 2GB / 16Gb | 美光 x32 从 4GB 起步；三星附件为 32Gb / 4GB | 原 2GB 不满足；需需求变更或继续寻源 |
| 速率 | 主控 3733 MT/s；优先 5500/6400 可降频 | 美光候选为 9600 Mb/s per pin；三星候选为 7500 Mbps | 可降频假设需供应商和 Quartus 双重确认 |
| 温度等级 | 商业级 | 三星 datasheet 显示 Tc -25 to 85 C；美光 `WT:D` 温度/等级待正式确认 | 美光温度等级是 P0 待确认项 |
| 生命周期 | 5-8 年无 EOL | 美光旧 2GB 相关料号有 EOL/停产风险；三星渠道称消费类 2-3 年 | 2GB 路线风险高；美光 Y62P 4GB 需正式生命周期确认 |
| 封装 | Standard BGA | 美光 315-ball TFBGA DS；三星 245FBGA 8.2x12.4 | 原理图库、封装、pinout 需重新评估 |

## 3. 邮件证据索引

| Gmail Message ID | 时间 | 来源 | 主题 | 证据价值 |
| --- | --- | --- | --- | --- |
| `19e065df94f3cfec` | 2026-05-08 14:53:57 +0800 | 何鹏程转发，原始来源 Vince Huo / WPI | 转发：回复: LPDDR5 存储颗粒选型需求 | 美光 PCN / 主推 9600 MT/s 产品 / 多容量候选 |
| `19e065cdbd67077e` | 2026-05-08 14:53:09 +0800 | 何鹏程转发，原始来源 Kun Cao / WT Microelectronics | 转发：回复: LPDDR5 存储颗粒选型需求 | 美光 4GB x32 推荐料号和项目资料需求 |
| `19e065d03c1d5052` | 2026-05-08 14:53:28 +0800 | 何鹏程转发，原始来源 Fifi Lin / WT Microelectronics | 转发：Re: LPDDR5 存储颗粒选型需求 | 南亚无 LPDDR5 |
| `19e065c771a63d06` | 2026-05-08 14:52:31 +0800 | 何鹏程转发，原始来源 Link Liu / Golden Supreme | 转发：回复: LPDDR5 存储颗粒选型需求 | 三星 LP5X 不匹配、生命周期 2-3 年、附件料号 |
| `19e065c87163f67f` | 2026-05-08 14:53:00 +0800 | 何鹏程转发，采购发给 Henry | 转发：LPDDR5 存储颗粒选型需求 | Henry 渠道仅见发出需求，未见回复 |

## 4. 美光证据

### 4.1 邮件反馈

Kun Cao / WT Microelectronics 反馈：

- 美光 x32 LPDDR5/LPDDR5X 从 4GB 起步。
- 推荐：`MT62F1G32D2DS-020 WT:D`。
- 需要补充项目信息：终端客户、项目名称、应用、试产时间、量产时间、主芯片、年用量、每片用几颗。

Vince Huo / WPI 反馈：

- 美光后续主推 9600 MT/s 产品。
- 原 8533 速率型号将停产。
- 7500 以下已经停产。
- 列出 Y62P / Y6CP 系列候选。

### 4.2 Datasheet 证据

附件：

- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x.pdf`

从附件抽取到的关键字段：

| 字段 | 内容 |
| --- | --- |
| 标题 | Y62P LPDDR5X SDRAM |
| 接口 | LPDDR5X/LPDDR5 data interface |
| 推荐料号 | `MT62F1G32D2DS-020 WT:D` |
| 总容量 | 4GB / 32Gb |
| 数据速率 | 9600 Mb/s per pin |
| 封装 | 315-ball TFBGA，package code DS |
| 文档版本 | Rev. G 03/2026 |

相关扩展候选：

| 料号 | 容量 | 备注 |
| --- | --- | --- |
| `MT62F1G32D2DS-020 WT:D` | 4GB / 32Gb | 当前最接近候选 |
| `MT62F2G32D4DS-020 WT:D` | 8GB / 64Gb | 容量更大 |
| `MT62F4G32D8DV-020 WT:D` | 16GB | 容量更大 |
| `MT62F6G32D8DV-020 WT:B` | 24GB | Y6CP 路线，容量过大 |

### 4.3 PCN / EOL 证据

附件：

- `attachments/PCN 36290.pdf`

抽取到的关键字段：

| 字段 | 内容 |
| --- | --- |
| PCN | 36290 |
| 标题 | End of Life Notification for Y52P Specific 315b Packages |
| Published | 2026-02-04 |
| Description | Micron discontinuing specific LPDDR5 Y52P 315b DDP/QDP/8DP packages |
| Last Order Date | 2026-08-04 |
| Last Ship Date | 2027-02-04 |
| NCNR Date | 2026-05-06 |

邮件正文还引用 PCN_36383：

| 字段 | 内容 |
| --- | --- |
| PCN | 36383 |
| Published | 2026-04-22 |
| 标题 | End of Life of LPDDR5 Y52Q Embedded Automotive and Non-Automotive |
| 影响 | Y52Q 315b x32 2GB SDP、441b x64 4GB DDP 等 |
| Last Order Date | 2026-10-23 |
| Last Ship Date | 2028-12-31 |
| NCNR Date | 2026-07-25 |

工程判断：

- 旧代 2GB x32 路线与 5-8 年生命周期目标冲突。
- 若项目坚持 2GB，需要供应商给出非 EOL、可长期供货的正式替代料号，否则不能冻结。

## 5. 三星证据

### 5.1 邮件反馈

Link Liu / Golden Supreme 反馈：

- 三星目前出货 LP5X 产品，从容量和生命周期角度都没有能匹配需求的产品。
- 最小容量产品预计 2026 年 5 月底或 6 月中出样品。
- 该产品为消费类。
- 消费类生命周期通常 2-3 年。

### 5.2 Datasheet 证据

附件：

- `attachments/[Datasheet]LP5X_32Gb_D_245F_8.2x12.4_K3KL8L80DM-TGCT_Rev0.0.pdf`

抽取到的关键字段：

| 字段 | 内容 |
| --- | --- |
| 料号 | `K3KL8L80DM-TGCT` |
| 类型 | LPDDR5X SDRAM |
| 容量 | 32Gb / 4GB |
| 组织 | x32 |
| 封装 | 245FBGA，8.2 x 12.4 mm |
| 最大频率 | 7500 Mbps |
| 温度 | Tc -25 to 85 C |

工程判断：

- 该料号容量和位宽接近美光 4GB x32 方向，但供应商已明确生命周期不匹配。
- 245FBGA 封装不同于美光 315-ball TFBGA，不能无缝替代。
- 不建议进入主设计路径。

## 6. 南亚证据

Fifi Lin / WT Microelectronics 反馈：Nanya 没有 LPDDR5。

工程判断：南亚路线关闭。

## 7. Henry / HSRP 证据

采购于 2026-05-08 10:10 向 Henry 发出 LPDDR5 需求。当前 Gmail 搜索范围内未见回复。

工程判断：不可计入可用候选。采购可催一次作为补充渠道。

## 8. 工程风险登记

| 风险 ID | 风险 | 影响 | 当前状态 | 缓解措施 |
| --- | --- | --- | --- | --- |
| R1 | 2GB x32 长生命周期料号不可得 | 原始需求无法直接满足 | 已发生 | 接受 4GB x32 或扩大供应商范围 |
| R2 | 美光候选容量上浮至 4GB | BOM、系统内存映射、初始化配置可能变化 | 待决策 | 项目负责人确认需求变更 |
| R3 | LPDDR5X 9600 降频到 3733 使用 | EMIF 参数、training、ODT、SI 需验证 | 待验证 | 供应商确认 + Quartus EMIF 验证 |
| R4 | 旧代美光料号 EOL | 生命周期不满足 5-8 年 | 已有 PCN 证据 | 不选旧代 2GB 料号 |
| R5 | 三星消费类生命周期短 | 量产后供应风险 | 已明确 | 不作为主推料号 |
| R6 | pin/bank/PLL/RZQ 资源冲突 | Fitter 失败或 PCB 返工 | 待验证 | 逻辑侧建立最小 Quartus 工程 |
| R7 | 封装差异 | 原理图库、PCB footprint、SI 模型不同 | 待验证 | 只冻结一个主料号后再建库 |

## 9. Quartus / 原理图验证建议

建议逻辑侧先按美光 `MT62F1G32D2DS-020 WT:D` 做最小验证：

输入参数：

- Device：Intel Agilex 5，当前按 A5ED052A B32A 方向评估。
- Memory：LPDDR5/LPDDR5X x32。
- Candidate：`MT62F1G32D2DS-020 WT:D`。
- Data rate：先按主控可支持上限 3733 MT/s 建立目标约束。
- Topology：每组一个 LPDDR5 主控，对应一个 x32 颗粒；项目当前按两组 x32 规划。

逻辑侧输出：

- EMIF 配置截图或参数导出。
- Pin Planner 结果。
- Fitter 规则检查结果。
- QSF / pin report。
- 与 MIPI D-PHY、QSFP、clock/reset/config 共存的资源冲突说明。

硬件侧输出：

- 315-ball TFBGA DS footprint 和符号页。
- 电源 rail、RZQ、reset、refclk、ODT/termination、VREF/相关接口设计检查。
- 与板级空间和 SI 约束的初步结论。

## 10. 工程验收标准

在进入原理图 pin list 冻结前，至少满足：

1. 供应商正式确认 `MT62F1G32D2DS-020 WT:D` 的生命周期、温度等级、供货周期和价格。
2. 项目负责人确认可接受 4GB x32 方案。
3. 逻辑侧完成 Quartus EMIF + Pin Planner / Fitter 验证。
4. 硬件侧确认封装、供电、pinout、原理图资源和 PCB 可实现性。
5. 采购确认是否存在 2GB x32 长生命周期替代料号；如无，则在需求中正式记录容量变更。

## 11. 附录：当前工作文件

- `lpddr5_mail_summary.md`
- `lpddr5_supplier_matrix.csv`
- `lpddr5_reply_drafts.md`
- `attachments/PCN 36290.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x_19e065df94f3cfec.pdf`
- `attachments/315b-441b-561b-y6cp-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/[Datasheet]LP5X_32Gb_D_245F_8.2x12.4_K3KL8L80DM-TGCT_Rev0.0.pdf`

