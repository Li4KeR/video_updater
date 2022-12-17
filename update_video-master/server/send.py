from base64 import encode
import socket



ip = '10.4.20.150'
port = 55000
send = 'CheckOldVideo_test2.txt_test.txt'


def send_data(ip, port, send):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    data_send = f'{send}'
    sock.send(bytes(data_send, encoding = 'UTF-8'))
    data_rec = sock.recv(1024).decode('UTF-8')
    print(data_rec)
    sock.close()


send_data(ip, port, send)


