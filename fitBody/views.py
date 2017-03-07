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
# ----------------- ADMIN LOGIN PAGE ---------------------
# ========================================================
# TODO create flask login so it checks password for login, as well as session to show name in navbar

@fitBody.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            flash('Username or Password is incorrect! Please try again')
        else:
            return redirect(url_for('admin.index'))
    return render_template('login.html', error=error)

# ========================================================
# ------------------- USER LOGIN  ------------------------
# ========================================================
# TODO create any user login, and show name when logged in (session)


# ========================================================
# ------------------- USER LOGOUT  -----------------------
# ========================================================
# TODO create logout for users


# ========================================================
# ----------------- USER REGISTRATION PAGE ---------------
# ========================================================
# TODO change SQL statements to SQLAlchemy

@fitBody.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm()
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt(14))  # 14 = # of rounds

            username_query = cursor.execute("SELECT username FROM registration WHERE username = (?)", (username,))
            username_check = cursor.fetchall()

            email_query = cursor.execute("SELECT email FROM registration WHERE email = (?)", (email,))
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