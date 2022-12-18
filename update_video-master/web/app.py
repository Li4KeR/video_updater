from flask import Flask, render_template, url_for, request, redirect
import os
from datetime import datetime
from sql_logic import check_sql, add_nuke, add_video, all_videos, all_nukes, linking_nuke, name_nuke, \
    all_video_on_nuke, create_link_video_and_nuke, delete_link_video_and_nuke, sql_ip_nuke
from logic import compare_lists, send_data, ping_nuke


file_path = f"\\\\192.168.100.92\\public\\video\\all"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = file_path


@app.route('/')
@app.route('/home')
def index():
    nukes = all_nukes()
    return render_template("index.html", nukes=nukes)


@app.route('/about/<id>', methods=['POST', 'GET'])
def about(id):
    name = name_nuke(id)
    print(name)
    if request.method == 'POST':
        response_data = request.form['index']
        # button ping
        if response_data == f'Ping_{id}':
            ip = sql_ip_nuke(id)
            print(ip)
            if ping_nuke(ip[0]):
                return render_template("about.html", ping=True, id=id, name=name)
            else:
                return render_template("about.html", ping=False, id=id, name=name)
        # button play video
        elif response_data == f'PlayVideo_{id}':
            print(f'PlayVideo_{id}')
            return render_template("about.html", play="play", id=id, name=name)
        # button pause video
        elif response_data == f'PauseVideo_{id}':
            print(f'PauseVideo_{id}')
            return render_template("about.html", pause="pause", id=id, name=name)
        # button restart video
        elif response_data == f'Restart_{id}':
            print(f'Restart_{id}')
            return render_template("about.html", pause="pause", id=id, name=name)
        # button check playlist
        elif response_data == f'CheckPlaylist_{id}':
            print(f'CheckPlaylist_{id}')
            return render_template("about.html", checkplaylist='checkplaylist', id=id, name=name)
        else:
            return redirect('/')
    elif request.method == 'GET':
        check_sql()
        videos = linking_nuke(id)
    else:
        return 'ERROR BD'
    return render_template("about.html", videos=videos, id=id, name=name)


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
                print(f'Добавляем на {id} видео {item}')
                ip_nuke, video_name, full_name = create_link_video_and_nuke(id, item)
                print(f'Добавляем на {ip_nuke} видео {video_name} с тру именем {full_name}')
                send_data(ip_nuke, f'DownloadVideo_____{full_name}')
                """ Передача айди нюка и айди видео, отправить команду для скачивания видео и добавления в плейлист """
            for item in not_in_mark: # если видео есть на нюке, но не помечено маркером
                print(f'Удаляем с {id} видео {item}')
                ip_nuke, video_name, full_name = delete_link_video_and_nuke(id, item)
                print(full_name)
                send_data(ip_nuke, f'DeleteVideo_____{full_name}')
                """ передача айди нюка и айди видео, отправить на нюк команду удаления видео """
        return redirect('/')
    else:
        all_video = all_videos()
        videos = linking_nuke(id)
        name = name_nuke(id)
        return render_template("edit.html", id=id, all_video=all_video, videos=videos, name=name)


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


@app.route('/create_video', methods=['POST', 'GET'])
def create_video():
    if request.method == 'POST':
        name = request.form['name']
        file = request.files['file']
        full_name = file.filename
        print(os.path.join(file_path))
        print(file_path)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        if check_sql():
            add_video(name, full_name)
        return render_template('seccuss.html', name=file.filename)
    else:
        return render_template('create_video.html')


@app.route('/seccuss/<job>')
def feedback_job(job):
    return redirect('/')


@app.route('/edit/restart/<id>')
def restart(id):
    print(f'restart {id} нюк')
    # restart_nuke(id)
    job = 'restart_nuke'
    return redirect('/')


@app.route('/edit/pause/<id>')
def pause(id):
    print(f'pause {id} нюк')
    # restart_nuke(id)
    job = 'restart_nuke'
    return redirect('/')


@app.route('/edit/play/<id>')
def play(id):
    print(f'play {id} нюк')
    # restart_nuke(id)
    job = 'restart_nuke'
    return redirect('/')


@app.route('/edit/check_playlist/<id>')
def check_playlist(id):
    print(f'check_playlist {id} нюк')
    # restart_nuke(id)
    job = 'restart_nuke'
    return redirect('/')


@app.route('/edit/ping/<id>')
def ping(id):
    print(f'ping {id} нюк')
    # restart_nuke(id)
    job = 'restart_nuke'
    return redirect('/')


@app.route('/user/<string:name>/<int:id>')  # для изминения урла
def user(name, id):
    return f"User {name}, {str(id)}"
    # return render_template("user.html")


if __name__ == "__main__":
    app.run(debug=True)
