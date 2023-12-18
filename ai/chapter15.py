import openai, os
from langchain.chains import LLMRequestsChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain, TransformChain
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

template = """在 >>> 和 <<< 直接是来自Google的原始搜索结果.
请把对于问题 '{query}' 的答案从里面提取出来，如果里面没有相关信息的话就说 "找不到"
请使用如下格式：
Extracted:<answer or "找不到">
>>> {requests_result} <<<
Extracted:"""

question_prompt = PromptTemplate(
    input_variables=["query", "requests_result"],
    template=template,
)
os.environ["OPENAI_API_BASE"] = "https://api.aiproxy.io/v1"
llm = ChatOpenAI(model_name="gpt-3.5-turbo")


def transform_func(inputs: dict) -> dict:
    text = inputs["output"]
    return {"weather_info": text}


requests_chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=question_prompt))
transformation_chain = TransformChain(
    input_variables=["output"],
    output_variables=["weather_info"],
    transform=transform_func,
)

final_chain = SequentialChain(
    chains=[requests_chain, transformation_chain],
    input_variables=["query", "url"],
    output_variables=["weather_info"],
)
question = "今天上海的天气怎么样？"
inputs = {
    "query": question,
    "url": "https://cn.bing.com/search?q=" + question.replace(" ", "+"),
}
final_result = final_chain.run(inputs)
# final_result = requests_chain(inputs)
print(final_result)
