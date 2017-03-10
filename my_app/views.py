import bcrypt
from flask import flash, redirect, render_template, request, session, url_for
from my_app.models import RegistrationForm, cursor, conn, Login, Registration, Admin

from my_app import app


# ========================================================
# ----------------- HOME PAGE LAYOUT ---------------------
# ========================================================

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# ========================================================
# ----------------- USER LOGIN PAGE ----------------------
# ========================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit() and request.method == 'POST':
        user = Registration.query.filter_by(username=form.username.data).first()
        if user:
            psw_hash = bcrypt.checkpw(form.password.data.encode('utf-8'), user.password)
            if psw_hash:
                session['username'] = user.username
                return redirect(url_for('home', session=session))
            else:
                flash('That username or password does not match our records!')
        else:
            flash('That username or password does not match our records!')

    return render_template('login.html', form=form)


# ========================================================
# ----------------- ADMIN LOGIN PAGE ---------------------
# ========================================================

@app.route('/employee', methods=['GET', 'POST'])
def admin_login():
    form = Login()
    if form.validate_on_submit() and request.method == 'POST':
        user = Admin.query.filter_by(username=form.username.data).first()
        if user:
            psw_hash = bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8'))
            if psw_hash:
                session['username'] = user.username
                return redirect(url_for('admin.index', session=session))
            else:
                flash('That username or password does not match our records!')
        else:
            flash('That username or password does not match our records!')

    return render_template('login.html', form=form)


# ========================================================
# ------------------- USER LOGOUT  -----------------------
# ========================================================

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You\'ve been successfully signed out!')
    return redirect(url_for('home'))


# ========================================================
# ----------------- USER REGISTRATION PAGE ---------------
# ========================================================

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm()
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt(14))  # 14 = # of rounds

            cursor.execute("SELECT username FROM registration WHERE username = (?)", (username,))
            username_check = cursor.fetchall()

            cursor.execute("SELECT email FROM registration WHERE email = (?)", (email,))
            email_check = cursor.fetchall()

            if len(username_check) > 0:
                flash("Sorry that username is already taken, please choose another!")
                return render_template('register.html', form=form)

            if len(email_check) > 0:
                flash('That email is already associated with another account, please use another!')
                return render_template('register.html', form=form)

            else:
                cursor.execute("INSERT INTO registration (email, username, password) VALUES (?, ?, ?)",
                               (email, username, password))
                conn.commit()
                flash("Thanks for registering, {u}!".format(u=username))

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('home'))

    except Exception as e:
        print(e)

    return render_template("register.html", form=form)
