import numpy as np
from openai import OpenAI

client = OpenAI(base_url="https://api.aiproxy.io/v1")


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_embedding(text, engine="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=engine).data[0].embedding
