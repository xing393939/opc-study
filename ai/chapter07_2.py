import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

embedding_df = pd.read_parquet("data/20_newsgroup_with_embedding.parquet")
matrix = np.vstack(embedding_df.embedding.values)
num_of_clusters = 20

kmeans = KMeans(
    n_clusters=num_of_clusters, init="k-means++", n_init=10, random_state=42
)
kmeans.fit(matrix)
labels = kmeans.labels_
embedding_df["cluster"] = labels

# 统计每个cluster里最多的分类的数量
new_df = embedding_df.groupby("cluster")["cluster"].count().reset_index(name="count")
title_count = (
    embedding_df.groupby(["cluster", "title"]).size().reset_index(name="title_count")
)
first_titles = title_count.groupby("cluster").apply(
    lambda x: x.nlargest(1, columns=["title_count"])
)
first_titles = first_titles.reset_index(drop=True)
new_df = pd.merge(
    new_df, first_titles[["cluster", "title", "title_count"]], on="cluster", how="left"
)
new_df = new_df.rename(columns={"title": "rank1", "title_count": "rank1_count"})

import os
import openai

openai.api_base = "https://api.aiproxy.io/v1"
openai.api_key = os.getenv("OPENAI_API_KEY")
items_per_cluster = 10
for i in range(num_of_clusters):
    cluster_name = new_df[new_df.cluster == i].iloc[0].rank1
    print(f"Cluster {i}, Rank 1: {cluster_name}, Theme:", end=" ")

    content = "\n".join(
        embedding_df[embedding_df.cluster == i]
        .text.sample(items_per_cluster, random_state=42)
        .values
    )
    messages = [
        {
            "role": "user",
            "content": f'''我们想要给下面的内容，分组成有意义的类别，以便我们可以对其进行总结。请根据下面这些内容的共同点，总结一个50个字以内的新闻组的名称。比如 “PC硬件”\n\n内容:\n"""\n{content}\n"""新闻组名称：''',
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=128,
        top_p=1,
    )
    print(response["choices"][0]["message"]["content"])
