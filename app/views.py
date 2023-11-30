from app import app

from flask import render_template,request,redirect,jsonify,make_response,flash,url_for

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import  InputRequired,Length
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from app.form import LoginForm,RegistrationForm,ContactForm
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from email_validator import validate_email, EmailNotValidError
from app.__init__ import login_manager
from app.models import db,User
from flask_mail import Message,Mail
from app.__init__ import mail
import PyPDF2
from pdf2image import convert_from_path
from flask import abort

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")
@app.template_filter("reverse_string")
def reverse_string(name):
    return name[::-1]
@app.route('/about')
def about():
    return render_template('public/about.html')


@app.route('/jinja')
def jinja():
    name = 'Loris'

    age = 22

    langs = ["Python","JavaScript","C"]

    friends = {"Tom":30,
               "Amy":60,
               "Tony":56,
               "Clarissa":23}

    colours = ("Red","Green")

    cool = True


    class GitRemote:
        def __init__(self,name,description,url):
            self.name = name
            self.description = description
            self.url = url
        def pull(self):
            return f"Pullin repo {self.name}"
        def clone(self):
            return f"Cloning into {self.url}"

    my_remote = GitRemote(
        name = "Flask",
        description = "Template design tutorial",
        url = "https://github.com/LLoris18/jinja.git"
    )
    def repeat(x,qty):
        return x * qty

    date = datetime.utcnow()

    my_html = "<h1>This is html</h1>"

    suspicious = "<script> alert('You got hacked')</script>"

    return render_template('public/jinja.html',
                           name=name,age=age,langs=langs,
                           friends=friends,colours=colours,
                           cool=cool,GitRemote=GitRemote,repeat=repeat,my_remote=my_remote,
                           date=date,my_html=my_html,suspicious=suspicious)

@app.route("/signup",methods=['GET','POST'])
def sign_up():
    if request.method == "POST":

        req = request.form
        username = req["username"]
        email = req.get("email")
        password = request.form["password"]

        return redirect(request.url)
    return render_template("public/signup.html")

users = {
    "mitsuhiko":{
        "name":"Armin Ronacher",
        "bio":"Cretor of the Flask framework",
        "twitter_handele":"@mitshuiko"
    },
    "gvanrossum":{
        "name": "Guido Van Rossum",
        "bio": "Cretor of the Python programming language ",
        "twitter_handele": "@gvanrossum"
    },
    "elonmusk":{
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor and engineer",
        "twitter_handele": "@elonmusk"
    }
}


@app.route("/multiple/<foo>/<bar>/<baz>")
def multi(foo,bar,baz):
    return f"foo is {foo}, bar is {bar}, baz is{baz}"

@app.route('/json',methods=["POST"])
def json():
    if request.is_json:
        req = request.get_json()

        response={
            "message": "JSON received!",
            "name": req.get("name")
        }

        res = make_response(jsonify(response),200)

        return res

    else:
        res = make_response(jsonify({"message":"No JSON receieved"}),400)
        return "No JSON received",400

@app.route('/guestbook')
def guestbook():
    return render_template("public/guestbook.html")


@app.route('/guestbook/create-entry',methods=["POST"])
def create_entry():
    req = request.get_json()
    print(req)

    res = make_response(jsonify({"message": "JSON received"},200))

    return res

@app.route('/query')
def query():

    args = request.args

    return 'Query received',200

@app.route('/sent')
def sent():
    return render_template('public/sent.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User(username=username, email=email, password=password)
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()
        flash('Utente registrato correttamente')
        return redirect(url_for('login'))
    return render_template('public/register.html',form=form)

@app.route('/', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            validate_email(form.email.data)
        except EmailNotValidError as e:
            flash('Email non valida')
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(url_for('home'))
        flash('Email o password non validi')
    return render_template('public/login1.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sei stato scollegato dal sito')
    return redirect(url_for('home'))

@app.route('/home',methods=['GET','POST'])
@login_required
def home():
    form = ContactForm()
    if form.validate_on_submit() and request.method == 'POST':
        msg = Message(form.email_body.data,
                      sender=form.email.data,
                      recipients=['admin@gmail.com'])
        msg.html = render_template('public/messaggio_utente.html',nomeC=form.nomeC.data,
                                   email=form.email.data,
                                   telefono=form.telefono.data,
                                   email_body=form.email_body.data)
        try:
            mail.send(msg)
            return redirect(url_for('sent'))
        except Exception as e:
            return f'Errore nell\'invio dell\'email: {str(e)}'

    return render_template('public/index_form.html',form = form)


@app.route('/check_password_strenght',methods=['POST'])
def check_password_strenght():
    form = RegistrationForm
    password = request.form.get('password')

    is_valid = len(password) >=8

    return jsonify({'is_valid' : is_valid})


@app.route('/capitolo1')
def capitolo1():
    return render_template('public/capitolo1.html')


@app.route('/capitolo2')
def capitolo2():
    return render_template('public/capitolo2.html')
@app.route('/capitolo3')
def capitolo3():
   return render_template('public/capitolo3.html')

@app.route('/capitolo4')
def capitolo4():
    return render_template('public/capitolo4.html')

@app.route('/capitolo5')
def capitolo5():
    return render_template('public/capitolo5.html')

@app.route('/capitolo6')
def capitolo6():
    return render_template('public/capitolo6.html')

@app.route('/profile')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('public/profile.html',user=user)

@app.route('/profile1')
def profile1():
    return render_template('public/profile1.html')