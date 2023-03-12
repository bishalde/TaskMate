from flask import *
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="bishalde",
    password="bishalde",
    database="flask_todo"
)

#Online Database

# mydb = mysql.connector.connect(
#     host="db4free.net",
#     user="bishalde",
#     password="8299260163",
#     database="clustix"
# )

mycursor = mydb.cursor()
mycursor.execute("""
                CREATE TABLE IF NOT EXISTS todo_data(
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    user_id varchar(255) ,
                    deadline DATE NOT NULL,
                    deadlinetime VARCHAR(10) NOT NULL,
                    priority int(10) NOT NULL DEFAULT 5,
                    description VARCHAR(255) NOT NULL,
                    filename varchar(255)
                )                
;""")
mycursor.execute("""CREATE TABLE IF NOT EXISTS todo_users(
                    username VARCHAR(255) NOT NULL PRIMARY KEY,
                    password VARCHAR(255) NOT NULL
);
""")

app = Flask(__name__)
app.secret_key = 'bishalde5741'


@app.route('/homepage',methods=['POST','GET'])
def homepage():
    if 'username' in session:

        user=session['username']
        if(request.method == "POST"):
            user=session['username']
            date=request.form.get('date')
            time=request.form.get('time')
            priority=request.form.get('priority')
            description=request.form.get('description')
            f = request.files['file']

            sql="""
                INSERT INTO `todo_data` (`deadline`,`user_id` ,`deadlinetime`, `priority`, `description`,`filename`) 
                VALUES ('{}','{}' ,'{}', '{}', '{}','{}')
            ;""".format(date,user,time,priority,description,f.filename)

            mycursor.execute(sql)
            mydb.commit()

        sql="""
            SELECT * FROM todo_data WHERE user_id='{}' ORDER BY deadline,deadlinetime DESC,priority ASC;
        ;""".format(user)
        mycursor.execute(sql)
        a=mycursor.fetchall()
        data={'todo':a}
        return render_template('index.html',data=data)
    else:
        return redirect(url_for("login"))

@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]

        sql="SELECT * FROM todo_users WHERE username ='{}' && password='{}';".format(username,password)
        mycursor.execute(sql)
        data=mycursor.fetchall()
        if len(data)>0:
            session['username'] = username
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html',error="Credentials not found..!")
    return render_template('login.html',error=None)

@app.route("/delete/<int:idd>",methods=["GET","POST"])
def delete(idd):
    sql="DELETE FROM todo_data WHERE id ='{}';".format(idd)
    mycursor.execute(sql)
    return redirect(url_for('homepage'))

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        sql="SELECT * FROM todo_users WHERE username ='{}';".format(username)
        mycursor.execute(sql)
        data=mycursor.fetchall()
        if len(data)>0:
            error="Username already In USE...!"
            return render_template('signup.html',error=error)
        
        sql="INSERT INTO todo_users VALUES('{}','{}');".format(username,password)
        print(username,password)
        mycursor.execute(sql)
        mydb.commit()
        error="CREATED"
        return render_template('signup.html',error=error)

    error=None
    return render_template('signup.html',error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
app.run(debug=True,host='0.0.0.0')
