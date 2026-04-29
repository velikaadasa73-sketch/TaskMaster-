
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
