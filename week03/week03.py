import ipaddress
import json
import multiprocessing as mp
import socket
import sys
import os

# 异常自定义
class CustomizeError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


# 扫描 IP 段
ipLists = []


def ping_ip(ip, file, lock):
    print(f"进程(ID:{os.getpid()})开始扫描" + ip)
    ret = os.popen('ping -c 1 %s' % ip).read()
    if ret.upper().find('TTL') >= 0:
        ipLists.append(ip)
        try:
            lock.acquire()
            with open(file, "a+", encoding="utf-8") as json_file:
                json.dump(ipLists, fp=json_file, ensure_ascii=False)
                json_file.write("\n")
                json_file.close()
        except IOError:
            print("文件操作失败!")
        finally:
            lock.release()
        print("%s 可以 ping 通!" % ip)
    else:
        print("%s 不可以 ping 通!" % ip)

    print("存活 IP 有:", ipLists)


def tcp_port(ip, port, file, lock):
    print(f"进程 (ID:{os.getpid()}) 开始扫描" + ip + f"端口: %s" % port)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if result == 0:
            try:
                lock.acquire()
                portlist = {
                    "ip": ip,
                    "port": port,
                }
                with open(file, "a+", encoding="utf-8") as json_file:
                    print('%s :' % ip + '%s 端口开启！' % port)
                    json.dump(portlist, fp=json_file, ensure_ascii=False)
                    json_file.write("\n")
                    json_file.close()
            except IOError:
                print("文件操作失败!!!")
            finally:
                lock.release()
        else:
            print("端口关闭!")
    except Exception as err:
        print("error:", err)


if __name__ == '__main__':
    n = ""
    f = ""
    w = ""
    ip_list = []
    mutex = mp.Manager().RLock()
    cpu_count = mp.cpu_count()
    print("最大进程数:", cpu_count)
    mp_pool = mp.Pool(cpu_count)
    # 获取 s 命令行参数列表
    args = sys.argv
    # 处理命令行参数
    for i in range(1, len(args)):
        arg = args[i]
        if arg == '-n':
            n = args[i + 1]
            if int(n) > cpu_count:
                raise CustomizeError("进程数过多，应小于 %s 个！" % cpu_count)
        elif arg == '-f':
            f = args[i + 1]
        elif arg == '-ip':
            ip_list = args[i + 1].split("-")
            if len(ip_list) == 1:
                start_ip = ip_list[0]
                if [1] * 4 != [x.isdigit() and 0 <= int(x) <= 255 for x in start_ip.split(".")]:
                    raise CustomizeError("不合法的 IP !!!")
            else:
                start_ip = ip_list[0]
                if [1] * 4 != [x.isdigit() and 0 <= int(x) <= 255 for x in start_ip.split(".")]:
                    raise CustomizeError("不合法的 IP !!!")
                end_ip = ip_list[1]
                start_addr = ipaddress.IPv4Address(start_ip)
                end_addr = ipaddress.IPv4Address(end_ip)
                if start_addr >= end_addr:
                    raise CustomizeError("IP 范围不合法!!!")
        elif arg == '-w':
            w = args[i + 1]

    if len(ip_list) == 1:
        if f == 'ping':
            w = 'result.json'
            mp_pool.apply_async(ping_ip, args=(start_ip, w, mutex))
        if f == 'tcp':
            for port in range(1, 1024):
                mp_pool.apply_async(tcp_port, args=(start_ip, port, w, mutex))
    elif len(ip_list) == 2:
        if f == 'ping':
            w = 'result.json'
            for i in range(int(start_ip.split(".")[-1]), int(end_ip.split(".")[-1]) + 1):
                ip = start_ip[:start_ip.rfind('.') + 1] + str(i)
                mp_pool.apply_async(ping_ip, args=(ip, w, mutex))
        if f == 'tcp':
            for i in range(int(start_ip.split(".")[-1]), int(end_ip.split(".")[-1]) + 1):
                ip = start_ip[:start_ip.rfind('.') + 1] + str(i)
                for port in range(3300, 3310):
                    mp_pool.apply_async(tcp_port, args=(ip, port, w, mutex))
    mp_pool.close()
    mp_pool.join()
