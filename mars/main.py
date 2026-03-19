from flask import Flask, render_template, redirect
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.jobs import JobForm
from forms.user import RegisterForm
from forms.login import LoginForm
from flask_login import LoginManager,login_required, logout_user, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


db_session.global_init('db/mars.db')
db_sess = db_session.create_session()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User,user_id)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = session.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names)

@app.route('/register', methods=['GET', 'POST'])
def register():
    context = {}
    context["title"] = "Регистрация"
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login.data).first():
            context["form"] = form
            context["message"] = "Такой пользователь уже есть"
            return render_template('register.html', **context)
        user = User(
            email=form.login.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            speciality=form.speciality.data,
            position=form.position.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    context["form"] = form
    return render_template('register.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    context = {}
    context["title"] = "Добавление работы"
    context["form"] = form
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            team_leader=form.team_leader.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template('add_job.html', **context)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)