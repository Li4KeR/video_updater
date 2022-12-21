from flask import Flask, render_template, url_for, request, redirect
import os
from datetime import datetime
from sql_logic import check_sql, add_nuke, add_video, all_videos, all_nukes, linking_nuke, name_nuke, \
    all_video_on_nuke, create_link_video_and_nuke, delete_link_video_and_nuke, sql_ip_nuke, sql_all_video_on_nuke, \
    sql_ip_from_name_video, sql_sync_video
from logic import compare_lists, send_data, ping_nuke


""" переменные """
file_path = f"\\\\192.168.100.92\\public\\video\\all"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = file_path
path_all_video = f"\\\\192.168.100.92\\public\\video\\all"


""" главная страничка """
@app.route('/')
@app.route('/home')
def index():
    nukes = all_nukes()
    return render_template("index.html", nukes=nukes)


""" страничка /about """
@app.route('/about/<id>', methods=['POST', 'GET'])
def about(id):
    name = name_nuke(id)
    ip_nuke = sql_ip_nuke(id)[0]
    if request.method == 'POST':
        response_data = request.form['index']
        # button ping
        if response_data == f'Ping_{id}':
            print(ip_nuke)
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
            sql_video_on_nuke = sql_all_video_on_nuke(id)
            sql_video_on_nuke.sort() # 2 лист
            video_on_hard_nuke = send_data(ip_nuke, f"CheckOldVideo_____").split('____') # 1 лист
            video_on_hard_nuke.sort()

            not_in_nuke = compare_lists(sql_video_on_nuke, video_on_hard_nuke)
            not_in_mark = compare_lists(video_on_hard_nuke, sql_video_on_nuke)

            for item in not_in_nuke:  # если видео нет на нюке, но помечено маркером
                id_video = sql_ip_from_name_video(item)
                print(f'Добавляем на {id} видео {item}')
                ip_nuke, video_name, full_name = create_link_video_and_nuke(id, id_video)
                print(f'Добавляем на {ip_nuke} видео {video_name} с тру именем {full_name}')
                send_data(ip_nuke, f'DownloadVideo_____{full_name}')
                """ Передача айди нюка и айди видео, отправить команду для скачивания видео и добавления в плейлист """
            for item in not_in_mark:  # если видео есть на нюке, но не помечено маркером
                id_video = sql_ip_from_name_video(item)
                print(f'Удаляем с {id} видео {id_video}')
                ip_nuke, video_name, full_name = delete_link_video_and_nuke(id, id_video)
                print(ip_nuke)
                print(full_name)
                send_data(ip_nuke, f'DeleteVideo_____{full_name}')
                """ передача айди нюка и айди видео, отправить на нюк команду удаления видео """

            #print(f'В скуле: {not_in_nuke}\nНа харде: {not_in_mark}')
            # print(video_on_hard_nuke)
            #download_and_delete_video_on_nuke(sql_video_on_nuke, video_on_hard_nuke, id)
            return render_template("about.html", checkplaylist='checkplaylist', id=id, name=name)
        else:
            return redirect('/')
    elif request.method == 'GET':
        check_sql()
        videos = linking_nuke(id)
    else:
        return 'ERROR BD'
    return render_template("about.html", videos=videos, id=id, name=name)


# страничка edit
@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    if request.method == 'POST':
        markers = request.form.getlist("check_box")
        video_on_nuke = all_video_on_nuke(id)
        markers.sort()
        video_on_nuke.sort()
        # если список маркеров совападает со списком видео на нюке
        if markers == video_on_nuke:
            print('true')
        else:
            not_in_nuke = compare_lists(markers, video_on_nuke)
            not_in_mark = compare_lists(video_on_nuke, markers)
            for item in not_in_nuke: # если видео нет на нюке, но помечено маркером
                # print(f'Добавляем на {id} видео {item}')
                ip_nuke, video_name, full_name = create_link_video_and_nuke(id, item)
                print(f'Добавляем на {ip_nuke} видео {video_name} с тру именем {full_name}')
                send_data(ip_nuke, f'DownloadVideo_____{full_name}')
                """ Передача айди нюка и айди видео, отправить команду для скачивания видео и добавления в плейлист """
            for item in not_in_mark: # если видео есть на нюке, но не помечено маркером
                print(f'Удаляем с {id} видео {item}')
                ip_nuke, video_name, full_name = delete_link_video_and_nuke(id, item)
                test = f'DeleteVideo_____{full_name}'
                send_data(ip_nuke, test)
                """ передача айди нюка и айди видео, отправить на нюк команду удаления видео """
        return redirect('/')
    else:
        all_video = all_videos()
        nuke = {}
        for item in all_video:
            id_video = item[0]
            name = item[1]
            nuke[name] = {'name': name, 'id_video': id_video}
        videos = linking_nuke(id)
        name = name_nuke(id)
        return render_template("edit.html", id=id, all_video=nuke, videos=videos, name=name)


# страничка добавления нюка
@app.route('/create_nuke', methods=['POST', 'GET'])
def create_nuke():
    if request.method == 'POST':
        name = request.form['name']
        ip = request.form['ip']
        comment = request.form['comment']
        print(comment)
        if comment == '':
            comment = 'Нет описания'
        if check_sql():
            add_nuke(name, ip, comment)
        return redirect('/')
    else:
        return render_template('create_nuke.html')


# страничка добавления видео и синхронизация видео между фтп и скулем
@app.route('/create_video', methods=['POST', 'GET'])
def create_video():
    if request.method == 'POST':
        # добавление видео
        if request.form['send'] == "Отправить":
            name = request.form['name']
            file = request.files['file']
            full_name = file.filename
            print(os.path.join(file_path))
            print(file_path)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            if check_sql():
                add_video(name, full_name)
            return render_template('seccuss.html', name=file.filename)
        # синхронизация видосов
        else:
            all_video = all_videos()
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
        return render_template('create_video.html')


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
