class Board:
    board_id = 0
    owner_id = 0
    title = ""

    def __init__(self, board_id, owner_id, title):
        self.board_id = board_id
        self.owner_id = owner_id
        self.title = title

    def to_json(self):
        return {"board_id": self.board_id, "owner_id": self.owner_id,  "title": self.title}



