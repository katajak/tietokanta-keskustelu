from db import db

def get_arealist():
    sql = "SELECT id, title FROM areas ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_name(id):
    sql = "SELECT title FROM areas WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]
