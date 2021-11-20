class Task:
    task_id = 0
    column_id = 0
    worker = 0
    title = ""
    position = 0
    prio = 0

    def __init__(self, task_id, column_id, worker, title, prio, position):
        self.task_id = task_id
        self.column_id = column_id
        self.worker = worker
        self.title = title
        self.prio = prio
        self.position = position

    def __repr__(self):
        return str({"task_id": self.task_id, "column_id": self.column_id, "worker": self.worker, "title": self.title, "prio": self.prio, "position": self.position}).replace("'", "\"")

