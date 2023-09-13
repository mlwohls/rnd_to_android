import sqlite3
import datetime

class Database:
    def __init__(self):
        self.con = sqlite3.connect('rnd.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.cursor = self.con.cursor()
        self.create_score_table()

    '''CREATE the Scores TABLE'''
    def create_score_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS scores(id integer PRIMARY KEY AUTOINCREMENT, created_at timestamp NOT NULL, drill varchar(50) NOT NULL, session_id varchar(50) NOT NULL, score INTEGER NOT NULL, other BLOB)")
    
    '''Add A Score'''
    def submit_score(self, drill, session_id, score, other=None):
        created_at = datetime.datetime.now()
        self.cursor.execute("INSERT INTO scores(created_at, drill, session_id, score, other) VALUES(?, ?, ?, ?, ?)", (created_at, drill, session_id, score, other))
        self.con.commit()

        last_id = self.cursor.lastrowid

        # Getting the last entered item to add in the list
        created_score= self.cursor.execute("SELECT id, created_at, drill, session_id, score, other FROM scores WHERE id = ?", (last_id,)).fetchall()

        
        return created_score[-1]
    
    '''READ / GET the scores'''
    
    def get_session_scores(self, drill, session_id, limit = 10):
        # Getting CURRENT session_id scores
        scores = self.cursor.execute("SELECT id, created_at, drill, session_id, score, other FROM scores WHERE drill = ? and session_id = ? ORDER BY created_at ASC LIMIT ?", (drill, session_id, limit)).fetchall()

        return scores

    def get_historical_scores(self, drill, session_id, limit = 5):
        # Getting scores that are NOT the current session_ID
        scores = self.cursor.execute(
            '''
            SELECT session_id, MAX(created_at) as "[timestamp]", COUNT(id), AVG(score) 
            FROM scores 
            WHERE drill = ? and session_id != ? 
            GROUP BY session_id
            ORDER BY MAX(created_at) DESC 
            LIMIT ?
            ''', (drill, session_id, limit)).fetchall()
        return scores

    '''Closing the connection '''
    def close_db_connection(self):
        self.con.close()