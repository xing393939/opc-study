from transformers import AutoTokenizer, AutoModelForCausalLM
from util import cosine_similarity, get_embedding
import torch

tokenizer = AutoTokenizer.from_pretrained("cerebras/Cerebras-GPT-111M")
model = AutoModelForCausalLM.from_pretrained("cerebras/Cerebras-GPT-111M")
model.eval()


# encode the input sentence
def get_t5_vector(line):
    input_ids = tokenizer.encode(line, return_tensors="pt")
    with torch.no_grad():
        outputs = model(input_ids=input_ids)[0]
        vector = outputs.mean(dim=1)
    return vector[0]


positive_text = """Wanted to save some to bring to my Chicago family but my North Carolina family ate all 4 boxes before I could pack. These are excellent...could serve to anyone"""
negative_text = """First, these should be called Mac - Coconut bars, as Coconut is the #2 ingredient and Mango is #3. Second, lots of people don't like coconut. I happen to be allergic to it. Word to Amazon that if you want happy customers to make things like this more prominent. Thanks."""
positive_review_in_t5 = get_t5_vector("An Amazon review with a positive sentiment.")
negative_review_in_t5 = get_t5_vector("An Amazon review with a negative sentiment.")


def test_t5():
    positive_example_in_t5 = get_t5_vector(positive_text)
    negative_example_in_t5 = get_t5_vector(negative_text)

    def get_t5_score(sample_embedding):
        return cosine_similarity(
            sample_embedding, positive_review_in_t5
        ) - cosine_similarity(sample_embedding, negative_review_in_t5)

    positive_score = get_t5_score(positive_example_in_t5)
    negative_score = get_t5_score(negative_example_in_t5)

    print("T5好评例子的评分 : %f" % (positive_score))
    print("T5差评例子的评分 : %f" % (negative_score))


import pandas as pd
from sklearn.metrics import classification_report

datafile_path = "data/fine_food_reviews_with_embeddings_1k.parquet"
df = pd.read_parquet(datafile_path)
df["t5_embedding"] = df.Text.apply(get_t5_vector)
df = df[df.Score != 3]
df["sentiment"] = df.Score.replace(
    {1: "negative", 2: "negative", 4: "positive", 5: "positive"}
)


def evaluate_embeddings_approach():
    def label_score(review_embedding):
        return cosine_similarity(
            review_embedding, positive_review_in_t5
        ) - cosine_similarity(review_embedding, negative_review_in_t5)

    probas = df["t5_embedding"].apply(lambda x: label_score(x))
    preds = probas.apply(lambda x: "positive" if x > 0 else "negative")

    report = classification_report(df.sentiment, preds)
    print(report)


evaluate_embeddings_approach()
