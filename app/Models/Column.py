class Column:
    column_id = 0
    board_id = 0
    title = ""
    position = 0

    def __init__(self, column_id, board_id, title, position):
        self.column_id = column_id
        self.board_id = board_id
        self.title = title
        self.position = position

    def to_json(self):
        return {"column_id": self.column_id, "board_id": self.board_id,  "title": self.title,  "position": self.position}

