import openai, os
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

os.environ["OPENAI_API_BASE"] = "https://api.aiproxy.io/v1"
# 加载 documents
documents = SimpleDirectoryReader("./data/mr_fujino").load_data()
index = GPTVectorStoreIndex.from_documents(documents)
index.storage_context.persist("./data/index_mr_fujino")
