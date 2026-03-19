from flask import Flask, render_template, redirect
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'




db_session.global_init('db/mars.db')
db_sess = db_session.create_session()

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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')