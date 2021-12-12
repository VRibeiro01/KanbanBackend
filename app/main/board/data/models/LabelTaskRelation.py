class LabelTaskRelation:
    label_id = 0
    task_id = 0

    def __init__(self, label_id, task_id):
        self.label_id = label_id
        self.task_id = task_id

    def __repr__(self):
        return str({"label_id": self.label_id, "task_id": self.task_id}).replace("'", "\"")

