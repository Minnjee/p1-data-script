# p1-data-script

一个天气数据脚本：调公开天气 API，把未来三天的预报整理成表格输出。

> 「AI 实习计划」阶段 A 的 **P1 项目** —— 目标是跑通「取数 → 处理 → 输出」这条链路。

## 效果

```
python weather_first.py

2026-09-15  雷阵雨    最高 30.9  最低 24.7  降雨概率 90%
2026-09-16  小阵雨    最高 30.8  最低 24.6  降雨概率 64%
2026-09-17  小毛毛雨  最高 32.0  最低 25.0  降雨概率 13%
```

## 快速开始

```bash
pip install requests
python weather_first.py
```

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
| `try / except requests.exceptions.RequestException` | 网络失败时给友好提示，而不是吐一屏红色报错 |
| **两步 API 调用** | 后一步依赖前一步的返回值 |
| **嵌套 dict / list 定位字段** | `weather["daily"]["temperature_2m_max"][0]` |
| **字典做查表** | 天气码（数字）→ 中文 |
| `dict.get(键, 默认值)` | 查不到的码返回"未知"，不崩溃 |

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
└── weather_first.py      # 天气脚本
```

## 已完成 / 待办

- [x] 调 API 拿数据
- [x] 两步调用（地理编码 → 预报）
- [x] 解析三天预报的 5 个字段
- [x] 天气码翻译成中文
- [x] 网络失败给友好提示
- [ ] 落盘 CSV / JSON
- [ ] 失败自动重试
- [ ] 历史累积 + 趋势对比
- [ ] 城市名支持命令行参数（现在写死在代码里）

## 已知限制

- Open-Meteo 免费版**仅限非商业用途**
- 城市名写死在代码里（`Foshan`），换城市要改代码
- **没有重试机制**，请求失败直接退出
- 目前只输出到屏幕，**还没写文件**
