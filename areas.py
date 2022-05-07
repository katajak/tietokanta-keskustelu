from db import db
import users

def get_arealist():
    sql = "SELECT id, title FROM areas WHERE visible=True ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_name(area_id):
    sql = "SELECT title FROM areas WHERE id=:id AND visible=True"
    result = db.session.execute(sql, {"id":area_id})
    return result.fetchone()[0]

def send(title, admin_only):
    user_id = users.user_id()
    admin = users.admin()
    if user_id == 0:
        return False
    timezone = "SET TIMEZONE='Europe/Helsinki'"
    sql = "INSERT INTO areas (title, visible, admin_only) VALUES (:title, :visible, :admin_only)"
    db.session.execute(timezone)
    if admin_only is False:
        db.session.execute(sql, {"title":title, "visible":True, "admin_only":False})
    if admin_only is True:
        if admin is not True:
            return False
        db.session.execute(sql, {"title":title, "visible":True, "admin_only":True})
    db.session.commit()
    return True

def get_admin_only(area_id):
    sql = "SELECT admin_only FROM areas WHERE id=:id AND visible=True"
    result = db.session.execute(sql, {"id":area_id})
    return result.fetchone()[0]
