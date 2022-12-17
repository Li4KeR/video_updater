from flask import Flask, render_template, url_for, request, redirect
#from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime

from def_app import print_title
from sql_logic import check_sql, add_nuke, add_video, select_nuke, add_video_nuke, all_nukes, linking_nuke


app = Flask(__name__)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)


#class Article(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(155), nullable=False)
#    intro = db.Column(db.String(255), nullable=False)
#    text = db.Column(db.Text, nullable=False)
#    date = db.Column(db.DateTime, default=datetime.utcnow)
#
#    def __repr__(self):
#        return "<Article %r>" % self.id


@app.route('/')
@app.route('/home')
def index():
    nukes = all_nukes()
    return render_template("index.html", nukes=nukes)


@app.route('/test/<id>')
def test(id):
    nukes = linking_nuke(id)
    return render_template("index.html", nukes=nukes)
    # nukes = linking_nuke(41)
    # return f'test'


@app.route('/about/<id>')
def about(id):
    if check_sql():
        videos = select_nuke(id)
        print(videos)
        #conn = sqlite3.connect('base.sqlite3')
        #cursor = conn.cursor()
        #nukes = cursor.execute(f'SELECT * from nuke').fetchall()
        #f"SELECT * FROM VIDEO where {nukes}=1"
        #print(nukes)

        #conn.commit()
        #cursor.close()
    else:
        return "error bd"
    return render_template("about.html", videos=videos, id=id)


@app.route('/create_nuke', methods=['POST', 'GET'])
def create_nuke():
    if request.method == 'POST':
        name = request.form['name']
        ip = request.form['ip']
        print_title(name, ip)
        if check_sql():
            add_nuke(name, ip)
            add_video_nuke(name)
        return redirect('/')
    else:
        return render_template('create_nuke.html')


@app.route('/create_video', methods=['POST', 'GET'])
def create_video():
    if request.method == 'POST':
        name = request.form['name']
        path_video = request.form['path']
        if check_sql():
            add_video(name, path_video)
        return redirect('/')
    else:
        return render_template('create_video.html')


@app.route('/user/<string:name>/<int:id>') # для изминения урла
def user(name, id):
    return f"User {name}, {str(id)}"
    #return render_template("user.html")


if __name__ == "__main__":
    app.run(debug=True)
