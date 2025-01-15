# Task-Manager

- This is an Interactive Task Manager built in Python, utilizing the rich library for creating beautiful and dynamic terminal-based interfaces. The app allows you to efficiently manage your tasks, including adding, viewing, completing, deleting, editing, and searching tasks.

- The rich library enhances the user experience with color, formatting, and interactive elements, making task management both functional and visually appealing.

## Features

- Add new tasks with customizable names, priorities, and deadlines.
- Mark tasks as completed.
- Search tasks by keyword or priority.
- Edit tasks to update their details.
- Sort tasks by deadline, priority, or name.
- View a detailed list of all tasks.

## Task Storage

- Tasks are stored in a JSON file (tasks.json), which contains a list of tasks in JSON format. This file is automatically updated whenever you add, edit, delete, or complete a task. The structure of the tasks.json file allows for easy retrieval and manipulation of task data.
- Tasks are stored in an array, making it easy to add new tasks and update existing ones.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jenishmsoni45/task-manager.git
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the program:
   ```bash
   python task_manager.py
   ```
