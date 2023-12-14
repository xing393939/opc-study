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

# 统计每个cluster的数量
new_df = embedding_df.groupby("cluster")["cluster"].count().reset_index(name="count")

# 统计这个cluster里最多的分类的数量
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

# 输出结果
from IPython.display import display

head5 = embedding_df[:5].drop("embedding", axis=1)
display(head5)
display(new_df)
