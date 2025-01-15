from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
import json

console = Console()


# Modify the Task class definition
class Task:
    def __init__(self, name, priority, deadline, completed=False, category="General"):
        """
        Initializes a task with the given parameters.
        :param name: Name/Description of the task.
        :param priority: Priority of the task (high, medium, low).
        :param deadline: Deadline of the task (string, YYYY-MM-DD format).
        :param completed: Boolean indicating if the task is completed.
        :param category: Category of the task (e.g., Work, Personal).
        """
        self.name = name
        self.priority = priority
        self.deadline = deadline
        self.completed = completed
        self.category = category


    def mark_completed(self):
        """
        Marks the task as completed.
        """
        self.completed = True


    def __str__(self):
        return f"{self.name} (Priority: {self.priority}, Deadline: {self.deadline}, Category: {self.category})"



class TaskManager:
    def __init__(self, filename):
        """
        Initializes the TaskManager with a file to save and load tasks.
        :param filename: The name of the file to store tasks persistently.
        """
        self.filename = filename
        self.tasks = []  # Initialize an empty list for tasks
        self.load_tasks()  # Load existing tasks from the file, if any

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [
                    Task(
                        name=task["name"],
                        priority=task["priority"],
                        deadline=task["deadline"],
                        completed=task.get("completed", False),  # Default to False if missing
                        category=task.get("category", "General")  # Default to "General" if missing
                    )
                    for task in tasks_data
            ]
        except FileNotFoundError:
            self.tasks = []  # If no file, start with an empty list
        except Exception as e:
            print(f"An error occurred while loading tasks: {e}")
            self.tasks = []

    def save_tasks(self):
        tasks_data = [
        {
            "name": task.name,
            "priority": task.priority,
            "deadline": task.deadline,
            "completed": task.completed,  # Save the completed status
            "category": task.category  # Save the category
        }
        for task in self.tasks
        ]
        with open(self.filename, 'w') as file:
            json.dump(tasks_data, file, indent=4)
        """
        Saves the current list of tasks to the file.
        """
    


    #addition of search tasks
    # Add this method to the TaskManager class
    """
    Search tasks by keyword in name or by priority.
    """
    def search_tasks(self, keyword=None, priority=None):
        results = []
        for task in self.tasks:
            if keyword and keyword.lower() in task.name.lower():
                results.append(task)
            elif priority and task.priority.lower() == priority.lower():
                results.append(task)
        return results
    
    #addn of edit task method
    """
    Edit an existing task.
    """
    
    def edit_task(self, task_index, new_name=None, new_priority=None, new_deadline=None):
        if 0 <= task_index < len(self.tasks):
            task = self.tasks[task_index]
            if new_name:
                task.name = new_name
            if new_priority:
                task.priority = new_priority
            if new_deadline:
                task.deadline = new_deadline
            print("Task updated successfully!")
        else:
            print("Invalid task index.")

    
    #addn of sort_tasks
    # Add this method to the TaskManager class
    """
    Sort tasks by deadline, priority, or name.
    """
    def sort_tasks(self, by="deadline"):
        if by == "deadline":
            self.tasks.sort(key=lambda task: task.deadline)
        elif by == "priority":
            priority_map = {"high": 1, "medium": 2, "low": 3}
            self.tasks.sort(key=lambda task: priority_map.get(task.priority.lower(), 4))
        elif by == "name":
            self.tasks.sort(key=lambda task: task.name.lower())
        else:
            print("Invalid sort option.")
        print(f"Tasks sorted by {by}.")
    
    

    """
    Adds a new task to the list.
    :param name: Name/Description of the task.
    :param priority: Priority of the task (high, medium, low).
    :param deadline: Deadline of the task (string, YYYY-MM-DD format).
    :param category: Category of the task (e.g., Work, Personal).
    """
    def add_task(self, name, priority, deadline, category="General"):
        new_task = Task(name, priority, deadline, completed=False, category=category)
        self.tasks.append(new_task)
        self.save_tasks()  # Save tasks to file
        console.print(f"[bold green]Task '{name}' added successfully under category '{category}'![/bold green]")



    """
    Displays all tasks in the list.
    """
    def view_tasks(self):
        if not self.tasks:
            console.print("[bold red]No tasks available.[/bold red]")
            return

        # Create a table with headers
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Task #", style="dim", width=6)
        table.add_column("Task Name", style="cyan", width=30)
        table.add_column("Priority", style="magenta")
        table.add_column("Deadline", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Category", style="white")

        for idx, task in enumerate(self.tasks, start=1):
            status = "Completed" if task.completed else "Pending"
            table.add_row(
                str(idx),
                task.name,
                task.priority.capitalize(),
                task.deadline,
                status,
                task.category
            )
    
        console.print(table)


    """
    Marks a task as completed by index.
    :param index: The index of the task to complete (0-based).
    """
    def complete_task(self, index):
        try:
            self.tasks[index].mark_completed()
            self.save_tasks()  # Save the updated state to the file
            print(f"Task '{self.tasks[index].name}' marked as completed.")
        except IndexError:
            print("Invalid task index. Please try again.")

    """
    Deletes a task from the list.
    :param index: The index of the task to delete.
    """
    def delete_task(self, index):
        try:
            deleted_task = self.tasks.pop(index)
            self.save_tasks()  # Save changes to file
            console.print(f"[bold red]Task '{deleted_task.name}' deleted successfully.[/bold red]")
        except IndexError:
            console.print("[bold red]Invalid task index.[/bold red]")



def main():
    console.print(Panel("Welcome to the Task Manager!", style="bold cyan"))
    filename = "tasks.json"  # Specify the file to save/load tasks
    manager = TaskManager(filename)  # Initialize the task manager
    manager.load_tasks()  # Load tasks from the file, if any

    while True:
        console.print("""
Options:
[1] Add Task
[2] View Tasks
[3] Complete Task
[4] Delete Task
[5] Search Tasks
[6] Edit Task
[7] Sort Tasks
[8] Exit
""", style="bold yellow")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7", "8"], default="1")

        if choice == "1":
            console.print("\n[bold green]Add New Task:[/bold green]")
            name = input("Enter task name: ")
            priority = input("Enter priority (high, medium, low): ")
            deadline = input("Enter deadline (YYYY-MM-DD): ")
            category = input("Enter category (e.g., Work, Personal, Study, or press Enter to skip): ")
            manager.add_task(name, priority, deadline, category or "General")


        elif choice == "2":
            console.print("\n[bold green]View Tasks:[/bold green]")
            manager.view_tasks()

        elif choice == "3":
            console.print("\n[bold green]Complete Task:[/bold green]")
            manager.view_tasks()
            try:
                task_index = int(input("Enter the task number to complete: ")) - 1
                manager.complete_task(task_index)
            except ValueError:
                console.print("[bold red]Invalid input![/bold red]")

        elif choice == "4":
            console.print("\n[bold red]Delete Task:[/bold red]")
            manager.view_tasks()
            try:
                task_index = int(input("Enter the task number to delete: ")) - 1
                manager.delete_task(task_index)
            except ValueError:
                console.print("[bold red]Invalid input![/bold red]")

        elif choice == "5":
            console.print("\n[bold blue]Search Tasks:[/bold blue]")
            search_type = input("Search by [1] Keyword or [2] Priority: ")
            if search_type == "1":
                keyword = input("Enter keyword to search: ")
                results = manager.search_tasks(keyword=keyword)
            elif search_type == "2":
                priority = input("Enter priority (high, medium, low): ")
                results = manager.search_tasks(priority=priority)
            else:
                console.print("[bold red]Invalid choice![/bold red]")
                results = []

            if results:
                console.print("\n[bold green]Search Results:[/bold green]")
                for idx, task in enumerate(results, 1):
                    status = "Completed" if task.completed else "Pending"
                    console.print(f"{idx}. {task.name} | {task.priority} | {task.deadline} | {status}")
            else:
                console.print("[bold red]No matching tasks found.[/bold red]")

        elif choice == "6":
            console.print("\n[bold yellow]Edit Task:[/bold yellow]")
            manager.view_tasks()
            try:
                task_index = int(input("Enter the task number to edit: ")) - 1
                new_name = input("Enter new task name (or press Enter to skip): ")
                new_priority = input("Enter new priority (high, medium, low, or press Enter to skip): ")
                new_deadline = input("Enter new deadline (YYYY-MM-DD, or press Enter to skip): ")
                manager.edit_task(task_index, new_name, new_priority, new_deadline)
            except ValueError:
                console.print("[bold red]Invalid input![/bold red]")

        elif choice == "7":
            console.print("\n[bold cyan]Sort Tasks:[/bold cyan]")
            sort_choice = input("Choose [1] by Deadline, [2] by Priority, [3] by Name: ")
            if sort_choice == "1":
                manager.sort_tasks(by="deadline")
            elif sort_choice == "2":
                manager.sort_tasks(by="priority")
            elif sort_choice == "3":
                manager.sort_tasks(by="name")
            else:
                console.print("[bold red]Invalid sort option![/bold red]")

        elif choice == "8":
            console.print("[bold magenta]Exiting Task Manager. Goodbye![/bold magenta]")
            manager.save_tasks()  # Save tasks to the file
            break

        else:
            console.print("[bold red]Invalid option. Please choose a valid number (1-8).[/bold red]")


if __name__ == "__main__":
    main()






