# Label Loom

[English](README.md) | 中文

**Label Loom 是一个完全离线的命令行工具：在标注预算有限时，为文本分类任务推荐下一批最值得标注的样本。** 它将模型不确定性、样本多样性和预测类别均衡结合起来，输出可审核的标注清单和轮次成本记录。当前版本：**v0.1.0**。

![Label Loom 实际演示导出](docs/demo-output.svg)

- 完全本地运行：使用 TF-IDF 与 scikit-learn 逻辑回归，不调用网络服务。
- 可选不确定性、多样性或混合策略；相同输入稳定复现。
- 导出 CSV/JSON，并记录策略、批量、时间与成本，便于审计。

## 最快开始

```bash
python -m pip install -e '.[dev]'
label-loom recommend examples/demo_pool.csv --output recommendations.csv --ledger annotation-rounds.json --strategy hybrid --budget 6 --batch-size 6
```

输入 CSV 需要 `text` 列，可选 `id` 列；空 `label` 代表待标注池。工具仅从空标签行中选择样本。完整参数与真实输入输出示例见 [English README](README.md#cli)。

## 使用流程

1. 导入 UTF-8 CSV，已有标签的行用于训练，至少覆盖两个类别。
2. 选择 `uncertainty`、`diversity` 或 `hybrid` 策略，并设置预算与批量大小。
3. 将导出的清单交给标注人员；完成后把标签写回源 CSV，再开始下一轮。
4. 通过 JSON 轮次记录追踪已选数量、单位成本、总成本与导出位置。

随仓库提交的 [样例](examples/demo_pool.csv) 为合成客服文本，覆盖 billing、access、payment、technical、security 五类，不含个人或生产数据。项目边界、测试、隐私、安全与贡献说明分别见 [架构](docs/ARCHITECTURE.md)、[隐私与安全](docs/PRIVACY_AND_SECURITY.md)、[CONTRIBUTING](CONTRIBUTING.md) 和 [SECURITY](SECURITY.md)。

## 差异化

公开仓库抽样检索未发现同名且高度同构的活跃项目。相较 modAL、ALiPy、BaaL 等通用框架，Label Loom 聚焦本地 CSV、可审核导出、轮次成本记录与轻量 sklearn 基线，适合小团队和外包标注负责人。

MIT 许可证，见 [LICENSE](LICENSE)。
