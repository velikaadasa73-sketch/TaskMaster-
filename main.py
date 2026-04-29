import json
import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
import os

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Предопределённые задачи по категориям
        self.tasks_db = {
            "Учёба": [
                "Прочитать главу учебника по Python",
                "Решить 10 задач по математике",
                "Написать эссе по истории",
                "Подготовиться к экзамену",
                "Сделать домашнее задание",
                "Изучить новую тему по программированию",
                "Повторить пройденный материал"
            ],
            "Спорт": [
                "Сделать 50 отжиманий",
                "Пробежать 3 км",
                "Пойти в спортзал",
                "Сделать утреннюю зарядку",
                "Позаниматься йогой 20 минут",
                "Покататься на велосипеде",
                "Сыграть в футбол с друзьями"
            ],
            "Работа": [
                "Завершить отчёт до обеда",
                "Провести встречу с командой",
                "Написать письмо клиенту",
                "Разобрать почту",
                "Составить план на неделю",
                "Позвонить партнёрам",
                "Закончить проект до дедлайна"
            ]
        }
        
        self.history = []
        self.filename = "task_history.json"
        self.load_history()
        
        self.create_widgets()
        self.update_history_display()
    
    def create_widgets(self):
        # Верхняя панель с генерацией
        control_frame = ttk.LabelFrame(self.root, text="Генерация задачи", padding=15)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # Предпросмотр категорий
        categories_frame = ttk.Frame(control_frame)
        categories_frame.pack(fill="x", pady=5)
        
        ttk.Label(categories_frame, text="Доступные категории:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        categories_text = "📚 Учёба: {} задач | ⚽ Спорт: {} задач | 💼 Работа: {} задач".format(
            len(self.tasks_db["Учёба"]),
            len(self.tasks_db["Спорт"]),
            len(self.tasks_db["Работа"])
        )
        ttk.Label(categories_frame, text=categories_text).pack(anchor="w", pady=5)
        
        # Кнопка генерации
        self.generate_btn = tk.Button(
            control_frame, 
            text="🎲 СГЕНЕРИРОВАТЬ СЛУЧАЙНУЮ ЗАДАЧУ 🎲",
            command=self.generate_random_task,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.generate_btn.pack(pady=10)
        
        # Отображение текущей сгенерированной задачи
        self.current_task_frame = ttk.LabelFrame(self.root, text="Текущая задача", padding=10)
        self.current_task_frame.pack(fill="x", padx=10, pady=5)
        
        self.task_label = tk.Label(
            self.current_task_frame,
            text="Нажмите кнопку для генерации случайной задачи",
            font=("Arial", 11),
            wraplength=800,
            justify="center"
        )
        self.task_label.pack(pady=10)
        
        # Панель фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация истории", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        filter_row = ttk.Frame(filter_frame)
        filter_row.pack(fill="x")
        
        ttk.Label(filter_row, text="Фильтр по типу задачи:").pack(side="left", padx=5)
        self.filter_category = ttk.Combobox(
            filter_row, 
            values=["Все"] + list(self.tasks_db.keys()),
            state="readonly",
            width=15
        )
        self.filter_category.set("Все")
        self.filter_category.pack(side="left", padx=5)
        self.filter_category.bind("<<ComboboxSelected>>", lambda e: self.update_history_display())
        
        ttk.Button(filter_row, text="Применить фильтр", command=self.update_history_display).pack(side="left", padx=5)
        ttk.Button(filter_row, text="Сбросить фильтр", command=self.reset_filter).pack(side="left", padx=5)
        
        # История генераций
        history_frame = ttk.LabelFrame(self.root, text="История генераций", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Таблица для истории
        columns = ("ID", "Дата/Время", "Категория", "Задача")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            if col == "Задача":
                self.history_tree.column(col, width=400)
            elif col == "Дата/Время":
                self.history_tree.column(col, width=150)
            else:
                self.history_tree.column(col, width=80)
        
        self.history_tree.pack(fill="both", expand=True)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Нижняя панель с кнопками управления
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(bottom_frame, text="🗑️ Очистить историю", command=self.clear_history).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="💾 Сохранить историю", command=self.save_history).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="📂 Экспорт в JSON", command=self.export_to_json).pack(side="right", padx=5)
        
        # Статус-бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе. Всего сгенерировано задач: " + str(len(self.history)))
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x", padx=10, pady=2)
    
    def generate_random_task(self):
        """Генерация случайной задачи из предопределённого списка"""
        # Выбираем случайную категорию
        category = random.choice(list(self.tasks_db.keys()))
        # Выбираем случайную задачу из выбранной категории
        task = random.choice(self.tasks_db[category])
        
        # Сохраняем в историю
        task_entry = {
            "id": len(self.history) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "task": task
        }
        self.history.append(task_entry)
        
        # Отображаем текущую задачу
        self.task_label.config(
            text=f"📌 {task}\n\n🏷️ Категория: {category}",
            fg="#2E7D32",
            font=("Arial", 12, "bold")
        )
        
        # Обновляем отображение истории
        self.update_history_display()
        self.save_history()
        
        # Обновляем статус
        self.status_var.set(f"✅ Сгенерирована задача #{len(self.history)}: [{category}] {task}")
        
        # Эффект мигания кнопки
        self.flash_button()
    
    def flash_button(self):
        """Визуальный эффект при нажатии"""
        original_bg = self.generate_btn.cget("bg")
        self.generate_btn.config(bg="#FFC107")
        self.root.after(200, lambda: self.generate_btn.config(bg=original_bg))
    
    def update_history_display(self):
        """Обновление таблицы истории с учётом фильтра"""
        # Очищаем таблицу
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Фильтруем историю
        filter_cat = self.filter_category.get()
        filtered_history = self.history
        if filter_cat != "Все":
            filtered_history = [h for h in self.history if h["category"] == filter_cat]
        
        # Заполняем таблицу
        for entry in filtered_history:
            self.history_tree.insert("", "end", values=(
                entry["id"],
                entry["timestamp"],
                entry["category"],
                entry["task"]
            ))
        
        # Обновляем статус с информацией о фильтрации
        if filter_cat != "Все":
            self.status_var.set(f"🔍 Отфильтровано: {len(filtered_history)} из {len(self.history)} задач (категория: {filter_cat})")
        else:
            self.status_var.set(f"📋 Всего сгенерировано задач: {len(self.history)}")
    
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_category.set("Все")
        self.update_history_display()
    
    def clear_history(self):
        """Очистка истории с подтверждением"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.update_history_display()
            self.save_history()
            self.task_label.config(
                text="История очищена. Нажмите кнопку для генерации новой задачи",
                fg="black",
                font=("Arial", 11)
            )
            self.status_var.set("🗑️ История успешно очищена")
    
    def save_history(self):
        """Сохранение истории в JSON"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)
    
    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    # Валидация загруженных данных
                    if isinstance(loaded, list):
                        self.history = loaded
                    else:
                        self.history = []
            except (json.JSONDecodeError, IOError):
                self.history = []
        else:
            self.history = []
    
    def export_to_json(self):
        """Экспорт текущей истории в отдельный файл"""
        export_name = f"task_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(export_name, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", f"История экспортирована в файл: {export_name}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
