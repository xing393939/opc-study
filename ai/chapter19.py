from openai import OpenAI

# 上传训练数据集并训练
client = OpenAI(base_url="https://api.aiproxy.io/v1")
audio_file = open("./data/podcast_clip.mp3", "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
print(transcript)
