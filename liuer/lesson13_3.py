# https://zhuanlan.zhihu.com/p/29212896
import numpy as np
import torch
from torch import nn
from torch.autograd import Variable
from torch.utils.data import DataLoader
from tqdm import tqdm


class DefaultConfig(object):
    # Dataset.
    txt = "./dataset/jay.txt"
    len = 20
    max_vocab = 8000
    begin = "天青色等烟雨"  # begin word of text
    predict_len = 50  # predict length
    load_model = "./dataset/CharRNN_best_model.pth"

    # Model parameters.
    embed_dim = 512
    hidden_size = 512
    num_layers = 2
    dropout = 0.5

    # Model hyper parameters.
    use_gpu = True  # use GPU or not
    ctx = 0  # running on which cuda device
    batch_size = 128  # batch size
    num_workers = 4  # how many workers for loading data
    max_epoch = 5
    lr = 1e-3  # initial learning rate


opt = DefaultConfig()


class CharRNN(nn.Module):
    def __init__(self, num_classes, embed_dim, hidden_size, num_layers, dropout):
        super().__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size

        self.word_to_vec = nn.Embedding(num_classes, embed_dim)
        self.rnn = nn.GRU(embed_dim, hidden_size, num_layers, dropout=dropout)
        self.project = nn.Linear(hidden_size, num_classes)

    def forward(self, x, hs=None):
        batch = x.shape[0]
        if hs is None:
            hs = Variable(torch.zeros(self.num_layers, batch, self.hidden_size))
            if opt.use_gpu:
                hs = hs.cuda()
        word_embed = self.word_to_vec(x)  # (batch, len, embed)
        word_embed = word_embed.permute(1, 0, 2)  # (len, batch, embed)
        out, h0 = self.rnn(word_embed, hs)  # (len, batch, hidden)
        le, mb, hd = out.shape
        out = out.view(le * mb, hd)
        out = self.project(out)
        out = out.view(le, mb, -1)
        out = out.permute(1, 0, 2).contiguous()  # (batch, len, hidden)
        return out.view(-1, out.shape[2]), h0


class TextConverter(object):
    def __init__(self, text_path, max_vocab=5000):
        with open(text_path, "r", encoding="UTF-8") as f:
            text = f.read()
        text = (
            text.replace("\n", " ")
            .replace("\r", " ")
            .replace("，", " ")
            .replace("。", " ")
        )
        vocab = set(text)
        # If the number of words is larger than limit, clip the words with minimum frequency.
        vocab_count = {}
        for word in vocab:
            vocab_count[word] = 0
        for word in text:
            vocab_count[word] += 1
        vocab_count_list = []
        for word in vocab_count:
            vocab_count_list.append((word, vocab_count[word]))
        vocab_count_list.sort(key=lambda x: x[1], reverse=True)
        if len(vocab_count_list) > max_vocab:
            vocab_count_list = vocab_count_list[:max_vocab]
        vocab = [x[0] for x in vocab_count_list]
        self.vocab = vocab
        self.word_to_int_table = {c: i for i, c in enumerate(self.vocab)}
        self.int_to_word_table = dict(enumerate(self.vocab))

    @property
    def vocab_size(self):
        return len(self.vocab) + 1

    def word_to_int(self, word):
        if word in self.word_to_int_table:
            return self.word_to_int_table[word]
        else:
            return len(self.vocab)

    def int_to_word(self, index):
        if index == len(self.vocab):
            return "<unk>"
        elif index < len(self.vocab):
            return self.int_to_word_table[index]
        else:
            raise Exception("Unknown index!")

    def text_to_arr(self, text):
        arr = []
        for word in text:
            arr.append(self.word_to_int(word))
        return np.array(arr)

    def arr_to_text(self, arr):
        words = []
        for index in arr:
            words.append(self.int_to_word(index))
        return "".join(words)


class TextDataset(object):
    def __init__(self, text_path, n_step, arr_to_idx):
        with open(text_path, "r", encoding="UTF-8") as f:
            text = f.read()
        text = (
            text.replace("\n", " ")
            .replace("\r", " ")
            .replace("，", " ")
            .replace("。", " ")
        )
        num_seq = int(len(text) / n_step)
        self.num_seq = num_seq
        self.n_step = n_step
        # Clip more than maximum length.
        text = text[: num_seq * n_step]
        arr = arr_to_idx(text)
        arr = arr.reshape((num_seq, -1))
        self.arr = torch.from_numpy(arr)

    def __getitem__(self, item):
        x = self.arr[item, :]
        y = torch.zeros(x.shape)
        y[:-1], y[-1] = x[1:], x[0]
        return x, y

    def __len__(self):
        return self.num_seq


