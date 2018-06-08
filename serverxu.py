#-*-coding:utf-8-*-
import socket
import os
import json
import struct

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#定义socket类型
host='192.168.137.77'
port=51110
buffersize=1024

s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#重用端口
s.bind((host,port))#建立连接
s.listen(5)#监听，数字表示等待连接的最大数量

c,addr=s.accept()#阻塞，等待客户端的连接
print("开始通话")
while True:
    print("等待选择")
    accept_data=str(c.recv(1024),encoding="utf8")#用UFT8解码
    if accept_data=="1":
        print("对方选择传文件")
        if not c:
            print('客户端连接中断')
            break
        filemesg=input('请输入要传送的文件名：').strip()
        filesize_bytes=os.path.getsize(filemesg)#文件大小
        filename=filemesg+'new'
        dirc={
            'filename':filename,
            'filesize_bytes':filesize_bytes,
        }
        head_info=json.dumps(dirc)#把python对象编码成json字符串
        head_info_len=struct.pack('i',len(head_info))#打包
        c.send(head_info_len)
        c.send(head_info.encode('utf-8'))#编码
        with open(filemesg,'rb') as f:
            data=f.read()
            c.sendall(data)
        print('发送成功')
    else:
        if accept_data=="2":
            print("对方选择对话")
            while True:
                accept_data=str(c.recv(1024),encoding="utf8")
                print("Client:",accept_data)
                if accept_data=="stop":
                    break
                send_data=input("I(Server):")
                c.sendall(bytes(send_data,encoding="utf8"))
        else:
            if accept_data =="3":
                break
c.close()
