from db import db
import users

def like(message_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = """INSERT INTO likes (user_id, message_id, liked)
                 VALUES (:user_id, :message_id, :liked)"""
        db.session.execute(sql, {"user_id":user_id, "message_id":message_id, "liked":True})
        db.session.commit()
        return True
    except:
        return False

def get_likes(message_id):
    sql = "SELECT COUNT(id) FROM likes WHERE likes.message_id=:message_id AND liked=True"
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()
