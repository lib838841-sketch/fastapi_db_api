# GaussDB 智能运维知识库 + 本地 AI 问答 平台 (Chroma + Ollama)

此目录包含用于把 GaussDB 巡检/报告导入 Chroma 向量库并用本地 Ollama/qwen3 模型进行 RAG 问答的示例脚本与说明。

目录结构（已创建）:
- deploy/requirements.txt
- deploy/scripts/ingest_gaussdb.py
- deploy/app/qa_proxy.py
- deploy/data/sample_gauss_export.csv  (可由脚本生成)

快速开始（在 Ubuntu VM 上执行）:

1. 进入目录并创建虚拟环境
```bash
cd /path/to/fastapi_db_api/deploy
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

2. 生成示例数据并导入到 Chroma
```bash
python scripts/ingest_gaussdb.py --gen-sample
python scripts/ingest_gaussdb.py --input ./data/sample_gauss_export.csv --mode chroma
```

3. 启动 QA 服务（FastAPI）
```bash
export OLLAMA_URL=http://192.168.169.1:11434
uvicorn app.qa_proxy:app --host 0.0.0.0 --port 9000
```

4. 调用 QA 接口测试
```bash
curl -s -X POST "http://127.0.0.1:9000/qa" -H "Content-Type: application/json" -d '{"question":"为什么 checkpoint 太频繁？", "top_k":3}'
```

注意事项：
- 如果 Ollama 的本地 API 路径不是 `/api/generate`，请修改 `app/qa_proxy.py` 中的 endpoint 组合逻辑。
- Chroma 数据目录默认：`./deploy/chroma_db`。请定期备份该目录。
- 把环境变量（如 OLLAMA_URL、EMBED_MODEL、CHROMA_DIR）加入系统服务或 .env（避免把敏感信息提交到 git）。
- 若要使用 Milvus，请替换 ingest 与 qa 逻辑中对 Chroma 的操作（脚本为 Chroma 示例）。

下一步：
- 我可以根据你的真实巡检 CSV/MD 文件把 loader 调整为更准确的字段映射，并帮助你把这个服务容器化为 Docker Compose（如果需要）。

