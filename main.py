import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster - Менеджер задач")
        self.root.geometry("800x500")
        
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()
        
        self.create_widgets()
        self.update_task_list()
    
    def create_widgets(self):
        # Рамка ввода
        input_frame = ttk.LabelFrame(self.root, text="Новая задача", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Название:*").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Описание:").grid(row=1, column=0, sticky="w")
        self.desc_entry = ttk.Entry(input_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(input_frame, text="Приоритет:*").grid(row=2, column=0, sticky="w")
        self.priority_var = tk.StringVar(value="Средний")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, 
                                      values=["Высокий", "Средний", "Низкий"], state="readonly", width=27)
        priority_combo.grid(row=2, column=1, padx=5)
        
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):*").grid(row=3, column=0, sticky="w")
        self.date_entry = ttk.Entry(input_frame, width=30)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=3, column=1, padx=5)
        
        ttk.Button(input_frame, text="Добавить задачу", command=self.add_task).grid(row=4, column=1, pady=5)
        
        # Рамка фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по приоритету:").pack(side="left", padx=5)
        self.filter_priority = ttk.Combobox(filter_frame, values=["Все", "Высокий", "Средний", "Низкий"], 
                                            state="readonly", width=15)
        self.filter_priority.set("Все")
        self.filter_priority.pack(side="left", padx=5)
        
        ttk.Button(filter_frame, text="Применить фильтр", command=self.update_task_list).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter).pack(side="left", padx=5)
        
        # Список задач
        columns = ("ID", "Название", "Приоритет", "Дата", "Статус")
        self.task_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=100)
        self.task_tree.column("Название", width=200)
        
        self.task_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.task_tree.yview)
        scrollbar.pack(side="right", fill="y", pady=5)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="Отметить выполнено", command=self.mark_done).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Удалить задачу", command=self.delete_task).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Сохранить", command=self.save_tasks).pack(side="right", padx=5)
    
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        priority = self.priority_var.get()
        date = self.date_entry.get().strip()
        
        if not title:
            messagebox.showerror("Ошибка", "Название задачи обязательно!")
            return
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return
        
        task_id = max([t["id"] for t in self.tasks], default=0) + 1
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "date": date,
            "status": "Активна"
        }
        self.tasks.append(task)
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.update_task_list()
        self.save_tasks()
        messagebox.showinfo("Успех", f"Задача '{title}' добавлена!")
    
    def update_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        filter_priority = self.filter_priority.get()
        
        filtered_tasks = self.tasks
        if filter_priority != "Все":
            filtered_tasks = [t for t in self.tasks if t["priority"] == filter_priority]
        
        for task in filtered_tasks:
            self.task_tree.insert("", "end", values=(
                task["id"], task["title"], task["priority"], 
                task["date"], task["status"]
            ))
    
    def mark_done(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите задачу!")
            return
        
        task_id = int(self.task_tree.item(selected[0])["values"][0])
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "Выполнена"
                break
        self.update_task_list()
        self.save_tasks()
        messagebox.showinfo("Успех", "Задача отмечена как выполненная!")
    
    def delete_task(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите задачу!")
            return
        
        task_id = int(self.task_tree.item(selected[0])["values"][0])
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.update_task_list()
        self.save_tasks()
        messagebox.showinfo("Успех", "Задача удалена!")
    
    def reset_filter(self):
        self.filter_priority.set("Все")
        self.update_task_list()
    
    def save_tasks(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)
    
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
