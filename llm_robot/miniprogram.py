import wave
import requests
import time
import base64
from pyaudio import PyAudio, paInt16
import gradio as gr
import socket
import bridge_api
import threading
import time
import math
import socketio
from flask import Flask, request
import voice2text
import generate_code
import sys
import select

position_x = None
position_y = None
orientation_x = None
orientation_y = None
orientation_z = None
orientation_w = None
initial_angle = None  # 初始角度
current_angle = None  # 实时更新的角度
current_angle_0 = 0  # 用来保存current_angle的上一次更新值
initial_position_x = None
initial_position_y = None
current_position_x = None
current_position_y = None

app = Flask(__name__)

def socket_io_thread():
    # 创建Socket.IO客户端实例
    sio = socketio.Client()

    # Socket.IO服务器地址和端口号
    socket_url = 'http://192.168.200.118:8005'

    # 定义事件名称
    odom_subscribe_event = 'odomSubscribe'

    # 连接到Socket.IO服务器
    @sio.event
    def connect():
        # 发送订阅请求
        sio.emit(odom_subscribe_event, "")

    # 接收服务器响应
    @sio.on('odom')
    def handle_response(data):
        global position_x, position_y, orientation_x, orientation_y, orientation_z, orientation_w, initial_angle, current_angle
        global initial_position_x, initial_position_y, current_position_x, current_position_y

        pose = data['pose']['pose']
        # print("ENTER", pose)
        # 在这里处理服务器响应
        position = pose['position']
        orientation = pose['orientation']

        position_x = position['x']
        position_y = position['y']
        orientation_x = orientation['x']
        orientation_y = orientation['y']
        orientation_z = orientation['z']
        orientation_w = orientation['w']
        # angle_0 = bridge_api.calculate_rotation_angle(orientation_w, orientation_x, orientation_y, orientation_z)
        # angle_0 = bridge_api.calculate_rotation_angle(orientation_x, orientation_y, orientation_z, orientation_w)
        # print(angle_0)
        # print(orientation_w, orientation_x, orientation_y, orientation_z)
        if initial_angle is None:
            # 计算初始角度
            time.sleep(0.001)
            initial_angle = bridge_api.calculate_rotation_angle(orientation_x, orientation_y, orientation_z,
                                                                orientation_w)

        if initial_position_x is None:
            time.sleep(0.001)
            # 获取初始x坐标
            initial_position_x = position_x

        if initial_position_y is None:
            time.sleep(0.001)
            # 获取初始y坐标
            initial_position_y = position_y

        # 更新实时角度
        current_angle = bridge_api.calculate_rotation_angle(orientation_x, orientation_y, orientation_z, orientation_w)

        # 更新实时位置坐标
        current_position_x = position_x
        current_position_y = position_y

        # 保存上一次更新的角度
        # current_angle_0 = current_angle

        # print(current_angle)
        # print(initial_angle)

    # 启动Socket.IO客户端
    sio.connect(socket_url)

    def get_current_angle():
        return current_angle

    def get_current_position_x():
        return current_position_x

    def get_current_position_y():
        return current_position_y

    def update_thread():
        update_current_angle()
        update_current_position()

    # 更新当前角度的函数
    def update_current_angle():
        global current_angle, initial_angle, current_angle_0
        previous_angle = None
        while True:
            # 这里假设bridge_api提供了一个获取当前角度的函数get_current_angle()
            angle = get_current_angle()
            if angle is not None:
                current_angle = float(angle)
                if previous_angle is not None:
                    # 更新上一次更新的角度
                    current_angle_0 = previous_angle
                previous_angle = current_angle
                # print(current_angle - current_angle_0)

                # 角度到达-180°后，会变为+180°，将初始角+360°，保证不影响角度判定
                if current_angle - current_angle_0 > 300:
                    initial_angle += 360
            time.sleep(0.01)

    # 更新当前的位置坐标
    def update_current_position():
        global current_position_x, current_position_y
        while True:
            current_position_x = get_current_position_x()
            current_position_y = get_current_position_y()
            time.sleep(0.01)
    # 创建并启动更新当前角度的线程
    update_thread = threading.Thread(target=update_thread)
    update_thread.start()

    # 等待一段时间
    time.sleep(0.1)

    # 等待Socket.IO连接完成
    sio.wait()

