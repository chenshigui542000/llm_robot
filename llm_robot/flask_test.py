from flask import Flask
import generate_code
app = Flask(__name__)
import sounddevice as sd
import soundfile as sf
import os
import speech_recognition as sr
import sys
import pyttsx3
import json
import generate_data_plus


#训练数据的数量
TEST_COUNT = 0
TEST_PATH = "test_data"


sys.path.append('./google-servicecount.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./google-servicecount.json"

prompt = f""""

    假设你是一个圆形底盘可移动机器人，可调用的指令有：
    move_ahead(distance),distance为移动距离，执行该指令可向前移动distance的距离。
    move_back(distance),distance为移动距离，执行该指令可向后移动distance的距离。
    turn_left(angle),angle为向左转的角度，执行该指令可将机器人向左转动angle的角度。
    turn_right(angle),angle为向右转的角度，执行该指令可将机器人向右转动angle的角度。
    bridge_api.nav2positon(position_x, positon_y, positon_z, orientation_x, orientation_y, orientation_z, orientation_w),position_x, positon_y, positon_z分别为目标点的x轴y轴和z轴坐标，orientation_x, orientation_y, orientation_z, orientation_w是表示机器人朝向的四元数，执行该指令可将机器人导航到目标点位，同时满足其四元数对应的朝向。
    帮我去拿一瓶水，就需要移动到水瓶的坐标，水瓶的坐标（xyz加四元数）:(1.84, 1.01, 0, 0, 0, -0.2, 0.979)
    向左前方移动就是先向左转45°后，再移动。
    向右前方移动就是先向右转45°后，再移动。
    向左后方移动就是先向左转135°后，再移动。
    向右后方移动就是先向右转135°后，再移动。
    向左走就是先向左转90°后，再移动。
    向右走就是先向右转90°后，再移动。
    注意与左前，和右前的区别

    我接下来会给你一些自然语言指令，请你生成满足指令的控制代码。
    在回答的过程中，不需要你解析指令，这一部分如果回答，请在每一回答前加上#
    具体的控制代码，每一条控制代码，单独占一行，且每行代码前不能有#

    如果出现类似于回来吧，回到起点，返回，下面是一个示例：
    之前你的移动是：
    move_ahead(1)
    turn_right(45)
    move_ahead(1)
    发出回来吧，你的指令是：
    move_back(1)
    turn_left(45)
    move_back(1)

    另一个示例：
    之前你的移动：
    move_ahead(1)
    turn_right(90)
    move_ahead(1)
    turn_left(90)
    move_ahead(1)
    发出回来吧，你的响应指令是：
    move_back(1)
    turn_right(90)
    move_back(1)
    turn_left(90)
    move_back(1)

    “”“
    在回答过程中，将所有文字解释写成代码的注释，不要将文字单独放置在注释以外的地方。不需要解析指令，只需要生成控制代码。
    在生成控制代码的时候，只需要生成最近一条指令即可，不要将之前生成过的代码，在当前控制代码之前再执行一遍。
    回到起始点，或者回来一类的词，均是指回到第一次出发的地方。
    
    记住以上部分是代码段的部分，我还希望你可以与我交互，用自然语言回复我，比如
        我让你去拿一个瓶子，那么你不知道瓶子的位置，这时候你就需要问我文字的详细信息，然后
        得到这些详细信息之后再去拿瓶子。
    返回的格式一定是一个json格式，比如：
        我给你的指令是：向前移动一个单位
        那么你的回复是一个json格式，并且这个json格式中包括两个字段，
        具体为：
            "code" : "move_ahead(1)",
            "reply": "好的，我将向前移动1一个单位"
        注意：回答的一定是json格式，code字段中就只有代码，不能其他的内容，reply字段中是你有自然有语言回复我的内容，除此之外不能有除了这两个内容之外的其他内容。
        
    ”“”

    

    你准备好了吗？

    """



messages = [{"role": "system", "content": prompt}]

@app.route('/', methods = ['GET'])
def test():
    messages = [{"role": "user", "content": "你好"}]
    response = generate_code.generate_response(messages)
    return "hello"


def voice2text():
    # 用客户端麦克风录音
    # 设置录音参数
    duration = 5  # 录音时长（单位：秒）
    samplerate = 16000  # 采样率
    filename = "recording.wav"  # 文件名

    # 开始录音
    print("开始录音...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()  # 等待录音完成

    # 删除之前的录音文件（如果存在）
    if os.path.exists(filename):
        os.remove(filename)

    # 保存录音为.wav文件
    sf.write(filename, recording, samplerate)

    # 发送文件数据
    file_name = 'recording.wav'
    r = sr.Recognizer()

    with sr.AudioFile(file_name) as source:
        audio_data = r.record(source)

    data = r.recognize_google(audio_data, language='zh_CN')

    # #播放音频
    # sd.play(recording, samplerate)
    # sd.wait()
    print(data)
    return data


def text2voice(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def data2gpt():
    files = os.listdir(TEST_PATH)
    file_num = len(files)

    for i in range(0,file_num):
        file_name = os.path.join(TEST_PATH,"test" + str(i) + ".json")
        file = open(file_name, 'r', encoding='utf-8')
        file_data = file.read()
        obj = json.loads(file_data)
        print(obj)
        messages.append({"role": "user", "content": obj[0]['question']})
        messages.append({"role": "assistant", "content": obj[1]['answer']})




if __name__ == '__main__':
    #request = voice2text()

    #从文件中获取训练数据
    # file = open('test_data.json', 'r', encoding='utf-8')
    # file_data = file.read()



    #直接用数据生成器生成数据
    question_count = input("训练问题数量：")
    obj = json.loads(generate_data_plus.get_train_data(int(question_count)))


    #将之前的数据喂给gpt
    data2gpt()


    for i in range(0,len(obj)):
        #读出其中一个训练数据
        request = obj["question" + str(i)]

        print("提出来的问题: " + request)
        #将这个数据加入到messages中

        messages.append({"role": "user", "content": request})

        #获取gpt回复的信息
        response = generate_code.generate_response(messages)


        #将回复的信息转成json格式
        data_json = json.loads(response)


        code_data = data_json["code"]

        messages.append({"role": "assistant", "content": response})

        reply_data = data_json["reply"]


        #开始判断是否要将这次训练的数据写入到data中

        print("得到的回答：\n" + response)

        user_ans = input("\n是否要将本次训练的数据加入的data中（y|n):")
        print("\n\n")

        if user_ans == "y":

            files = os.listdir(TEST_PATH)
            TEST_COUNT = len(files)

            test_file_name = "test"+str(TEST_COUNT) + ".json"

            TEST_COUNT = TEST_COUNT + 1
            test_file_path = os.path.join(os.getcwd(),TEST_PATH, test_file_name)

            print(test_file_path)
            if not os.path.exists(test_file_path):
                test_data = []
                test_data.append({"question": request})
                test_data.append({"answer": response})


                with open(test_file_path, 'w', encoding='utf-8') as f:
                    json.dump(test_data,f,ensure_ascii=False)









    # text2voice(reply_data)

    #app.run(host='192.168.1.20' , port = 5002, debug=True)
    #app.run()