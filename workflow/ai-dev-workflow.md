# Claude 开发工作流

> 这份文档定义 `ai_curation` 项目的 Claude-only 工作流。目标不是把流程做重，而是在长周期、大项目里保持实现效率、验证质量和知识收口。

> 当前项目按平台化产品建设，但现阶段默认优先服务 `crawler` 能力域的可行性验证。

## 一、适用范围

本工作流面向整个 `ai_curation` 项目，而不只面向当前的 KP 爬虫子项目。

当前已确认的项目全貌：

- 前端：`Vue3`
- 主平台后端：`Java + Spring Boot`
- 爬虫能力域：`Python` 独立服务
- 服务协作：`HTTP + 回调`
- 状态补偿：`轮询`
- 后续能力：AI 分析、比价与利润计算、通知模块、营销能力

因此，这份工作流既要适配当前 `crawler/` 阶段，也要能支撑后续 `platform / analysis / notification / frontend` 的长期演进。

## 二、设计目标

这套工作流只解决四件事：

1. 让小改动不被流程拖慢
2. 让中大改动有明确的探索、计划、实现、验证闭环
3. 让长期知识不会只停留在会话里
4. 让 Claude、Superpowers、mem 的职责边界清楚

## 三、核心原则

### 1. 流程不能比业务重

不是所有改动都值得进入完整链路。

- 小修小补应快速完成
- 常规功能改动应有最小闭环
- 跨模块或高不确定性任务才进入完整流程

### 2. 当前阶段优先服务 `crawler`

虽然项目全貌是平台化产品，但当前阶段的主线仍然是：

- 先完成 KP 单站点可行性验证
- 先验证真实抓取与字段稳定性
- 先确认是否需要浏览器兜底
- 不提前做多站点抽象

因此工作流默认优先适配 `crawler/` 的开发节奏，而不是先为未来多模块系统做过度治理。

### 3. 先验证可行性，再抽象

当前阶段不追求过早抽象。

- 不为了未来多平台而提前做复杂框架
- 不为了流程完整而引入大而全制品链
- 真实联调、fixture 回归、字段稳定性记录，优先级高于纸面设计

### 4. 验证必须真实

对本项目来说，`w-verify` 不是形式步骤。

优先验证：

- 真实请求联调
- fixture 回归
- 结果落盘检查
- 关键字段覆盖度与缺失原因记录
- 接口契约与回调链路检查

缺少验证证据时，不能声称任务已经完整完成。

### 5. 项目记忆不能只靠 mem

这个项目会比较大、周期也会比较长，因此长期记忆必须分层：

- `mem`：用户偏好、协作习惯、阶段性约束
- repo 文档 / `.workflow/knowledge/`：项目知识主库
- task / plan：当前执行状态

`mem` 继续使用，但不承担项目主知识库职责。

## 四、模块划分

工作流与知识路由统一按以下模块理解：

- `_project`
- `platform`
- `crawler`
- `analysis`
- `pricing`
- `notification`
- `frontend`
- `infra`
- `multi`
- `unknown`

### 模块含义

- `_project`：项目总目标、阶段性约束、跨模块共识
- `platform`：Java 主平台，账号、权限、任务、业务流转
- `crawler`：Python 爬虫服务、adapter、解析、回调、落盘
- `analysis`：AI 润色、结果分析、语义处理
- `pricing`：税率、利润、比价计算逻辑
- `notification`：飞书、钉钉、统一通知模块
- `frontend`：Vue3 Web 端
- `infra`：环境、配置、脚本、测试、部署
- `multi`：跨两个及以上模块的任务
- `unknown`：暂时无法判定模块时的兜底入口

## 五、工作流分级

### 总览

| 改动规模 | 档位 | 典型场景 | 默认流程 |
|------|------|------|------|
| 极小改动 | `w-direct` | 文案、小修、确定性局部修补 | read -> edit -> verify |
| 轻量改动 | `w-lite` | 简单 bug、解析调整、fixture 修补、局部行为修正 | explore -> implement -> verify -> close |
| 常规改动 | `w-standard` | 新增明确能力、结构性演进、模块内中等改动 | start -> explore -> plan -> implement -> verify -> close |
| 大型改动 | `w-full` | 跨模块、架构调整、高不确定性、多 agent 协作 | start -> explore -> plan -> implement -> review -> verify -> close -> capture |

