from flask import Flask,render_template,request,flash,redirect,url_for,session
import sqlite3

app = Flask(__name__)
app.secret_key = "123"

conn = sqlite3.connect("database.db")
conn.execute("""CREATE TABLE IF NOT EXISTS customer(
                pid INTEGER PRIMARY KEY,
                firstname TEXT NOT NULL,
                lastname TEXT,
                address TEXT NOT NULL,
                emailid TEXT NOT NULL,
                password TEXT NOT NULL,
                confirmpassword TEXT NOT NULL
                )""")
conn.commit()
conn.close()

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        emailid = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer WHERE emailid=? AND password=?",(emailid,password))
        data=cursor.fetchone()
        
        if data:
            session["email-id"] = data["emailid"]
            session["pass-word"] = data["password"]
            return redirect(url_for("customer"))
        else:
            flash("email and password are mismatched","danger")
    
    return render_template("login.html")


@app.route('/customer',methods=['GET','POST'])
def customer():
    return render_template("customer.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            fname = request.form['fname']
            lname = request.form['lname']
            address = request.form['address']
            emailid = request.form['email']
            password = request.form['password']
            cpassword = request.form['cpassword']
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customer(firstname,lastname,address,emailid,password,confirmpassword)values(?,?,?,?,?,?)",(fname,lname,address,emailid,password,cpassword))
            conn.commit()
            flash("Record added successfully","success")
            
        except Exception as e:
            flash("Error in insert operation",+str(e),"danger")
        finally:
            conn.close()
            return redirect(url_for("index"))
            
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
    