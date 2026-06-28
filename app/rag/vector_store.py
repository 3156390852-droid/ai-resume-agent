"""
向量知识库 —— FAISS 索引 + 语义检索
"""
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
from app.core.logger import logger
from app.rag.knowledge_base import KNOWLEDGE_BASE

# ── 全局单例：模块加载时构建，后续请求复用 ──
_index = None

embeddings = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_API_BASE,
    model=settings.EMBEDDING_MODEL,
)


def _build_index():
    """构建 FAISS 索引（仅首次调用时执行）"""
    global _index
    if _index is not None:
        return _index

    logger.info("正在构建 FAISS 向量索引（%d 条知识）...", len(KNOWLEDGE_BASE))
    docs_embeddings = embeddings.embed_documents(KNOWLEDGE_BASE)
    dimension = len(docs_embeddings[0])
    _index = faiss.IndexFlatL2(dimension)
    _index.add(np.array(docs_embeddings, dtype=np.float32))
    logger.info("FAISS 索引构建完成，维度: %d", dimension)
    return _index


def retrieve_context(query: str, k: int = 3):
    """检索与查询最相关的知识条目"""
    index = _build_index()
    query_embedding = embeddings.embed_query(query)
    _, indices = index.search(np.array([query_embedding], dtype=np.float32), k)
    return [KNOWLEDGE_BASE[i] for i in indices[0]]
