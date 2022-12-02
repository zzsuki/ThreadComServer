import socketserver
import socket
from .settings import PORT_MAP
import logging
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process

class SimpleUDPServer:
    """简单UDP服务器"""

    def __init__(self, host: str, port: int = None,  *args, **kwargs):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.recv_buf = 1024
        

    def recv_and_send(self) -> None:
        """持续接收并返回给客户端相同的数据"""
        logging.info('UDP sock {} start listening...'.format((self.host, self.port)))
        while True:
            try:
                msg, addr = self.sock.recvfrom(self.recv_buf)
                logging.info('Got msg from {}: {}'.format(addr[0], msg))
                self.sock.sendto(msg, addr)
                logging.info('Send return msg to {}: {}'.format(addr[0], msg))
            except Exception as e:
                logging.info('Got exception: {}'.format(e))

    def serve_forever(self) -> None:
        """启动服务器"""
        self.recv_and_send()

    def close(self) -> None:
        """关闭服务器"""

        self.sock.close()

class SimpleTCPRequestHandler(socketserver.BaseRequestHandler):
    """简单的tcp请求处理类，收到消息后返回相同字符"""
    
    def handle(self) -> None:
        """消息处理方法"""
        while True:
            try:
                buf = self.request.recv(1024)
                logging.info('Got msg from {}: {}'.format(self.client_address[0], buf))
                self.request.send(buf)
                logging.info('Return msg to {}: {}'.format(self.client_address[0], buf))
            except Exception as e:
                logging.error('Got exception: {}'.format(e), exc_info=True)
                self.request.close()
                break
                

class ThreadTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """多线程tcp服务器，一个端口可以同时处理多个客户端"""
    daemon_threads: bool = True
    allow_reuse_address: bool = True
    
    def __init__(self, server_address, RequestHandlerClass):
        logging.info('TCP Sock {} Start listening ...'.format(server_address))
        super().__init__(server_address=server_address, RequestHandlerClass=RequestHandlerClass)

        

def run_server(ip: str = "127.0.0.1"):
    """根据port_mapserver"""
    serverlist = []    # 保存进程任务的Future， 调用result可获取结果

    for _, v in PORT_MAP.items():
        if isinstance(v, dict):
            port = v.get("TCP")
            if port:
                server = ThreadTCPServer((ip, port), SimpleTCPRequestHandler)
                serverlist.append(Process(target=server.serve_forever))
            
            port = v.get("UDP")
            if port:
                serverlist.append(Process(target=SimpleUDPServer(ip, port).serve_forever))

    for p in serverlist:
        p.start()

    serverlist[-1].join()
        
