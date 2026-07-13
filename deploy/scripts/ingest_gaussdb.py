#!/usr/bin/env python3
"""
ingest_gaussdb.py

将 GaussDB 巡检 CSV/JSON/MD 转为 chunk，生成 embedding 并写入 Chroma 或调用 Dify API。
用法示例：
  python ingest_gaussdb.py --input ../data/sample_gauss_export.csv --mode chroma

依赖：pip install -r ../requirements.txt
"""
import os
import argparse
import json
from typing import List, Dict
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from rich.progress import track

# Config via env
CHROMA_DIR = os.getenv("CHROMA_DIR", "./deploy/chroma_db")
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
DIFY_API = os.getenv("DIFY_API", "http://localhost:8080")
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "")


def chunk_text(text: str, max_chars=1000, overlap=150) -> List[str]:
    if not text:
        return []
    paragraphs = text.replace('\r', '\n').split('\n')
    chunks: List[str] = []
    cur = ''
    for p in paragraphs:
        s = p.strip()
        if not s:
            continue
        if len(cur) + len(s) + 1 > max_chars:
            if cur:
                chunks.append(cur.strip())
            cur = s
        else:
            cur = cur + ('\n' if cur else '') + s
    if cur:
        chunks.append(cur.strip())

    # add simple overlap by merging preceding tail
    if overlap and len(chunks) > 1:
        merged = []
        for i, c in enumerate(chunks):
            if i == 0:
                merged.append(c)
            else:
                prev = merged[-1]
                tail = prev[-overlap:] if len(prev) > overlap else prev
                merged.append(tail + '\n' + c)
        return merged
    return chunks


def load_csv(path: str) -> List[Dict]:
    df = pd.read_csv(path, dtype=str).fillna("")
    records = []
    for i, row in df.iterrows():
        rec = {
            "id": str(row.get("id", f"row_{i}")),
            "description": row.get("description", "") or row.get("desc", ""),
            "db": row.get("db", ""),
            "table": row.get("table", ""),
            "risk": row.get("risk", ""),
            "timestamp": row.get("timestamp", "")
        }
        records.append(rec)
    return records


def build_docs_from_records(records: List[Dict]) -> List[Dict]:
    docs = []
    for r in records:
        text = r.get('description', '')
        chunks = chunk_text(text, max_chars=900, overlap=150)
        if not chunks:
            chunks = [text]
        for idx, c in enumerate(chunks):
            docs.append({
                "id": f"{r.get('id')}_chunk{idx}",
                "content": c,
                "metadata": {
                    "source_type": "inspection",
                    "source_name": r.get('id'),
                    "db": r.get('db'),
                    "table": r.get('table'),
                    "risk": r.get('risk'),
                    "timestamp": r.get('timestamp'),
                    "chunk_index": idx
                }
            })
    return docs


def embed_texts(texts: List[str], model_name: str = EMBED_MODEL):
    embedder = SentenceTransformer(model_name)
    embs = embedder.encode(texts, batch_size=64, show_progress_bar=True)
    return embs


def insert_chroma(docs: List[Dict]):
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_DIR))
    collection_name = "gauss_kb"
    existing = [c.name for c in client.list_collections()]
    if collection_name in existing:
        coll = client.get_collection(collection_name)
    else:
        coll = client.create_collection(collection_name)

    ids = [d["id"] for d in docs]
    texts = [d["content"] for d in docs]
    metadatas = [d["metadata"] for d in docs]
    embeddings = embed_texts(texts)
    coll.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=embeddings)
    client.persist()
    print(f"Inserted {len(ids)} docs into Chroma collection {collection_name}")


def upload_to_dify_api(docs: List[Dict]):
    # Placeholder: real Dify API may differ. Keep for reference.
    import requests
    headers = {"Authorization": f"Bearer {DIFY_API_KEY}"} if DIFY_API_KEY else {}
    for d in track(docs, description="Uploading to Dify"):
        payload = {
            "title": d["id"],
            "content": d["content"],
            "metadata": d["metadata"]
        }
        try:
            r = requests.post(f"{DIFY_API}/api/knowledge/documents", headers=headers, json=payload, timeout=30)
            if r.status_code not in (200, 201):
                print("Dify upload failed for", d["id"], r.status_code, r.text)
        except Exception as e:
            print("Dify upload error for", d["id"], e)


def generate_sample_csv(path: str):
    sample = [
        {
            "id": "ins_001",
            "description": "Checkpoint 发生频繁，平均间隔 30 秒，有大量小事务导致 WAL 写入频繁。建议检查应用提交频率并合并事务；考虑调整 checkpoint_timeout 和 checkpoint_completion_target。",
            "db": "gaussdb_prod",
            "table": "orders",
            "risk": "MEDIUM",
            "timestamp": "2026-05-20T10:12:00"
        },
        {
            "id": "ins_002",
            "description": "shared_buffers 当前设置为 256MB。文档不建议动态修改该参数，因为修改可能需要重启并引起内存分配变化导致性能抖动。",
            "db": "gaussdb_prod",
            "table": "",
            "risk": "LOW",
            "timestamp": "2026-05-19T09:00:00"
        },
        {
            "id": "ins_003",
            "description": "SQL: SELECT * FROM user WHERE created_at > '2026-01-01' 未使用索引，表扫描导致响应慢。EXPLAIN 显示 cost 很高。建议增加索引或改写查询。",
            "db": "gaussdb_prod",
            "table": "user",
            "risk": "HIGH",
            "timestamp": "2026-05-18T14:30:00"
        }
    ]
    df = pd.DataFrame(sample)
    df.to_csv(path, index=False)
    print(f"Sample CSV generated at {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=False, help="CSV/JSON/MD path")
    parser.add_argument("--mode", choices=["chroma", "dify"], default="chroma")
    parser.add_argument("--gen-sample", action='store_true', help="Generate sample CSV at deploy/data/sample_gauss_export.csv")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    sample_path = os.path.join(data_dir, "sample_gauss_export.csv")

    if args.gen_sample:
        generate_sample_csv(sample_path)
        return

    input_path = args.input or sample_path
    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}. You can generate a sample with --gen-sample")
        return

    if input_path.endswith('.csv'):
        records = load_csv(input_path)
    else:
        raise ValueError("Currently only CSV sample loader is implemented")

    docs = build_docs_from_records(records)
    if args.mode == 'chroma':
        insert_chroma(docs)
    else:
        upload_to_dify_api(docs)


if __name__ == '__main__':
    main()

