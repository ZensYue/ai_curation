# Select Agent

一个轻量的技能化项目骨架，当前内置 `docx` 阅读技能。

## 功能

- 技能注册与发现
- 命令行调用技能
- 无第三方依赖读取 `docx`
- 输出结构化 JSON 或可读文本

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
select-agent list-skills
select-agent read-docx "n8n KP平台电子产品自动选品需求文档.docx"
```

如果不安装，也可以直接运行：

```bash
PYTHONPATH=src python3 -m select_agent list-skills
PYTHONPATH=src python3 -m select_agent read-docx "n8n KP平台电子产品自动选品需求文档.docx" --json
```

## 技能模块

技能放在 `src/select_agent/skills/` 下，实现 `Skill` 协议并注册到 `SkillRegistry`。

当前内置：

- `read_docx`: 读取文档元数据、段落、标题和表格

## 目录

```text
src/select_agent/
  cli.py
  skills/
    base.py
    registry.py
    docx_reader.py
tests/
```

