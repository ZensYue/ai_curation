# workflow config

## 模块候选值

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

## 当前阶段默认重点

- `crawler`

## 当前阶段高优先级约束

- 当前项目按平台化产品建设
- 当前默认优先服务 `crawler` 能力域
- 当前 `crawler` 只做 `KP` 单站点可行性验证
- 当前不提前做多站点抽象
- 当前抓取策略是 `HTTP 优先`，必要时再补 browser fallback
- 当前先输出 raw JSON，不做标准化、写表或 AI 分析

## 敏感模块

第一版建议视为敏感模块的有：

- `platform`
- `crawler`
- `pricing`
- `notification`

说明：

- `platform` 涉及账号、权限、任务流转
- `crawler` 涉及抓取结果正确性、回调链路与真实联调
- `pricing` 涉及业务计算正确性
- `notification` 涉及外部触达与告警

## 默认知识加载顺序

- 单一模块任务：`_project -> <module>`
- 跨模块任务：`_project -> multi`
- 模块不明确：`_project -> unknown`

## 默认验证偏好

优先级从高到低：

1. 真实联调 / 真实接口验证
2. fixture / 单元测试
3. 本地运行与结果检查
4. 文档一致性检查
