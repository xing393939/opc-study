import torch
from modelscope.models.base.base_model import Model
from modelscope.preprocessors.base import Preprocessor

model_dir = "C:\\Users\\bookan\\.cache\\modelscope\\hub\\damo\\ChatPLUG-240M"
model = Model.from_pretrained(
    model_dir,
    device='gpu',
    model_prefetched=True)
preprocessor = Preprocessor.from_pretrained(model_dir)

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

params = {
    'preprocess_params': preprocess_params,
    'forward_params': forward_params
}


class Done:
    def __init__(self):
        self.model = model
        self.preprocessor = preprocessor

    def _check_input(self, input):
        pass

    def _check_output(self, input):
        pass

    def process_single(self, input):
        self._check_input(input)
        out = self.preprocessor(input, **preprocess_params)

        with torch.no_grad():
            out = self.model(out, **forward_params)

        self._check_output(out)
        return out


d = Done()
d.process_single("aaa")

