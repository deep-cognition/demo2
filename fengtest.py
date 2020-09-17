import subprocess as sp
import cv2
import numpy as np
from openvino.inference_engine import IENetwork, IEPlugin # 导入openvino库

input_size = 256
# 搭建网络，调用IENetwork，返回net对象，参数为xml和bin文件的路径
model_xml_CPU = r'person-detection-retail-0013.xml'
model_bin_CPU = r'person-detection-retail-0013.bin'
net = IENetwork(model=model_xml_CPU, weights=model_bin_CPU)
# 定义输入输出
input_blob = next(iter(net.inputs)) # 迭代器
out_blob   = next(iter(net.outputs))
print(input_blob, out_blob)
n, c, h, w = net.inputs[input_blob].shape
print(n,c,h,w)
# 加载设备，调用IEPlugin，返回设备对象，参数为设备名，如CPU、GPU、MYRIAD
plugin = IEPlugin(device='CPU')
# 加载网络，调用设备对象的load方法，返回执行器，参数为网络
exec_net = plugin.load(network=net) 
print('load ok!')


rtmpUrl="rtmp://192.168.0.155:1935/live/1"
#rtmpUrl="rtmp://113680.livepush.myqcloud.com/live/b1?txSecret=feef165f4e767d7933398b76d8063922&txTime=5F747B4B"
camera_path = "rtsp://admin:jishu123@192.168.0.115:554/h264/ch1/main/av_stream"
cap = cv2.VideoCapture(0)
# Get video information
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# ffmpeg command
command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
           '-i', '-',
           '-c:v', 'libx264',
           '-bf','0',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           rtmpUrl]

# 管道配置
p = sp.Popen(command, stdin=sp.PIPE)
# read webcamera
while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        print("Opening camera is failed")
        break
    img = cv2.resize(frame,(320,544))
    img = np.array(img)
    img = np.expand_dims(img,axis=0)
    img = np.transpose(img,(0,3,1,2)) 
    outputs = exec_net.infer(inputs={input_blob:img})
    print(outputs['detection_out'][0,0,0,:]) 
    p.stdin.write(frame.tostring())
