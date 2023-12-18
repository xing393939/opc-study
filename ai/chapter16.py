import openai, os
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_BASE"] = "https://api.aiproxy.io/v1"
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
memory = ConversationSummaryMemory(llm=llm)

prompt_template = """你是一个中国厨师，用中文回答做菜的问题。你的回答需要满足以下要求:
1. 你的回答必须是中文
2. 回答限制在100个字以内

{history}
Human: {input}
AI:"""
prompt = PromptTemplate(input_variables=["history", "input"], template=prompt_template)
conversation_with_summary = ConversationChain(llm=llm, memory=memory, prompt=prompt)
conversation_with_summary.predict(input="你好")
conversation_with_summary.predict(input="鱼香肉丝怎么做？")
conversation_with_summary.predict(input="那宫保鸡丁呢？")
conversation_with_summary.predict(input="我问你的第一句话是什么？")
rs = memory.load_memory_variables({})
print(rs)
