from app import app
from flask import render_template
from flask import request
from flask import redirect
import users
import messages

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/thread")
def thread():
    return render_template("thread.html")

@app.route("/message")
def message():
    messagelist = messages.get_messages()
    return render_template("message.html", messages = messagelist, count = len(messagelist))

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods = ["post"])
def send():
    content = request.form["content"]
    if len(content) < 1:
        return render_template("error.html", message = "Et voi lähettää tyhjää viestiä")
    if len(content) > 4000:
        return render_template("error.html", message = "Viesti on liian pitkä (Max. 4000 merkkiä)")
    if messages.send(content) is True:
        return redirect("/")
    else:
        return render_template("error.html", message = "Et ole kirjautunut sisään")

@app.route("/login", methods = ["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password) is True:
            return redirect("/")
        else:
            return render_template("error.html", message = "Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods = ["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) < 3 or len(password) < 3:
            return render_template("error.html", message = "Käyttäjänimi tai salasana liian lyhyt")
        if users.register(username, password) is True:
            return redirect("/")
        else:
            return render_template("error.html", message = "Käyttäjänimi on jo olemassa")
