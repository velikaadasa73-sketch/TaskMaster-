import unittest
import json
import os
import tempfile
from datetime import datetime

class TestTaskManager(unittest.TestCase):
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.filename = self.temp_file.name
        self.temp_file.close()
    
    def tearDown(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.filename):
            os.unlink(self.filename)
    
    def test_validate_date_valid(self):
        """Позитивный тест: корректная дата"""
        from main import TaskManager
        import tkinter as tk
        
        root = tk.Tk()
        app = TaskManager(root)
        self.assertTrue(app.validate_date("2024-12-31"))
        root.destroy()
    
    def test_validate_date_invalid(self):
        """Негативный тест: некорректная дата"""
        from main import TaskManager
        import tkinter as tk
        
        root = tk.Tk()
        app = TaskManager(root)
        self.assertFalse(app.validate_date("31-12-2024"))
        self.assertFalse(app.validate_date("2024-13-45"))
        self.assertFalse(app.validate_date("not a date"))
        root.destroy()
    
    def test_save_and_load_tasks(self):
        """Граничный тест: сохранение и загрузка пустого списка"""
        from main import TaskManager
        import tkinter as tk
        
        root = tk.Tk()
        app = TaskManager(root)
        app.filename = self.filename
        app.tasks = []
        app.save_tasks()
        
        # Загружаем в новый экземпляр
        app2 = TaskManager(root)
        app2.filename = self.filename
        app2.load_tasks()
        self.assertEqual(len(app2.tasks), 0)
        root.destroy()
    
    def test_add_task_validation(self):
        """Негативный тест: добавление задачи без названия"""
        from main import TaskManager
        import tkinter as tk
        
        root = tk.Tk()
        app = TaskManager(root)
        initial_count = len(app.tasks)
        
        # Пытаемся добавить без названия
        app.title_entry.delete(0, tk.END)
        app.title_entry.insert(0, "")
        app.date_entry.delete(0, tk.END)
        app.date_entry.insert(0, "2025-01-01")
        app.add_task()
        
        self.assertEqual(len(app.tasks), initial_count)
        root.destroy()

if __name__ == "__main__":
    unittest.main()
