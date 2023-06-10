from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.models import Todo, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo (content=task_content)

        try:
            new_task.save()
            return redirect('/')
        except:
            return 'There was an error adding the task'
    else:
        tasks = Todo.getTasks()
        return render_template('index.html', tasks=tasks)

@app.route ('/tasks/delete/<int:id>', methods=['POST'])
def delete(id):
    task = Todo.query.get_or_404(id)
    try:
        task.delete()
        return redirect('/')
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
            return redirect('/')
        except:
            return 'There was a problem updating that task'
    else:
        return render_template('update.html', task=task)
if __name__ == '__main__':
     app.run(port=8000, debug=True)