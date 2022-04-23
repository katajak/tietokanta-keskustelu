from db import db

def get_threads(area_id):
	sql = "SELECT id, area_id, title FROM threads WHERE area_id=:area_id ORDER BY id"
	result = db.session.execute(sql, {"area_id":area_id})
	return result.fetchall()

def get_name(id):
    sql = "SELECT title FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]
