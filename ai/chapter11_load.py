import openai, os
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
)
from llama_index.text_splitter import SentenceSplitter
from llama_index.vector_stores import TencentVectorDB
from llama_index.vector_stores.tencentvectordb import (
    CollectionParams,
    FilterField,
)
import tcvectordb
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
os.environ["OPENAI_API_BASE"] = "https://api.aiproxy.io/v1"
new_vector_store = TencentVectorDB(
    url=os.getenv("TENCENT_VECTOR_DB_URL"),
    key="WGefITvf9mQDNBSJ0VBkluqEjciiXNiwfUWp07Hk",
    collection_params=CollectionParams(dimension=768, drop_exists=False),
)
from llama_index.embeddings import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)
service_context = ServiceContext.from_defaults(embed_model=embed_model)
index = VectorStoreIndex.from_vector_store(
    vector_store=new_vector_store, service_context=service_context
)

query_engine = index.as_query_engine(similarity_top_k=5, retriever_mode="embedding")
response = query_engine.query("请问你们海南能发货吗？")
print(response)
