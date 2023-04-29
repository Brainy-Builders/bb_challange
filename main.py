from flask import *
import sqlite3

def get_conn():
    conn=sqlite3.connect("db.db")
    cursor=conn.cursor()
    return conn,cursor
conn,cur = get_conn()

cur.execute("CREATE TABLE IF NOT EXISTS `Records` (`Persons` TEXT NOT NULL,`Height` DECIMAL,`Snowballs` INT);")
conn.commit()
conn.close()
app = Flask(__name__)


def get_all():
    conn,cur=get_conn()
    cur.execute("SELECT * FROM Records")
    rows = cur.fetchall()
    fetches = []
    for i in rows:
        fetches.append(i)
    fetches.sort(key = lambda x: x[1] * x[2],reverse=True)
    fetches = [[i[0],i[1],i[2],i[1]*i[2]] for i in fetches]
    return fetches
def add_result(names,height,count):
    conn,cur=get_conn()
    cur.execute("INSERT INTO Records (Persons,Height,Snowballs) VALUES ('{}','{}','{}');".format(names,height,count))
    conn.commit()
@app.route("/")
def index():
    return render_template("index.html",scores=get_all())
@app.route("/input",methods=["GET","POST"])
def new():
    if request.method == "POST":
        form=request.form
        add_result(form["person"],form["height"],form["count"])
        return redirect("/")
    return render_template("load.html")
app.jinja_env.globals.update(int=int)
if __name__  == "__main__":
    app.run("0.0.0.0",8080,debug=True)