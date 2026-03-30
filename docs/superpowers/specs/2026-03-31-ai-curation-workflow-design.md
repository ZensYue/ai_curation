# AI Curation (AI 选品) Workflow Design

## 1. Overview
This document specifies the foundational workflow architecture for the "AI 选品" (AI Curation) project. The goal is to establish a robust, spec-driven development environment using **OpenSpec** and **Superpowers**. The project will utilize a multi-agent ("Agent Team") approach.

## 2. Directory Structure
The workspace will adopt a "Hybrid Domain-Driven" approach (Option A), separating specifications from implementations.

```text
.openspec/
├── team.md                 # Agent Team collaboration definition
├── agents/                 # Individual Agent specifications
│   ├── base_agent.md       # Shared foundational rules, persona, and error handling
│   ├── scraper_agent.md    # [Template] Scraper Agent
│   └── analysis_agent.md   # [Template] Analysis Agent
└── prompts/
    └── meta_prompts/       # Meta-prompts to generate code based on specs

scripts/
└── agents/                 # Python scripts implementing the agents for initial validation
```

## 3. Core Specification Templates
The core workflow configuration files in `.openspec/` will define the team dynamics and agent capabilities.

### 3.1. `team.md` (Agent Collaboration Center)
- **Team Goal**: Define the overarching pipeline for AI curation (e.g., Data Gathering -> Analysis -> Decision/Recommendation).
- **Roles & Responsibilities**: Outline which agent is responsible for which phase of the pipeline.
- **Communication Protocol**: Define how agents pass context (e.g., JSON schema, event streams, shared memory).
- **Global Error Handling**: Define the team's fallback strategy if an agent fails (e.g., if `scraper_agent` is blocked, should the team abort or use cached data?).

### 3.2. `agents/*.md` (Individual Agent Specification)
Each agent specification will act as the blueprint for its code implementation.
- **Role/Persona**: The System Prompt and core objective of the agent.
- **Input/Output**: The exact JSON schema or data structure the agent accepts and emits.
- **Tools**: Authorized actions the agent can perform (e.g., web requests, database queries, LLM calls).
- **Validation Criteria**: Unit/Integration test cases to verify the agent behaves according to its spec.

## 4. Implementation Strategy
1. **Initialize OpenSpec structure**: Create the directories and blank/template `.openspec` files.
2. **User Review**: The user will review the blank templates and fill in specific business logic for the AI curation use case.
3. **Validation Implementation**: Use the `scripts/agents/` directory to write Python validation code based on the refined `.openspec` specifications.
