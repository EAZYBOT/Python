from app import app
from flask import render_template, request, redirect, url_for, flash, make_response, session
from flask_login import login_required, login_user, current_user, logout_user
# from .models import User, Post, Category, Feedback, db
from .models import User, Employee, RequestToDoctor, Position, Status, Service, db
from .forms import RegistrationForm, LoginForm, EditProfileForm, SearchServicesForm, SendTicketForm

import datetime


@app.route('/')
def index():
    return render_template('pages/index.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/contacts')
def contacts():
    return render_template('pages/contacts.html')


@app.route("/services", methods=['get'])
def services():
    list_of_services = []
    form = SearchServicesForm()

    if request.values:
        min_cost = request.values['min_cost'] if request.values['min_cost'] else 0
        max_cost = request.values['max_cost'] if request.values['max_cost'] else 10000000
        name = request.values['name_service'] if request.values['name_service'] else ""

        try:
            min_cost = float(min_cost)
            max_cost = float(max_cost)
        except ValueError:
            flash("Минимальная/Максимальная цена должны быть числом", "error")
            redirect(url_for('services'))

        list_of_services = db.session.query(Service).filter(
            (Service.name.like('%{}%'.format(name))) &
            (Service.cost > min_cost) & (Service.cost < max_cost)
        ).all()
    else:
        list_of_services = db.session.query(Service).all()
    return render_template("pages/services.html", services=list_of_services, form=form)


# @app.route('/user/<int:user_id>/')
# def user_profile(user_id):
#     return "Profile page of user #{}".format(user_id)
#
#
# @app.route('/books/<genre>/')
# def books(genre):
#     return "All Books in {} category".format(genre)
#
#
@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash("Неверное имя пользователи/пароль!", 'error')
        return redirect(url_for('login'))
    return render_template('pages/login.html', form=form)


