#!/usr/bin/env python3
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
import requests

CHROMA_DIR = os.getenv("CHROMA_DIR", "/j/fastapi_db_api/deploy/chroma_db")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:8b")
TOP_K = int(os.getenv("TOP_K", 3))

# 向量模型（和导入脚本统一：Ollama nomic-embed-text）
OLLAMA_EMBED_URL = f"{OLLAMA_URL}/api/embeddings"
OLLAMA_EMBED_MODEL = "nomic-embed-text"

# 连接向量库
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
try:
    collection = chroma_client.get_collection("gauss_kb")
except Exception:
    collection = None

app = FastAPI(title="GaussDB QA Proxy")

class QARequest(BaseModel):
    question: str
    top_k: int = TOP_K

# 生成向量
def get_embedding(text):
    try:
        r = requests.post(OLLAMA_EMBED_URL, json={
            "model": OLLAMA_EMBED_MODEL,
            "prompt": text
        }, timeout=30)
        r.raise_for_status()
        return r.json()["embedding"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"向量失败: {str(e)}")

@app.post("/qa")
def qa(req: QARequest):
    if not collection:
        raise HTTPException(status_code=500, detail="请先导入数据")

    # 向量查询
    q_emb = get_embedding(req.question)
    res = collection.query(
        query_embeddings=[q_emb],
        n_results=req.top_k,
        include=["documents", "metadatas", "distances"]
    )

    # 组装证据
    docs = []
    for i in range(len(res["documents"][0])):
        docs.append({
            "id": f"chunk_{i}",
            "content": res["documents"][0][i],
            "metadata": res["metadatas"][0][i],
            "distance": round(res["distances"][0][i], 4)
        })

    # 构造提示词
    evidences = "\n".join([f"[{i+1}] {d['content']}" for i, d in enumerate(docs)])
    prompt = f"""你是GaussDB专家，请根据下面信息回答问题。
问题：{req.question}
参考信息：
{evidences}
请给出专业、简洁的答案。"""

    # ====================== 重点：使用 /api/generate（全版本兼容）
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        resp.raise_for_status()
        answer = resp.json()["response"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM失败: {str(e)}")

    return {
        "question": req.question,
        "answer": answer,
        "evidences": docs
    }