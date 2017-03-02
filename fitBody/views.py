import logging
import sys

import bcrypt
from flask import flash, redirect, render_template, request, session, Blueprint, url_for

from fitBody.models import RegistrationForm
from fitBody.models import cursor, conn

fitBody = Blueprint('fitBody', __name__)

'''
# LOGGING LEVELS:
# 1 DEBUG = detailed info
# 2 INFO - confirmation that things according to plan
# 3 WARNING - something unexpected
# 4 ERROR - some function failed
# 5 CRITICAL - something failed application must close
# i.e. level=logging.DEBUG
'''

logging.basicConfig(filename='logfile.log', format='\n%(asctime)s %(message)s', level=logging.ERROR)


# formatting the output of the log
def error_handling():
    return ('\n{}. {}, @ line: {}'.format(sys.exc_info()[0],
                                          sys.exc_info()[1],
                                          sys.exc_info()[2].tb_lineno))


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
                cursor.execute("INSERT INTO registration (email, username, hash) VALUES (?, ?, ?)",
                               (email, username, password))
                conn.commit()
                flash("Thanks for registering, {u}!".format(u=username))

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('fitBody.home'))

    except Exception as e:
        logging.error(error_handling())

    return render_template("register.html", form=form)
