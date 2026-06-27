import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from app.rag.knowledge_base import KNOWLEDGE_BASE
import os
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    model=os.getenv("EMBEDDING_MODEL")
)

# ======================
# 1️⃣ 向量化知识库
# ======================
docs_embeddings = embeddings.embed_documents(KNOWLEDGE_BASE)

dimension = len(docs_embeddings[0])

index = faiss.IndexFlatL2(dimension)
index.add(np.array(docs_embeddings))


# ======================
# 2️⃣ 检索函数
# ======================
def retrieve_context(query: str, k: int = 3):

    query_embedding = embeddings.embed_query(query)

    distances, indices = index.search(
        np.array([query_embedding]),
        k
    )

    results = [KNOWLEDGE_BASE[i] for i in indices[0]]

    return results