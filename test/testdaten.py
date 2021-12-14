import datetime

from app.main.board.data.db.database_board import DatabaseBoard
from app.main.board.data.db.database_column import DatabaseColumn
from app.main.board.data.db.database_label import DatabaseLabel
from app.main.board.data.db.database_label_task_relation import DatabaseLabelTaskRelation
from app.main.board.data.db.database_task import DatabaseTask
from app.main.user.data.db.database_user import DatabaseUser


def run():
    #Path für den DatenBank zulegen
    DatabaseUser.path = './dbs/database'
    DatabaseBoard.path = './dbs/database'
    DatabaseColumn.path = './dbs/database'
    DatabaseTask.path = './dbs/database'
    DatabaseLabel.path = './dbs/database'
    DatabaseLabelTaskRelation.path = './dbs/database'

    #Datenbank reinigen
    DatabaseUser.drop_db()
    DatabaseBoard.drop_db()
    DatabaseColumn.drop_db()
    DatabaseTask.drop_db()
    DatabaseLabel.drop_db()
    DatabaseLabelTaskRelation.drop_db()

    #Tabelen erstellen
    DatabaseUser.create_db()
    DatabaseBoard.create_db()
    DatabaseColumn.create_db()
    DatabaseTask.create_db()
    DatabaseLabel.create_db()
    DatabaseLabelTaskRelation.create_db()

    #(USERNAME, PASSWORD)
    DatabaseUser.insert_user("Denise","111")
    DatabaseUser.insert_user("Vivi","222")
    DatabaseUser.insert_user("Ferdi","333")
    DatabaseUser.insert_user("Kjell","444")
    DatabaseUser.insert_user("Ahmad","555")


    #(USER_ID, TITLE)
    DatabaseBoard.insert_board(3,"Backend")
    DatabaseBoard.insert_board(1,"Frontend")


    #(BOARD_ID, TITLE, POSITION)
    DatabaseColumn.insert_column(1,"ToDo",0)
    DatabaseColumn.insert_column(1,"in-Progress",1)
    DatabaseColumn.insert_column(1,"Solved",2)
    DatabaseColumn.insert_column(1,"Test",2)

    DatabaseColumn.insert_column(2,"ToDo",0)
    DatabaseColumn.insert_column(2,"in-Progress",1)
    DatabaseColumn.insert_column(2,"Solved",2)


    #(BOARD_ID, TITLE)


    DatabaseLabel.insert_label(3, "TODO")
    DatabaseLabel.insert_label(3, "SOLVED")
    DatabaseLabel.insert_label(3, "BACKEND")


    #(COLUMN_ID, WORKER, TITLE, PRIO, POSITION, DEADLINE, LABELLIST)


    deadline = datetime.datetime.now().timestamp()

    DatabaseTask.insert_task(5,4,"Add pen Butten to change a Column",3,0, deadline, [1, 3])
    DatabaseTask.insert_task(5,1,"Create LogIn Butten",3,1, deadline, [1])
    DatabaseTask.insert_task(5,2,"Show board title",3,2, deadline, [2])
    DatabaseTask.insert_task(6,1,"CSS-Styling",1,0, deadline, [])
    DatabaseTask.insert_task(6,2,"Add bin Button to delete Column",2,1, deadline, [3])
    DatabaseTask.insert_task(6,4,"Add Drag and Drop functionality",2,2, deadline, [])
    DatabaseTask.insert_task(6,4,"Deployment Frontend",2,3, deadline, [])
    DatabaseTask.insert_task(7,1,"Wireframe",1,0, deadline, [])
    DatabaseTask.insert_task(7,4,"Create React Project",1,1, deadline, [])


    DatabaseTask.insert_task(1,5,"Bekomme alle Task bei Column_id",1,0, deadline, [])
    DatabaseTask.insert_task(1,3,"Lebel_erstellen",2,1, deadline, [])
    DatabaseTask.insert_task(1,3,"Lebel löschen",2,2, deadline, [])
    DatabaseTask.insert_task(1,5,"Lebel bearbeiten",2,3, deadline, [])
    DatabaseTask.insert_task(1,2,"Add column Deadline to Task",3,4, deadline, [])
    DatabaseTask.insert_task(2,3,"Test schreiben",1,0, deadline, [])
    DatabaseTask.insert_task(2,2,"Task user zuweisen",2,1, deadline, [])
    DatabaseTask.insert_task(2,3,"Deployment der Anwendung",2,2, deadline, [])
    DatabaseTask.insert_task(3,3,"Lebel_erstellen",1,0, deadline, [])
    DatabaseTask.insert_task(3,5,"TestDaten erstllen",3,1, deadline, [])
    DatabaseTask.insert_task(4,2,"get Task be Worker_id",1,0, deadline, [])
