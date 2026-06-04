# Stock Analysis Project（金融数据分析大作业）

基于 **Python / Pandas / NumPy** 对四只标的近两年日线数据进行分析：

| 代码 | 说明 |
|------|------|
| GOOGL | 谷歌 |
| AVGO | 博通 |
| SLV | iShares 白银 ETF |
| NVDA | 英伟达 |

## 项目结构

```
financial-analysis/
├── data/
│   ├── raw/              # 各标的原始 CSV（运行后生成）
│   └── processed/        # 清洗后的收盘价宽表 prices_wide.csv
├── notebooks/
│   └── main.ipynb        # 主分析报告（作业提交用）
├── src/
│   ├── data_fetch.py     # 数据采集与清洗
│   ├── analysis.py       # 收益、滚动、相关性、重采样
│   ├── utils.py          # NumPy 统计工具函数
│   ├── plotting.py       # 图表生成
│   └── config.py         # 常量配置
├── images/               # 导出的图表 PNG
├── main.py               # 一键运行全流程
├── requirements.txt
└── README.md
```

## 环境准备

```powershell
cd C:\Users\ltz\Projects\financial-analysis
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
python -m ipykernel install --user --name financial-analysis --display-name "Python (financial-analysis)"
```

## 运行方式

**方式一：命令行一键运行（下载数据 + 分析 + 出图）**

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

若出现 **yfinance 限流**（`Too Many Requests`），可先用演示数据跑通流程：

```powershell
python main.py --demo
```

稍后再去掉 `--demo` 重新下载真实行情。

**方式二：Jupyter Notebook（含 Markdown 结论）**

```powershell
code notebooks/main.ipynb
# 或
python -m jupyter lab notebooks/main.ipynb
```

在 VS Code 中选择内核 **Python (financial-analysis)**，从上到下运行所有单元格。

**仅重新下载数据：**

```powershell
python -m src.data_fetch
```

## 作业对应关系

| 步骤 | 内容 | 主要代码 |
|------|------|----------|
| 1 | 采集、清洗、`merge` 宽表 | `src/data_fetch.py` |
| 2 | 收益率、NumPy 向量化统计 | `src/analysis.py`, `src/utils.py` |
| 3 | 滚动均线/波动率、`corr`、`groupby`、`resample` | `src/analysis.py` |
| 4 | Notebook 报告 + 图表 + GitHub | `notebooks/main.ipynb`, `images/` |

## 推送到 GitHub

```powershell
gh auth login
gh repo create financial-analysis --private --source=. --remote=origin --push
```

## 依赖

见 [requirements.txt](requirements.txt)。核心：`yfinance`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `jupyter`。
