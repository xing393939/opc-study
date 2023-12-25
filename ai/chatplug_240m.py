from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.models import Model

model_id = 'damo/ChatPLUG-240M'
# device可以设置为cpu, cuda, gpu, gpu:X 或 cuda:X
pipeline_ins = pipeline(Tasks.fid_dialogue, model=model_id, model_revision='v1.0.1', device='gpu')

input = {
    "history": "你好[SEP]你好!很高兴与你交流![SEP]以春天为主题写一首诗",
    "bot_profile": "我是达摩院的语言模型ChatPLUG，是基于海量数据训练得到。"
}

# 数据预处理设置
preprocess_params = {
    'max_encoder_length': 380,  # encoder最长输入长度
    'context_turn': 3  # context最长轮数
}

# 解码策略，默认为sampling
forward_params = {
    'min_length': 10,
    'max_length': 512,
    'num_beams': 1,
    'temperature': 0.8,
    'do_sample': True,
    'early_stopping': True,
    'top_k': 50,
    'top_p': 0.8,
    'repetition_penalty': 1.2,
    'length_penalty': 1.2,
    'no_repeat_ngram_size': 6
}

kwargs = {
    'preprocess_params': preprocess_params,
    'forward_params': forward_params
}

result = pipeline_ins(input, **kwargs)

print(result)
