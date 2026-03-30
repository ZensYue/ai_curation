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