@app.route('/registration/', methods=['post', 'get'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data.lower()).first()
        if user:
            flash("Такое имя пользователя занято!")
            return redirect(url_for('registration'))
        user = db.session.query(User).filter(User.email == form.email.data.lower()).first()
        if user:
            flash("Такой email уже занят!")
            return redirect(url_for('registration'))

        user = User()
        user.is_admin = False
        user.username = form.username.data.lower()
        user.email = form.email.data.lower()
        user.first_name = form.first_name.data.title()
        user.second_name = form.second_name.data.title()
        user.middle_name = form.middle_name.data.title()
        user.phone = form.phone.data
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Вы успешно зарегистрировались! Теперь войдите под своими данными.", "success")
        return redirect(url_for('login'))

    return render_template('pages/registration.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта!", 'success')
    return redirect(url_for('login'))


@app.route('/settings/', methods=['post', 'get'])
@login_required
def settings():
    form = EditProfileForm()

    if form.validate_on_submit():
        if current_user.username != form.username.data:
            user = db.session.query(User).filter(User.username == form.username.data.lower()).first()
            if user:
                flash("Такое имя пользователя занято!")
                return redirect(url_for('settings'))
            current_user.username = form.username.data

        if current_user.email != form.email.data:
            user = db.session.query(User).filter(User.email == form.email.data.lower()).first()
            if user:
                flash("Такой email уже занят!")
                return redirect(url_for('settings'))
            current_user.email = form.email.data

        if len(form.password.data) != 0:
            if current_user.check_password(form.old_password.data):
                current_user.set_password(form.password.data)
            else:
                flash("Неверный старый пароль", "error")
                return redirect(url_for('settings'))

        if current_user.first_name != form.first_name.data:
            current_user.first_name = form.first_name.data

        if current_user.second_name != form.second_name.data:
            current_user.second_name = form.second_name.data

        if current_user.middle_name != form.middle_name.data:
            current_user.middle_name = form.middle_name.data

        if str(current_user.phone) != str(form.phone.data):
            current_user.phone = form.phone.data
        print("Old: ", current_user.phone, " New: ", form.phone.data)
        db.session.add(current_user)
        db.session.commit()

        flash("Успешно изменено", "success")
        return redirect(url_for('settings'))

    form.username.data = current_user.username
    form.email.data = current_user.email
    form.first_name.data = current_user.first_name
    form.second_name.data = current_user.second_name
    form.middle_name.data = current_user.middle_name
    form.phone.data = current_user.phone

    return render_template('pages/settings.html', form=form)


@app.route('/my_tickets/')
@login_required
def my_tickets():
    my_ticks = db.session.query(RequestToDoctor).filter(RequestToDoctor.user_id == current_user.id).all()
    return render_template('pages/my_tickets.html', tickets=my_ticks)


@app.route('/send_ticket/', methods=['post', 'get'])
@login_required
def send_ticket():
    form = SendTicketForm()
    empl = db.session.query(Employee).all()

    if form.validate_on_submit():
        ticket = RequestToDoctor()
        dt_str = form.desired_date.data
        dt = 0
        try:
            dt = datetime.datetime(int(dt_str[:4]), int(dt_str[6:7]), int(dt_str[9:10]), int(dt_str[12:13]),
                                   int(dt_str[15:]))
        except ValueError:
            flash("Формат YYYY-MM-DD HH:MM", "error")
            redirect(url_for('send_ticket'))

        if dt <= datetime.datetime.utcnow():
            flash("Дата не может быть раньше чем сегодня", 'error')
            redirect(url_for('send_ticket'))
        ticket.desired_date = form.desired_date.data
        ticket.user = current_user
        ticket.employee = db.session.query(Employee).filter(Employee.id == form.id_employee.data).first()
        str = "Ожидание"
        ticket.status = db.session.query(Status).filter(Status.name == str).first()

        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for('my_tickets'))

    return render_template('pages/send_ticket.html', employees=empl, form=form)
#
#
# @app.route('/contact/', methods=['get', 'post'])
# def contact():
#     form = ContactForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         email = form.email.data
#         message = form.message.data
#
#         # здесь логика БД
#         feedback = Feedback(name=name, email=email, message=message)
#         db.session.add(feedback)
#         db.session.commit()
#
#         flash("Message Received", "success")
#         return redirect(url_for('contact'))
#
#     return render_template('contact.html', form=form)
#
#
# @app.route('/cookie/')
# def cookie():
#     if not request.cookies.get('foo'):
#         res = make_response("Setting a cookie")
#         res.set_cookie('foo', 'bar', max_age=60 * 60 * 24 * 365 * 2)
#     else:
#         res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
#     return res
#
#
# @app.route('/delete-cookie/')
# def delete_cookie():
#     res = make_response("Cookie Removed")
#     res.set_cookie('foo', 'bar', max_age=0)
#     return res
#
#
# @app.route('/article', methods=['POST', 'GET'])
# def article():
#     if request.method == 'POST':
#         res = make_response("")
#         res.set_cookie("font", request.form.get('font'), 60 * 60 * 24 * 15)
#         res.headers['location'] = url_for('article')
#         return res, 302
#
#     return render_template('article.html')
#
#
# @app.route('/visits-counter/')
# def visits():
#     if 'visits' in session:
#         session['visits'] = session.get('visits') + 1
#     else:
#         session['visits'] = 1
#     return "Total visits: {}".format(session.get('visits'))
#
#
# @app.route('/delete-visits/')
# def delete_visits():
#     session.pop('visits', None)  # удаление посещений
#     return 'Visits deleted'
#
#
# @app.route('/session/')
# def updating_session():
#     res = str(session.items())
#
#     cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}
#     if 'cart_item' in session:
#         session['cart_item']['pineapples'] = '100'
#         session.modified = True
#     else:
#         session['cart_item'] = cart_item
#
#     return res
#
#
# @app.route('/admin/')
# @login_required
# def admin():
#     return render_template('admin.html')


# if form.validate_on_submit():
#     print("Worked")
#     if form.min_cost.data > form.max_cost.data:
#         flash("Минимимальная цена не должна быть больше максимальной!")
#         redirect(url_for('services'))
#     if len(form.name_service.data) != 0:
#         list_of_services = db.session.query(Service).filter(
#             str(Service.name).find(form.name_service.data) != 1
#         ).all()
#     min_list = []
#     max_list = []
#     if form.min_cost.data > 0:
#         min_list = db.session.query(Service).filter(Service.cost >= form.min_cost.data).all()
#     if form.max_cost > 0:
#         max_list = db.session.query(Service).filter(Service.cost <= form.max_cost.data).all()
#     result = set(list_of_services).intersection(set(min_list).intersection(set(max_list)))
#     return render_template("pages/services.html", services=result, form=form)
