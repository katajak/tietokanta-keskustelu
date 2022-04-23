from db import db
import users

def get_messages():
	sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
	result = db.session.execute(sql)
	return result.fetchall()

def send(content):
	user_id = users.user_id()
	if user_id == 0:
		return False
	timezone = "SET TIMEZONE='Europe/Helsinki'"
	sql = "INSERT INTO messages (content, user_id, sent_at, visible) VALUES (:content, :user_id, NOW(), :visible)"
	db.session.execute(timezone)
	db.session.execute(sql, {"content":content, "user_id":user_id, "visible":True})
	db.session.commit()
	return True
