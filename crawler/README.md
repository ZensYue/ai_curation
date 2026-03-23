# KP Crawler

`crawler/` 是独立的 KP 可行性验证子项目。

当前能力：

- `POST /jobs/kp/crawl`
- HTTP 优先抓取
- 原始响应与解析结果落盘
- 预留 `auth_profile` 注入 Cookie/Header
- 当 HTTP 抓取失败或解析为空时，明确返回 `browser_fallback_required`

## 启动

```bash
cd crawler
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
kp-crawler serve --host 127.0.0.1 --port 8080
```

## 请求示例

```bash
curl -X POST http://127.0.0.1:8080/jobs/kp/crawl \
  -H 'Content-Type: application/json' \
  -d '{
    "seed_url": "https://www.kupujemprodajem.com/mobilni-telefoni",
    "category_name": "手机",
    "page_limit": 1,
    "include_detail": true
  }'
```

## 认证配置

可选的认证配置文件路径：

- `crawler/config/auth_profiles.json`
- 或环境变量 `KP_CRAWLER_AUTH_FILE`

格式：

```json
{
  "profiles": {
    "kp-default": {
      "headers": {
        "x-example-header": "value"
      },
      "cookies": {
        "sessionid": "abc"
      }
    }
  }
}
```

## 落盘结构

原始文件默认保存在 `crawler/data/runs/kp/YYYY-MM-DD/<job_id>/`。

会包含：

- `request.json`
- `result.json`
- `list_page_*.json`
- `detail_*.json`
- `html/*.html` 或 `html/*.json`

## 测试

```bash
cd crawler
python3 -m unittest discover -s tests -v
```
