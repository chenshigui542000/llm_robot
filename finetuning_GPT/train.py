import openai
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "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"


openai.api_key = "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"

client = OpenAI()

training_file = client.files.create(
    file=open("mydata.jsonl", "rb"),
    purpose="fine-tune"
)


print(training_file.id)

