import requests
import math
import socketio
import signal
import json

# Socket.IO服务器地址和端口号
socket_url = 'http://192.168.1.238:8005'

#控制速度api，x表示向前速度，y代表向左速度，z代表转动角速度（xy表示机器人所在二维平面坐标系）
#移动速度不要超过0.1，转动速度不要超过0.2
# 调用示例
def act(x, y ,z):
    # 定义事件名称和数据
    event_name = 'cmdvelCSubscribe'
    event_data = {
        "linear_x": x,
        "linear_y": y,
        "angular_z": z
    }
    # 创建Socket.IO客户端实例
    sio = socketio.Client()

    # 连接到Socket.IO服务器
    @sio.event
    def connect():
        # 发送Socket.IO请求
        sio.emit(event_name, event_data)
        #断开连接
        # sio.disconnect()

    # 接收服务器响应
    @sio.on(event_name)
    def handle_response(data):
        print('Received response:', data)
        # 在这里处理服务器响应

    # 启动Socket.IO客户端
    sio.connect(socket_url)

def nav2positon(position_x, positon_y, positon_z, orientation_x, orientation_y, orientation_z, orientation_w):
    # 定义事件名称和数据
    event_name = 'navGoalSend'
    event_data = {
        "goal": {
            "position_x": position_x,
            "position_y": positon_y,
            "position_z": positon_z,
            "orientation_x": orientation_x,
            "orientation_y": orientation_y,
            "orientation_z": orientation_z,
            "orientation_w": orientation_w
        }
    }
    # 创建Socket.IO客户端实例
    sio = socketio.Client()

    # 连接到Socket.IO服务器
    @sio.event
    def connect():
        # 发送Socket.IO请求
        sio.emit(event_name, event_data)
        #断开连接
        # sio.disconnect()

    # 接收服务器响应
    @sio.on(event_name)
    def handle_response(data):
        print('Received response:', data)
        # 在这里处理服务器响应

    # 启动Socket.IO客户端
    sio.connect(socket_url)

def calculate_rotation_angle(x, y, z, w):  #利用四元数来计算机器人绕z轴的旋转角度，方向与x轴重合时为0，向左转为正
    # 计算旋转矩阵中的分量
    R11 = 1 - 2 * (y ** 2) - 2 * (z ** 2)
    R21 = 2 * x * y - 2 * w * z
    R31 = 2 * x * z + 2 * w * y
    R32 = 2 * y * z - 2 * w * x
    R33 = 1 - 2 * (x ** 2) - 2 * (y ** 2)

    # 计算yaw角度
    yaw = math.atan2(R21, R11)  # 使用math.atan2()计算反正切值，返回弧度

    return math.degrees(yaw)  # 将弧度转换为角度并返回




