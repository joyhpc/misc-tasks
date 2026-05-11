# A5ED065B B32A LPDDR5 寻样问题整理

日期：2026-05-11  
项目口径：A38 / DF108 Agilex 5  
报告类型：项目会议 + 采购跟进简报  
当前状态：`selected-not-frozen`，但 `A5ED065B B32A` 目标器件证据为 `TBD-evidence`

## 1. 当前结论

LPDDR5/LPDDR5X 寻样当前没有找到完全满足原始需求的料号：

| 原始需求 | 当前状态 |
|---|---|
| 单颗 2GB / 16Gb | 未找到长期稳定供货候选 |
| 单颗 x32 | 美光、三星候选均可到 x32 |
| LPDDR5 / LPDDR5X | 实际反馈主要转向 LPDDR5X |
| 商业级即可 | 三星 245FBGA 消费类生命周期不足；美光温度/等级仍待正式确认 |
| 5-8 年无 EOL 风险 | 旧 2GB 路线存在 EOL/停产风险；新 4GB 路线仍需供应商正式确认 |

当前可推进主线是美光 `MT62F1G32D2DS-020 WT:D`，但它是 `4GB / 32Gb x32 LPDDR5X`，不是原计划的 `2GB / 16Gb x32 LPDDR5`。如果每板仍按 2 颗 x32 规划，整板 LPDDR 容量会从原计划 4GB 上浮到 8GB。

## 2. A5ED065B B32A 证据缺口

本次在当前工作区、`my-daily`、本地 opendatasheet export 和 DF108 项目资料中，没有找到 `A5ED065B B32A` 的既有记录。现有 daily 与报告主要使用以下口径：

| 资料中出现的器件口径 | 状态 |
|---|---|
| `A5EC052A B32A` | 原理图/pin-net 工作表当前假设，daily 记录中用于 bank 2A/2B LPDDR5 x32 工作流 |
| `A5ED052A B32A` / `A5ED052AB32AE2V` | DF108 目标方案历史口径，仍有 A5EC/A5ED naming cleanup |
| `A5ED065B B32A` | `TBD-evidence`，需要确认是否为新的目标型号、口误，或后续器件升级 |

因此，不能把既有 `A5EC052A/A5ED052A B32A` 的 pin assign、bank 2A/2B、资源和 EMIF 结论直接签核迁移到 `A5ED065B B32A`。采购寻样结论可作为 LPDDR5/LPDDR5X 颗粒路线参考，但 FPGA 端可行性必须按最终确认为准的器件重新跑 Quartus / Pin Planner / Fitter。

## 3. 候选路线状态

| 路线 | 当前分类 | 证据状态 | 动作 |
|---|---|---|---|
| 美光 `MT62F1G32D2DS-020 WT:D` | Primary candidate | 已有供应商推荐和资料；生命周期、温度等级、价格、lead time、MOQ/MPQ、降频使用建议仍待正式回复 | 采购继续推进，作为主线寻样 |
| 三星 245FBGA `K3KL8L80DM-TGCT` | Rejected for mainline | 渠道反馈消费类、生命周期通常 2-3 年，不满足 5-8 年要求 | 不作为主推 |
| 三星 315FBGA x32 32Gb 路线 | Watchlist / parallel check | daily 中建议不要把三星全线关闭，但正式渠道证据仍待补 | 采购找正式渠道确认生命周期、样品、价格和 PCN/EOL 机制 |
| 南亚 / Nanya | Closed | 反馈没有 LPDDR5 | 关闭 |
| Henry / HSRP | Watchlist | 只见需求发出，未见回复 | 采购催一次 |
| 海力士 / Hynix | Watchlist | 当前无有效反馈 | 找其他渠道确认是否有 32Gb x32 LPDDR5X |

## 4. Daily 相关状态

| 日期 | 状态摘录 | 对寻样问题的影响 |
|---|---|---|
| 2026-05-08 | 完成 LPDDR5 采购寻样整理；美光主候选、三星/南亚/Henry 状态已形成报告 | 供应链侧进入“主线美光 + 三星正式渠道并行确认”的状态 |
| 2026-05-09 | `A38+agilex5方案的 lpddr5 fpga端网络连接好了` | 原理图 FPGA 端网络有进展，但只是 `schematic_connected` |
| 2026-05-09 | LP5 网络数量统计：U0 63、U1 63、总计 126 | 可作为 OrCAD/netlist 核对基线，不是签核证据 |
| 2026-05-09 | 架构评审后：two independent x32 + bank 2A/2B 继续作为主线，但 LPDDR5 原理图扩面暂停 | 继续推进前必须补 Quartus/Fitter/FAE 和封装确认 |
| 2026-05-09 | daily 明确提醒不要把美光 4GB 可评估写成料号已冻结 | 当前只能写 `selected-not-frozen` |

## 5. 必须拆开的三个决策

