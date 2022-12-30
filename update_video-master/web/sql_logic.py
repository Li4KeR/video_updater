import sqlite3
from datetime import datetime


# проверяем есть ли бд, таблицы и тп
def sql_check_sql():
    try:
        conn = sqlite3.connect('base.sqlite3')
        cursor = conn.cursor()
        # таблица для видео
        cursor.execute("""CREATE TABLE IF NOT EXISTS video(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    full_name TEXT);
                    """)
        # таблица для нюков
        cursor.execute("""CREATE TABLE IF NOT EXISTS nuke(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    ip TEXT NOT NULL UNIQUE,
                    comment TEXT);
                    """)
        # таблица для ассоциации видео на нюках
        cursor.execute("""CREATE TABLE IF NOT EXISTS linking(
                    id INTEGER PRIMARY KEY,
                    id_nuke  INTEGER REFERENCES nuke (id) ON DELETE CASCADE,
                    id_video INTEGER REFERENCES video (id) ON DELETE CASCADE);
                    """)
        conn.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
        #f = open(log_path,'w')
        #f.write(str(error_text))
        return False


# добавить новый нюк в бд (стр. create_nuke)
def sql_add_nuke(nuke_name, nuke_ip, comment):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(f'INSERT INTO nuke(name, ip, comment) VALUES("{nuke_name}", "{nuke_ip}", "{comment}")')
        conn.commit()
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    cursor.close()


# добавляем новое видео в бд (стр. create_video)
def sql_add_video(name, full_name):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(f'INSERT INTO video(name, full_name) VALUES("{name}", "{full_name}")')
        conn.commit()
    except sqlite3.Error as error:
        print(error)
    cursor.close()


# получениt имени нюка по айди (стр edit, about)
def sql_get_name_nuke(id):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        name = cursor.execute(f'SELECT name FROM nuke where id="{id}"').fetchall()[0]
        return name[0]
    except sqlite3.Error as error:
        print(error)
    cursor.close()


# создание ассоциации видео и нюка (стр. edit)
def sql_create_link_video_and_nuke(id_nuke, id_video):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(f'INSERT INTO linking(id_nuke, id_video) VALUES("{id_nuke}", "{id_video}")')
        conn.commit()
        ip_nuke = cursor.execute(f'SELECT ip FROM nuke where id="{id_nuke}"').fetchall()[0]
        video_name = cursor.execute(f'SELECT name FROM video where id="{id_video}"').fetchall()[0]
        full_name = cursor.execute(f'SELECT full_name FROM video where id="{id_video}"').fetchall()[0]
        return ip_nuke[0], video_name[0], full_name[0]
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    cursor.close()


# удаление ассоциации нюка и видео (стр. edit)
def sql_delete_link_video_and_nuke(id_nuke, id_video):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(f'DELETE FROM linking WHERE id_nuke="{id_nuke}" AND id_video="{id_video}"')
        conn.commit()
        ip_nuke = cursor.execute(f'SELECT ip FROM nuke where id="{id_nuke}"').fetchall()[0]
        # print(ip_nuke)
        video_name = cursor.execute(f'SELECT name FROM video where id="{id_video}"').fetchall()[0]
        # print(video_name)
        full_name = cursor.execute(f'SELECT full_name FROM video where id="{id_video}"').fetchall()[0]
        # print(full_name)
        return ip_nuke[0], video_name[0], full_name[0]
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    cursor.close()


# получение ассоциации, НЕ ИСПОЛЬЗУЕТСЯ, ВОЗМОЖНО УДАЛИТЬ
def sql_all_linking():
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM linking')
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    cursor.close()


# получение всех видео в ассоциациях с нюком (стр about, edit)
def sql_get_all_video_on_nuke(id_nuke):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    print(id_nuke)
    try:
        all_videos_on_nuke = cursor.execute(f"""SELECT video.name FROM linking, nuke, video
        where linking.id_nuke=nuke.id and linking.id_video=video.id and linking.id_nuke='{id_nuke}'""").fetchall()
        video_on_nuke = []
        for video in all_videos_on_nuke:
            print(video)
            video_on_nuke.append(video[0])
        print(video_on_nuke)
        return video_on_nuke
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    cursor.close()


# получение всех нюков (стр. index)
def sql_get_all_nukes():
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        nukes = cursor.execute(f'SELECT * from nuke').fetchall()
        nuke = {}
        for item in nukes:
            id_nuke = item[0]
            name = item[1]
            ip = item[2]
            comment = item[3]
            nuke[name] = {'ip_nuke': ip, 'name': name, 'id_nuke': id_nuke, 'comment': comment}
        return nuke
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    cursor.close()


# получение всех видео (стр. edit)
def sql_get_all_videos():
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        videos = cursor.execute(f'SELECT * from video').fetchall()
        return videos
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)


# получение названия видео. НЕ ИСПОЛЬЗУЕТСЯ, ВОЗМОЖНО УДАЛИТЬ
def sql_select_nuke(id):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()

    videos = []
    video_4_nuke = cursor.execute(f'SELECT name FROM video where "{id}" = 1').fetchall()
    for video in video_4_nuke:
        videos.append(video[0])
    return videos


# получение всех id видео из ассоциаций для нюка (стр. edit)
def sql_all_video_on_nuke(id_nuke):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        all_videos_on_nuke = cursor.execute(f"""SELECT video.id FROM linking, nuke, video
        where linking.id_nuke=nuke.id and linking.id_video=video.id and linking.id_nuke='{id_nuke}'""").fetchall()
        video_on_nuke = []
        for video in all_videos_on_nuke:
            video_on_nuke.append(str(video[0]))
        return video_on_nuke
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    cursor.close()


# получение всех id видео из ассоциаций для нюка (стр. edit)
def sql_all_video_on_nuke(id_nuke):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        all_videos_on_nuke = cursor.execute(f"""SELECT video.full_name FROM linking, nuke, video
        where linking.id_nuke=nuke.id and linking.id_video=video.id and linking.id_nuke='{id_nuke}'""").fetchall()
        video_on_nuke = []
        for video in all_videos_on_nuke:
            video_on_nuke.append(str(video[0]))
        return video_on_nuke
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    cursor.close()

# получение ip нюка для кнопки ping
def sql_ip_nuke(id):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        ip_nuke = cursor.execute(f'SELECT ip FROM nuke WHERE id="{id}"').fetchall()
        return ip_nuke[0]
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    cursor.close()


# получение айди видео по имени
def sql_id_from_name_video(full_name):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    id_video = cursor.execute(f'SELECT id FROM video WHERE full_name="{full_name}"').fetchall()[0]
    return id_video[0]


# запрос для кнопки синхронизации видео
def sql_sync_video(name_video):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO video(name, full_name) VALUES("{name_video}", "{name_video}")')
    conn.commit()
    cursor.close()


# все видео + имена
def sql_all_test_video():
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    all_video = cursor.execute(f'SELECT video.id, video.name, video.full_name from video, linking WHERE video.id=linking.id_video').fetchall()
    cursor.close()
    return all_video


# список всех видео для нюка. в формате id_video, video_name, full_name
def sql_get_all_video_on_nuke(id_nuke):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    all_videos = cursor.execute(f"""SELECT video.id, video.name, video.full_name FROM linking, video 
    WHERE video.id = linking.id_video AND linking.id_nuke={id_nuke}""").fetchall()
    return all_videos


def sql_get_info_video_from_id(video_id):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    info_video = cursor.execute(f"""SELECT * FROM video WHERE id={video_id}""").fetchall()
    return info_video[0]
