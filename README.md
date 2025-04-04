# Todo App

This is a simple Todo application built with Flask. It allows users to add, edit, and delete todos, as well as filter them by status.

## Features

- Add new todos with a title, description, and priority.
- Edit existing todos.
- Mark todos as completed or pending.
- Delete todos.
- Filter todos by status (all, pending, completed).

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/todo-app.git
   cd todo-app
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the application:
   ```sh
   flask run
   ```

## Usage

- Open your web browser and go to `http://127.0.0.1:5000/` to access the Todo App.
- Use the navigation links to view all todos or add a new todo.
- Use the filter links to filter todos by status.
- Click on the edit icon to edit a todo.
- Click on the delete icon to delete a todo.

## Screenshots

![Todo List](./imgs/1.png)
![Todo List](./imgs/2.png)