| 决策 | Owner | 当前状态 | 输出物 |
|---|---|---|---|
| 供应商正式回复 | 采购 | 待美光/WT/WPI、三星正式渠道、Henry/Hynix 补证 | 生命周期、温度等级、价格、lead time、MOQ/MPQ、降频建议、PCN/EOL 机制 |
| 容量是否接受上浮 | 项目 / 罗奇军 | 未确认 | 是否接受 2 颗 4GB x32 导致整板 8GB；成本、功耗、软件地址空间、初始化影响 |
| FPGA/逻辑验证 | 逻辑 / 吴志安 + FAE | 未见 Quartus / Pin Planner / Fitter 输出 | EMIF 配置、QSF、pin report、Fitter report、FAE review 结论 |

这三个决策不能合并成“LPDDR5 已确定”。供应商主候选、项目容量接受、FPGA pin/fitter 可行性是三个独立 gate。

## 6. 当前阻塞

| 阻塞项 | 影响 | 下一步 |
|---|---|---|
| `A5ED065B B32A` 未在本地资料中找到证据 | 无法判断既有 A5EC/A5ED052A pin/bank 假设是否适用 | 确认目标 FPGA 完整 ordering code，并补官方 pinout / package / power / EMIF 资料 |
| 2GB x32 长生命周期料号未找到 | 原始容量需求无法直接满足 | 决策是否接受 4GB x32 主流路线 |
| 美光主候选未获正式商务/生命周期闭环 | 不能冻结 BOM | 采购获取正式回复 |
| LPDDR5X 降频到 3733 MT/s 未经供应商和工具闭环 | 不能冻结时序和 SI 约束 | 要求供应商确认降频使用建议；逻辑跑 EMIF/Fitter |
| 最终封装未冻结 | memory-side ball mapping 可能变化 | 锁定料号/封装后重核 LPDDR5 颗粒侧 ball |
| LPDDR5 pin list 没有 Quartus/Fitter/FAE 证据 | 原理图继续扩面有返工风险 | 暂停扩面，先做 OrCAD 核对 + 最小工程验证 |

## 7. 采购问题清单

### 美光 / WT / WPI

请围绕 `MT62F1G32D2DS-020 WT:D` 要求供应商按表格回复：

| 问题 | 需要的回复格式 |
|---|---|
| 是否为长期主推料号 | Yes/No + roadmap/longevity 说明 |
| 是否支持未来 5-8 年供货 | 年限说明 + PCN/EOL 通知机制 |
| `WT:D` 温度等级和供货等级 | datasheet / ordering guide 截图或链接 |
| 样品、小批量、量产 lead time | 分别给周数 |
| 单价、MOQ、MPQ | 按数量阶梯 |
| 9600 Mb/s 料号是否可长期降频到 3733 MT/s | 原厂建议 + 初始化/ODT/training/SI 注意事项 |
| 是否仍有 2GB / 16Gb x32 长生命周期料号 | 料号 + 生命周期；没有则明确回复 No |

### 三星正式渠道

请不要只问 245FBGA 消费类料号，重点问 315FBGA / x32 / 32Gb LPDDR5X 路线：

| 问题 | 需要的回复格式 |
|---|---|
| 是否有 32Gb x32 315FBGA LPDDR5X 可供 | 料号 + datasheet/package |
| 料号生命周期是否能覆盖 5-8 年 | roadmap/longevity 或 PCN/EOL 机制 |
| 当前是否可供样 | sample lead time |
| 是否有工业级或扩展温度等级 | ordering code + 温度范围 |
| 是否适合 3733 MT/s 降频使用 | 原厂建议 |

## 8. 推荐下一步

1. 先确认 `A5ED065B B32A` 是否是最终目标器件；如果是，建立独立的器件证据包，不能沿用 `A5EC052A/A5ED052A` 的签核口径。
2. 采购继续以美光 `MT62F1G32D2DS-020 WT:D` 为主线拿正式回复，同时并行问三星 315FBGA x32 32Gb 路线。
3. 项目负责人明确是否接受整板 LPDDR 容量从 4GB 上浮到 8GB。
4. 逻辑侧用最终 FPGA 目标型号 + 美光主候选 + 三星并行候选各跑一次最小 Quartus EMIF / Pin Planner / Fitter。
5. 硬件侧保留当前 LPDDR5 网络为工作输入，标注 `schematic_connected / not_signoff / pending_quartus / pending_fae / pending_package_confirm`，不要冻结 pin list。

## 9. Source Links

- `/home/ubuntu/misc-tasks/lpddr5_report_decision.md`
- `/home/ubuntu/misc-tasks/lpddr5_report_procurement.md`
- `/home/ubuntu/misc-tasks/lpddr5_supplier_matrix.csv`
- `/home/ubuntu/my-daily/Daily/raw/2026-05-08/5月8日_extracted/lpddr5 情况群内反馈.md`
- `/home/ubuntu/my-daily/Daily/raw/2026-05-08/5月8日_extracted/lpddr5 情况群内反馈 2.md`
- `/home/ubuntu/my-daily/Daily/raw/2026-05-09/5月9日_extracted/今日完成项.md`
- `/home/ubuntu/my-daily/Daily/raw/2026-05-09/5月9日_extracted/LP5 网络数量统计.md`
- `/home/ubuntu/my-daily/Daily/compiled/2026-05-09/_cyberlog.md`
- `/home/ubuntu/my-daily/Daily/compiled/2026-05-09/_ai-context.md`
