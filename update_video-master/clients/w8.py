from base64 import encode
import socket
import os
import shutil
import logging
import subprocess


logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


""" Переменные"""
""" /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ """
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
sock.bind(('', 55000))  # связываем сокет с портом, где он будет ожидать сообщения
sock.listen(30)  # указываем сколько может сокет принимать соединений

path_video_TV = "C:\\video\\"
file_path = f"\\\\192.168.100.92\\public\\video\\all"
console_command = "start vlc C:\\video --fullscreen --loop"
console_kill = "taskkill /im vlc.exe"
#console_command = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe C:\\video --fullscreen --loop"
my_ip = socket.gethostbyname(socket.getfqdn())
""" /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ """


def check_video_tv(data):
    video_names = os.listdir(path_video_TV)
    fb_test = ''
    for video in video_names:
        if fb_test == '':
            fb_test += f"{video}"
        else:
            fb_test += f"____{video}"
    # print(fb_test)
    # print(video_names)
    return fb_test
    # if sorted(data) == sorted(video_names):
    #     return True
    # else:
    #     # parse_video() ??
    #     return video_names


def download_video_TV(data):
    try:
        print(f'Начало загрузки файла {data}')
        shutil.copy2(f'{file_path}\\{data}', f'{path_video_TV}')
        return f'Загрузка {data} на хосте: {my_ip} - OK'
    except shutil.Error as err:
        return f'Ошибка загрузки файла: {data} на хосте: {my_ip}\n{err}'


def delete_video_TV(data):
    try:
        print(f'Starting delete {data} на хосте {my_ip}')
        os.remove(f'{path_video_TV}\\{data}')
        return f'Удаление {data} на хосте {my_ip}- OK'
    except:
        return f'Ошибка удаление файла: {data} на хосте: {my_ip}'


def parse_video(data):  # for what?!
    videos_on_tv = []
    for filename in os.listdir(path=path_video_TV):
        videos_on_tv.append(filename)
    #feed_back = f'DownloadVideo {data} на хосте {my_ip}- OK'
    print(videos_on_tv)
    return videos_on_tv


def play_video():
    os.system(console_command)
    #subprocess.run(console_command)


def kill_vlc():
    os.system(console_kill)


while True:
    connect, addr = sock.accept()
    print(addr)
    bytes_data = connect.recv(1024)
    received_data = bytes_data.decode('UTF-8').split('_____')
    data_check = received_data.pop(0)
    data = received_data[0]
    print(data)
    if data_check == 'CheckOldVideo':
        videos = check_video_tv(data)
        feedback = videos
    elif data_check == 'DownloadVideo':
        feedback = download_video_TV(data)
    elif data_check == 'DeleteVideo':
        feedback = delete_video_TV(data)
    elif data_check == 'ParseVideo':
        feedback = parse_video(data)
    elif data_check == 'Play':
        play_video()
        feedback = 'Видео запущено'
    elif data_check == 'Stop':
        kill_vlc()
        feedback = 'VLC закрыт'
    # elif data_check == 'CheckPlaylist':
    #     pass
    else:
        print(data)
    data_send = str(feedback)
    connect.send(bytes(data_send, encoding='UTF-8'))
    connect.close()
