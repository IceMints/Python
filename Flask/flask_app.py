from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from argon2 import PasswordHasher as ph
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import string, os, secrets, requests, re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# timeout user after 5 minutes of inactivity
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# Google ReCaptcha sitekey
sitekey = os.getenv("SITEKEY")

# username and password for mysql database
u = os.getenv("USER")
p = os.getenv("DATABASEPW")

# hostname and database name
h = os.getenv("DATAHOST")
d = os.getenv("DATABASE")

# Flask-SQLAlchemy database URL for mysql://username:password@hostname/database
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{u}:{p}@{h}/{d}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299

# SendGrid (email) Client
send_client = SendGridAPIClient(os.getenv("sendgridkey"))
fr_email = 'XXXX@student.mtsac.edu'

# Twilio SMS account information and proxy
proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
account = os.getenv("sms_account")
token = os.getenv("sms_token")
client = Client(account, token, http_client=proxy_client)
fr_sms_num = "+###########"

# system random numbers
rand_num = secrets.SystemRandom()

min_pw_length = 8
max_pw_length = 64
regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

# create the db object
db = SQLAlchemy(app)


# instance of LoginManager
login_manager=LoginManager(app)
# redirect user to index page instead of showing 401 - Unauthorized
login_manager.login_view='index'
login_manager.refresh_view='login2'
login_manager.login_message=''

# user_loader callback - loads user from the user id stored in the session cookie
@login_manager.user_loader
def load_user(user_id):
    return UserIndex.query.get(int(user_id))


# the model for user objects
class User(db.Model):
    __tablename__ = 'usersWeek8'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(len(ph().hash(''))))
    email = db.Column(db.String(64))

    def __repr__(self):
        return f'{self.username},{self.email}'

# the model for UserIndex objects
class UserIndex(db.Model, UserMixin):
    __tablename__ = 'usersWeek10'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(64))
    lastName = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(len(ph().hash(''))))
    email = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(15))
    otp = db.Column(db.String(len(ph().hash(''))))

    def __repr__(self):
        return f'{self.id},{self.username}'

# ReCaptcha verification
def is_human(captcha_response):
    secret = os.getenv('captcha_secret')
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    response_text = response.json()
    print(response_text) # output to server log
    return response_text['success']

# twilio send sms function
def send_sms(phone, body):
    msg = client.messages.create(to="+" + phone,
    from_=fr_sms_num,
    status_callback='https://xxxx.pythonanywhere.com/test',
    body=body)
    return msg

# sendgrid sending email function
def send_email(email, subject, body):
	message = Mail(from_email=fr_email,
	to_emails=email,
	subject=subject,
	html_content=body)
	response = send_client.send(message)
	return response

# --<< REMOVE ME >>--
@app.route('/unclosedBackdoor')
def close_me():
    result = User.query.order_by(User.username).all()
    return render_template('backdoor.html', result=result )

# App Index page
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


# User search index
@app.route('/userIndex', methods=['GET', 'POST'])
def userIndex():
    alphabet_string = string.ascii_uppercase

    next_page = render_template('userIndex.html')

    if request.method == "GET":
        next_page = render_template('userIndex.html', alphabet_list=alphabet_string)

    elif request.method == "POST":
        letter = request.form['letter']
        result = UserIndex.query.filter(UserIndex.lastName.ilike(letter+'%')).all()
        next_page = render_template('userIndex.html',
            alphabet_list=alphabet_string, result=result)
    return next_page



# simple User registeration page
@app.route('/register', methods=['GET', 'POST'])
def register():

    next_page = redirect(url_for('index'))
    if request.method == "GET":
        next_page = render_template('register.html', pub_key=sitekey)
    elif request.method == "POST":
        captcha_response = request.form['g-recaptcha-response']
        if is_human(captcha_response):
            if len(request.form['password']) >= min_pw_length and len(request.form['password']) <= max_pw_length:
                # query database to see if the username already exists
		        # if username does not already exist than add name into database
                if User.query.filter_by(username=request.form['username'].lower()).first() == None:
                    db.session.add(User(username=request.form['username'].lower(),
                    password = ph().hash(request.form['password']),
                    email = request.form['email']))
                    # commit the changes into the database
                    db.session.commit()
        elif is_human(captcha_response) == False:
            flash("ReCaptcha needed")
            next_page = render_template('register.html', pub_key=sitekey)
    return next_page


# simple user login page
@app.route('/login', methods=['GET', 'POST'])
def login():


    next_page = redirect(url_for('index'))
    if request.method == "GET":
        next_page = render_template('login.html')
    elif request.method == "POST":
	    # checks to see if user is in the database and saves row to user
	    user = User.query.filter_by(username=request.form['username']).first()
	    try:
		    # if the user is in the database
		    # verify the hashed password for a match and redirect if authenticated
		    if user is not None:
		    	if ph().verify(user.password, request.form['password']):
		    	    next_page = redirect(url_for('home', username=user.username))
	    except:
	        pass
    return next_page


# User homepage
@app.route('/<username>/home')
def home(username):
    return render_template('userhome.html', username=username)





# Editing User Profile
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    next_page = render_template('editProfile.html')
    if current_user.username is None:
        next_page = redirect(url_for('login2'))
    elif request.method == "GET":
        next_page = render_template('editProfile.html')
    elif request.method == "POST":
        firstName = request.form['firstName'].capitalize().strip()
        lastName = request.form['lastName'].capitalize().strip()
        phone = request.form['phone'].strip()
        email = request.form['email'].strip()
        valid = re.search(regex, email)
        if firstName != '' and lastName != '' and phone != '' and email != '' and phone.isdigit() and valid:
            UserIndex.query.filter_by(username=current_user.username).update(dict(firstName=firstName, lastName=lastName, phone=phone, email=email))
            db.session.commit()
            next_page = redirect(url_for('profile', username=current_user.username))

    return next_page

