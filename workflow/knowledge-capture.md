# 知识沉淀策略

> 这份文档定义 `ai_curation` 项目的长期知识沉淀方案。目标不是积累越多越好，而是让 Claude 在长周期项目里以最低上下文成本读到最相关、最稳定、最值钱的知识。

> 本文档只面向 Claude 工作流，不再兼容 Cursor、Codex 或其他环境的额外约束。

## 一、这份文档解决什么问题

随着项目从当前 `crawler` 可行性验证，逐步演进到完整的平台化产品，知识会越来越多：

- 技术选型结论
- 模块边界
- 接口约定
- 真实联调经验
- 解析坑点
- 长期设计决策
- AI 分析与业务计算规则

如果这些内容只停留在会话里，或者散落在大量普通文档里，后续 Claude 很难低成本使用。

因此，知识沉淀体系只做三件事：

1. 帮 Claude 快速路由到正确模块
2. 只在命中时展开最小必要正文
3. 让长期有价值的经验成为 repo 内可维护资产

## 二、核心原则

### 1. 项目知识主库在 repo，不在 mem

本项目会比较大、开发周期也会比较长，因此长期项目知识必须收敛到 repo。

职责分层如下：

- `mem`：用户偏好、协作习惯、阶段性约束
- `.workflow/knowledge/`：项目知识主库
- `.workflow/decisions/`：长期决策记录
- task / plan：当前执行状态

不要把项目主知识库塞进 `mem`。

### 2. 知识加载优先于知识完备

Claude 在当前任务中首先要做到的是：

- 读得少
- 读得准
- 只读当前任务需要的知识

不是把所有知识都装进上下文。

### 3. 先索引，后正文

知识装载统一遵循：

```text
Rule / Routing -> INDEX -> Entry
```

即：

- 路由规则只负责提示去哪里看
- `INDEX.md` 只做一行式摘要索引
- 只有命中某条摘要时，才读对应正文

### 4. 决策、规则、坑点分层管理

不是所有长期内容都应该放进同一类知识文件。

需要区分：

- **Decision**：为什么这么做
- **Rule**：以后默认怎么做
- **Pitfall**：容易踩的坑与识别信号
- **Case**：完整但有保留价值的历史案例

### 5. 当前阶段优先沉淀 `crawler` 高价值知识

项目全貌是平台化产品，但当前阶段默认优先沉淀：

- KP 真实页面联调经验
- 字段稳定性结论
- selector / JSON-LD / 详情页解析规律
- browser fallback 触发条件
- fixture 与真实页面差异

## 三、知识体系结构

推荐结构：

```text
.workflow/
├── knowledge/
│   ├── _project/
│   ├── platform/
│   ├── crawler/
│   ├── analysis/
│   ├── pricing/
│   ├── notification/
│   ├── frontend/
│   ├── infra/
│   ├── multi/
│   └── unknown/
├── decisions/
└── templates/
```

### 模块含义

- `_project`：项目总目标、全局原则、阶段性边界
- `platform`：Java 主平台知识
- `crawler`：Python 爬虫服务知识
- `analysis`：AI 分析与语义处理知识
- `pricing`：税率、利润、比价知识
- `notification`：通知能力知识
- `frontend`：Vue3 前端知识
- `infra`：环境、测试、部署、协作约束
- `multi`：跨模块知识
- `unknown`：模块暂未判定时的兜底入口

## 四、三类长期资产

## 1. Knowledge

放在：

```text
.workflow/knowledge/<module>/
```

适合记录：

- 模块内重复有用的经验
- 坑点
- 稳定规则
- 值得反复引用的案例

## 2. Decision

放在：

```text
.workflow/decisions/
```

适合记录：

- 为什么做出某个长期设计选择
- 为什么当前不做某件事
- 哪个技术方向已被明确否决或收束

例如：

- 为什么平台主干选 Java
- 为什么爬虫能力域独立用 Python
- 为什么当前坚持 HTTP-first
- 为什么现在不做多站点抽象

## 3. 项目事实文档

继续放在现有项目文档中，例如：

- `技术选型讨论结论.md`
- `docs/kp_crawler_plan.md`
- `crawler/README.md`

它们承载的是“当前项目事实”，不替代知识条目和长期决策记录。

## 五、知识条目类型

后续知识条目建议统一为三类：

- `rule`
- `pitfall`
- `case`

### 1. `rule`

适用于：

- 已经非常稳定
- 后续默认都应遵守
- 用短规则就能表达清楚

例如：

- 当前阶段不要提前做多站点抽象
- `crawler` 改动优先补 fixture 或真实联调验证证据

### 2. `pitfall`

适用于：

- 某模块常见坑点
- 需要快速提醒
- 还没稳定到能升级成硬规则

例如：

- KP 某类页面 JSON-LD 缺字段
- 某些字段只在详情页存在
- HTTP 请求成功但核心字段为空时应视为解析失败而不是成功

### 3. `case`

适用于：

- 有完整背景仍然值得保留
- 问题反直觉
- 后续排障可能需要完整上下文

例如：

- 某次 KP 真实联调里，列表页和详情页字段出现冲突，最后如何判定来源优先级

## 六、知识文件命名

统一建议：

- `INDEX.md`
- `w-rule-*.md`
- `w-p-*.md`
- `w-case-*.md`

例如：

```text
.workflow/knowledge/crawler/
├── INDEX.md
├── w-rule-http-first.md
├── w-p-kp-jsonld-missing-fields.md
└── w-case-kp-detail-price-mismatch.md
```

## 七、知识文件最小字段

为了保持简单、可维护，第一版不建议一开始上很复杂的 schema。

建议统一 frontmatter：

