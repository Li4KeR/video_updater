from flask import Flask, render_template, url_for, request, redirect, jsonify
import os
from datetime import datetime
from sql_logic import *
from logic import compare_lists, send_data, ping_nuke, get_all_nukes, check_playlist_sql_physic

import time

""" переменные """
# path_all_video = r"\\192.168.100.92\public\video\all"
path_all_video = r"D:\Video\test"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = path_all_video


""" главная страничка """


@app.route('/', methods=['POST', 'GET'])
def index():
    sql_check_sql()
    all_nukes = get_all_nukes()
    # all_videos = sql_get_all_videos()
    # nukes = sql_get_all_nukes()  # возвращает словарь всех нюков.
    # # name{'ip_nuke': ip, 'name': name, 'id_nuke': id_nuke, 'comment': comment}
    # all_nukes = []
    # for nuke in nukes:
    #     nuke = Nuke(nukes.get(nuke).get('id_nuke'), nukes.get(nuke).get('ip_nuke'), nukes.get(nuke).get('name'),
    #                 nukes.get(nuke).get('comment'))
    #     all_nukes.append(nuke)

    if request.method == 'POST':
        response_marks = request.values.lists()

        if len(response_marks) == 2:
            for row in response_marks:
                if row[0] == 'check_box':
                    markers = row[1]
                else:
                    nuke_form = row[1]
        else:
            nuke_form = response_marks[0][1]
            markers = []

        # print(nuke_form)
        # print(markers)

        nuke_resp = nuke_form[0]
        print(nuke_resp)
        for nuke in all_nukes:
            all_video_on_nuke = []
            video_for_delete = []
            for video in nuke.videos:
                all_video_on_nuke.append(video[0])
                if str(nuke_resp) == str(nuke.id):
                    if str(video[0]) not in markers:
                        video_for_delete.append(video[0])
                        # print(f"Нет в марке, но есть на нюке {nuke.id}: {int(video)}")
            for vid in video_for_delete:
                nuke.delete_video(vid)
                print(vid)

            if str(nuke_resp) == str(nuke.id):
                for video in markers:
                    if int(video) not in all_video_on_nuke:
                        nuke.add_video(int(video))
                        # print(f"в марке, но нет на нюке {nuke.id}: {int(video)}")
            # print(all_video_on_nuke)
            # print(markers)
        # test_dict = { "nuke": nuke_resp, "markers": markers}
        # print(test_dict)
        return "response_marks"

        # return jsonify(test_dict)
        # return render_template("index.html", test_dict=test_dict)
        # return render_template("index.html", nukes=nukes, all_videos=all_videos, all_nukes=all_nukes)
    else:
        all_videos = sql_get_all_videos()
        return render_template("index.html", all_videos=all_videos, all_nukes=all_nukes)


""" страничка /about """


@app.route('/about/<id>', methods=['POST', 'GET'])
def about(id):
    name = sql_get_name_nuke(id)
    ip_nuke = sql_ip_nuke(id)[0]
    all_nukes = get_all_nukes()
    all_videos = sql_get_all_videos()

    for nuke_cache in all_nukes:
        if str(nuke_cache.id) == id:
            nuke = nuke_cache

    if request.method == 'POST':
        response_data = request.form['index']
        # button ping
        if response_data == f'Ping_{id}':
            if ping_nuke(ip_nuke):
                return render_template("about.html", ping=True, id=id, name=name)
            else:
                return render_template("about.html", ping=False, id=id, name=name)
        # button play video
        elif response_data == f'PlayVideo_{id}':
            send_data(ip_nuke, 'Play_____')
            print(f'PlayVideo_{id} на {ip_nuke}')
            return render_template("about.html", play="play", id=id, name=name)
        # button pause video
        elif response_data == f'PauseVideo_{id}':
            send_data(ip_nuke, 'Stop_____')
            return render_template("about.html", pause="pause", id=id, name=name)
        # button restart video
        elif response_data == f'Restart_{id}':
            print(f'Restart_{id}')
            return render_template("about.html", pause="pause", id=id, name=name)
        # button check playlist
        elif response_data == f'CheckPlaylist_{id}':
            print(f'CheckPlaylist_{id}')
            check_playlist_sql_physic(ip_nuke, id)
            return render_template("about.html", checkplaylist='checkplaylist', id=id, name=name)
        else:
            return redirect('/')
    elif request.method == 'GET':
        # videos = sql_get_all_video_on_nuke(id)

        if ping_nuke(ip_nuke):
            return render_template("about.html", all_videos=all_videos, all_nukes=all_nukes, ping=True, id=id,
                                   nuke=nuke, name=name)
        else:
            return render_template("about.html", all_videos=all_videos, all_nukes=all_nukes, ping=True, id=id,
                                   nuke=nuke, name=name)


