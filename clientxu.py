#-*-coding:utf-8-*-
#coding=gbk
import socket
import struct
import json

c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#定义socket类型
host="192.168.137.77"
port=51110
buffersize=1024
c.connect((host,port))#建立服务器的连接
print('等待连接...')
print("开始会话")
print("1：传送文件2：通话3：退出")
print("如果要通话结束，请输入stop")
while True:
    send_data=input("选择：")
    c.sendall(bytes(send_data,encoding="utf8"))#发送内容必须为bytes类型，用uft8格式编码
    if send_data=="1":#传文件
        head_struct=c.recv(4)#接收报头的长度
        if head_struct:#接收到报头
            print('已连接，等待接收数据')
        head_len=struct.unpack('i',head_struct)[0]#解包
        data=c.recv(head_len)#接收长度为head_len的报头内容的信息
        head_dir=json.loads(data.decode('utf8'))#把已编码的json解码成python对象
        filesize_bytes=head_dir['filesize_bytes']#返回参数属性，方法列表
        filename=head_dir['filename']
        recv_len=0
        recv_mesg=b''#以二进制表示
        f=open(filename,"wb")#以二进制写入文件
        while recv_len<filesize_bytes:#收到的长度与缓冲区比较
            if filesize_bytes-recv_len>buffersize:
                recv_mesg=c.recv(buffersize)
                f.write(recv_mesg)
                recv_len+=len(recv_mesg)
            else:
                recv_mesg=c.recv(filesize_bytes-recv_len)
                recv_len+=len(recv_mesg)
                f.write(recv_mesg)
        print(recv_len,filesize_bytes)
        f.close()
        print("文件接收完毕")
    else:
        if send_data=="2":#字符串交互
            while True:
                send_data=input("I(Client):")
                c.sendall(bytes(send_data,encoding="utf8"))
                if send_data=="stop":#stop停止
                    break
                accept_data=str(c.recv(1024),encoding="utf8")#用uft8解码
                print("".join(("Server:",accept_data)))
        else:
            if send_data == "3":
                break
c.close()
print("会话结束")
