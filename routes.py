from app import app
from flask import render_template
from flask import request
from flask import redirect
import users
import messages
import threads
import areas

@app.route("/")
def index():
    arealist = areas.get_arealist()
    return render_template("index.html", arealist = arealist)

@app.route("/<int:area_id>")
def thread(area_id):
    area_name = areas.get_name(area_id)
    threadlist = threads.get_threads(area_id)
    return render_template("thread.html", area_name = area_name, threadlist = threadlist)

@app.route("/<int:area_id>/<int:thread_id>", methods = ["GET","POST"])
def message(area_id, thread_id):
    if request.method == "GET":
        thread_name = threads.get_name(thread_id)
        messagelist = messages.get_messages(area_id, thread_id)
        return render_template("message.html", messages = messagelist, count = len(messagelist), thread_name = thread_name)

    if request.method == "POST":
        content = request.form["content"]
        if len(content) < 1:
            return render_template("error.html", message = "Et voi lähettää tyhjää viestiä")
        if len(content) > 4000:
            return render_template("error.html", message = "Viesti on liian pitkä (Max. 4000 merkkiä)")
        if messages.send(content, area_id, thread_id) is True:
            return redirect(request.url)
        else:
            return render_template("error.html", message = "Et ole kirjautunut sisään")

@app.route("/login", methods = ["GET","POST"])
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

@app.route("/register", methods = ["GET","POST"])
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
