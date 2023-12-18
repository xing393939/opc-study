import openai
import os
import pandas as pd
from util import cosine_similarity, get_embedding

# 获取访问open ai的密钥
openai.api_base = "https://api.aiproxy.io/v1"
openai.api_key = os.getenv("OPENAI_API_KEY")
# 选择使用最小的ada模型
EMBEDDING_MODEL = "text-embedding-ada-002"

datafile_path = "data/fine_food_reviews_with_embeddings_1k.parquet"
df = pd.read_parquet(datafile_path)
df = df[df.Score != 3]
df["sentiment"] = df.Score.replace(
    {1: "negative", 2: "negative", 4: "positive", 5: "positive"}
)

from sklearn.metrics import classification_report


def evaluate_embeddings_approach(
    labels=["negative", "positive"],
    model=EMBEDDING_MODEL,
):
    label_embeddings = [get_embedding(label, engine=model) for label in labels]

    def label_score(review_embedding, label_embeddings):
        return cosine_similarity(
            review_embedding, label_embeddings[1]
        ) - cosine_similarity(review_embedding, label_embeddings[0])

    probas = df["embedding"].apply(lambda x: label_score(x, label_embeddings))
    preds = probas.apply(lambda x: "positive" if x > 0 else "negative")

    report = classification_report(df.sentiment, preds)
    print(report)


evaluate_embeddings_approach(
    labels=[
        "An Amazon review with a negative sentiment.",
        "An Amazon review with a positive sentiment.",
    ]
)
