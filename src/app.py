from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from model import log, db, Cuisine, Attractions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return log.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = log.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Неверный логин или пароль')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = log.query.filter_by(username=username).first()
        if user:
            flash('Это имя пользователя уже занято, придумайте другое')
        else:
            hashed_password = generate_password_hash(password)
            new_user = log(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Аккаунт успешно создан')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/attractions')
def attractions():
    return render_template('Attractions.html')


@app.route('/NationalCuisine')
def national_cuisine():
    return render_template('NationalCuisine.html')


@app.route('/Home')
def home():
    return render_template('Home.html')


@app.route('/blocks')
def block():
    cur_cuisine = Cuisine.query.all()
    cur_attract = Attractions.query.all()
    return render_template('blocks.html', app_cuisine=cur_cuisine, app_attract=cur_attract)


@app.route('/edit')
def edit():
    return redirect(url_for("editprofile"))


@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        log.query.where(log.username == username).update({"firstname": firstname, "lastname": lastname})
        db.session.commit()
        flash('Аккаунт успешно изменен')
    return render_template('edit.html', userload=current_user)


@app.errorhandler(401)
def no_such_user(e):
    return render_template('401.html'), 401


# @app.errorhandler(402)
# def no_many(e):
#     return render_template('402.html'), 402


@app.errorhandler(403)
def access_is_denied(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=11000)
