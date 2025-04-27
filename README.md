# PubMed MCP Server

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-green.svg)](https://fastapi.tiangolo.com/)

## 项目简介

PubMed MCP Server 是一个基于 fastapi-mcp 的服务，提供了对 PubMed 数据库的访问接口。该服务允许用户搜索 PubMed 文章、获取文章元数据以及下载 PMC 文章的 PDF 文件

基本功能:

- **搜索文章**：根据关键词搜索 PubMed 数据库中的文章
- **获取元数据**：获取特定 PubMed ID 的文章详细信息，包括标题、摘要、作者、关键词等
- **下载 PDF**：下载 PMC 文章的 PDF 文件到本地

## 安装与配置

1. 克隆仓库

```bash
git clone https://github.com/yourusername/pubmed-mcp-server.git
cd pubmed-mcp-server

# 安装 uv 工具，用于管理虚拟环境和依赖项同步
pip install uv
```

2. 创建并激活虚拟环境

```bash
uv sync
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

### 配置

创建 `.env` 文件来自定义配置：

```
DOWNLOAD_PATH=/path/to/store/pdfs
```

默认情况下，PDF 文件将保存在 `/tmp/pubmed-pdfs` 目录下。

## 使用方法

```bash
uv run main.py
```

服务器将在 http://localhost:8977 上运行。

然后你可以在 mcp client 中配置这个endpoint，并使用SSE模式

## 项目结构

```
.
├── app/               # API 应用定义
│   └── pubmed.py      # PubMed API 端点
├── core/              # 核心功能
│   └── config.py      # 配置管理
├── service/           # 服务层
│   ├── __init__.py    # 基础 URL 和工具函数
│   ├── file.py        # 文件下载功能
│   └── search.py      # PubMed 搜索和解析功能
├── tests/             # 测试目录
├── .env               # 环境变量配置
├── main.py            # 应用入口
└── pyproject.toml     # 项目依赖
```


## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