### 1. `w-direct`

适用场景：

- 一行修复
- 文档小改
- 配置微调
- 局部确定性修补
- 明确不需要方案选择、任务拆分、额外设计说明

特点：

- 不进入完整流程主链
- 不强制计划
- 不强制知识沉淀
- 如果影响长期规则，再补文档或知识记录

### 2. `w-lite`

适用场景：

- 简单 bug 修复
- KP 解析 selector 调整
- fixture 更新
- 小范围接口或参数修正
- 范围明确、但已不属于纯实现修补

默认流程：

```text
w-explore -> w-implement -> w-verify -> w-close
```

特点：

- 不强制计划模式
- 以最小闭环完成任务
- 当前 `crawler/` 阶段会高频使用
- 如变更影响约定或对外行为，需要同步相关文档

### 3. `w-standard`

适用场景：

- 新增明确能力
- 浏览器兜底接入
- 代理 / 限速策略接入
- 平台模块内边界清晰的能力演进
- 需要明确计划与验证点

默认流程：

```text
w-start
-> w-explore
-> w-plan
-> w-implement
-> w-verify
-> w-close
```

特点：

- 需要显式计划
- 需要任务拆分
- 需要完整验证
- 必要时更新相关项目文档或知识索引

### 4. `w-full`

适用场景：

- 跨 `platform / crawler / analysis / notification / frontend` 的改动
- 架构调整
- 回调链路、任务流转等高不确定性任务
- 需要方案比较
- 需要并行 agent 或完整知识沉淀

默认流程：

```text
w-start
-> w-explore
-> w-plan
-> w-implement
-> w-review
-> w-verify
-> w-close
-> w-capture
```

特点：

- 需要显式 review
- 可以启用并行 agent
- 应执行完整知识沉淀
- 适合长期架构性任务，而不是当前日常默认路径

## 六、档位判断规则

### 进入 `w-direct`

必须同时满足：

- 改动边界极小
- 不改变外部约定
- 不需要方案比较
- 不需要任务拆分

### 进入 `w-lite`

通常满足：

- 行为层有局部变化
- 范围可控
- 不需要完整计划
- 不需要跨模块协作

### 进入 `w-standard`

通常满足：

- 需要计划和验证点
- 涉及模块内能力演进
- 不是一两处局部修补
- 但复杂度尚未高到需要并行 agent

### 进入 `w-full`

满足任一条就应优先考虑：

- 涉及多个模块
- 需求不稳定
- 需要方案比较
- 需要并行 agent
- 需要完整知识沉淀

### 显式指定

用户可直接指定：

- `[w:direct]`
- `[w:lite]`
- `[w:standard]`
- `[w:full]`

显式指定后，优先按指定档位执行。

## 七、节点定义

### `w-start`

职责：

- 判断本次任务属于哪个档位
- 判断模块归属
- 决定是否进入完整流程
- 检查是否存在需要优先关注的历史决策或知识索引

### `w-explore`

职责：

- 只读探索需求、代码、现有文档、知识索引
- 明确模块归属、边界、风险点
- 建立最小必要上下文

对当前项目尤其重要的是：

- 先读 `docs/kp_crawler_plan.md`、`技术选型讨论结论.md` 等项目事实文档
- 再决定是否需要深入某个模块知识条目

### `w-plan`

职责：

- 把目标拆成可执行任务
- 明确顺序、依赖、验证点
- 只服务于 `w-standard / w-full`

### `w-implement`

职责：

- 实现改动
- 控制上下文范围
- 不做与当前目标无关的额外重构

### `w-review`

职责：

- 对实现做显式审核
- 检查边界是否偏移
- 对跨模块、高风险、长期影响改动进行额外把关

### `w-verify`

职责：

- 用当前条件下最有价值的方式验证改动
- 明确哪些已验证、哪些只能降级验证

本项目推荐验证层次：

1. 单元 / fixture 测试
2. 本地运行与接口验证
3. 真实页面 / 真实数据联调
4. 回调、轮询、任务状态链路检查
5. 文档与实现一致性检查

### `w-close`

职责：

