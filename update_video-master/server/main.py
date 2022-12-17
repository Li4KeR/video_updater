""" Сервер собирает инфу из бд, опрашивает нюки по айпи, отправляет список видео. 
    В доп функциях из веб-интерфейса может перезагрузить пк, чекать статус(пинги), изменять
    список видео для каждой машины, останавливать видео, запускать видео.  """


def send_data(self):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    sock.connect((self.ip, self.port))  # подключемся к серверному сокету
    data_send = f'{self.cab_num}@{self.data_recived}' # создаем переменную для отправки
    sock.send(bytes(data_send, encoding = 'UTF-8'))  # отправляем переменную в двоичном формате
    data_rec = sock.recv(1024)  # читаем ответ от серверного сокета
    data_recy = data_rec.decode('UTF-8') # перекодиуем ответ в UTF-8'
    if data_rec == self.data_recived:
        print(data_recy)
    else:
        print(data_recy)
        print(self.data_recived)
        self.data_recived = data_rec
    sock.close() 