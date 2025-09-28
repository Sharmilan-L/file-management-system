import os
import shutil

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_front(self, data):
        new_node = Node(data)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        # Removed raise NotImplementedError

    def insert_end(self, data):
        new_node = Node(data)
        new_node.prev = self.tail
        if self.tail:
            self.tail.next = new_node
        else:
            self.head = new_node
        self.tail = new_node
        # Removed raise NotImplementedError

    def delete(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        # Removed raise NotImplementedError

    def find(self, data):
        current = self.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None
        # Removed raise NotImplementedError

    def display_forward(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
        # Removed raise NotImplementedError

    def display_backward(self):
        result = []
        current = self.tail
        while current:
            result.append(current.data)
            current = current.prev
        return result
        # Removed raise NotImplementedError

class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)
        # Removed raise NotImplementedError

    def pop(self):
        if self.is_empty():
            print("Stack underflow!")
            return None
        return self._items.pop()
        # Removed raise NotImplementedError

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]
        # Removed raise NotImplementedError

    def is_empty(self):
        return len(self._items) == 0
        # Removed raise NotImplementedError

# File Management System (FMS) functions

def list_directory(path):
    try:
        return os.listdir(path)
    except FileNotFoundError:
        print("Directory not found.")
        return []

def create_file(path):
    try:
        with open(path, 'x') as f:  # 'x' mode: create, fail if exists
            pass
    except FileExistsError:
        print(f"File '{path}' already exists.")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

def append_file(path, content):
    with open(path, 'a') as f:
        f.write(content)

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("File not found.")
        return ""

def delete_file(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        print("File not found.")

def move_file(src, dest):
    try:
        shutil.move(src, dest)
    except FileNotFoundError:
        print("Source file not found.")

def undo_last_operation(stack, dll):
    op = stack.pop()
    if not op:
        return

    if op[0] == 'create':
        delete_file(op[1])
        node = dll.find(op[1])
        if node:
            dll.delete(node)

    elif op[0] == 'delete':
        create_file(op[1])
        write_file(op[1], op[2])
        dll.insert_end(op[1])

    elif op[0] in ('write', 'append'):
        write_file(op[1], op[2])

    elif op[0] == 'move':
        move_file(op[2], op[1])

    print(f"Undid {op[0]} on {op[1]}")

def demo_integration():
    dll = DoublyLinkedList()
    stack = Stack()

    print("\n=== Integration Demo ===")
    create_file('demo1.txt')
    dll.insert_end('demo1.txt')
    stack.push(('create', 'demo1.txt'))
    print("After create:", list_directory('.'))

    old_content = ''
    write_file('demo1.txt', 'Hello, World!')
    stack.push(('write', 'demo1.txt', old_content))

    content = read_file('demo1.txt')
    delete_file('demo1.txt')
    stack.push(('delete', 'demo1.txt', content))
    node = dll.find('demo1.txt')
    if node:
        dll.delete(node)
    print("After delete:", list_directory('.'))

    print("\nUndoing last 3 operations:")
    for _ in range(3):
        undo_last_operation(stack, dll)
    print("Directory now:", list_directory('.'))

def show_menu():
    print("\nFMS Menu:")
    print("1. List directory")
    print("2. Create file")
    print("3. Write file")
    print("4. Append file")
    print("5. Read file")
    print("6. Delete file")
    print("7. Move file")
    print("8. Demo DoublyLinkedList & Stack integration")
    print("9. Exit")

def handle_choice(choice):
    if choice == "1":
        path = input("Directory path: ")
        entries = list_directory(path)
        print(entries)
    elif choice == "2":
        path = input("File path to create: ")
        create_file(path)
        print(f"Created file: {path}")
    elif choice == "3":
        path = input("File path to write: ")
        content = input("Content: ")
        write_file(path, content)
        print(f"Written to file: {path}")
    elif choice == "4":
        path = input("File path to append: ")
        content = input("Content: ")
        append_file(path, content)
        print(f"Appended to file: {path}")
    elif choice == "5":
        path = input("File path to read: ")
        data = read_file(path)
        print(data)
    elif choice == "6":
        path = input("File path to delete: ")
        delete_file(path)
        print(f"Deleted file: {path}")
    elif choice == "7":
        src = input("Source path: ")
        dest = input("Destination path: ")
        move_file(src, dest)
        print(f"Moved file from {src} to {dest}")
    elif choice == "8":
        demo_integration()
    else:
        print("Invalid choice, please try again.")

if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Enter choice: ")
        if choice == "9":
            print("Exiting.")
            break
        handle_choice(choice)
