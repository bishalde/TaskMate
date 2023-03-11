from flask import *
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="bishalde",
    password="bishalde",
    database="flask_todo"
)

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

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def homepage():
    if(request.method == "POST"):
        date=request.form.get('date')
        time=request.form.get('time')
        priority=request.form.get('priority')
        description=request.form.get('description')
        file=request.form.get('file')

        sql="""
            INSERT INTO `todo_data` (`deadline`, `deadlinetime`, `priority`, `description`,`filename`) 
            VALUES ('{}', '{}', '{}', '{}','{}')
        ;""".format(date,time,priority,description,file)
        mycursor.execute(sql)
        mydb.commit()

    sql="""
        SELECT * FROM todo_data ORDER BY deadline,deadlinetime,priority DESC;
    ;"""
    mycursor.execute(sql)
    a=mycursor.fetchall()
    data={'todo':a}
    return render_template('index.html',data=data)

@app.route("/delete/<int:idd>",methods=["GET","POST"])
def delete(idd):
    sql="DELETE FROM todo_data WHERE id ='{}';".format(idd)
    mycursor.execute(sql)
    return redirect(url_for('homepage'))

app.run(debug=True,host='0.0.0.0')
