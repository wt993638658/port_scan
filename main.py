import socket
import multiprocessing
import sys


def ports(port_service):
    #获取常用端口对应的服务名称
    for port in list(range(1,100))+[143,145,113,443,445,3389,8080]:
        try:
            port_service[port] = socket.getservbyport(port)
        except socket.error:
            pass
def ports_scan(host,port_service):
    port_open=[]
    try:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error:
        print('socket create error!')
        sys.exit()
    for port in port_service:
        try:
            sock.connect((host,port))
            port_open.append(port)
            sock.close()
        except socket.error:
            pass
    return port_open
if __name__=='__main__':
    ports_service=dict()
    ports(ports_service)

    pool = multiprocessing.Pool(processes=8)
    net='10.2.1.'
    results=dict()
    for host_number in map(str,range(0,5)):
        host=net+host_number
        results[host]=pool.apply_async(ports_scan,(host,ports_service))
        print('starting '+host+'...')

    pool.close()
    pool.join()

    for host in results:
        print('='*30)
        print(host,'.'*10)
        for port in results[host].get():
            print(port,':',ports_service[port])