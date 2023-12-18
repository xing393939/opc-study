import pandas as pd
import json
from openai import OpenAI

df = pd.read_csv("data/ultraman_stories.csv")
df['sub_prompt'] = df['dynasty'] + "," + df['super_power'] + "," + df['story_type']
prepared_data = df.loc[:, ['sub_prompt', 'story']]
formatted_data = []
for _, chat in df.iterrows():
    messages = [{
        "role": "user",
        "content": chat.sub_prompt
    }, {
        "role": "assistant",
        "content": chat.story
    }]
    formatted_data.append({
        "messages": messages
    })

with open('data/fine_tuning.jsonl', 'w', encoding='utf-8') as file:
    for item in formatted_data:
        file.write(json.dumps(item, ensure_ascii=False))
        file.write('\n')

# 上传训练数据集并训练
client = OpenAI(base_url="https://api.aiproxy.io/v1")
training_file = client.files.create(
    file=open("./data/fine_tuning.jsonl", "rb"),
    purpose="fine-tune"
)
print(training_file.id)
rs = client.fine_tuning.jobs.create(training_file=training_file.id, model="gpt-3.5-turbo")
print(rs)
