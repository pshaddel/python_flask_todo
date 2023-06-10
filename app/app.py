from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
from datetime import datetime
# from models.todo import Todo

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Integer, default=0)

    def __repr__ (self):
        return '<Task %r>' % self.id

    def update(self):
        db.session.commit()

    def delete(self):
        self.is_deleted = 1
        self.update()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getTasks():
        return Todo.query.order_by(Todo.date_created).filter_by(is_deleted=0).all()

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