import openai, os
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import  HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SimpleSequentialChain

os.environ["OPENAI_API_BASE"] = "https://api.aiproxy.io/v1"
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

en_to_zh_prompt = PromptTemplate(
    template="请把下面这句话翻译成英文： \n\n {question}?", input_variables=["question"]
)

question_prompt = PromptTemplate(
    template = "{english_question}", input_variables=["english_question"]
)

zh_to_cn_prompt = PromptTemplate(
    input_variables=["english_answer"],
    template="请把下面这一段翻译成中文： \n\n{english_answer}?",
)

chinese_qa_chain = SimpleSequentialChain(chains=[
    LLMChain(llm=llm, prompt=en_to_zh_prompt, output_key="english_question"),
    LLMChain(llm=llm, prompt=question_prompt, output_key="english_answer"),
    LLMChain(llm=llm, prompt=zh_to_cn_prompt)
], input_key="question")
answer = chinese_qa_chain.run(question="请你作为一个机器学习的专家，介绍一下CNN的原理。")
print(answer)
