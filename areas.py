from db import db
import users

def get_arealist():
    sql = "SELECT id, title FROM areas ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_name(id):
    sql = "SELECT title FROM areas WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def send(title):
	user_id = users.user_id()
	if user_id == 0:
		return False
	timezone = "SET TIMEZONE='Europe/Helsinki'"
	sql = "INSERT INTO areas (title, visible) VALUES (:title, :visible)"
	db.session.execute(timezone)
	db.session.execute(sql, {"title":title, "visible":True})
	db.session.commit()
	return True