# страничка edit
@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    if request.method == 'POST':
        markers = request.form.getlist("check_box")
        video_on_nuke = sql_all_video_on_nuke(id)
        markers.sort()
        video_on_nuke.sort()
        # если список маркеров совападает со списком видео на нюке
        if markers == video_on_nuke:
            print('true')
        else:
            """ ВЫВЕСТИ В ОТДЕЛЬНУЮ ФУНКЦИЮ? """
            not_in_nuke = compare_lists(markers, video_on_nuke)
            not_in_mark = compare_lists(video_on_nuke, markers)
            for item in not_in_nuke:  # если видео нет на нюке, но помечено маркером
                # print(f'Добавляем на {id} видео {item}')
                ip_nuke, video_name, full_name = sql_create_link_video_and_nuke(id, item)
                print(f'Добавляем на {ip_nuke} видео {video_name} с тру именем {full_name}')
                send_data(ip_nuke, f'DownloadVideo_____{full_name}')
                """ Передача айди нюка и айди видео, отправить команду для скачивания видео и добавления в плейлист """
            for item in not_in_mark:  # если видео есть на нюке, но не помечено маркером
                print(f'Удаляем с {id} видео {item}')
                ip_nuke, video_name, full_name = sql_delete_link_video_and_nuke(id, item)
                test = f'DeleteVideo_____{full_name}'
                send_data(ip_nuke, test)
                """ передача айди нюка и айди видео, отправить на нюк команду удаления видео """
        return redirect('/')
    else:
        all_video = sql_get_all_videos()
        print(all_video)
        nuke = {}
        for item in all_video:
            id_video = item[0]
            name = item[1]
            nuke[name] = {'name': name, 'id_video': id_video}
        videos = sql_get_all_video_on_nuke(id)
        print(videos)
        name = sql_get_name_nuke(id)
        return render_template("edit.html", id=id, all_video=all_video, nuke=nuke, videos=videos, name=name)


# страничка добавления нюка
@app.route('/create_nuke', methods=['POST', 'GET'])
def create_nuke():
    if request.method == 'POST':
        if request.form['name'].split('_')[0] == 'delete':
            id_nuke = request.form['nuke_id'].split('_')[1]
            sql_delete_nuke(id_nuke)
            print(id_nuke)

            # sql_delete_nuke(id) write!!!!!!

            # if request.form['nuke_id']:
            #     print(request.form['nuke_id'])
            #     return redirect('/')
            # else:
            return redirect('/create_nuke')
        else:
            name = request.form['name']
            ip = request.form['ip']
            comment = request.form['comment']
            if comment == '':
                comment = 'Нет описания'
            sql_add_nuke(name, ip, comment)
            return redirect('/')
    else:
        all_nukes = sql_get_all_nukes()
        for row in all_nukes:
            print((all_nukes.get(row)).get('ip_nuke'))
            # cache = all_nukes.get(row)
            # cache.get('name')
            # print(cache.get('name'))
        return render_template('create_nuke.html', all_nukes=all_nukes)


# страничка добавления видео и синхронизация видео между фтп и скулем
@app.route('/create_video', methods=['POST', 'GET'])
def create_video():
    if request.method == 'POST':
        # добавление видео
        if request.form['send'] == "Отправить":
            name = request.form['name']
            file = request.files['file']
            full_name = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            sql_add_video(name, full_name)
            return render_template('seccuss.html', name=file.filename)
        # синхронизация видосов
        else:
            all_video = sql_get_all_videos()
            videos_sql = []
            for row in all_video:
                videos_sql.append(row[2])
            videos_on_ftp = []
            for filename in os.listdir(path=path_all_video):
                videos_on_ftp.append(filename)
            print(videos_sql)
            print(videos_on_ftp)
            for video in videos_on_ftp:
                if video not in videos_sql:
                    print(video)
                    sql_sync_video(video)
            return render_template('create_video.html', status=True)
    else:
        all_video = sql_get_all_videos()
        print(all_video)
        return render_template('create_video.html', all_video=all_video)


# @app.route('/seccuss/<job>')
# def feedback_job(job):
#     return redirect('/')
#
#
# @app.route('/edit/restart/<id>')
# def restart(id):
#     print(f'restart {id} нюк')
#     # restart_nuke(id)
#     job = 'restart_nuke'
#     return redirect('/')
#
#
# @app.route('/edit/pause/<id>')
# def pause(id):
#     print(f'pause {id} нюк')
#     # restart_nuke(id)
#     job = 'restart_nuke'
#     return redirect('/')
#
#
# @app.route('/edit/play/<id>')
# def play(id):
#     print(f'play {id} нюк')
#     # restart_nuke(id)
#     job = 'restart_nuke'
#     return redirect('/')
#
#
# @app.route('/edit/check_playlist/<id>')
# def check_playlist(id):
#     print(f'check_playlist {id} нюк')
#     # restart_nuke(id)
#     job = 'restart_nuke'
#     return redirect('/')
#
#
# @app.route('/edit/ping/<id>')
# def ping(id):
#     print(f'ping {id} нюк')
#     # restart_nuke(id)
#     job = 'restart_nuke'
#     return redirect('/')
#
#
# @app.route('/user/<string:name>/<int:id>')  # для изминения урла
# def user(name, id):
#     return f"User {name}, {str(id)}"
#     # return render_template("user.html")


if __name__ == "__main__":
    app.run(debug=True)
