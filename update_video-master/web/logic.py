import os
import socket
from sql_logic import *
from app import path_all_video


def logging(log_data):
    with open('log.txt', 'a') as f:
        date_now = datetime.now().strftime("%d.%m.%y %H:%M")
        f.write(f"{date_now} - {log_data}\n")


def logging_errors(log_data):
    with open('error.txt', 'a') as f:
        date_now = datetime.now().strftime("%d.%m.%y %H:%M")
        f.write(f"{date_now} - {log_data}\n")


class Nuke:
    def __init__(self, id_nuke, ip, name, comment):
        self.id = id_nuke
        self.ip = ip
        self.name = name
        self.comment = comment
        self.videos = sql_get_all_video_on_nuke(id_nuke)
        # self.status = self.check_connection()
        self.status = None
        self.status_ping = sql_get_ping_status(self.id)[0]

    def add_video(self, id_video):
        full_info_video = sql_get_info_video_from_id(id_video)
        self.videos.append(full_info_video)
        sql_create_link_video_and_nuke(self.id, id_video)
        full_name_video = full_info_video[2]
        send_data(self.ip, f"DownloadVideo_____{full_name_video}")

    def delete_video(self, id_video):
        sql_delete_link_video_and_nuke(self.id, id_video)
        full_info_video = sql_get_info_video_from_id(id_video)
        self.videos.remove(full_info_video)
        full_name_video = full_info_video[2]
        send_data(self.ip, f"DeleteVideo_____{full_name_video}")

    def check_connection(self):
        try:
            send_data(self.ip, f"CheckConnections_____")
            self.status = True
        except:
            self.status = False

    def stop_video(self):
        send_data(self.ip, 'Stop_____')

    def play_video(self):
        send_data(self.ip, 'Play_____')

    def print_info(self):
        print(f"{self.name}: {self.videos}")

    def sync_video(self):
        pass


# сравнение 2х списков, вернуть итемы, которые только в 1 списке. В БУДУЩЕМ ПЕРЕПИСАТЬ!
def compare_lists(list_1, list2):
    cache_list = []
    for item in list_1:
        if item not in list2:
            cache_list.append(item)
    return cache_list


def ping_nuke(ip):
    response = os.system(f"ping -n 1 -w 10 {ip} > None")
    if response == 0:
        return True
    else:
        return False


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
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.settimeout(0.7)
        sock.connect((ip, 55000))
        data_send = f'{send}'
        sock.send(bytes(data_send, encoding='UTF-8'))
        data_rec = sock.recv(1024).decode('UTF-8')
        sock.close()
        return data_rec
    except socket.error as er:
        logging_errors(f"error {er}: {ip} try {send}")
        return data_rec


def get_all_nukes():
    nukes = sql_get_all_nukes()  # возвращает словарь всех нюков.
    # name{'ip_nuke': ip, 'name': name, 'id_nuke': id_nuke, 'comment': comment}
    all_nukes = []
    for cache_nuke in nukes:
        nuke_object = Nuke(nukes.get(cache_nuke).get('id_nuke'),
                           nukes.get(cache_nuke).get('ip_nuke'),
                           nukes.get(cache_nuke).get('name'),
                           nukes.get(cache_nuke).get('comment'))
        all_nukes.append(nuke_object)
    return all_nukes


def check_playlist_sql_physic(ip_nuke, id_nuke):
    sql_video_on_nuke = sql_get_all_video_name_on_nuke(id_nuke)
    sql_video_on_nuke.sort()  # 2 лист
    video_on_hard_nuke = send_data(ip_nuke, f"CheckPhysicVideos_____").split('____')  # 1 лист
    video_on_hard_nuke.sort()

    not_in_nuke = compare_lists(sql_video_on_nuke, video_on_hard_nuke)
    not_in_mark = compare_lists(video_on_hard_nuke, sql_video_on_nuke)

    for item in not_in_nuke:  # если видео нет на нюке, но помечено маркером
        id_video = sql_id_from_name_video(item)
        ip_nuke, video_name, full_name = sql_get_ip_name_fname(id_nuke, id_video)
        try:
            send_data(ip_nuke, f'DownloadVideo_____{full_name}')
            sql_create_link_video_and_nuke(id_nuke, id_video)
            logging(f' {ip_nuke}: download video {full_name} name {video_name} - OK')
        except:
            logging_errors(f'{ip_nuke}: download {full_name} name {video_name}')
        """ Передача айди нюка и айди видео, отправить команду для скачивания видео и добавления в плейлист """
    for item in not_in_mark:  # если видео есть на нюке, но не помечено маркером
        try:
            id_video = sql_id_from_name_video(item)
            ip_nuke, video_name, full_name = sql_delete_link_video_and_nuke(id_nuke, id_video)
            send_data(ip_nuke, f'DeleteVideo_____{item}')
            logging(f'{ip_nuke}: delete {full_name} name {video_name} - OK')
        except:
            logging_errors(f'{ip_nuke}: delete {full_name} name {video_name}')
        """ передача айди нюка и айди видео, отправить на нюк команду удаления видео """


def delete_video_from_host(video_name):
    try:
        os.remove(f'{path_all_video}\\{video_name}')
        sql_delete_video(video_name)
        logging(f"delete {video_name} from host")
    except os.error as error:
        logging_errors(f"delete {video_name}")
        print(error)
