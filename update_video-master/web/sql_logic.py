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


def add_nuke(nuke_name, nuke_ip):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(f'INSERT INTO nuke(name, ip) VALUES("{nuke_name}", "{nuke_ip}")')
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    conn.commit()
    cursor.close()


def add_video(name, ftp_path):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    vid_info = name, ftp_path
    try:
        cursor.execute(f'INSERT INTO video(name, ftp_path) VALUES("{name}", "{ftp_path}")')
    except sqlite3.Error as error:
        print(error)
    conn.commit()
    cursor.close()


def linking(id_nuke, id_video):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(f'INSERT INTO linking(id_nuke, id_video) VALUES("{id_nuke}", "{id_video}")')
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    conn.commit()
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
        link = cursor.execute(f"""SELECT video.name FROM linking, nuke, video 
        where linking.id_nuke=nuke.id and linking.id_video=video.id and linking.id_nuke='{id_nuke}'""").fetchall()
        #link = cursor.execute(f"""SELECT nuke.name, nuke.ip, video.name FROM linking, nuke, video
        #where linking.id_nuke=nuke.id and linking.id_video=video.id and linking.id_nuke='{id_nuke}'""").fetchall()
        return link
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
    conn.commit()
    cursor.close()


def add_video_nuke(nuke_name):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()
    nuke_id = cursor.execute("""SELECT id FROM nuke where name=?""", (nuke_name,)).fetchall()
    for x in nuke_id:
        nuke_real_id = x[0]
    #cursor.execute(f"ALTER TABLE video ADD COLUMN '{str(nuke_real_id)}' INTEGER DEFAULT 0")
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
        #print(id_nuke, name, ip)
        #print(f"SELECT * from video where {str(id_nuke)}=1")
        videos = select_nuke(id_nuke)
        nuke[item[1]] = videos
    print(nuke)
    return nuke


def select_nuke(id):
    conn = sqlite3.connect('base.sqlite3')
    cursor = conn.cursor()

    videos = []
    video_4_nuke = cursor.execute(f'SELECT name FROM video where "{id}" = 1').fetchall()
    for video in video_4_nuke:
        videos.append(video[0])
    return videos
    #nukes = cursor.execute(f'SELECT id from nuke')
    #for nuke in nukes:
    #    videos = []
    #    video_4_nuke = cursor.execute(f'SELECT name FROM video where "{nuke[0]}" = 1').fetchall()
    #    print(nuke[0])
    #    for video in video_4_nuke:
    #        videos.append(video[0])
    #    return videos