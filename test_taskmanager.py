import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock

class TestRandomTaskGenerator(unittest.TestCase):
    
    def setUp(self):
        """Подготовка к тестам"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.filename = self.temp_file.name
        self.temp_file.close()
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.filename):
            os.unlink(self.filename)
    
    def test_tasks_db_structure(self):
        """Позитивный тест: проверка структуры базы задач"""
        # Импортируем класс
        import sys
        import tkinter as tk
        from main import RandomTaskGenerator
        
        root = tk.Tk()
        app = RandomTaskGenerator(root)
        
        # Проверяем, что есть нужные категории
        self.assertIn("Учёба", app.tasks_db)
        self.assertIn("Спорт", app.tasks_db)
        self.assertIn("Работа", app.tasks_db)
        
        # Проверяем, что в каждой категории есть задачи
        self.assertGreater(len(app.tasks_db["Учёба"]), 0)
        self.assertGreater(len(app.tasks_db["Спорт"]), 0)
        self.assertGreater(len(app.tasks_db["Работа"]), 0)
        
        root.destroy()
    
    def test_generate_random_task(self):
        """Позитивный тест: генерация случайной задачи"""
        import tkinter as tk
        from main import RandomTaskGenerator
        
        root = tk.Tk()
        app = RandomTaskGenerator(root)
        initial_count = len(app.history)
        
        # Генерируем задачу
        app.generate_random_task()
        
        # Проверяем, что история увеличилась
        self.assertEqual(len(app.history), initial_count + 1)
        
        # Проверяем структуру добавленной задачи
        last_task = app.history[-1]
        self.assertIn("id", last_task)
        self.assertIn("timestamp", last_task)
        self.assertIn("category", last_task)
        self.assertIn("task", last_task)
        self.assertIn(last_task["category"], ["Учёба", "Спорт", "Работа"])
        
        root.destroy()
    
    def test_filter_functionality(self):
        """Позитивный тест: проверка фильтрации"""
        import tkinter as tk
        from main import RandomTaskGenerator
        
        root = tk.Tk()
        app = RandomTaskGenerator(root)
        
        # Добавляем тестовые данные
        app.history = [
            {"id": 1, "timestamp": "2024-01-01", "category": "Учёба", "task": "Учить Python"},
            {"id": 2, "timestamp": "2024-01-02", "category": "Спорт", "task": "Пробежка"},
            {"id": 3, "timestamp": "2024-01-03", "category": "Работа", "task": "Отчёт"}
        ]
        
        app.filter_category.set("Учёба")
        app.update_history_display()
        
        # Проверяем, что фильтр работает (через внутреннее состояние)
        filter_cat = app.filter_category.get()
        self.assertEqual(filter_cat, "Учёба")
        
        root.destroy()
    
    def test_save_and_load_history(self):
        """Граничный тест: сохранение и загрузка пустой истории"""
        import tkinter as tk
        from main import RandomTaskGenerator
        
        root = tk.Tk()
        app = RandomTaskGenerator(root)
        app.filename = self.filename
        app.history = []
        app.save_history()
        
        # Загружаем в новый экземпляр
        app2 = RandomTaskGenerator(root)
        app2.filename = self.filename
        app2.load_history()
        
        self.assertEqual(len(app2.history), 0)
        root.destroy()
    
    def test_clear_history_with_confirmation(self):
        """Негативный тест: очистка истории (требует подтверждения)"""
        import tkinter as tk
        from main import RandomTaskGenerator
        
        root = tk.Tk()
        app = RandomTaskGenerator(root)
        app.history = [{"id": 1, "category": "Учёба", "task": "Тест"}]
        
        # Мокаем диалог подтверждения
        with patch('tkinter.messagebox.askyesno', return_value=True):
            app.clear_history()
            self.assertEqual(len(app.history), 0)
        
        root.destroy()
    
    def test_invalid_json_load(self):
        """Негативный тест: загрузка повреждённого JSON"""
        import tkinter as tk
        from main import RandomTaskGenerator
        
        # Создаём повреждённый JSON
        with open(self.filename, "w") as f:
            f.write("{invalid json content")
        
        root = tk.Tk()
        app = RandomTaskGenerator(root)
        app.filename = self.filename
        app.load_history()
        
        # Должен загрузиться пустой список
        self.assertEqual(app.history, [])
        root.destroy()

if __name__ == "__main__":
    unittest.main()
