# p1-data-script

Python 数据处理脚本练习：**抓天气 → 输出 CSV / JSON**。

> 目标：跑通「取数 → 处理 → 输出」这条完整链路，练 `requests` / `json` / `csv` / 文件读写 / 异常处理。
> 待办：加超时与重试、加历史累积与趋势对比。

## 效果

```
python weather.py

【Foshan】当前 07:54 AM
  多云  33°C（体感 35°C）  湿度 43%  NNE风 17km/h

日期        星期  天气        最高    最低    降雨
2026-09-12  周六  晴         33°   24°   12%
2026-09-13  周日  阵雨       32°   26°   74%
2026-09-14  周一  阵雨       31°   25°   75%
```

## 快速开始

```bash
pip install requests
python weather.py            # 抓天气（默认佛山）
python weather.py Shenzhen   # 换城市（用英文城市名）
python weather.py --selftest # 自检解析逻辑，不联网
```

## 脚本做什么

- 数据源：[wttr.in](https://wttr.in)——免费、**不需要 API key**、直接返回 JSON
- 解析当前天气：温度、体感、湿度、天气、风向风速
- 解析未来 3 天预报：最高/最低/平均温、降雨概率、代表天气、日出日落
- 天气代码（WWO）翻译成中文；代表天气用 `Counter` 取当天出现次数最多的那个
- 输出：
  - `out/weather.csv`（utf-8-sig，Excel 直接打开不乱码）
  - `out/weather.json`（`ensure_ascii=False`，中文不转义）

## 技术点

| 技术点 | 用在哪 |
|---|---|
| `requests` + `timeout` + `raise_for_status` | 调接口，超时和错误码要显式处理 |
| 嵌套 dict/list 定位字段 | 从原始 JSON 里取出想要的值 |
| `csv.DictWriter` | 写 CSV |
| `json.dump(ensure_ascii=False)` | 中文 JSON 不乱码 |
| `datetime.strptime` | 日期 → 星期几 |
| `collections.Counter` | 统计当天出现最多的天气 |
| `assert` 自检 | `--selftest`，不用测试框架也能验证解析逻辑 |

## 目录结构

```
p1-data-script/
├── weather.py          # 天气脚本
└── out/                # 输出结果（脚本自动创建）
```

## 已知限制

- wttr.in 是免费公共接口，偶尔会慢或返回 502；脚本已设 15s 超时
- 城市名要用英文（`Foshan` / `Shenzhen`），中文名不稳定
- 目前**没有重试机制**，网络失败会直接抛异常（待办）
