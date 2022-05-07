from db import db
import users

def get_messages(area_id, thread_id):
    sql = "SELECT M.content, U.username, M.sent_at, M.id FROM messages M, users U WHERE M.user_id=U.id AND area_id=:area_id AND thread_id=:thread_id AND M.visible=True ORDER BY M.id"
    result = db.session.execute(sql, {"area_id":area_id, "thread_id":thread_id})
    return result.fetchall()

def send(content, area_id, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    timezone = "SET TIMEZONE='Europe/Helsinki'"
    sql = "INSERT INTO messages (content, user_id, area_id, thread_id, sent_at, visible) VALUES (:content, :user_id, :area_id, :thread_id, NOW(), :visible)"
    db.session.execute(timezone)
    db.session.execute(sql, {"content":content, "user_id":user_id, "area_id":area_id, "thread_id":thread_id, "visible":True})
    db.session.commit()
    return True

def edit(id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT user_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    m_user_id = result.fetchone()[0]
    if user_id == m_user_id:
        sql = "UPDATE messages SET content=:content WHERE id=:id"
        db.session.execute(sql, {"id":id, "content":content})
        db.session.commit()
        return True
    return False
