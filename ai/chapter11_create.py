import os

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
)

# 加载 documents
documents = SimpleDirectoryReader("./data/faq").load_data()
from llama_index.embeddings import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)
vector_store = TencentVectorDB(
    url=os.getenv("TENCENT_VECTOR_DB_URL"),
    key="WGefITvf9mQDNBSJ0VBkluqEjciiXNiwfUWp07Hk",
    collection_params=CollectionParams(dimension=768, drop_exists=False),
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
text_splitter = SentenceSplitter(separator="\n\n", chunk_size=100, chunk_overlap=20)
service_context = ServiceContext.from_defaults(
    text_splitter=text_splitter, embed_model=embed_model
)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, service_context=service_context
)
