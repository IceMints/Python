'''
Create a flask app with a custom error (404) page using Jinja2 template:
-basic or fancy UI
-Include either a humorous GIF, IMAGE or Quote
	File name or URL should be passed to template from app
-Page showing date and time in 2 formats 1) UTC 2) Client's time zone and locale settings
	Passed from to template from app
'''

from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from pytz import reference


app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)

#courtesy of GIPHY website at https://giphy.com
source = 'https://giphy.com/embed/xULW8PLGQwyZNaw68U'


#used datetime and pytz to locate the timezone of local time
localtime = reference.LocalTimezone()
time_zone = localtime.tzname(datetime.now())


@app.route('/index')
def index():
    return render_template('lab_index.html', current_time=datetime.utcnow())

# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def page_not_found(e):
# defining function	
    return render_template('lab_404.html',
							current_time=datetime.utcnow(),
							source=source,
							time_zone = time_zone), 404
