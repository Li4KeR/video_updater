import sqlite3
from datetime import datetime


def check_sql():
    try:
        conn = sqlite3.connect('base.sqlite3')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS video(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    ftp_path TEXT NOT NULL UNIQUE);
                    """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS nuke(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    ip TEXT NOT NULL UNIQUE);
                    """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS linking(
                    id INTEGER PRIMARY KEY,
                    id_nuke  INTEGER REFERENCES nuke (id),
                    id_video INTEGER REFERENCES video (id) );
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


def add_nuke(nuke_name, nuke_ip, comment):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(f'INSERT INTO nuke(name, ip, comment) VALUES("{nuke_name}", "{nuke_ip}", "{comment}")')
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    conn.commit()
    cursor.close()


def add_video(name, full_name):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(f'INSERT INTO video(name, full_name) VALUES("{name}", "{full_name}")')
    except sqlite3.Error as error:
        print(error)
    conn.commit()
    cursor.close()


def name_nuke(id):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        name = cursor.execute(f'SELECT name FROM nuke where id="{id}"').fetchall()
        return name[0]
    except sqlite3.Error as error:
        print(error)
    conn.commit()
    cursor.close()


def create_link_video_and_nuke(id_nuke, id_video):
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


def delete_link_video_and_nuke(id_nuke, id_video):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(f'DELETE FROM linking WHERE id_nuke="{id_nuke}" AND id_video="{id_video}"')
        conn.commit()
        ip_nuke = cursor.execute(f'SELECT ip FROM nuke where id="{id_nuke}"').fetchall()[0]
        video_name = cursor.execute(f'SELECT name FROM video where id="{id_video}"').fetchall()[0]
        full_name = cursor.execute(f'SELECT full_name FROM video where id="{id_video}"').fetchall()[0]
        return ip_nuke[0], video_name[0], full_name[0]
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    cursor.close()


def all_linking():
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM linking')
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    conn.commit()
    cursor.close()


def linking_nuke(id_nuke):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        all_videos_on_nuke = cursor.execute(f"""SELECT video.name FROM linking, nuke, video
        where linking.id_nuke=nuke.id and linking.id_video=video.id and linking.id_nuke='{id_nuke}'""").fetchall()
        video_on_nuke = []
        for video in all_videos_on_nuke:
            video_on_nuke.append(video[0])
        print(video_on_nuke)
        return video_on_nuke
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    conn.commit()
    cursor.close()


def all_nukes():
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    nukes = cursor.execute(f'SELECT * from nuke').fetchall()
    nuke = {}
    for item in nukes:
        id_nuke = item[0]
        name = item[1]
        ip = item[2]
        comment = item[3]
        #print(id_nuke, name, ip)
        #print(f"SELECT * from video where {str(id_nuke)}=1")
        #videos = select_nuke(id_nuke)
        #nuke[item[1]] = videos
        nuke[name] = {'ip': ip, 'id_nuke': id_nuke, 'comment': comment}
    return nuke


def all_videos():
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        nukes = cursor.execute(f'SELECT * from video').fetchall()
        nuke = {}
        for item in nukes:
            id_video = item[0]
            name = item[1]
            nuke[name] = {'name': name, 'id_video': id_video}
        return nuke
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)


def select_nuke(id):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()

    videos = []
    video_4_nuke = cursor.execute(f'SELECT name FROM video where "{id}" = 1').fetchall()
    for video in video_4_nuke:
        videos.append(video[0])
    return videos


def all_video_on_nuke(id_nuke):
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
    conn.commit()
    cursor.close()


def sql_ip_nuke(id):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        ip_nuke = cursor.execute(f'SELECT ip FROM nuke WHERE id="{id}"').fetchall()
        return ip_nuke[0]
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)

