# _project INDEX

- w-rule-platform-product-scope | 类型: rule | 适用: 全项目 | 说明: 本项目按平台化产品建设，爬虫是核心能力域，但不是整个平台本身
- w-rule-crawler-current-priority | 类型: rule | 适用: 当前阶段 | 说明: 当前默认优先服务 crawler，可行性验证优先于平台扩展
- w-rule-no-multi-site-abstraction-yet | 类型: rule | 适用: crawler 当前阶段 | 说明: 未完成单站点验证前，不提前做多站点抽象
- w-rule-http-first-validation | 类型: rule | 适用: crawler 当前阶段 | 说明: 先验证 HTTP 方案，再决定是否接 browser fallback
- w-rule-memory-layering | 类型: rule | 适用: Claude 工作流 | 说明: mem 只存协作记忆，项目知识主库在 repo
- adr-001-java-as-platform-backbone | 类型: decision | 适用: platform | 说明: 平台主干长期采用 Java + Spring Boot
- adr-002-python-crawler-service | 类型: decision | 适用: crawler | 说明: 爬虫能力域独立采用 Python 服务承载
- adr-003-http-callback-first | 类型: decision | 适用: platform+crawler | 说明: 主链路 HTTP + 回调，轮询仅作补偿
- adr-004-no-multi-site-abstraction-yet | 类型: decision | 适用: crawler 当前阶段 | 说明: 当前阶段不提前做多站点抽象