```markdown
---
id: w-p-kp-jsonld-missing-fields
type: pitfall
module: crawler
title: KP 页面 JSON-LD 字段缺失
keywords: [kp, jsonld, missing-fields]
summary: 某些 KP 页面 JSON-LD 不包含完整业务字段，不能单独作为成功抓取依据。
updated_at: 2026-04-03
status: active
---
```

正文再写：

- 现象
- 根因
- 判定信号
- 推荐处理方式
- 必要时附相关文件或文档链接

第一版先保持字段最小，后续再考虑工具化校验。

## 八、INDEX 的职责

每个模块下都应有一个 `INDEX.md`，只做轻量路由。

### `INDEX.md` 只回答四个问题

1. 这个模块有哪些重要知识
2. 哪些属于 rule，哪些属于 pitfall，哪些属于 case
3. 哪些信号命中时值得展开正文
4. 先读哪一条最划算

### 格式要求

- 一行一条
- 不写长解释
- 最多 10-20 条
- 超过上限就拆分目录或上提规则

### 示例

```text
- w-rule-http-first | 类型: rule | 适用: crawler 当前阶段 | 说明: 先 HTTP，再决定是否补 browser fallback
- w-p-kp-jsonld-missing-fields | 类型: pitfall | 信号: JSON-LD 缺少价格/卖家/时间字段 | 优先级: 高
- w-case-kp-detail-price-mismatch | 类型: case | 信号: 列表页与详情页价格冲突 | 优先级: 中
```

## 九、什么值得沉淀

不是所有问题都值得进入知识库。

满足任一条，就值得考虑沉淀：

- 根因反直觉
- 定位成本高
- 下次再遇到仍然容易踩坑
- 会跨人、跨任务重复出现
- 会影响架构或长期做法

### 对当前 `crawler` 阶段，优先沉淀这些

#### 1. 字段稳定性

- 哪些字段能稳定抓到
- 哪些字段经常拿不到
- 空值的真实原因是什么

#### 2. 页面解析规律

- 哪些字段来自列表页
- 哪些字段来自详情页
- 哪些字段来自 JSON-LD
- 哪些字段必须浏览器兜底

#### 3. 真实联调经验

- 某类 URL 的抓取结果是否稳定
- 哪些页面容易被反爬或返回异常结构
- 哪些 header / cookie / 节流策略会影响结果

#### 4. fixture 与真实页面差异

- 现有 fixture 缺了哪些真实页面特征
- 哪些测试通过但真实页面会失败

#### 5. 长期架构边界

- 当前为什么不做多站点抽象
- 当前为什么不做自动登录
- 当前为什么先只输出 raw JSON

## 十、什么不值得沉淀

以下内容通常不要写入长期知识库：

- 当前任务的临时状态
- 某次会话里的临时 todo
- 明显可从代码直接看出的事实
- 单次、低价值、无复用意义的问题
- 会很快失效、又没有历史价值的碎片信息

## 十一、什么时候沉淀

沉淀动作通常发生在收口阶段，但判断可以在整个过程中提前进行。

### 与工作流节点的关系

- `w-explore`：先读索引，判断是否已有相关知识
- `w-implement`：遇到反直觉问题时标记候选条目
- `w-review`：发现模式性问题时标记候选条目
- `w-verify`：补充验证证据，决定是否值得沉淀
- `w-capture`：最终写入长期知识

## 十二、案例上提原则

后续应尽量推动：

```text
case -> pitfall -> rule
```

意思是：

- 如果一个案例反复证明稳定，就不必每次都展开完整历史
- 如果一个坑点已经足够确定，就可以升级成 rule
- 目标不是保留更多文档，而是让后续上下文越来越短

## 十三、token 控制规则

知识库必须优先控制 token。

至少遵守这些规则：

- 默认先读 `.workflow/knowledge/_project/INDEX.md`
- 默认只读索引，不读正文
- 一次最多展开一个主要模块
- 跨模块任务先读 `multi/INDEX.md`
- 模块不明确时先读 `unknown/INDEX.md`
- 没命中信号，不展开 case 正文
- 同类 case 一次最多展开 1-2 篇

## 十四、Decision 的写法建议

对于长期影响大的结论，不要硬塞进 pitfall 或 case，应该单独写 decision 文档。

例如：

```text
.workflow/decisions/
├── adr-001-java-as-platform-backbone.md
├── adr-002-python-crawler-service.md
├── adr-003-http-callback-first.md
└── adr-004-no-multi-site-abstraction-yet.md
```

每份 decision 至少回答：

- 做了什么决定
- 为什么做这个决定
- 当前适用边界是什么
- 后续在什么条件下可能重审

## 十五、当前阶段的最小落地建议

如果现在开始建设知识库，不需要一步到位。

建议第一批先做：

```text
.workflow/knowledge/
├── _project/INDEX.md
├── crawler/INDEX.md
└── decisions/
```

### 第一批优先内容

#### `_project/INDEX.md`

写：

- 当前项目是平台化产品
- 当前阶段默认优先 `crawler`
- 当前不做多站点抽象
- 当前主链路是 HTTP-first

#### `crawler/INDEX.md`

写：

- KP 真实联调相关入口
- 字段稳定性相关入口
- fixture 差异相关入口
- browser fallback 判定入口

#### `decisions/`

至少先沉淀这些长期结论：

- 平台主干选 Java
- 爬虫能力域选 Python
- 服务协作采用 HTTP + 回调，轮询兜底
- 当前阶段不提前做多站点抽象

## 十六、最终原则

这套知识沉淀策略的核心不是“积累很多文档”，而是：

- 让 Claude 在未来长对话、长周期开发中仍然读得准
- 让项目真正重要的经验留在 repo 里
- 让长期决策与短期执行分层清楚
- 让知识库服务项目，而不是反过来拖累项目
