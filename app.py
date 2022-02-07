from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import Script as launch_script
from Script import script




app = Flask(__name__)                                           # Стандарт для проекта на Flask определяет приложение
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wnner.db'    # Подключаем базу данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False            # Отключаем в базе устаревшую функцию трекинга
db = SQLAlchemy(app)                                            # Инициализируем БД


class Article(db.Model):                                    # Создаем БД
    id = db.Column(db.Integer, primary_key=True)            # Создаем поле в БД
    title = db.Column(db.String(100), nullable=False)       # Создаем поле в БД
    intro = db.Column(db.String(300), nullable=True)        # Создаем поле в БД
    text = db.Column(db.Text, nullable=False)               # Создаем поле в БД
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Создаем поле в БД для даты подключаем 'from datetime import datetime'


    def __repr__(self):                                     # При обращении к статье возвращаем еще и ее ID
        return '<Article %r' %self.id


@app.route('/')             # Маршрут для домашней
@app.route('/home')         # Маршрут для алиаса домашней
def index():
    return render_template("index.html")    # Какой темплейт для домашней


@app.route('/posts')            # Маршрут для постов
def posts():
    # articles = Article.query.first() первая статья
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)    # Какой темплейт для постов


@app.route('/posts/<int:id>')            # Маршрут для постов
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)    # Какой темплейт для постов


@app.route('/posts/<int:id>/del')            # Маршрут для постов
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При уделании статьи произошла ошибка"



@app.route('/about')            # Маршрут для about
def about():
    return render_template("about.html")    # Какой темплейт для about


@app.route('/privacy.html')
def privacy():
    return render_template("privacy.html")


@app.route('/create-article', methods=['POST', 'GET'])  # Маршрут для create-article и какие методы для нее активны, Нужно подключить 'request'
def create_article():
    if request.method == "POST":            # Описание метода POST на странице:
        title = request.form['title']       # В поле title записываем из формы id title
        intro = request.form['intro']       # В поле intro записываем из формы id intro
        text = request.form['text']         # В поле text записываем из формы id text

        article = Article(title=title, intro=intro, text=text) # Создаем объект для передачи в базу, В поле базы передаем значение переменной

        try:                                # Конструкция для обработки ошибок
            db.session.add (article)        # в текущей сессии добавить ранее созданный объект Article
            db.session.commit()             # commit сохраняет объект в базе
            return redirect('/posts')            # В случае успеха - редирект на главную. Функцию 'redirect' надо установить наверху
        except:
            return "Ошибка при добавлении статьи" # При какой либо ошибке выдать указанное
    else:
        return render_template("create-article.html") # если ничего не происходит отрисовать шаблон


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])  # Маршрут для create-article и какие методы для нее активны, Нужно подключить 'request'
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":            # Описание метода POST на странице:
        article.title = request.form['title']       # В поле title записываем из формы id title
        article.intro = request.form['intro']       # В поле intro записываем из формы id intro
        article.text = request.form['text']         # В поле text записываем из формы id text

        try:                                # Конструкция для обработки ошибок
            db.session.commit()             # commit сохраняет объект в базе
            return redirect('/posts')            # В случае успеха - редирект на главную. Функцию 'redirect' надо установить наверху
        except:
            return "Ошибка при редактировании произошла ошибка" # При какой либо ошибке выдать указанное
    else:
        return render_template("post-update.html", article=article) # если ничего не происходит отрисовать шаблон
# @app.route('/user/<string:name>/<int:id>')
# def user(name, id):
#     return"User page:" + name + " - " + str(id)
#
#
# @app.route('/konk/<string:name>/<int:id>')
# def konk():
#     return render_template("konk.html")
@app.route('/launch-page', methods=['POST', 'GET'])       # Маршрут для launch-page

def runscript():
    a = 'Artyom!'
    b = ' you did IT'
    if request.method == 'POST':
        result = launch_script.script(a, b)
        print(result)
    else:
        result = launch_script.script(a, b)
        print(result)
        return render_template("launch-page.html", result=result )  # Какой темплейт для launch-page


if __name__ == "__main__":          # запуск приложения
    app.run(debug=True)