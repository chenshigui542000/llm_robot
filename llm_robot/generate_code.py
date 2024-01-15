
import os
from openai import OpenAI


# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"
# openai.api_base = "https://api.closeai-proxy.xyz/v1"
# openai.api_key = "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"


os.environ["OPENAI_API_KEY"] = "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"


# asr = ASRExecutor()
# result = asr(audio_file="received.wav")   #result是对.wav文件的识别结果
# # print(result)
# #
# # result1 = punctuation_model.punctuation(text = result)
# print(result)

client = OpenAI()



def get_completion(messages):
    # # messages = [{"role": "user", "content": prompt}]
    # response = openai.ChatCompletion.create(
    #     model=model,
    #     messages=messages,
    #     temperature=0,   #表示每次回答的随机程度，越接近1,随机性越大, 一般设置为0
    # )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return  completion.choices[0].message.content

def generate_response(messages):
    # asr = ASRExecutor()
    # result = asr(audio_file="received.wav")  # result是对.wav文件的识别结果
    # userinput = result

    # prompt = f""""
    #
    # 假设你是一个圆形底盘可移动机器人，可调用的指令有：
    # move_ahead(distance),distance为移动距离，执行该指令可向前移动distance的距离。
    # move_back(distance),distance为移动距离，执行该指令可向后移动distance的距离。
    # turn_left(angle),angle为向左转的角度，执行该指令可将机器人向左转动angle的角度。
    # turn_right(angle),angle为向右转的角度，执行该指令可将机器人向右转动angle的角度。
    # 我接下来会给你一些自然语言指令，请你生成满足指令的控制代码。
    # 在回答的过程中，不需要你解析指令，这一部分如果回答，请在每一回答前加上#
    # 具体的控制代码，每一条控制代码，单独占一行，且每行代码前不能有#
    #
    # “”“在回答过程中，将所有文字解释写成代码的注释，不要将文字单独放置在注释以外的地方。不需要解析指令，只需要生成控制代码。”“”
    #
    # """
    # messages = [{"role": "user", "content": prompt}]
    response = get_completion(messages)

    return response

# print(generate_response("向前走2米"))
