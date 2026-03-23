# KP 爬虫实施记录

## 当前目标

当前项目被拆成 3 部分：

1. AI 分析商品需求
2. 爬虫
3. AI 分析爬虫结果

当前优先做第 2 部分，且只做 `KP(kupujemprodajem)` 单站点的可行性验证。

## 已确认的范围

- 只做 `KP`，不接入 `Alza`、`MediaMarkt`、国内平台或 RSS。
- 爬虫单独放在 `crawler/` 目录。
- 形态是独立 HTTP 服务，不是纯脚本。
- 抓取策略是 `HTTP 优先`，失败或字段不足时再切浏览器。
- 当前阶段只输出原始 JSON，不做 AI 分析、不做写表、不做标准化。
- 首期重点是 `先快为主，先验证可行性`，不要提前做多站点抽象。
- `auth_profile` 只预留 Cookie/Header 注入能力，不做自动登录和验证码处理。
- KP 首期入口按业务要求走 `指定类目榜单页`，由调用方传入 `seed_url`。
- 验收字段尽量接近最终业务字段，允许部分字段为空，但必须有明确错误或空值来源说明。

## HTTP API 约定

接口：

- `POST /jobs/kp/crawl`
- `GET /healthz`

请求体：

```json
{
  "seed_url": "https://www.kupujemprodajem.com/mobilni-telefoni",
  "category_name": "手机",
  "page_limit": 1,
  "include_detail": true,
  "auth_profile": "kp-default"
}
```

返回体结构：

- `job_meta`
- `items`
- `errors`
- `artifacts`

每条 `item` 当前目标字段：

- `source_url`
- `title`
- `price_raw`
- `currency`
- `image_urls`
- `category_raw`
- `rank_in_page`
- `listing_id`
- `seller_name`
- `view_count`
- `favorite_count`
- `posted_at_raw`
- `scraped_at`
- `raw_payload_ref`

## 当前实现状态

已实现代码位置：

- `crawler/pyproject.toml`
- `crawler/README.md`
- `crawler/src/kp_crawler/`
- `crawler/tests/`

当前已完成内容：

- HTTP 服务骨架
- KP 抓取服务编排
- 请求参数校验
- 原始响应和结果 JSON 落盘
- 认证配置预留
- 列表页解析
- 详情页增强解析
- HTTP 失败时标记 `browser_fallback_required`
- 基于 fixture 的单元测试

启动方式：

```bash
cd crawler
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
kp-crawler serve --host 127.0.0.1 --port 8080
```

测试命令：

```bash
cd crawler
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## 文件落盘约定

原始数据默认保存在：

```text
crawler/data/runs/kp/YYYY-MM-DD/<job_id>/
```

当前会生成：

- `request.json`
- `result.json`
- `list_page_*.json`
- `detail_*.json`
- `html/*.html`

## 下一步优先事项

1. 用真实 KP 类目 URL 进行联调，确认当前 HTML 选择器和 JSON-LD 解析是否适配真实页面。
2. 记录真实抓取结果中哪些字段能稳定拿到，哪些字段拿不到。
3. 如果 HTTP 方案拿不到关键字段或被反爬拦截，再补浏览器兜底方案。
4. 补真实页面样本 fixture，避免后续改动把解析逻辑改坏。
5. 再决定是否需要抽象多站点路由和统一抓取框架。

## 当前已知限制

- 还没有对真实 KP 页面做在线联调。
- 还没有实现浏览器兜底。
- 还没有自动登录。
- 还没有代理配置、限速策略细化和更强的反爬处理。
- 还没有把结果写入外部系统。

## 工作区状态提醒

当前仓库除了新增的 `crawler/` 之外，还有一个既有未提交修改：

- `docs/select/实施前清单_对接版.docx`

后续提交时不要误覆盖或误回滚这个文件。
