import openai, os
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.vector_stores import TencentVectorDB
from llama_index.vector_stores.tencentvectordb import (
    CollectionParams,
    FilterField,
)
import tcvectordb

os.environ["OPENAI_API_BASE"] = "https://api.aiproxy.io/v1"

# 加载 documents
documents = SimpleDirectoryReader("./data/mr_fujino").load_data()
vector_store = TencentVectorDB(
    url=os.getenv("TENCENT_VECTOR_DB_URL"),
    key="WGefITvf9mQDNBSJ0VBkluqEjciiXNiwfUWp07Hk",
    collection_params=CollectionParams(dimension=1536, drop_exists=False),
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
