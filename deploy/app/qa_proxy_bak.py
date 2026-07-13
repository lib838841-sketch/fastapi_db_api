#!/usr/bin/env python3
"""
qa_proxy_bak.py

FastAPI 服务：接收用户问题 -> 对向量库检索 -> 构建 RAG prompt -> 调用本地 Ollama (或其他 LLM) 返回答案及证据。

运行示例：
  export OLLAMA_URL=http://192.168.169.1:11434/
  uvicorn app.qa_proxy:app --host 0.0.0.0 --port 9000
"""
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import requests

CHROMA_DIR = os.getenv("CHROMA_DIR", "./deploy/chroma_db")
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://192.168.169.1:11434/")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:8b")
TOP_K = int(os.getenv("TOP_K", "5"))

embedder = SentenceTransformer(EMBED_MODEL)
chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_DIR))
try:
    collection = chroma_client.get_collection("gauss_kb")
except Exception:
    collection = None

app = FastAPI(title="GaussDB QA Proxy")


class QARequest(BaseModel):
    question: str
    top_k: int = TOP_K


@app.post("/qa")
def qa(req: QARequest):
    if collection is None:
        raise HTTPException(status_code=500, detail="Chroma collection 'gauss_kb' not found. Run ingest first.")

    q = req.question
    # embed
    q_emb = embedder.encode([q])[0].tolist()
    # query chroma
    results = collection.query(query_embeddings=[q_emb], n_results=req.top_k, include=['metadatas', 'documents', 'distances', 'ids'])
    hits = results['results'][0]
    docs = []
    for i, doc in enumerate(hits['documents']):
        md = hits['metadatas'][i]
        dist = hits['distances'][i]
        docs.append({
            "id": hits['ids'][i],
            "content": doc,
            "metadata": md,
            "distance": dist
        })

    evidences = []
    for i, d in enumerate(docs):
        evidences.append(f"[{i+1}] id:{d['id']} distance:{d['distance']}\nmeta:{json.dumps(d['metadata'])}\n{d['content']}\n")

    rag_prompt = f"""
你是 GaussDB 专家助理。基于下列证据回答用户问题，回答请包含：1) 简短结论；2) 详细诊断；3) 优先级排序的修复步骤（每步说明风险和是否需要停机）。最后列出使用的证据编号。

用户问题: {q}

证据:
{chr(10).join(evidences)}

请开始回答：
"""

    # 调用本地 Ollama (示例 HTTP API)。不同版本的 Ollama 请求体可能不同，请按你的版本调整。
    # 这里尝试使用类似 /api/generate 的通用调用；如果你的 Ollama 使用不同路径，请修改 OLLAMA_URL。
    endpoint = OLLAMA_URL.rstrip('/') + '/api/generate'
    payload = {
        "model": LLM_MODEL,
        "prompt": rag_prompt,
        "max_tokens": 1024,
        "temperature": 0.0
    }
    try:
        r = requests.post(endpoint, json=payload, timeout=120)
        r.raise_for_status()
        resp = r.json()
        # 常见返回格式可能在 key 'text' or 'output' or 'choices'
        answer = None
        if isinstance(resp, dict):
            answer = resp.get('text') or resp.get('output')
            if not answer and 'choices' in resp and isinstance(resp['choices'], list):
                # try extract
                ch = resp['choices'][0]
                answer = ch.get('text') or ch.get('message') or json.dumps(ch)
        if not answer:
            answer = json.dumps(resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM 调用失败: {e}")

    return {"question": q, "answer": answer, "evidences": docs}

