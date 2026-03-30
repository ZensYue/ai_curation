# AI Curation (AI 选品) Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 初始化基于 OpenSpec 和 Superpowers 的“AI 选品” Agent Team 基础配置文件和目录结构。

**Architecture:** 混合领域驱动架构。`.openspec` 存放规范，`scripts/agents` 存放初期验证的 Python 代码。

**Tech Stack:** Markdown (OpenSpec 格式), Bash (用于创建结构)

---

### Task 1: 初始化全局团队配置 (team.md)

**Files:**
- Create: `.openspec/team.md`

- [ ] **Step 1: 验证文件不存在**

Run: `ls .openspec/team.md`
Expected: `No such file or directory` (或者文件未创建)

- [ ] **Step 2: 写入 team.md**

```markdown
# Agent Team: AI 选品 (AI Curation)

## 1. 团队目标 (Team Goal)
实现从各大电商平台及内容平台的信息中，自动挖掘、分析并推荐具有高潜力的商品。

## 2. 角色与职责 (Roles & Responsibilities)
- **Scraper Agent (信息采集器)**: 负责定向或泛化抓取商品基础信息、用户评价和价格趋势。
- **Analysis Agent (数据分析师)**: 负责对采集到的非结构化数据进行情感分析、优劣势提取和卖点总结。
- **Decision Agent (决策推荐官)**: [待定] 基于分析结果和特定场景（如送礼、性价比）输出最终推荐。

## 3. 通信协议 (Communication Protocol)
- **上下文传递**: 采用标准化 JSON 格式进行数据流转。
- **共享状态**: 团队共享一个虚拟的“选品池 (Curation Pool)”，各 Agent 在不同阶段对其进行读写。

## 4. 全局错误处理 (Global Error Handling)
- **采集失败**: 如果 Scraper Agent 遇到反爬或解析错误，需上报 `ScrapeError`，Team 可选择跳过该商品或使用历史缓存。
- **分析超时**: 如果 Analysis Agent 响应超时，进行最多 3 次指数退避重试，失败则标记商品状态为 `analysis_failed`。
```

- [ ] **Step 3: 验证内容已写入**

Run: `cat .openspec/team.md`
Expected: 包含上述 Markdown 内容。

- [ ] **Step 4: Commit**

```bash
git add .openspec/team.md
git commit -m "chore: add agent team workflow definition"
```

### Task 2: 初始化基础 Agent 规范 (base_agent.md)

**Files:**
- Create: `.openspec/agents/base_agent.md`

- [ ] **Step 1: 创建目录并写入 base_agent.md**

```bash
mkdir -p .openspec/agents
```

写入以下内容到 `.openspec/agents/base_agent.md`:
```markdown
# Base Agent 规范

> 这是所有 AI 选品 Team 成员的基础设定，所有子 Agent 都隐式继承本规范。

## 1. 核心人设与纪律 (Core Persona & Discipline)
- 你是 AI 选品团队的专业成员，必须严格遵守 JSON 格式输出的要求。
- 不捏造数据：如果获取不到信息，必须明确返回 `null` 或抛出指定错误，禁止大模型幻觉编造评价或销量。

## 2. 标准输入输出 (Standard I/O)
所有 Agent 的最终结果必须包装在标准响应信封中：
```json
{
  "status": "success | error",
  "agent_name": "...",
  "data": {},
  "error_message": null
}
```

## 3. 日志与追踪 (Logging & Tracing)
- 所有关键步骤必须记录日志（在验证阶段可通过 Python 的 `logging` 模块）。
- 每次处理商品必须携带唯一的 `item_id` 或 `task_id` 以便全链路追踪。
```

- [ ] **Step 2: 验证文件存在**

Run: `ls -l .openspec/agents/base_agent.md`
Expected: 文件存在且非空。

- [ ] **Step 3: Commit**

```bash
git add .openspec/agents/base_agent.md
git commit -m "chore: add base agent specification"
```

### Task 3: 初始化具体业务 Agent 模板 (scraper & analysis)

**Files:**
- Create: `.openspec/agents/scraper_agent.md`
- Create: `.openspec/agents/analysis_agent.md`

- [ ] **Step 1: 写入 scraper_agent.md**

写入内容到 `.openspec/agents/scraper_agent.md`:
```markdown
# Scraper Agent (信息采集器)

## 1. Role (角色)
你是一个专业的数据采集专家，负责从指定 URL 或平台接口获取商品详情、价格变动和用户评价。你需要绕过简单的反爬机制（合法范围内）并清理 HTML 杂质。

## 2. Input/Output (输入/输出)
**Input (JSON)**:
```json
{
  "task_id": "req-123",
  "url": "https://example.com/product/1",
  "platform": "example_mall"
}
```

**Output (JSON)**:
```json
{
  "item_id": "prod-abc",
  "title": "...",
  "price": 199.0,
  "raw_reviews": ["...", "..."]
}
```

## 3. Tools (可用工具)
- `fetch_html(url)`: 获取网页源码
- `extract_json_from_script(html)`: 从页面内联脚本提取结构化数据

## 4. Validation (验证标准)
- [ ] 能够成功提取标题和价格
- [ ] 当页面 404 时能正确返回 error 状态
```

- [ ] **Step 2: 写入 analysis_agent.md**

写入内容到 `.openspec/agents/analysis_agent.md`:
```markdown
# Analysis Agent (数据分析师)

## 1. Role (角色)
你是一个犀利的商品分析师。擅长从杂乱的用户评论和商品参数中，提取出真正的“核心卖点”和“致命缺点”，并给出客观评分。

## 2. Input/Output (输入/输出)
**Input (来自 Scraper Agent 的 Output)**:
```json
{
  "item_id": "prod-abc",
  "title": "...",
  "price": 199.0,
  "raw_reviews": ["非常好用", "发热太严重了", "性价比高"]
}
```

**Output (JSON)**:
```json
{
  "item_id": "prod-abc",
  "sentiment_score": 8.5,
  "pros": ["好用", "性价比高"],
  "cons": ["发热严重"],
  "buy_recommendation": "推荐购买，但需注意散热"
}
```

## 3. Tools (可用工具)
- `llm_sentiment_analysis(text)`: 调用大模型进行细粒度情感分析

## 4. Validation (验证标准)
- [ ] 必须输出明确的优缺点数组
- [ ] `sentiment_score` 必须在 0-10 之间
```

- [ ] **Step 3: 验证文件存在**

Run: `ls .openspec/agents/scraper_agent.md .openspec/agents/analysis_agent.md`
Expected: 两个文件均显示存在。

- [ ] **Step 4: Commit**

```bash
git add .openspec/agents/scraper_agent.md .openspec/agents/analysis_agent.md
git commit -m "chore: add specific agent templates"
```

### Task 4: 初始化辅助目录

**Files:**
- Create Directory: `.openspec/prompts/meta_prompts/`
- Create Directory: `scripts/agents/`

- [ ] **Step 1: 创建目录**

```bash
mkdir -p .openspec/prompts/meta_prompts
mkdir -p scripts/agents
touch .openspec/prompts/meta_prompts/.keep
touch scripts/agents/.keep
```

- [ ] **Step 2: 验证目录存在**

Run: `ls -la .openspec/prompts/meta_prompts/.keep scripts/agents/.keep`
Expected: 文件存在。

- [ ] **Step 3: Commit**

```bash
git add .openspec/prompts/meta_prompts/.keep scripts/agents/.keep
git commit -m "chore: initialize auxiliary directories for agent workflow"
```
