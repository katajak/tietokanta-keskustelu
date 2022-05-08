from db import db
from flask import session
import werkzeug.security
import secrets

def login(username, password):
    sql = "SELECT password, id, admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user is None:
        return False
    else:
        if werkzeug.security.check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["admin"] = user[2]
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["admin"]
    del session["csrf_token"]

def register(username, password):
    hash_value = werkzeug.security.generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)"
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":False})
        db.session.commit()
    except:
        print("Virhe")
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def admin():
    return session.get("admin")

def get_number():
    sql = "SELECT COUNT(id) FROM users"
    result = db.session.execute(sql)
    return result.fetchone()[0]
