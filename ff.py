import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

TASKS_FILE = 'tasks.json'

# Предопределённый список задач
predefined_tasks = [
    {"task": "Выучить 10 новых слов", "type": "учёба"},
    {"task": "Пробежать 5 км", "type": "спорт"},
    {"task": "Сделать важный звонок", "type": "работа"},
    # добавьте свои задачи
]

# Загрузка истории
def load_tasks():
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Сохранение истории
def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

# Генерация случайной задачи
def generate_task():
    task = random.choice(predefined_tasks)
    task_text.set(task["task"])
    # Добавляем в историю
    tasks_history.append(task)
    save_tasks(tasks_history)
    update_history()

# Обновление отображения истории
def update_history():
    for item in tree.get_children():
        tree.delete(item)
    for t in tasks_history:
        tree.insert('', 'end', values=(t["task"], t["type"]))

# Ввод новой задачи
def add_task():
    task_desc = new_task_entry.get().strip()
    task_type = task_type_var.get()
    if not task_desc:
        messagebox.showwarning("Внимание", "Введите описание задачи")
        return
    new_task = {"task": task_desc, "type": task_type}
    predefined_tasks.append(new_task)
    tasks_history.append(new_task)
    save_tasks(tasks_history)
    update_history()
    new_task_entry.delete(0, tk.END)

# Фильтрация по типу
def filter_tasks():
    selected_type = filter_var.get()
    filtered = [t for t in tasks_history if t["type"] == selected_type or selected_type == "Все"]
    for item in tree.get_children():
        tree.delete(item)
    for t in filtered:
        tree.insert('', 'end', values=(t["task"], t["type"]))

# Основной код
root = tk.Tk()
root.title("Генератор случайных задач")

tasks_history = load_tasks()

task_text = tk.StringVar()

# Интерфейс
ttk.Button(root, text="Сгенерировать задачу", command=generate_task).pack(pady=5)
ttk.Label(root, textvariable=task_text, font=("Arial", 14)).pack(pady=5)

# Ввод новой задачи
ttk.Label(root, text="Новая задача:").pack()
new_task_entry = ttk.Entry(root, width=50)
new_task_entry.pack()
task_type_var = tk.StringVar(value="учёба")
ttk.Radiobutton(root, text="Учёба", variable=task_type_var, value="учёба").pack()
ttk.Radiobutton(root, text="Спорт", variable=task_type_var, value="спорт").pack()
ttk.Radiobutton(root, text="Работа", variable=task_type_var, value="работа").pack()
ttk.Button(root, text="Добавить задачу", command=add_task).pack(pady=5)

# История и фильтр
ttk.Label(root, text="История задач:").pack()
filter_var = tk.StringVar(value="Все")
ttk.Radiobutton(root, text="Все", variable=filter_var, value="Все", command=filter_tasks).pack()
ttk.Radiobutton(root, text="Учёба", variable=filter_var, value="учёба", command=filter_tasks).pack()
ttk.Radiobutton(root, text="Спорт", variable=filter_var, value="спорт", command=filter_tasks).pack()
ttk.Radiobutton(root, text="Работа", variable=filter_var, value="работа", command=filter_tasks).pack()

columns = ("Задача", "Тип")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True)

update_history()

root.mainloop()