# 启动Socket.IO客户端的线程
socket_io_thread = threading.Thread(target=socket_io_thread)
socket_io_thread.start()
# # Socket.IO服务器地址和端口号
# socket_url = 'http://192.168.1.238:8005'
#
# # 定义事件名称
# odom_subscribe_event = 'odomSubscribe'
#
# # 创建Socket.IO客户端实例
# sio = socketio.Client()


# # 连接到Socket.IO服务器
# @sio.event
# def connect():
#     # 发送订阅请求
#     sio.emit(odom_subscribe_event, "")
#
#
# # 接收服务器响应
# @sio.on('odom')
# def handle_response(data):
#     global position_x, position_y, orientation_x, orientation_y, orientation_z, orientation_w, initial_angle, current_angle
#     global initial_position_x, initial_position_y, current_position_x, current_position_y
#
#     pose = data['pose']['pose']
#     # print("ENTER", pose)
#     # 在这里处理服务器响应
#     position = pose['position']
#     orientation = pose['orientation']
#
#     position_x = position['x']
#     position_y = position['y']
#     orientation_x = orientation['x']
#     orientation_y = orientation['y']
#     orientation_z = orientation['z']
#     orientation_w = orientation['w']
#     # angle_0 = bridge_api.calculate_rotation_angle(orientation_w, orientation_x, orientation_y, orientation_z)
#     # angle_0 = bridge_api.calculate_rotation_angle(orientation_x, orientation_y, orientation_z, orientation_w)
#     # print(angle_0)
#     # print(orientation_w, orientation_x, orientation_y, orientation_z)
#     if initial_angle is None:
#         # 计算初始角度
#         time.sleep(0.001)
#         initial_angle = bridge_api.calculate_rotation_angle(orientation_x, orientation_y, orientation_z, orientation_w)
#
#     if initial_position_x is None:
#         time.sleep(0.001)
#         # 获取初始x坐标
#         initial_position_x = position_x
#
#     if initial_position_y is None:
#         time.sleep(0.001)
#         # 获取初始y坐标
#         initial_position_y = position_y
#
#     # 更新实时角度
#     current_angle = bridge_api.calculate_rotation_angle(orientation_x, orientation_y, orientation_z, orientation_w)
#
#     # 更新实时位置坐标
#     current_position_x = position_x
#     current_position_y = position_y
#
#     # 保存上一次更新的角度
#     # current_angle_0 = current_angle
#
#     # print(current_angle)
#     # print(initial_angle)
#
#
# # 启动Socket.IO客户端
# sio.connect(socket_url)


# def get_current_angle():
#     return current_angle
#
#
# def get_current_position_x():
#     return current_position_x
#
#
# def get_current_position_y():
#     return current_position_y
#
#
# # 更新当前角度的函数
# def update_current_angle():
#     global current_angle, initial_angle, current_angle_0
#     previous_angle = None
#     while True:
#         # 这里假设bridge_api提供了一个获取当前角度的函数get_current_angle()
#         angle = get_current_angle()
#         if angle is not None:
#             current_angle = float(angle)
#             if previous_angle is not None:
#                 # 更新上一次更新的角度
#                 current_angle_0 = previous_angle
#             previous_angle = current_angle
#             # print(current_angle - current_angle_0)
#
#             # 角度到达-180°后，会变为+180°，将初始角+360°，保证不影响角度判定
#             if current_angle - current_angle_0 > 300:
#                 initial_angle += 360
#         time.sleep(0.01)
#
#
# # 更新当前的位置坐标
# def update_current_position():
#     global current_position_x, current_position_y
#     while True:
#         current_position_x = get_current_position_x()
#         current_position_y = get_current_position_y()
#         time.sleep(0.01)


# 向左转动函数
def turn_left(angle):
    global initial_angle

    # 设置初始角度
    initial_angle = current_angle

    # print(initial_angle)
    # 执行转向动作
    bridge_api.act(0, 0, 0.65)

    # 检查是否达到距离目标角度还剩20度的位置
    while abs(current_angle - initial_angle) < abs(angle-20):
        # print(current_angle - initial_angle)
        time.sleep(0.012)

    # 对转向动作进行减速
    bridge_api.act(0,0,0.3)

    # 阻塞程序，慢速转动，当距离目标角度还剩3度时，程序继续执行
    while angle - abs(current_angle - initial_angle) > 3:
        time.sleep(0.01)

    # 停止转向
    bridge_api.act(0, 0, 0)
    time.sleep(2)