def get_data(convert):
    dataset = TextDataset(opt.txt, opt.len, convert.text_to_arr)
    return DataLoader(
        dataset, opt.batch_size, shuffle=True, num_workers=opt.num_workers
    )


def get_model(convert):
    model = CharRNN(
        convert.vocab_size, opt.embed_dim, opt.hidden_size, opt.num_layers, opt.dropout
    )
    if opt.use_gpu:
        model = model.cuda()
    return model


def get_loss(score, label):
    return nn.CrossEntropyLoss()(score, label.view(-1))


def get_optimizer(model):
    optimizer = torch.optim.Adam(model.parameters(), lr=opt.lr)
    return optimizer


def pick_top_n(preds, top_n=5):
    top_pred_prob, top_pred_label = torch.topk(preds, top_n, 1)
    top_pred_prob /= torch.sum(top_pred_prob)
    top_pred_prob = top_pred_prob.squeeze(0).cpu().numpy()
    top_pred_label = top_pred_label.squeeze(0).cpu().numpy()
    c = np.random.choice(top_pred_label, size=1, p=top_pred_prob)
    return c


class CharRNNTrainer:
    def __init__(self, convert):
        self.convert = convert
        self.model = get_model(convert)
        self.criterion = get_loss
        self.optimizer = get_optimizer(self.model)
        self.n_iter = 0
        self.n_plot = 0

    def train(self, train_data):
        for data in tqdm(train_data):
            x, y = data
            y = y.long()
            if opt.use_gpu:
                x = x.cuda()
                y = y.cuda()
            x, y = Variable(x), Variable(y)

            # Forward.
            score, _ = self.model(x)
            loss = self.criterion(score, y)

            # Backward.
            self.optimizer.zero_grad()
            loss.backward()

            # Clip gradient.
            nn.utils.clip_grad_norm_(self.model.parameters(), 5)
            self.optimizer.step()

            # Update to tensorboard.
            if (self.n_iter + 1) % 100 == 0:
                self.n_plot += 1
            self.n_iter += 1

    def test(self, begin_str, text_len):
        self.model.eval()
        begin = np.array([i for i in begin_str])
        begin = np.random.choice(begin, size=1)
        samples = [self.convert.word_to_int(c) for c in begin]
        input_txt = torch.LongTensor(samples)[None]
        if opt.use_gpu:
            input_txt = input_txt.cuda()
        input_txt = Variable(input_txt)
        _, init_state = self.model(input_txt)
        result = samples
        model_input = input_txt[:, -1][:, None]
        for i in range(text_len):
            out, init_state = self.model(model_input, init_state)
            pred = pick_top_n(out.data)
            model_input = Variable(torch.LongTensor(pred))[None]
            if opt.use_gpu:
                model_input = model_input.cuda()
            result.append(pred[0])
        print(self.convert.arr_to_text(result))

    def predict(self, begin, predict_len):
        self.model.eval()
        samples = [self.convert.word_to_int(c) for c in begin]
        input_txt = torch.LongTensor(samples)[None]
        if opt.use_gpu:
            input_txt = input_txt.cuda()
        input_txt = Variable(input_txt)
        _, init_state = self.model(input_txt)
        result = samples
        model_input = input_txt[:, -1][:, None]
        for i in range(predict_len):
            out, init_state = self.model(model_input, init_state)
            pred = pick_top_n(out.data)
            model_input = Variable(torch.LongTensor(pred))[None]
            if opt.use_gpu:
                model_input = model_input.cuda()
            result.append(pred[0])
        text = self.convert.arr_to_text(result)
        print("Generate text is: {}".format(text))

    def load_state_dict(self, checkpoints):
        self.model.load_state_dict(torch.load(checkpoints))


def train():
    torch.cuda.set_device(opt.ctx)
    convert = TextConverter(opt.txt, max_vocab=opt.max_vocab)
    train_data = get_data(convert)
    char_rnn_trainer = CharRNNTrainer(convert)
    for epoch in range(opt.max_epoch):
        char_rnn_trainer.train(train_data)
    char_rnn_trainer.test(opt.begin, opt.predict_len)
    char_rnn_trainer.predict(opt.begin, opt.predict_len)


def predict():
    torch.cuda.set_device(opt.ctx)
    convert = TextConverter(opt.txt, max_vocab=opt.max_vocab)
    char_rnn_trainer = CharRNNTrainer(convert)
    char_rnn_trainer.load_state_dict(opt.load_model)
    char_rnn_trainer.predict(opt.begin, opt.predict_len)


if __name__ == "__main__":
    train()
