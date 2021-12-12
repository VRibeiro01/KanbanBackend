class Label:
    label_id = 0
    board_id = 0
    title = ""

    def __init__(self, label_id, title, board_id):
        self.label_id = label_id
        self.board_id = board_id
        self.title = title

    def __repr__(self):
        return str({"label_id": self.label_id, "title": self.title}).replace("'", "\"")

