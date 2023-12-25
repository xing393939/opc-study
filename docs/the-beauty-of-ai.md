### AI大模型之美

#### 基础知识篇
* 01，学会和AI对话，问了两个问题：
  * 把中文标题变成英文，写5个卖点，估一个卖价
  * 把英文标题中的人名找出来
  * PS：难点在于任务包含机器翻译、文本生成、知识推理、命名实体识别等，传统做法可能需要融合几个模型才能做到
* 02，情感分类
* 03，巧用提示语
* 04，情感分类对比谷歌的T5
* 05，文本多分类
* 06，部署聊天应用：
  * [大模型之Chat Markup Language](https://blog.csdn.net/fzcoolbaby/article/details/133970545)
  * 使用tiktoken计算token个数
* 07，标题聚类、文本归类、利用文章摘要压缩提示语
* 08，文本改写、屏蔽字词、moderation接口

#### 实战提高(一)
* 09，通过向量化进行语义搜索
* 10，使用llama_index来扩充知识库
* 11，使用开源向量化模型；开源模型的不足之处：
  * paraphrase-multilingual-mpnet-base-v2最多只支持128个token
  * 开源模型的推理能力不如chatgpt
* 12，使用ai写excel插件
* 13，使用ai写单元测试
* 14，使用langchain进行链式调用
* 15，使用langchain的工具
  * langchain.LLMMathChain，问数学题得到python代码，执行python代码
  * langchain.chains.LLMRequestsChain，先请求网页，再组成prompt问llm
  * langchain.chains.TransformChain，转换数据
* 16，使用langchain的工具
  * langchain.memory.ConversationBufferWindowMemory，控制保留几轮对话
  * langchain.memory.ConversationSummaryMemory，把历史对话生成英文摘要
  * langchain.memory.ConversationSummaryBufferMemory，即保留几轮对话，又生成摘要
* 17，利用prompt做决策
* 18，使用openai的[模型微调接口](https://www.eula.club/blogs/%E5%AF%B9OpenAI%E7%9A%84ChatGPT%E5%A4%A7%E6%A8%A1%E5%9E%8B%E8%BF%9B%E8%A1%8C%E5%BE%AE%E8%B0%83.html)

#### 实战提高(二)
* 19，语音转文本
  * 使用openai的whisper-1
  * 也可以使用开源的openai-whisper
* 20，文本转语音
  * Azure云azure.cognitiveservices.speech
  * 百度开源的paddlepaddle
* 21，数字人方案
  * 用Midjourney生成图片
  * 用D-ID将图片+文本生成对应口型的视频
  * 百度开源的PaddleBobo
* 22，HuggingFace
  * Pipeline指定task，会选择默认的model，也可以指定model
  * Inference API（带闪电符号的model），第一次访问可能需要预热
  * Inference Endpoint把大模型部署到云端
* 23，OpenClip
  * openai/clip-vit-base-patch32：零样本图片分类，文搜图，图搜图
  * google/owlvit-base-patch32：零样本图片目标检测
* 24，文生图
  * openai的DALL-E
  * google的Imagen
  * 面向用户的Midjourney
  * 完全开源的Stable Diffusion，它并不是指某一个特定的模型，而是指一类模型结构
* 25，图生图，controlnet是基于Stable Diffusion的
  * lllyasviel/sd-controlnet-canny，原图的边缘检测
  * fusing/stable-diffusion-v1-5-controlnet-openpose，模拟原图的人物动作
  * lllyasviel/sd-controlnet-scribble，根据简笔画生成图片
  * 除了以上3种，还有5种
* 26，Visual ChatGPT：已更名为Task Matrix
  * ai/visual_chatgpt.py：上传图片后尝试“Make the picture thinner, then detect the edges of it”
  * [架构图](../images/visual-chatgpt-figure.jpg)
* 27.Midjourney
  * 新手频道对新用户的引导很友好
  * 等待的过程也出图
  * 通过用户的反馈来强化训练














