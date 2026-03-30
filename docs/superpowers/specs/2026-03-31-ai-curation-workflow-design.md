# AI 选品 (AI Curation) 工作流设计

## 1. 概述
本文档规定了“AI 选品”项目基础工作流的架构设计。我们的目标是使用 **OpenSpec** 和 **Superpowers** 建立一个稳健的、以规范驱动的开发环境。本项目将采用多智能体（"Agent Team"）协作的方式来实现。

## 2. 目录结构
工作区将采用“混合领域驱动”（方案 A），将规范说明与代码实现分离开来。

```text
.openspec/
├── team.md                 # Agent Team 协同工作流定义（谁调用谁，如何传递上下文）
├── agents/                 # 每个独立 Agent 的规范
│   ├── base_agent.md       # 所有 Agent 的基础规范（共用人设、错误处理规范等）
│   ├── scraper_agent.md    # [模板] 负责信息采集的 Agent 规范
│   └── analysis_agent.md   # [模板] 负责分析的 Agent 规范
└── prompts/
    └── meta_prompts/       # 用于让大模型根据规范生成代码的 Prompt 模板

scripts/
└── agents/                 # 存放用于初期验证阶段、实现了各个 Agent 逻辑的 Python 脚本
```

## 3. 核心规范模板
位于 `.openspec/` 目录下的核心工作流配置文件，将定义团队的协作方式和各个智能体的能力。

### 3.1. `team.md` (Agent 协作中心)
- **Team Goal (团队目标)**: 定义 AI 选品的核心流水线（例如：数据抓取 -> 分析 -> 决策推荐）。
- **Roles & Responsibilities (角色与职责)**: 明确哪个 Agent 负责流水线中的哪个阶段。
- **Communication Protocol (通信协议)**: 定义 Agent 之间如何传递上下文（例如：JSON 数据格式、事件流、共享内存）。
- **Global Error Handling (全局错误处理)**: 定义某个 Agent 失败时的回退策略（例如，如果爬虫 agent 被屏蔽了，团队是应该中止流程，还是使用缓存数据？）。

### 3.2. `agents/*.md` (单个 Agent 规范)
每个 Agent 的规范文档将作为它代码实现的蓝图。
- **Role/Persona (角色/人设)**: Agent 的系统提示词 (System Prompt) 及其核心目标。
- **Input/Output (输入/输出)**: Agent 接收和返回的精确 JSON Schema 或数据结构。
- **Tools (工具)**: Agent 可以调用的授权操作（例如：网络请求、数据库查询、LLM 接口调用）。
- **Validation Criteria (验证标准)**: 单元测试/集成测试用例，用于验证 Agent 的行为是否符合规范。

## 4. 实施策略
1. **初始化 OpenSpec 结构**: 创建目录，并编写空白或带有基础模板的 `.openspec` 文件。
2. **用户审查**: 由用户审查空白模板，并在其中填入针对 AI 选品业务的具体逻辑。
3. **验证实现**: 基于完善后的 `.openspec` 规范，在 `scripts/agents/` 目录下编写 Python 验证代码。
