import os
import socket


# сравнение 2х списков, вернуть итемы, которые только в 1 списке. В БУДУЩЕМ ПЕРЕПИСАТЬ!
def compare_lists(list_1, list2):
    cache_list = []
    for item in list_1:
        if item not in list2:
            cache_list.append(item)
    return cache_list


def ping_nuke(ip):
    response = os.system(f"ping -n 1 {ip}")
    print(response)
    if response == 0:
        return True


def download():
    pass


# принимает 2 списка. 1 список для загрузки на нюк, 2 список для удаления.
# если есть в 1 списке, но нет во 2, то загрузка на нюк
# если есть во 2 списке, но нет в 1, то удаление с нюка

""" сокет для связи с нюком. передается в формате {КОМАНДА}_____{ПЕРЕМЕННЫЕ}
        СПИСОК КОМАНД:
            CheckOldVideo
            DownloadVideo_____{имя файла} - загрузить файла на нюк с шары. 
            DeleteVideo_____{имя файла} - удалить файл на нюке.
            ParseVideo
 """
def send_data(ip, send):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 55000))
    data_send = f'{send}'
    sock.send(bytes(data_send, encoding='UTF-8'))
    data_rec = sock.recv(1024).decode('UTF-8')
    print(data_rec)
    sock.close()
    return data_rec
