import re
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, tool
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import os
import json

os.environ["OPENAI_API_BASE"] = "https://api.aiproxy.io/v1"
answer_order_info = PromptTemplate(
    template="请把下面的订单信息回复给用户： \n\n {order}?", input_variables=["order"]
)
answer_order_llm = LLMChain(llm=ChatOpenAI(model_name="gpt-3.5-turbo"), prompt=answer_order_info)
ORDER_1 = "20230101ABC"
ORDER_2 = "20230101EFG"
ORDER_1_DETAIL = {
    "order_number": ORDER_1,
    "status": "已发货",
    "shipping_date": "2023-01-03",
    "estimated_delivered_date": "2023-01-05",
}
ORDER_2_DETAIL = {
    "order_number": ORDER_2,
    "status": "未发货",
    "shipping_date": None,
    "estimated_delivered_date": None,
}


@tool("Search Order", return_direct=True)
def search_order(input: str) -> str:
    """useful for when you need to answer questions about customers orders"""
    pattern = r"\d+[A-Z]+"
    match = re.search(pattern, input)

    order_number = input
    if match:
        order_number = match.group(0)
    else:
        return "请问您的订单号是多少？"
    if order_number == ORDER_1:
        return answer_order_llm.run(json.dumps(ORDER_1_DETAIL))
    elif order_number == ORDER_2:
        return answer_order_llm.run(json.dumps(ORDER_2_DETAIL))
    else:
        return f"对不起，根据{input}没有找到您的订单"


@tool("FAQ", return_direct=True)
def faq(intput: str) -> str:
    """"useful for when you need to answer questions about shopping policies, like return policy, shipping policy, etc."""
    return "7天无理由退货"


@tool("Recommend Product", return_direct=True)
def recommend_product(input: str) -> str:
    """"useful for when you need to search and recommend products and recommend it to the user"""
    return "红色连衣裙"


tools = [search_order, recommend_product, faq]
chatllm = ChatOpenAI(model_name="gpt-3.5-turbo")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation_agent = initialize_agent(tools, chatllm,
                                      agent="conversational-react-description",
                                      memory=memory, verbose=True, handle_parsing_errors=True)
question1 = "我有一张订单，一直没有收到，能麻烦帮我查一下吗？"
answer1 = conversation_agent.run(question1)
print(answer1)
question2 = "我的订单号是20230101ABC"
answer2 = conversation_agent.run(question2)
print(answer2)
question3 = "你们的退货政策是怎么样的？"
answer3 = conversation_agent.run(question3)
print(answer3)
