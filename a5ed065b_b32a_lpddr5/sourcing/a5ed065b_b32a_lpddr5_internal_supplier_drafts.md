# A5ED065B B32A LPDDR5 沟通短稿

## 1. 内部项目群

各位，A5ED065B B32A 方案的 LPDDR5 寻样需求需要确认：

1. FPGA 最终型号是否确定为 `A5ED065B B32A`？
2. 是否接受单颗从 2GB 改为 4GB，即两颗后整板 LPDDR 容量从 4GB 变 8GB？
3. 是否确认只选普通 LPDDR5，不选 LPDDR5X？
4. `16bit die` 是否为硬性要求？请确认准确表达。
5. 短生命周期料号是否可接受？如果接受，必须要求供应商同时提供替代料号、兼容性说明和 PCN/EOL 切换计划。
6. 逻辑侧是否可以基于最终 FPGA 型号 + 候选 LPDDR5 料号跑 Quartus EMIF / Pin Planner / Fitter？

在逻辑验证和替代料确认前，硬件侧不冻结 LPDDR5 pin list。

## 2. 发给代理商/原厂

主题：LPDDR5 颗粒寻样需求更新

Hi <Name>，

请帮忙按以下条件重新推荐 LPDDR5 颗粒：

- 普通 LPDDR5，不选 LPDDR5X
- 单颗 4GB / 32Gb
- 优先 x32 package width
- 需要确认是否为 16bit die / die organization
- 商业级或工业级均可
- 主控：Intel / Altera Agilex 5，当前按 A5ED065B B32A 评估
- 每板暂按 2 颗规划

短生命周期料号可以接受评估，但必须同时提供替代料号，避免后续采购断料风险。

请按表格回复：

| 推荐料号 | LPDDR5/LPDDR5X | 容量 | package width | die organization | 封装 | 温度等级 | 生命周期/EOL 状态 | 替代料号 | 替代料兼容性 | 样品交期 | 量产交期 | MOQ/MPQ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

另外请提供 datasheet、package drawing、ball map、ordering guide。

谢谢。

## 3. 发送注意

- 对外写“当前按 A5ED065B B32A 评估”，不要写最终已定。
- 短生命周期不是一票否决，但没有替代料和切换计划的料号不要作为主推。
- LPDDR5 pin list 等 Quartus / Fitter / FAE 结果后再冻结。