- 收口本轮任务
- 确认验证证据存在
- 确认是否需要同步文档
- 确认是否需要补知识沉淀

### `w-capture`

职责：

- 只在经验确实有长期价值时沉淀知识
- 决定写入 rule、pitfall、case 还是 decision
- 不把临时状态写进长期知识

## 八、Superpowers 的定位

Superpowers 在本项目中是“方法论增强层”，不是主流程本身。

也就是说：

- 主控仍然是 `w-*`
- Superpowers 只在需要时挂到节点内部使用

### 推荐映射

- `w-explore`：`brainstorming`、`systematic-debugging`
- `w-plan`：`writing-plans`
- `w-implement`：`executing-plans`
- `w-verify`：`verification-before-completion`
- `w-full` 的实现阶段：必要时使用 `subagent-driven-development`

### 使用原则

- 默认不强制每个节点都调用 Superpowers
- `w-lite` 通常只在复杂排障时使用
- `w-standard` 可选使用，用于提升计划与验证质量
- `w-full` 才应积极使用并行 agent 与方法论技能

## 九、mem 的定位

`mem` 继续保留，但只承担“协作记忆层”。

适合写入 `mem` 的内容：

- 用户偏好
- 协作习惯
- 长期有效的阶段性约束
- 反复确认过的做事方式

不适合写入 `mem` 的内容：

- 详细项目知识
- 频繁变化的技术事实
- 当前任务执行状态
- 需要版本审计的设计结论

一句话总结：

```text
mem = 协作记忆
repo knowledge = 项目记忆
task / plan = 执行记忆
```

## 十、文档与知识的职责边界

### 1. 项目事实文档

继续保留在现有文档中，例如：

- `技术选型讨论结论.md`
- `docs/kp_crawler_plan.md`
- `crawler/README.md`

它们负责承载：

- 真实项目范围
- 技术选型结论
- API 约定
- 当前阶段实现状态

### 2. `.workflow/knowledge/`

负责承载：

- 可重复使用的模块知识
- 坑点、案例、规则
- 跨会话、跨任务仍然有价值的经验

### 3. `mem`

负责承载：

- Claude 与用户的长期协作背景

### 4. task / plan

负责承载：

- 当前会话里的执行状态
- 任务拆分与推进顺序

## 十一、推荐目录方向

后续如果正式落地工作流资产，建议以 Claude 为中心逐步建设：

```text
.workflow/
├── flow/
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
├── templates/
└── config.md
```

其中：

- `flow/`：流程说明
- `knowledge/`：知识索引与条目
- `decisions/`：长期决策记录，适合 ADR 风格
- `templates/`：知识条目、决策、状态摘要模板
- `config.md`：模块候选值、敏感模块等集中配置

## 十二、当前阶段的默认路由建议

结合当前仓库现状，默认这样理解：

### `crawler` 当前常见任务

- selector、fixture、参数、落盘细调：`w-lite`
- 浏览器兜底、代理/限速、抓取链路增强：`w-standard`
- `crawler + platform` 回调链路、任务流转改造：`w-full`

### `platform` 未来常见任务

- 局部接口、小模块修正：`w-lite`
- 账号、权限、任务模块新增能力：`w-standard`
- 平台与爬虫、通知、分析的跨域协作：`w-full`

## 十三、路由摘要格式

当显式进入工作流时，推荐输出一行路由摘要：

```text
[w:lite] crawler -> explore -> implement -> verify -> close
```

例如：

```text
[w:standard] crawler -> start -> explore -> plan -> implement -> verify -> close
```

## 十四、落地顺序

为了避免流程先于业务，推荐按以下顺序落地：

1. 先用本文档统一术语和分级
2. 再逐步建立 `.workflow/knowledge/` 最小目录
3. 再补 `decisions/` 和模板
4. 最后再决定是否需要更多技能化或自动化能力

当前阶段不建议先建设大而全的工作流基础设施。

## 十五、最终原则

这套 Claude 工作流的核心不是“流程完整”，而是：

- 对当前业务最有帮助
- 对长周期项目可持续
- 对验证型阶段足够轻
- 对未来平台化演进不失控

如果后续项目重点从 `crawler` 转向 `platform` 或 `analysis`，应更新模块知识与默认路由，但不需要推翻这套主结构。
