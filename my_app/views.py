import bcrypt
from flask import flash, redirect, render_template, request, session, url_for

from my_app import app
from my_app.models import RegistrationForm, Login, Registration, Admin, db


# ========================================================
# ---------------------- HOME ----------------------------
# ========================================================

@app.route('/')
def home():
    return render_template('home.html')


# ========================================================
# -------------------- LOGIN PAGE ------------------------
# ========================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit() and request.method == 'POST':
        user = Registration.query.filter_by(username=username).first()
        admin = Admin.query.filter_by(username=username).first()
        if user:
            psw_hash = bcrypt.checkpw(password.encode('utf-8'), user.password)
            if psw_hash:
                session['username'] = user.username
                return redirect(url_for('home', session=session))
            else:
                flash('That username or password does not match our records!')

        if admin:
            psw_hash = bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8'))
            if psw_hash:
                session['username'] = username
                return redirect(url_for('admin.index', session=session))
            else:
                flash('That username or password does not match our records!')

        else:
            flash('That username or password does not match our records!')

    return render_template('login.html', form=form)


# ========================================================
# ---------------------- LOGOUT  -------------------------
# ========================================================

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You\'ve been successfully signed out!')
    return redirect(url_for('home'))


# ========================================================
# ----------------- USER REGISTRATION --------------------
# ========================================================

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm()
        if request.method == "POST" and form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt(14))
            
            # Query DB for existing username
            username_query = Registration.query.filter_by(username=username).first()
            # Query DB for existing email
            email_query = Registration.query.filter_by(email=email).first()
            
            # If username exits
            if username_query:
                flash("Sorry that username is already taken, please choose another!")
                return render_template('register.html', form=form)
                
            # If email exists
            if email_query:
                flash('That email is already associated with another account, please use another!')
                return render_template('register.html', form=form)

            else:
                new_user = Registration(email=email, username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash("Thanks for registering, {u}!".format(u=username))
                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('home'))

    except Exception as e:
        print(e)

    return render_template("register.html", form=form)
