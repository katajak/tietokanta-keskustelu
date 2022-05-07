from app import app
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import users
import messages
import threads
import areas

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        arealist = areas.get_arealist()
        return render_template("index.html", arealist = arealist)
    if request.method == "POST":
        area_name = request.form["area_name"]
        if len(area_name) < 1:
            return render_template("error.html", message = "Et voi lähettää tyhjää alueen nimeä")
        if len(area_name) > 240:
            return render_template("error.html", message = "Alueen nimi on liian pitkä (Max. 240 merkkiä)")
        if areas.send(area_name) is True:
            return redirect(request.url)
        else:
            return render_template("error.html", message = "Virhe tapahtui")

@app.route("/<int:area_id>", methods = ["GET", "POST"])
def thread(area_id):
    if request.method == "GET":
        area_name = areas.get_name(area_id)
        threadlist = threads.get_threads(area_id)
        return render_template("thread.html", area_name = area_name, threadlist = threadlist)

    if request.method == "POST":
        thread_title = request.form["thread_title"]
        if len(thread_title) < 1:
            return render_template("error.html", message = "Et voi lähettää tyhjää aloitusta")
        if len(thread_title) > 240:
            return render_template("error.html", message = "Aloitus on liian pitkä (Max. 240 merkkiä)")
        if threads.send(thread_title, area_id) is True:
            return redirect(request.url)
        else:
            return render_template("error.html", message = "Virhe tapahtui")

@app.route("/<int:area_id>/<int:thread_id>", methods = ["GET", "POST"])
def message(area_id, thread_id):
    if request.method == "GET":
        thread_name = threads.get_name(thread_id)
        messagelist = messages.get_messages(area_id, thread_id)
        return render_template("message.html", messages = messagelist, count = len(messagelist), thread_name = thread_name, area_id=area_id, thread_id=thread_id)

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

@app.route("/<int:area_id>/<int:thread_id>/<int:message_id>", methods = ["GET", "POST"])
def edit_message(area_id, thread_id, message_id):
    if request.method == "GET":
        return render_template("editmessage.html")
    if request.method == "POST":
        edited = request.form["content"]
        if len(edited) < 1:
            return render_template("error.html", message = "Et voi lähettää tyhjää viestiä")
        if len(edited) > 4000:
            return render_template("error.html", message = "Viesti on liian pitkä (Max. 4000 merkkiä)")
        if messages.edit(message_id, edited) is True:
            return redirect(url_for('message', area_id=area_id, thread_id=thread_id))
        else:
            return render_template("error.html", message="Voit muokata vain omia viestejä")

@app.route("/login", methods = ["GET", "POST"])
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

@app.route("/register", methods = ["GET", "POST"])
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
