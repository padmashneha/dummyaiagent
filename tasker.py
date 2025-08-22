class TaskAgent:
    def __init__(self, file_path="tasks.txt"):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        with open(self.file_path, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    def categorize(self):
        categories = {"work": [], "personal": [], "other": []}
        for task in self.tasks:
            if "- work" in task:
                categories["work"].append(task.replace("- work", "").strip())
            elif "- personal" in task:
                categories["personal"].append(task.replace("- personal", "").strip())
            else:
                categories["other"].append(task)
        return categories

    def suggest_next(self):
        # Naive priority: work > personal > other
        cats = self.categorize()
        if cats["work"]:
            return f"Next: {cats['work'][0]} (work)"
        elif cats["personal"]:
            return f"Next: {cats['personal'][0]} (personal)"
        elif cats["other"]:
            return f"Next: {cats['other'][0]} (other)"
        return "No tasks found!"

# Run
agent = TaskAgent()
print("Tasks organized:", agent.categorize())
print(agent.suggest_next())
