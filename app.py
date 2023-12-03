# note: The password will be your email address that you are going register

from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3

app = Flask(__name__)
app.secret_key="123"

todos = [{"task": "Sample Todo", "done": False}]

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS Users(name text,address text,contact integer,mail text)"""
connection.close()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from Users where name=? and mail=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            return redirect("todo")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("index"))


@app.route('/todo')
def index1():
    return render_template("todo.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    todo=request.form['todo']
    todos.append({"task": todo, "done": False})
    return redirect(url_for("index1"))

@app.route("/edit/<int:index1>", methods=("GET", "POST"))
def edit(index1):
    todo=todos[index1]
    if request.method == "POST":
        todo['task'] = request.form["todo"]
        return redirect(url_for("index1"))
    else:
        return render_template("edit.html", todo=todo, index1=index1)
    
@app.route("/check/<int:index1>")
def check(index1):
    todos[index1]['done'] = not todos[index1]['done']
    return redirect(url_for("index1"))

@app.route("/delete/<int:index1>")
def delete(index1):
    del todos[index1]
    return redirect(url_for("index1"))


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into Users(name,address,contact,mail)values(?,?,?,?)",(name,address,contact,mail))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("index"))
            con.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)