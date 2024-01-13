voice2code.py        实现音频输入，输出相应的代码实现。
generate_code.py     调用大模型接口,来返回大模型生成的代码

***
在机器上开两个终端，
npm run start:dev      在后端的sever路径下输入，启后端程序
ros2 launch roscbot_driver roscbot_base.launch.py   无需在任何路径下，启机器底盘的驱动（启动后底盘制动）

在个人笔记本上启下面程序
test.py      在终端实现语音控制机器人，在此脚本开发和测试机器人功能
***

gradio_web.py        利用gradio实现语音控制机器人的网页端实现
miniprogram.py       利用微信小程序实现语音控制机器人