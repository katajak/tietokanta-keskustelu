from db import db
import users

def get_threads(area_id):
	sql = "SELECT id, area_id, title, user_id, sent_at FROM threads WHERE area_id=:area_id ORDER BY id"
	result = db.session.execute(sql, {"area_id":area_id})
	return result.fetchall()

def get_name(id):
    sql = "SELECT title FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def send(title, area_id):
	user_id = users.user_id()
	if user_id == 0:
		return False
	timezone = "SET TIMEZONE='Europe/Helsinki'"
	sql = "INSERT INTO threads (title, user_id, area_id, sent_at, visible) VALUES (:title, :user_id, :area_id, NOW(), :visible)"
	db.session.execute(timezone)
	db.session.execute(sql, {"title":title, "user_id":user_id, "area_id":area_id, "visible":True})
	db.session.commit()
	return True
