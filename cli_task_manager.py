from datetime import datetime
import json
import argparse

class Task:
    def __init__(self, title, description, priority, status = "pending", created_at = None):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = created_at or datetime.now()
        self.completed_at = None

    
    def __repr__(self):
        return f"Task({self.title}, ({self.description}), {self.priority}, {self.status}, {self.created_at})"



class StorageBackend:
    def __init__(self, filename):
        self.filename = filename
    
    def save(self, tasks):
        tasks_dict = []
        for task in tasks:
            tasks_dict.append({"title": task.title, "description": task.description, "priority": task.priority, 'status': task.status, "creation": str(task.created_at)})

        with open(self.filename, 'w') as f:
            json.dump(tasks_dict, f)

    
    def load(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return []
        task = []
        for d in data:
            task.append(Task(d['title'], d['description'], d['priority'], d['status'], d['creation']))

        return task
    

class TaskManager():
    def __init__(self, storage):
        self.storage = storage
        self.tasks = self.storage.load()

    def add(self, task):
        self.tasks.append(task)
        self.storage.save(self.tasks)
        return self.tasks
    
    def delete(self, title):
        results = []
        for task in self.tasks:
            if title in task.title:
                results.append(task)
        if not results:
            return "task not found."
        for task in results:
            self.tasks.remove(task)
        self.storage.save(self.tasks)

    
    def complete(self, title):
        for task in self.tasks:
            if title in task.title:
                task.status = 'complete'
                task.completed_at = datetime.now()

        self.storage.save(self.tasks)
    
    def search(self, title):
        result = []
        for task in self.tasks:
            if title in task.title:
                result.append(task)
        return result
    
    def list(self):
        return self.tasks
    




                        




parser = argparse.ArgumentParser(description='task manager')
subparsers = parser.add_subparsers(dest='command')

#add command 

add_parser = subparsers.add_parser("add")
add_parser.add_argument("title")
add_parser.add_argument("description")
add_parser.add_argument("--priority", default="medium")

# delete command 

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("title")

# complete command 

complete_parser = subparsers.add_parser("complete")
complete_parser.add_argument("title")


# search command 

search_parser = subparsers.add_parser("search")
search_parser.add_argument("title")

#list command

list_parser = subparsers.add_parser("list")


args = parser.parse_args()

storage = StorageBackend("tasks.json")
manager = TaskManager(storage)

if args.command == "add":
    task = Task(args.title, args.description, args.priority)
    manager.add(task)
elif args.command == "delete":
    manager.delete(args.title)
elif args.command == "complete":
    manager.complete(args.title)
elif args.command == "search":
    print(manager.search(args.title))
elif args.command == 'list':
    print(manager.list())
else:
    print("enter a valid command in this.")