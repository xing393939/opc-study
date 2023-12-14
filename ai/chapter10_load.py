import openai, os
from llama_index import StorageContext, load_index_from_storage
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
os.environ["OPENAI_API_BASE"] = "https://api.aiproxy.io/v1"
# 加载 documents
storage_context = StorageContext.from_defaults(persist_dir="./data/index_mr_fujino")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()
response = query_engine.query("鲁迅先生在日本学习医学的老师是谁？")
print(response)
response = query_engine.query("鲁迅先生去哪里学的医学？")
print(response)
response = query_engine.query("请问林黛玉和贾宝玉是什么关系？")
print(response)
