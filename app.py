from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed= db.Column(db.Integer, default=0)
    dateCreated= db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %e>' %self.id
    
with app.app_context():
    db.create_all()
    
    
@app.route("/", methods=['POST','GET'])
def base():
    if request.method == 'POST':
        task_content= request.form['content']
        new_task=Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There is an issue adding task"
    else:
        tasks= Todo.query.order_by(Todo.dateCreated).all()
        return render_template('base.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete_key(id):
    task_to_delete= Todo.query.get(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return " Error in deletion"
    
@app.route('/update/<int:id>', methods=['POST','GET'])
def update_key(id):
    task_to_update=Todo.query.get(id)
    if request.method=='POST':
        task_to_update.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error in updating"
    else:
        return render_template('update.html', task=task_to_update)
    
    
    
    
    
    
    
if __name__=="__main__":
    app.run(debug=True)
    