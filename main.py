# Импорт необходимых модулей
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# Создание экземпляра приложения Flask
app = Flask(__name__)
# Настройка базы данных SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Определение модели данных для статьи
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.id}>'
# Определение маршрута для главной страницы
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")
# Определение маршрута для страницы "About"
@app.route('/about')
def about():
    return render_template("about.html")
# Определение маршрута для страницы "Posts"
@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)
@app.route('/posts/<int:id>')
def post_details(id):
    article = Article.query.get(id)
    return render_template('post_details.html', article=article)
@app.route('/posts/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except Exception as e:
        return "Произошла ошибка при удалении статьи: " + str(e)

# Изминение записи
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        # Получение данных из формы
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка"
    else:
        return render_template("post_update.html", article=article)
# Определение маршрута для создания статьи
@app.route('/write_article', methods=['POST', 'GET'])
def write_article():
    if request.method == "POST":
        # Получение данных из формы
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        # Создание новой статьи
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"
    else:
        return render_template("write_article.html")


if __name__ == "__main__":
    # Создание всех таблиц в базе данных
    with app.app_context():
        db.create_all()

    # Запуск приложения в режиме отладки
    app.run(debug=True)