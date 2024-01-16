from openai import OpenAI

import os


#这里加api_key
os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI()

response = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0613:personal::8hRgcE1b",
  messages=[
    {"role": "user", "content": "左转100度，再向左后前进10米，最后向后走10米"}
  ]
)
print(response.choices[0].message.content)