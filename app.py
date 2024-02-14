from  flask import Flask,render_template,request,redirect,flash,url_for,session
import sqlite3

app=Flask(__name__)
app.secret_key="123"

connection=sqlite3.connect('database.db')
cursor=connection.cursor()

cursor.execute("create table if not exists first(pid integer primary key,name text,password text)")
connection.close()
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login',methods=['GET','POST'])
def login():
     if request.method=="POST":
         
           name=request.form['username']
           password=request.form['password']
           with sqlite3.connect('database.db') as connection:
            connection.row_factory=sqlite3.Row

            cursor=connection.cursor()
            cursor.execute("select * from first where name=? and  password=?",(name,password))
            data=cursor.fetchone()

            if data:
                session["name"]=data["name"]
                session["password"]=data["password"]

                return redirect(url_for('index'))
            else:
                return redirect(url_for('signup'))




     return render_template("login.html")

@app.route('/signup',methods=['GET', 'POST'])
def signup():
     if request.method=="POST":
        
           name=request.form['username']
           password=request.form['password']
           
           with sqlite3.connect('database.db') as connection:
            cursor=connection.cursor()

            cursor.execute("insert into first(name,password)values(?,?)",(name,password))
            connection.commit()
            print("Data recived")
            return redirect(url_for('login'))
           
        
     else:
        print("data not recived")
    
    
     return render_template("signup.html")
if __name__=="__main__":
    app.run(debug=True)