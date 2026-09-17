# p1-data-script

一个天气数据脚本：调公开天气 API，把未来三天的预报整理成表格 —— **打印到屏幕 + 落盘成 CSV / JSON**。

> 「AI 实习计划」阶段 A 的 **P1 项目** —— 目标是跑通「取数 → 处理 → 输出」这条链路。

## 效果

```
$ python weather_first.py

2026-09-17  小毛毛雨  最高 32.8  最低 25.2  降雨概率 69%
2026-09-18  小毛毛雨  最高 33.2  最低 25.4  降雨概率 33%
2026-09-19  小毛毛雨  最高 34.3  最低 25.2  降雨概率 45%
```

同时生成两个文件：

```
out/weather.csv     ← Excel / WPS 直接打开，中文不乱码
out/weather.json    ← 结构化数据，程序可以直接读
```

## 快速开始

```bash
pip install requests
python weather_first.py
```

首次运行会自动创建 `out/` 目录。

## 数据源：Open-Meteo（免 API key）

用的是 [Open-Meteo](https://open-meteo.com/) —— **不用注册、不用申请 key**。

> 最初用的是 wttr.in，后来它的 HTTPS 证书过期了（`CERTIFICATE_VERIFY_FAILED`），于是换成 Open-Meteo。换数据源的过程在 git 历史里。

### 为什么要调两次

因为它的预报接口**只认经纬度，不认城市名**：

```
城市名 "Foshan"
    │
    │  ① 地理编码 API
    ▼
经纬度 23.02677, 113.13148
    │
    │  ② 预报 API
    ▼
三天预报数据
```

| 步骤 | 接口 |
|---|---|
| ① 地理编码 | `geocoding-api.open-meteo.com/v1/search` |
| ② 预报 | `api.open-meteo.com/v1/forecast` |

**顺序不能反** —— 第二步的参数要用第一步的结果。

## 技术点

| 技术点 | 用在哪 |
|---|---|
| `requests` + `timeout` | 调接口 |
| `try / except requests.exceptions.RequestException` | 网络失败给友好提示。**这一个父类能抓到 `Timeout` / `HTTPError` / `JSONDecodeError` 全部** |
| **两步 API 调用** | 后一步依赖前一步的返回值 |
| **嵌套 dict / list 定位字段** | `weather["daily"]["temperature_2m_max"][0]` |
| **字典查表 + `.get()` 防御** | 天气码（数字）→ 中文 |
| `pathlib.Path` + `mkdir(exist_ok=True)` | 保证 `out/` 存在；`Path(__file__).parent` 把路径**锚在脚本目录**，从哪运行都不会跑错地方 |
| **文件写入**（`with open(...)`） | 落盘 |
| `csv.DictWriter` | 写 CSV —— `fieldnames` 决定**列的顺序** |
| `json.dump(..., ensure_ascii=False)` | 写 JSON，中文不转义 |

## ⚠️ 两个文件，两种编码（反直觉，别改错）

| 文件 | 编码 | 为什么 |
|---|---|---|
| `weather.csv` | **`utf-8-sig`** | 带 BOM，**Excel 才知道这是 UTF-8**；不加中文就乱码 |
| `weather.json` | `utf-8` | **JSON 标准不允许 BOM**，加了反而会让某些解析器报错 |

> BOM 是文件开头的 3 个**不可见**字节。在 VS Code 里两个版本看起来一模一样 —— **只有 Excel/WPS 能暴露差别**。

## 天气码为什么要查表

API 返回的是**数字**，不是文字：

```
95  →  雷阵雨
3   →  阴
61  →  小雨
```

映射表是脚本里的 `WMO_ZH` 字典（[WMO 官方码表](https://open-meteo.com/en/docs)，Open-Meteo 用的是这套）。

**查表必须用 `.get(码, "未知")`，不能直接 `WMO_ZH[码]`**：

```python
WMO_ZH[95]                   # → "雷阵雨" ✅
WMO_ZH[77]                   # → KeyError，程序崩溃 ❌（77 不在表里）
WMO_ZH.get(77, "未知")        # → "未知" ✅
```

WMO 码表只定义了 0~99 中的一部分，**API 可能返回没收录的码**。

## 目录结构

```
p1-data-script/
├── weather_first.py      # 天气脚本
└── out/                  # 输出目录（脚本自动创建）
    ├── weather.csv
    └── weather.json
```

## 已完成 / 待办

- [x] 调 API 拿数据
- [x] 两步调用（地理编码 → 预报）
- [x] 解析三天预报的 5 个字段
- [x] 天气码翻译成中文
- [x] 网络失败给友好提示
- [x] **落盘 CSV / JSON**
- [ ] 失败自动重试（现在失败一次就退出）
- [ ] 历史累积 + 趋势对比
- [ ] 城市名支持命令行参数（现在写死在代码里）

## 已知限制

- Open-Meteo 免费版**仅限非商业用途**
- 城市名写死在代码里（`Foshan`），换城市要改代码
- **没有重试机制**，请求失败直接退出
- 每次运行**覆盖**输出文件，还没做历史累积
