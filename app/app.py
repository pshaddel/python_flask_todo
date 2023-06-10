from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.models import Todo, db, User
from functools import wraps
import hashlib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            print('not session')
            return redirect(url_for('login'))
        print('session')
        return f(*args, **kwargs)
    return decorated_function

@app.route ('/', methods=['GET'])
@login_required
def index():
    tasks = Todo.getTasks(user_id=session['user_id'])
    return render_template('index.html', tasks=tasks)

@app.route('/', methods=['POST'])
@login_required
def addTask():
    task_content = request.form['content']
    user_id = session['user_id']
    new_task = Todo (content=task_content, user_id=user_id)
    try:
        new_task.save()
        # redirect to index with url_for
        return redirect(url_for('index'))
    except:
        return 'There was an error adding the task'

@app.route ('/tasks/delete/<int:id>', methods=['POST'])
def delete(id):
    task = Todo.query.get_or_404(id)
    try:
        task.delete()
        return redirect(url_for('index'))
    except:
        return 'There was a problem deleting that task'

@app.route ('/tasks/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        print('update')
        print(id)
        task.content = request.form['content']
        try:
            task.update()
            return redirect(url_for('index'))
        except:
            return 'There was a problem updating that task'
    else:
        return render_template('update.html', task=task)

@app.route ('/users/register/', methods=['GET', 'POST'])
def register():
    # print string representation of all users
    stringUsers = User.getUsers()
    for user in stringUsers:
        print(user)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # hash password
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        new_user = User (name=name, email=email, password=hashed_password)

        try:
            result = new_user.save() # returns a boolean, if False it means the email already exists
            if not result:
                # send a flashed message to the register page
                return render_template('register.html', message='Email already exists')
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            return 'There was an error adding the user'
    else:
        return render_template('register.html')

@app.route ('/users/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # hash password
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # check if email and password match
        user = User.getUserByEmailAndPassword(email, hashed_password)
        if user:
            print('successful login')
            # set session
            print(user.id)
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            print('unsuccessful login')
            return render_template('login.html', message='Email or password is incorrect')
    else:
        return render_template('login.html')

@app.route ('/users/logout/', methods=['GET'])
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
     app.run(port=8000, debug=True)