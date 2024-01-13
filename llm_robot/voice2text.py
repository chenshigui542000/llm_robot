import os
import sounddevice as sd
import soundfile as sf
import socket
import generate_code
import speech_recognition as sr
def get_text():
    # 用客户端麦克风录音
    # 设置录音参数
    duration = 10  # 录音时长（单位：秒）
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


    print(f"录音已保存为 {filename}")

    # 向后端传.wav文件
    # 创建一个TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 服务端的IP地址和端口
    server_address = ('192.168.1.5', 8888)

    # 连接到服务端
    client_socket.connect(server_address)

    # 发送文件数据
    file_name = 'recording.wav'
    with open(file_name, 'rb') as file:
        # for data in file:
        #     client_socket.sendall(data)
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.sendall(data)

    print('文件发送完成')

    # 文件发送完成后，关闭连接
    client_socket.shutdown(socket.SHUT_WR)

    # 接收服务器返回的识别结果
    result = client_socket.recv(1024)
    print('识别结果:', result.decode())  # result.decode()为语音识别的结果，类型为str

    # 关闭连接
    client_socket.close()

    return result.decode()


