from base64 import encode
import socket
import os
from ftplib import FTP



""" Переменные"""
""" /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ """
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
sock.bind(('', 55000))  # связываем сокет с портом, где он будет ожидать сообщения
sock.listen(30)  # указываем сколько может сокет принимать соединений

path_video_TV = 'C:\\Users\\ngrigorev\\Documents\\py\\video\\'

ftp_host = 'ftp.example.com'
ftp_user = 'user'
ftp_pass = 'pass'
""" /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ """


def check_video_tv(data):
    video_names = os.listdir(path_video_TV)
    if sorted(data) == sorted(video_names):
        return True
    else:
        #parse_video() ??
        return video_names


def download_video_TV(data):
    try:
        ftp = FTP(ftp_host)
        ftp.login(ftp_user, ftp_pass)
        my_file = open(data, 'wb')
        ftp.retrbinary('RETR ' + data, my_file.write, 1024)
        ftp.quit()
        my_file.close()
        return True
    except:
        return f'Error download to ftp: {data}'


def delete_video_ftp(data):
    try:
        ftp = FTP(ftp_host)
        ftp.login(ftp_user, ftp_pass)
        ftp.delete(data)
        ftp.quit()
        return True
    except:
        return f'Error delete on ftp: {data}'


def delete_video_TV(data):
    try:
        os.remove(f'{path_video_TV}{data}')
        return True
    except:
        return f'Error delete on ftp: {data}'


def parse_video(): # for what?!
    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    ftp.retrlines('LIST')


while True:
    connect, addr = sock.accept()
    print(addr)
    bytes_data = connect.recv(1024)
    data = bytes_data.decode('UTF-8').split('_')
    data_check = data.pop(0)
    print(data)
    if data_check == 'CheckOldVideo':
        videos = check_video_TV(data)
        print(videos)
    elif data_check == 'DownloadVideo':
        download_video_TV(data)
    elif data_check == 'DeleteVideo':
        delete_video_ftp(data)
    elif data_check == 'ParseVideo':
        parse_video(data)
    else:
        print(data)
    data_send = "test_back"
    connect.send(bytes(data_send, encoding = 'UTF-8'))
    connect.close()
