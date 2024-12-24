import os
import json
from argparse import ArgumentParser
from datetime import datetime
import sys

abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)
todolist_file = os.path.join(dir_name,"Data",'ToDoList.json')
STATUS = ['todo', 'in-progress', 'done']

def check_list_exists(func):
    def wrapper(*args, **kwargs):
        if os.path.exists(todolist_file):
            result = func(*args, **kwargs)
        else:
            print("No list Exists, use '--create' to create a new list")
        return result
    return wrapper

@check_list_exists
def read_list():
    with open(todolist_file,'r') as file:
        data = json.load(file)
    return data

@check_list_exists
def write_list(data={}):
    with open(todolist_file,'w') as file:
        json.dump(data, file, indent=4)

def create_new_list():
    if not os.path.exists(todolist_file):
        write_list()
        print('List has been created')
        return
    print('File already Exists')

def list_items(status):
    data = read_list()
    if data:
        if status.lower() == 'all':
            for id, item in data.items():
                print(id, item['description'])
        elif status.lower() in STATUS:
            for id, item in data.items():
                if item['status'] == status.lower():
                    print(id, item['description'])
        else:
            print(f'Please choose a relevant status option: {STATUS}')

    else:        
        print('List is empty, use "--add" to add new items to the list.')

def add_item(item):
    data = read_list()
    if data:
        id = max([int(key) for key in data.keys()]) + 1
    else:
        id = 1
    data[id] = {
            'description' : item,
            'created_at' : datetime.now().isoformat(),
            'updated_at' : None,
            'status' : 'todo'
        }
    
    write_list(data)
    print('Item added')
        
def update(input):
    if len(input) != 2:
        print('mismatched values, Please provide two values')
        return
    id = input[0]
    description = input[1]
    
    data = read_list()
    if id not in data:
        print('No list available for ',input[0])
        return
    data[id]['description'] = description
    data[id]['updated_at'] = datetime.now().isoformat()
    write_list(data)
    print('Description had been updated for', id)

def mark_status(input):
    if len(input) != 2:
        print('mismatched values, Please provide two values')
        return
    data = read_list()
    id = input[0]
    status = input[1]

    if status.lower() not in STATUS:
        print(f'Please choose a relevant status option: {STATUS}')
        return
    
    data = read_list()
    if id not in data:
        print('No list available for ',id)
        return
    data[id]['status'] = status.lower()
    data[id]['updated_at'] = datetime.now().isoformat()
    write_list(data)
    print('Status had been updated for', id)

def main():
    print('Try "--help" to see the list of arguments that are available for this tool')

if __name__ == "__main__":
    parser = ArgumentParser(description='To Create, edit, view a todo list via CLI')
    parser.add_argument('--create', action='store_true', help='To create a new to do list')
    parser.add_argument('--list', help='To list down to do list')
    parser.add_argument('--add', help='To Add something to an existing to do list')
    parser.add_argument('--update', nargs='+', help='To update the description of an existing data')
    parser.add_argument('--mark', nargs='+', help='To mark the status of an existing data')

    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        main()

    if args.create:
        create_new_list()
    
    if args.list:
        list_items(args.list)

    if args.add:
        add_item(args.add)

    if args.update:
        update(args.update)

    if args.mark:
        mark_status(args.mark)