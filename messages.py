from db import db
import users

def get_messages(area_id, thread_id):
    sql = """SELECT M.content, U.username, M.sent_at, M.id FROM messages M, users U
             WHERE M.user_id=U.id AND area_id=:area_id AND thread_id=:thread_id AND M.visible=True
             ORDER BY M.id"""
    result = db.session.execute(sql, {"area_id":area_id, "thread_id":thread_id})
    return result.fetchall()

def get_one(area_id, thread_id, message_id):
    sql = """SELECT M.content, U.username, M.sent_at, M.id FROM messages M, users U
             WHERE M.user_id=U.id AND area_id=:area_id AND thread_id=:thread_id AND
             M.id=:message_id AND M.visible=True"""
    result = db.session.execute(sql, {"area_id":area_id, "thread_id":thread_id, "message_id":message_id})
    return result.fetchone()

def send(content, area_id, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    timezone = "SET TIMEZONE='Europe/Helsinki'"
    sql = """INSERT INTO messages (content, user_id, area_id, thread_id, sent_at, visible)
             VALUES (:content, :user_id, :area_id, :thread_id, NOW(), :visible)"""
    db.session.execute(timezone)
    db.session.execute(sql, {"content":content, "user_id":user_id,
                             "area_id":area_id, "thread_id":thread_id, "visible":True})
    db.session.commit()
    return True

def edit(message_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT user_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":message_id})
    m_user_id = result.fetchone()[0]
    if user_id == m_user_id:
        sql = "UPDATE messages SET content=:content WHERE id=:id"
        db.session.execute(sql, {"id":message_id, "content":content})
        db.session.commit()
        return True
    return False

def get_average_message_length():
    sql = "SELECT COALESCE(AVG(LENGTH(content)),0) FROM messages WHERE visible=True"
    result = db.session.execute(sql)
    return result.fetchone()

def get_user_with_most_messages():
    sql = """SELECT users.username, COUNT(*) FROM messages, users
             WHERE messages.user_id=users.id AND visible=True
             GROUP BY users.id ORDER BY COUNT(*) DESC LIMIT 1"""
    result = db.session.execute(sql)
    return result.fetchone()

def get_most_liked():
    sql = """SELECT messages.content, COUNT(*) FROM messages, likes
             WHERE likes.message_id=messages.id AND visible=True
             GROUP BY messages.id ORDER BY COUNT(*) DESC LIMIT 1"""
    result = db.session.execute(sql)
    return result.fetchone()
