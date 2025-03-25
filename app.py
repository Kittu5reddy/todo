from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(10), default='medium')
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Todo {self.title}>'

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """
    Home route to display all todos
    Supports filtering by status and sorting
    """
    # Get filter and sort parameters
    status = request.args.get('status', 'all')
    sort = request.args.get('sort', 'created_at')
    
    # Build query based on status
    if status == 'completed':
        todos = Todo.query.filter_by(completed=True)
    elif status == 'pending':
        todos = Todo.query.filter_by(completed=False)
    else:
        todos = Todo.query

    # Apply sorting
    if sort == 'priority':
        todos = todos.order_by(Todo.priority)
    elif sort == 'title':
        todos = todos.order_by(Todo.title)
    else:
        todos = todos.order_by(Todo.created_at.desc())

    return render_template('index.html', todos=todos.all(), 
                           current_status=status, 
                           current_sort=sort)

@app.route('/add', methods=['GET', 'POST'])
def add_todo():
    """
    Route to add a new todo
    Handles both GET (display form) and POST (submit form) methods
    """
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        priority = request.form.get('priority', 'medium')

        # Validate input
        if not title:
            flash('Title is required!', 'error')
            return redirect(url_for('add_todo'))

        # Create new todo
        new_todo = Todo(
            title=title, 
            description=description, 
            priority=priority
        )
        
        try:
            db.session.add(new_todo)
            db.session.commit()
            flash('Todo added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding todo: {str(e)}', 'error')

    return render_template('add_todo.html')

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    """
    Route to mark a todo as completed
    """
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = not todo.completed
    
    try:
        db.session.commit()
        flash(f"Todo {'completed' if todo.completed else 'marked as pending'}!", 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating todo: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    """
    Route to delete a todo
    """
    todo = Todo.query.get_or_404(todo_id)
    
    try:
        db.session.delete(todo)
        db.session.commit()
        flash('Todo deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting todo: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    """
    Route to edit an existing todo
    """
    todo = Todo.query.get_or_404(todo_id)
    
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form.get('description', '')
        todo.priority = request.form.get('priority', 'medium')
        
        try:
            db.session.commit()
            flash('Todo updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating todo: {str(e)}', 'error')
    
    return render_template('edit_todo.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True)