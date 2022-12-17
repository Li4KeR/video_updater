""" Принимает список видео с сервера, сравнивает со списком видео в папке.
    Если есть различия, то выполняет функцию download или delete.
    Так же ожидает прием функции для перезагрузки пк, пинги и тп. """




while True:
    conn, addr = sock.accept()  # начинаем принимать соединения
    data = conn.recv(1024)  # принимаем данные от клиента, по 1024 байт
    data = data.decode('UTF-8') # переводим байт-код в UTF-8
    kab_num = data.split('@')[0]
    kab_data = data.split('@')[1]
    for cab in cabs:
        if cab.cab == kab_num: 
            cab.get_schedule() # запускаем метод из logic.py
            cab.check_status() # запускаем метод из logic.py
            data = f'{cab.data};{cab.status}'
            if data != kab_data:
                conn.send(bytes(data, encoding = 'UTF-8'))
    conn.close()