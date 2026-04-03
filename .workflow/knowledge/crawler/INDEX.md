# crawler INDEX

- w-rule-kp-single-site-feasibility | 类型: rule | 适用: crawler 当前阶段 | 说明: 当前只做 KP 单站点可行性验证
- w-rule-raw-json-first | 类型: rule | 适用: crawler 当前阶段 | 说明: 当前先输出 raw JSON，不做标准化、写表或 AI 分析
- w-rule-http-before-browser | 类型: rule | 适用: crawler 当前阶段 | 说明: 抓取策略先 HTTP，失败或关键字段不足时再考虑浏览器兜底
- w-p-kp-field-stability | 类型: pitfall | 信号: 某些字段时有时无 | 说明: 需要记录哪些字段稳定可得、哪些字段缺失以及原因
- w-p-kp-list-detail-source-split | 类型: pitfall | 信号: 列表页和详情页字段来源不同 | 说明: 修改解析逻辑前先明确字段来自列表页、详情页还是 JSON-LD
- w-p-fixture-vs-real-page-gap | 类型: pitfall | 信号: fixture 测试通过但真实页面失败 | 说明: 真实联调优先级高于 fixture 自洽
- w-p-browser-fallback-trigger | 类型: pitfall | 信号: HTTP 成功但关键字段缺失或被反爬 | 说明: 需要明确何时标记 browser_fallback_required
- adr-003-http-callback-first | 类型: decision | 适用: crawler + platform 协作 | 说明: 爬虫服务与主平台主链路采用 HTTP + 回调
- adr-004-no-multi-site-abstraction-yet | 类型: decision | 适用: crawler 当前阶段 | 说明: 单站点验证完成前不提前做多站点抽象
