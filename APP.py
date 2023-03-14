from flask import *
import mysql.connector


# mydb = mysql.connector.connect(
#     host="localhost",
#     user="bishalde",
#     password="bishalde",
#     database="flask_todo"
# )

# Online Database

mydb = mysql.connector.connect(
    host="db4free.net",
    user="bishalde",
    password="8299260163",
    database="clustix"
)

"""---------------------------------Table creation Code-----------------------------------"""
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
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE NOT NULL
);
""")

app = Flask(__name__)
app.secret_key = 'bishalde5741'



"""--------------------------ENDPOINT for homepage------------------------"""
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

            #insert data into table
            sql="""
                INSERT INTO `todo_data` (`deadline`,`user_id` ,`deadlinetime`, `priority`, `description`,`filename`) 
                VALUES ('{}','{}' ,'{}', '{}', '{}','{}')
            ;""".format(date,user,time,priority,description,f.filename)

            mycursor.execute(sql)
            mydb.commit()


        #show all the data form the table
        sql="""
            SELECT * FROM todo_data WHERE user_id='{}' ORDER BY deadline,deadlinetime DESC,priority ASC;
        ;""".format(user)
        mycursor.execute(sql)
        a=mycursor.fetchall()

        #return the data to the webpage
        data={'todo':a}
        return render_template('index.html',data=data)
    else:
        return redirect(url_for("login"))


"""--------------------------ENDPOINT for login------------------------"""
@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]


        #Search fo the username
        sql="SELECT * FROM todo_users WHERE username ='{}' && password='{}';".format(username,password)
        mycursor.execute(sql)
        data=mycursor.fetchall()
        if len(data)>0:
            session['username'] = username
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html',error="Credentials not found..!")
    return render_template('login.html',error=None)


"""--------------------------ENDPOINT for delete a todo item------------------------"""
@app.route("/delete/<int:idd>",methods=["GET","POST"])
def delete(idd):
    sql="DELETE FROM todo_data WHERE id ='{}';".format(idd)
    mycursor.execute(sql)
    return redirect(url_for('homepage'))


"""--------------------------ENDPOINT for SIGNUP---------------------------------"""
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]

        #check if username/email already exists
        sql="SELECT * FROM todo_users WHERE username ='{}' || email='{}';".format(username,email)
        mycursor.execute(sql)
        data=mycursor.fetchall()
        if len(data)>0:
            error="Username or Email already In USE...!"
            return render_template('signup.html',error=error)
        
        #to add new user
        try:
            sql="INSERT INTO todo_users VALUES('{}','{}','{}');".format(username,password,email)
            print(username,password)
            mycursor.execute(sql)
            mydb.commit()
        except Exception as e:
            error=e
            return render_template('signup.html',error=error)
            
        error="Account Created Successfully..!"
        return render_template('signup.html',error=error)

    error=None
    return render_template('signup.html',error=error)



"""--------------------------ENDPOINT for LOGOUT------------------------"""
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



"""--------------------------ENDPOINT for RESETPASSWORD--------------------------"""
@app.route('/resetPassword',methods=['POST','GET'])
def resetPassword():
    if request.method == 'POST':
        error="Reset Link Sent To Yout mailID"
        return render_template('resetpassword.html',error=error)
    return render_template('resetpassword.html',error=None)
    
"""--------------------------ENDPOINT for EDIT todo"""
@app.route('/edit/<int:id>',methods=['POST','GET'])
def editTodo(id):
    data={}
    return render_template('edittodo.html',data=data)


app.run()