from flask import Flask, render_template, send_file, redirect, url_for, session, request
from werkzeug.utils import secure_filename
from config import *
from random import randint
import json
import os
from datetime import datetime
from database import DB


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET
auth = DB('users.db')

_id = lambda length: ''.join([CHARSET[randint(0, len(CHARSET) - 1)] for i in range(length)]) 

def read_data(f):
	with open(f, 'r') as df:
		return json.loads(df.read())

def dump_data(f, d):
	with open(f, 'w') as df:
		json.dump(d, df, indent=4)

def get_date():
	weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	date = str(datetime.now())[0:10]
	weekday = datetime.today().weekday()
	return f'{weekdays[weekday]} {date}'

def reverse_dict(d):
	ret = {}
	keys = list(reversed([key for key in d]))
	for key in keys: ret[key] = d[key]
	return ret

@app.route('/mothersday', methods=['GET', 'POST'])
def mothersday():
	if not 'logged_in' in session: return redirect(url_for('login'))
	if not session['logged_in']: return redirect(url_for('login'))
	email = session['email']
	file = f'storage/{email}/data.json'
	data = read_data(file)
	images = reverse_dict(data)
	from forms import ImageForm
	image_form = ImageForm()
	if image_form.validate_on_submit():
		images = read_data(file)
		for data in image_form.files.data:
			filename = _id(10) + '.jpg'
			data.save(f'storage/{email}/{filename}')
			date = get_date()
			if date in images: images[date].insert(0, filename)
			else:
				images[date] = []
				images[date].insert(0, filename)
		dump_data(file, images)
		return redirect(url_for('mothersday'))
	return render_template('mothersday.html', images=images, image_form=image_form, email=email)

@app.route('/', methods=['GET', 'POST'])
def index():
	if not 'logged_in' in session: return redirect(url_for('login'))
	if not session['logged_in']: return redirect(url_for('login'))
	email = session['email']
	file = f'storage/{email}/data.json'
	data = read_data(file)
	images = reverse_dict(data)
	from forms import ImageForm
	image_form = ImageForm()
	if image_form.validate_on_submit():
		images = read_data(file)
		for data in image_form.files.data:
			filename = _id(10) + '.jpg'
			data.save(f'storage/{email}/{filename}')
			date = get_date()
			if date in images: images[date].insert(0, filename)
			else:
				images[date] = []
				images[date].insert(0, filename)
		dump_data(file, images)
		return redirect(url_for('index'))
	return render_template('index.html', images=images, image_form=image_form, email=email)

@app.route('/image/<string:email>/<string:id>')
def image(email, id):
	return send_file(f'storage/{email}/{id}')

@app.route('/refresh')
def refresh():
	return read_data(DATAFILE)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'logged_in' in session: return redirect(url_for('index'))
	from forms import LoginForm
	login_form = LoginForm()
	if login_form.validate_on_submit():
		email = login_form.email.data
		password = login_form.password.data
		status = auth.check(email, password)
		if status is False:
			messages = ['Incorrect Email or Password']
			return render_template('login.html', login_form=login_form, messages=messages, alert_type='danger')
		if status is None:
			messages = ['Account Doesnt Exist']
			return render_template('login.html', login_form=login_form, messages=messages, alert_type='danger')
		session['logged_in'] = True
		session['email'] = email
		session['messages'] = ['Login Successful']
		return redirect(url_for('index'))
	if 'messages' in session:
		messages = session['messages']
		session.pop('messages')
		return render_template('login.html', login_form=login_form, messages=messages, alert_type='success')
	return render_template('login.html', login_form=login_form)


@app.route('/register', methods=['GET', "POST"])
def register():
	if 'logged_in' in session:
		if session['logged_in'] is True: 
			return redirect(url_for('index'))
	from forms import RegisterForm
	register_form = RegisterForm()
	if register_form.validate_on_submit():
		email = register_form.email.data
		password = register_form.password.data
		status = auth.register(email, password)
		if status is False:
			messages = ['Email Address ({}) Already Taken'.format(email)]
			return render_template('register.html', register_form=register_form, messages=messages, alert_type='danger')
		session['email'] = email
		session['messages'] = ['Successfully Created Account']
		os.mkdir(f'storage/{email}')
		dump_data(f'storage/{email}/data.json', {})
		return redirect(url_for('login'))
	return render_template('register.html', register_form=register_form)


@app.route('/verify', methods=['GET', 'POST'])
def verify():
	from forms import PasswordForm
	password_form = PasswordForm()
	if password_form.validate_on_submit():
		password = password_form.password.data
		if password == PASSWORD:
			session['logged_in'] = True
			return redirect(url_for('index'))
		else:
			messages = ['Incorrect Password.']
			return render_template('password.html', password_form=password_form, messages=messages, alert_type='danger')
	return render_template('password.html', password_form=password_form)

@app.route('/sync', methods=['GET', 'POST'])
def sync():
	req = request.files
	file = [key for key in req][0]
	print(f'Recieved File {file}')
	filename = _id(10) + '.jpg'
	date = get_date()
	images = read_data(DATAFILE)
	if date in images: images[date].insert(0, filename)
	else:
		images[date] = []
		images[date].insert(0, filename)
	dump_data(DATAFILE, images)
	req[file].save(f'storage/{filename}')
	return ""

@app.route('/logout')
def logout():
	session.pop('logged_in')
	return redirect(url_for('index'))

@app.route('/test')
def test():
	import os
	os.system('nautilus')
	return "else"

if __name__ == '__main__':
	app.run(port=5000)