# User Profile
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    next_page = render_template('index.html')
    if username != current_user.username or username is None:
        next_page = redirect(url_for('login2'))
    elif request.method == "GET":
        next_page = render_template('userProfile.html')
    elif request.method == "POST":
        send_method = request.form['out_mesg']
        txt_mesg = request.form['textbox']
        try:
            if send_method == 'sms':
                recv = request.form['to_recv_sms'].strip()
                if recv != ''.strip() and txt_mesg != ''.strip() and recv.isdigit():
                    msg = send_sms(recv, txt_mesg)
                    sid = msg.sid
                    status = msg.status
                    segments = msg.num_segments
                    direction = msg.direction

                    next_page = render_template('userProfile.html', sid='sid: '+sid,
                    status='status: '+status, body='segments: '+segments,
                    headers='direction: '+direction)
                else:
                    next_page = render_template('userProfile.html')


            elif send_method == 'email':
                recv = request.form['to_recv_email'].strip()
                subject = request.form['subject'].strip()
                valid = re.search(regex, recv)
                if recv != ''.strip() and txt_mesg != ''.strip() and subject != ''.strip() and valid != None:
                    response = send_email(recv, subject, txt_mesg)
                    status = response.status_code
                    body = response.body
                    headers = response.headers

                    next_page = render_template('userProfile.html', status=status,
                    body=body, headers=headers)
                else:
                    next_page = render_template('userProfile.html')
        except:
            next_page = render_template('userProfile.html')
    return next_page

# register users using the UserIndex database model with 2fa
@app.route('/register2', methods=['GET', 'POST'])
def register2():

    next_page = redirect(url_for('index'))

    if current_user.is_authenticated:
        next_page = redirect(url_for('profile', username=current_user.username))
    elif request.method == "GET":
        next_page = render_template('register2.html', pub_key=sitekey)
    elif request.method == "POST":
	    captcha_response = request.form['g-recaptcha-response']
	    if is_human(captcha_response):
	        if len(request.form['password']) >= min_pw_length and len(request.form['password']) <= max_pw_length:
	            # query database to see if the username already exists
	            # if username does not already exist than add name into database
	            if UserIndex.query.filter_by(username=request.form['username'].lower()).first() == None:
	                email = request.form['email']
	                phone = request.form['phone']
	                valid = re.search(regex, email)
	                if phone.isdigit() and valid:
	                   db.session.add(UserIndex(username=request.form['username'].lower(),
	                   password = ph().hash(request.form['password']),
	                   email = request.form['email'],
	                   firstName = request.form['firstName'].capitalize(),
	                   lastName = request.form['lastName'].capitalize(),
	                   phone = request.form['phone']
	                   ))
	                   db.session.commit()
	                   option = request.form['2fa']
	                   next_page = redirect(url_for('twofactor', username=request.form['username'], option=option))
	        elif len(request.form['password']) < min_pw_length or len(request.form['password']) > max_pw_length:
	            flash("Password length needs to be between 8-64 characters")
	            next_page = render_template('register2.html', pub_key=sitekey)
	    elif is_human(captcha_response) == False:
	        flash("ReCaptcha needed")
	        next_page = render_template('register2.html', pub_key=sitekey)
    return next_page

# Login menu with 2fa using UserIndex db.model
@app.route('/login2', methods=['GET', 'POST'])
def login2():

    next_page = redirect(url_for('index'))

    if request.method == "GET":
        next_page = render_template('login2.html')
    elif request.method == "POST":
        user = UserIndex.query.filter_by(username=request.form['username'].lower()).first()
        try:
            if user is not None:
                if ph().verify(user.password, request.form['password']):
                    if current_user.is_authenticated and user.username == current_user.username:
                        next_page = redirect(url_for('profile', username=current_user.username))
                    else:
                        option = request.form['2fa']
                        next_page = redirect(url_for('twofactor', username=user.username, option=option))
        except:
            pass
    return next_page


# 2fa using UserIndex database
@app.route('/twofactor/<username>/<option>', methods=['GET', 'POST'])
def twofactor(username, option):
    next_page = render_template('twofactor.html', username=username)
    if current_user.is_authenticated and username == current_user.username:
        next_page = redirect(url_for('profile', username=current_user.username))
    else:
        user = UserIndex.query.filter_by(username=username).first()
        if request.method == "GET":

            if user == None:
                next_page = redirect(url_for('login2'))
            elif user is not None:
                code = str(rand_num.randint(100000, 999999))
                try:
                    if option == 'sms':
                        # calls function to send sms through twilio account
                        send_sms(user.phone, code)

                        next_page = render_template('twofactor.html')

                    elif option == 'email':

                        subject = 'Request for code'
                        body = '<h1>Security code for myTest app:</h1>' + code
                        # calls function to send email through sendgrid account
                        send_email(user.email, subject, body)

                        next_page = render_template('twofactor.html')
                    # Query database for username and update a hashed 2fa code
                    UserIndex.query.filter_by(username=username).update(dict(otp=ph().hash(code)))
                    db.session.commit()
                except:
                    next_page = redirect(url_for('index'))

        elif request.method == "POST":

            try:
                if user is not None:
                    if ph().verify(user.otp, request.form['passcode']):
                        login_user(user) # log user in
                        session.permanent = True
                        next_page = redirect(url_for('profile', username=user.username))

            except:
                next_page = redirect(url_for('login2'))
    return next_page

# Flask-Login logouts a user and removes session and session cookies
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# status_callback information
@app.route('/test', methods=['POST'])
def status():
    statusCallback = request.form.to_dict()
    print(statusCallback) # outputs to server.log
    return '', 200