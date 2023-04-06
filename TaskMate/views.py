import mysql.connector
from django.shortcuts import render,redirect

mydb = mysql.connector.connect(
    host="localhost",
    user="bishalde",
    password="bishalde",
    database="flask_todo"
)

# mydb = mysql.connector.connect(
#     host="db4free.net",
#     user="bishalde",
#     password="8299260163",
#     database="clustix"
# )

"""---------------------------------Table creation Code-----------------------------------"""
mycursor = mydb.cursor()
mycursor.execute("""
                CREATE TABLE IF NOT EXISTS Taskmate_data(
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    user_id varchar(255) ,
                    deadline DATE NOT NULL,
                    deadlinetime VARCHAR(10) NOT NULL,
                    priority int(10) NOT NULL DEFAULT 5,
                    description VARCHAR(255) NOT NULL,
                    filename varchar(255)
                )                
;""")
mycursor.execute("""CREATE TABLE IF NOT EXISTS Taskmate_users(
                    username VARCHAR(255) NOT NULL PRIMARY KEY,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE NOT NULL
);
""")



def login(request):
    if request.session.has_key('username'):
        return redirect('homepage')
    data={'error':None}
    if request.method=="POST":
        f_data = request.POST
        username=f_data.get("username")
        password=f_data.get("password")
        #Search fo the username
        sql="SELECT * FROM Taskmate_users WHERE username ='{}' && password='{}';".format(username,password)
        mycursor.execute(sql)
        q_data=mycursor.fetchall()
        if len(q_data)>0:
            request.session['username'] = username
            return redirect('homepage/')
        else:
            data['error']="Credentials not found..!"
            return render(request,'login.html',data)
    return render(request,'login.html',data)


def signup(request):
    data={'error': None}
    if request.method=="POST":
        f_data = request.POST
        username=f_data.get("username")
        email=f_data.get("email")
        password=f_data.get("password")

        #check if username/email already exists
        sql="SELECT * FROM Taskmate_users WHERE username ='{}' || email='{}';".format(username,email)
        mycursor.execute(sql)
        q_data=mycursor.fetchall()

        if len(q_data)>0:
            data['error']="Username or Email already In USE...!"
            return render(request,'signup.html',data)
        
        #to add new user
        try:
            sql="INSERT INTO Taskmate_users VALUES('{}','{}','{}');".format(username,password,email)
            print(username,password)
            mycursor.execute(sql)
            mydb.commit()

        except Exception as e:
            data['error']=e
            return render(request,'signup.html',data)
            
        data['error']="Account Created Successfully..!"
        return render(request,'signup.html',data)
    return render(request,'signup.html',data)


def homepage(request):
    data={}
    if request.session.has_key('username'):
        user=request.session['username']
        data['username']=user
        if(request.method == "POST"):
            q_data = request.POST
            user=request.session['username']
            date=q_data.get('date')
            time=q_data.get('time')
            priority=q_data.get('priority')
            description=q_data.get('description')

            #insert data into table
            sql="""
                INSERT INTO `Taskmate_data` (`deadline`,`user_id` ,`deadlinetime`, `priority`, `description`,`filename`) 
                VALUES ('{}','{}' ,'{}', '{}', '{}','404-not-found')
            ;""".format(date,user,time,priority,description)

            mycursor.execute(sql)
            mydb.commit()


        #show all the data form the table
        sql="""
            SELECT * FROM Taskmate_data WHERE user_id='{}' ORDER BY deadline,deadlinetime DESC,priority ASC;
        ;""".format(user)
        mycursor.execute(sql)
        a=mycursor.fetchall()

        #return the data to the webpage
        data['todo']=a
        return render(request,'index.html',data)
    else:
        return redirect('/')


def logout(request):
    try:
      del request.session['username']
    except:
      pass
    return redirect('/')


def editTodo(request,id):
    data={'idd':id}
    return render(request,'edittodo.html',data)


def delete(request,idd):
    sql="DELETE FROM Taskmate_data WHERE id ='{}';".format(idd)
    mycursor.execute(sql)
    return redirect('homepage')











