import json
import tiktoken # for token counting
import numpy as np
from collections import defaultdict


data_path = "mydata.jsonl"

# Load the dataset
with open(data_path, 'r', encoding='utf-8') as f:
    dataset = [json.loads(line) for line in f]

# Initial dataset stats
# print("Num examples:", len(dataset))
# print("First example:")
# for message in dataset[0]["messages"]:
#     print(message)