# 向右转动函数
def turn_right(angle):
    global initial_angle

    # 设置初始角度
    initial_angle = current_angle
    # 信号传输延迟，角度裕量
    x = angle / 90

    # 执行转向动作
    bridge_api.act(0, 0, -0.65)

    # 检查是否达到距离目标角度还剩20度的位置
    while abs(current_angle - initial_angle) < abs(angle - 20):
        # print(current_angle - initial_angle)
        time.sleep(0.012)

    # 对转向动作进行减速
    bridge_api.act(0, 0, -0.3)

    # 阻塞程序，慢速转动，当距离目标角度还剩3度时，程序继续执行
    while angle - abs(current_angle - initial_angle) > 3:
        time.sleep(0.01)

    # 停止转向
    bridge_api.act(0, 0, 0)
    time.sleep(2)

# 移动函数
def move_ahead(distance):
    global initial_position_x, initial_position_y

    # 设置初始位置坐标
    initial_position_x = current_position_x
    initial_position_y = current_position_y

    # 检查当前位置是否可用
    while current_position_x is None or current_position_y is None:
        time.sleep(0.01)
    # 执行移动动作
    bridge_api.act(0.2,0,0)

    # 检查是否移动目标距离
    while math.sqrt((current_position_x - initial_position_x)**2 + (current_position_y - initial_position_y)**2) < distance-0.15:
        # print(math.sqrt((current_position_x - initial_position_x)**2 + (current_position_y - initial_position_y)**2))
        time.sleep(0.01)

    #
    bridge_api.act(0.05,0,0)

    #
    while distance - math.sqrt((current_position_x - initial_position_x)**2 + (current_position_y - initial_position_y)**2) > 0.03:
        # print("******")
        # print(math.sqrt((current_position_x - initial_position_x)**2 + (current_position_y - initial_position_y)**2))
        time.sleep(0.01)

    # 停止移动
    bridge_api.act(0,0,0)
    time.sleep(1.5)

def move_back(distance):
    global initial_position_x, initial_position_y

    # 设置初始位置坐标
    initial_position_x = current_position_x
    initial_position_y = current_position_y

    # 检查当前位置是否可用
    while current_position_x is None or current_position_y is None:
        time.sleep(0.01)
    # 执行移动动作
    bridge_api.act(-0.2,0,0)

    # 检查是否移动目标距离
    while math.sqrt((current_position_x - initial_position_x)**2 + (current_position_y - initial_position_y)**2) < distance-0.15:
        # print(math.sqrt((current_position_x - initial_position_x)**2 + (current_position_y - initial_position_y)**2))
        time.sleep(0.01)

    #
    bridge_api.act(-0.05,0,0)

    #
    while distance - math.sqrt((current_position_x - initial_position_x)**2 + (current_position_y - initial_position_y)**2) > 0.03:
        # print("******")
        # print(math.sqrt((current_position_x - initial_position_x)**2 + (current_position_y - initial_position_y)**2))
        time.sleep(0.01)

    # 停止移动
    bridge_api.act(0,0,0)
    time.sleep(1.5)


# def update_thread():
#     update_current_angle()
#     update_current_position()
#
#
# # 创建并启动更新当前角度的线程
# update_thread = threading.Thread(target=update_thread)
# update_thread.start()

# 等待一段时间
time.sleep(0.1)

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
    ”“”

    你准备好了吗？

    """
messages = [{"role": "system", "content": prompt}]

#
# sio.wait()

print('***')


# sio.wait()

@app.route('/', methods=['POST'])
def receive_message():
    content = request.json.get('content')  # 假设微信小程序发送的数据中有一个字段名为content
    print('999')
    if content:
        messages.append({"role": "user", "content": content})
        print('666')
        llm_answer = generate_code.generate_response(messages)
        messages.append({"role": "assistant", "content": llm_answer})
        time.sleep(0.2)
        exec(llm_answer)
    return 'success'

# sio.wait()
print('**')


if __name__ == '__main__':
    app.run(host='192.168.1.20', port=5011)