# go-web-rag

基于 **Go (Gin)** + **Python (FastAPI)** 的 RAG（检索增强生成）示例项目。
Go 服务作为对外网关接收请求，Python 服务负责文档切分、向量化、向量检索与大模型生成，底层依赖 [Ollama](https://ollama.com/) 提供本地大模型 / Embedding 能力，[Qdrant](https://qdrant.tech/) 作为向量数据库。

## 架构

```
Client
  │  HTTP
  ▼
Go Gin Server (:8080)  ── /api/v1/*
  │  HTTP
  ▼
Python FastAPI Server (:8000)
  │            │
  ▼            ▼
Ollama      Qdrant (:6333)
(LLM /      (向量存储 / 检索)
Embedding)
```

- **Go 服务**：对外提供 `/api/v1/*` 接口，接收用户请求后转发给 Python 服务，并把结果封装成统一响应返回。
- **Python 服务**：
  - 将 Markdown 文档按标题（`#`）切分为多个 chunk；
  - 使用 Ollama 的 `bge-m3` 模型对 chunk 做 embedding，写入 Qdrant；
  - 收到用户问题后，先 embedding 再在 Qdrant 中做向量检索（top-N），
    使用 `BAAI/bge-reranker-v2-m3` 做重排序（top-K），
    最后把检索到的上下文拼接进 prompt，交给 Ollama 的 `qwen2.5:7b` 生成回答。

## 目录结构

```
.
├── go-server/              # Go 网关服务
│   ├── cmd/main.go         # 程序入口，启动 Gin 服务（:8080）
│   ├── router/router.go    # 路由注册
│   ├── controller/chat.go  # 请求处理，转发到 Python 服务
│   └── model/chat.go       # 请求 / 响应结构体
└── python-server/          # Python RAG 服务
    ├── app.py               # FastAPI 入口，定义 /chat /chunk /ques 接口
    ├── spliter.py           # Markdown 切分 + embedding + 写入 Qdrant
    ├── reter.py             # 向量检索 + 重排序
    └── test.md              # 示例文档，用于测试切分与检索
```

## 环境依赖

| 组件 | 说明 |
| --- | --- |
| Go | 1.26+ |
| Python | 3.10+ |
| [Ollama](https://ollama.com/) | 本地大模型服务，需提前拉取模型 |
| [Qdrant](https://qdrant.tech/) | 向量数据库，默认监听 `6333` 端口 |

Ollama 所需模型：

```bash
ollama pull qwen2.5:7b   # 对话 / 生成模型
ollama pull bge-m3       # embedding 模型
```

Python 依赖（暂未提供 `requirements.txt`，可按需安装）：

```bash
pip install fastapi uvicorn ollama qdrant-client sentence-transformers pydantic
```

Qdrant 可用 Docker 快速启动：

```bash
docker run -p 6333:6333 qdrant/qdrant
```

## 快速开始

1. 启动 Qdrant（见上）。
2. 启动 Ollama，并确认 `qwen2.5:7b`、`bge-m3` 模型已拉取。
3. 启动 Python 服务：

   ```bash
   cd python-server
   uvicorn app:app --reload --port 8000
   ```

4. 启动 Go 网关：

   ```bash
   cd go-server
   go run ./cmd
   ```

5. Go 服务默认监听 `http://localhost:8080`，Python 服务监听 `http://localhost:8000`。

## API 说明

### Go 网关（`http://localhost:8080/api/v1`）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/chat` | 请求体 `{"content": "问题"}`，直接转发给 Python `/chat` 做无检索的直接问答 |
| POST | `/chunk/:path` | 转发给 Python `/chunk/{path}`，对指定路径的 Markdown 文档做切分、embedding 并写入 Qdrant |
| POST | `/qus` | 预留的 RAG 问答入口，**尚未实现**（见下方「当前进度」） |

### Python 服务（`http://localhost:8000`）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/chat` | 直接调用 `qwen2.5:7b` 回答问题，不做检索 |
| POST | `/chunk/{path}` | 读取本地 Markdown 文件，按 `#` 标题切分、embedding 后写入 Qdrant `my_chunk` collection |
| POST | `/ques` | RAG 问答：embedding → Qdrant 检索（top 8）→ 重排序（top 3）→ 拼接上下文 → `qwen2.5:7b` 生成回答 |

## 当前进度 / 已知问题

- Go 侧 `controller.DealQuestion`（对应 `/api/v1/qus`）目前是空实现，尚未对接 Python 的 `/ques` 接口。
- Go 侧 `GetAllChunks` 使用 `http.Get` 调用 Python 的 `/chunk/{path}`，而 Python 该接口注册为 `POST`，两端方法未对齐，联调前需要修正。
- 暂无 `requirements.txt` / 依赖锁定文件，需手动安装 Python 依赖。

欢迎在此基础上继续完善混合检索、多轮对话、Agent 等能力。

## License

本项目基于 [MIT License](./LICENSE) 开源。
