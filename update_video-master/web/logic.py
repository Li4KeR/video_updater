import os
import socket


def compare_lists(list_1, list2):
    cache_list = []
    for item in list_1:
        if item not in list2:
            cache_list.append(item)
    return cache_list


def print_title(title, intro):
    print(title, intro)


def ping_nuke(ip):
    response = os.popen(f"ping {ip} 1").read()
    #response = os.system(f"ping -c 1 {ip}")
    print(response)
    if response == 0:
        return True


def download():
    pass


def send_data(ip, send):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 55000))
    data_send = f'{send}'
    sock.send(bytes(data_send, encoding='UTF-8'))
    data_rec = sock.recv(1024).decode('UTF-8')
    print(data_rec)
    sock.close()
    return data_rec
