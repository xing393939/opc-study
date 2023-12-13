import pandas as pd
datafile_path = "data/fine_food_reviews_with_embeddings_1k.parquet"
df = pd.read_parquet(datafile_path)
df["category"] = df.Score.replace(
    {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
)

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


X_train, X_test, y_train, y_test = train_test_split(
    list(df.embedding.values), df.category, test_size=0.2, random_state=42
)
clf = RandomForestClassifier(n_estimators=300)
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
probas = clf.predict_proba(X_test)
report = classification_report(y_test, preds)
print(report)
