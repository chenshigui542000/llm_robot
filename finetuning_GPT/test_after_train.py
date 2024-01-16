import os
import openai
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "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"


openai.api_key = "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"

client = OpenAI()

client.fine_tuning.jobs.create(
    training_file="file-nG7qkbJWiVWdw8mgS7DmHacd",
    model="gpt-3.5-turbo"
)