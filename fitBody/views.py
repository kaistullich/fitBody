import bcrypt
from flask import flash, redirect, render_template, request, session, Blueprint, url_for
from fitBody.models import RegistrationForm
from fitBody.models import cursor, conn

fitBody = Blueprint('fitBody', __name__)


# ========================================================
# ----------------- HOME PAGE LAYOUT ---------------------
# ========================================================

@fitBody.route('/')
@fitBody.route('/home')
def home():
    return render_template('home.html')


# ========================================================
# ----------------- USER LOGIN PAGE ----------------------
# ========================================================

@fitBody.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username_data = request.form['username']
        cursor.execute("SELECT username, password FROM registration WHERE username = (?)", (username_data,))
        username = cursor.fetchall()
        if request.form['username'] == username[0][0]:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), username[0][1]):
                session['username'] = username[0]
                return redirect(url_for('fitBody.home', error=error, session=session))
            else:
                flash('That username or password does not match our records!')
        else:
            flash('That username or password does not match our records!')

    return render_template('login.html', error=error)


# ========================================================
# ----------------- ADMIN LOGIN PAGE ---------------------
# ========================================================

@fitBody.route('/employee', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username_data = request.form['username']
        cursor.execute("SELECT username, password FROM admin WHERE username = (?)", (username_data,))
        admin = cursor.fetchall()
        if request.form['username'] == admin[0][0]:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), admin[0][1]):
                return redirect(url_for('admin.index', error=error))
            else:
                flash('That username or password does not match our records!')
        else:
            flash('That username or password does not match our records!')

    return render_template('employee.html', error=error)

# ========================================================
# ------------------- USER LOGOUT  -----------------------
# ========================================================
# TODO create logout for users


# ========================================================
# ----------------- USER REGISTRATION PAGE ---------------
# ========================================================

@fitBody.route('/register/', methods=["GET", "POST"])
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

                return redirect(url_for('fitBody.home'))

    except Exception as e:
        print(e)

    return render_template("register.html", form=form)