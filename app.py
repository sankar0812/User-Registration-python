from flask import Flask,render_template,request,url_for,session,redirect,flash
from flask_mysqldb import MySQL
#import webview

app=Flask(__name__, static_folder='./static', template_folder='./templates')

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""

app.config["MYSQL_DB"]="registration"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


@app.route("/",methods=['GET','POST'])
def index():
   if 'alogin' in request.form:
       if request.method == 'POST':
           aname = request.form["aname"]
           apass = request.form["apass"]
           try:
               cur = mysql.connection.cursor()
               cur.execute("select * from admin where aname=%s and apass=%s", [aname,apass])
               res = cur.fetchone()
               if res:
                   session["aname"] = res["aname"]
                   session["id"] = res["id"]
                   return redirect(url_for('admin_home'))
               else:
                   return render_template("index.html")
           except Exception as e:
               print(e)
           finally:
               mysql.connection.commit()
               cur.close()

   elif 'register' in request.form:
       if request.method == 'POST':
           uname = request.form['uname']
           password = request.form['upass']
           age = request.form['age']
           address = request.form['address']
           contact = request.form['contact']
           mail = request.form['mail']
           cur = mysql.connection.cursor()
           cur.execute('insert into users (name,password,age,address,contact,mail) values (%s,%s,%s,%s,%s,%s)',
                        [uname, password, age, address, contact, mail])
           mysql.connection.commit()
       return render_template("index.html")

   elif 'ulogin' in request.form:
       if request.method == 'POST':
           name = request.form['uname']
           password = request.form['upass']
           try:
               cur = mysql.connection.cursor()
               cur.execute("select * from users where name=%s and password=%s", [name,password])
               res = cur.fetchone()
               if res:
                   session["name"] = res["name"]
                   session["id"] = res["id"]
                   return redirect(url_for('user_home'))
               else:
                   return render_template("index.html")
           except Exception as e:
               print(e)
           finally:
               mysql.connection.commit()
               cur.close()
   return render_template("index.html")

@app.route("/user_profile")
def user_profile():
    cur = mysql.connection.cursor()
    id = session['id']
    qry = "select * from users where id=%s"
    cur.execute(qry,[id])
    data = cur.fetchall()
    cur.close()
    count = cur.rowcount
    if count == 0:
        flash("Users not found...!!!","danger")
    else:
        return render_template("user_profile.html",res=data)
    
@app.route("/update_user",methods=['GET','POST'])
def update_user():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        age = request.form['age']
        address = request.form['address']
        contact = request.form['contact']
        mail = request.form['mail']
        id = session['id']
        cur = mysql.connection.cursor()
        cur.execute('update users set name=%s,password=%s,age=%s,address=%s,contact=%s,mail=%s where id=%s',[name, password, age, address, contact, mail,id])
        mysql.connection.commit()
        flash('User Updated Successfully')
        return redirect(url_for('user_profile'))
    return render_template('user_profile.html')

@app.route("/view_users")
def view_users():
    cur = mysql.connection.cursor()
    qry = "select * from users"
    cur.execute(qry)
    data = cur.fetchall()
    cur.close()
    count = cur.rowcount
    if count == 0:
        flash("User Not Found..!!")
    return render_template("view_users.html",res=data)

@app.route("/delete_users/<string:id>", methods=['GET','POST'])
def delete_users(id):
    cur = mysql.connection.cursor()
    cur.execute("delete from users where id=%s", [id])
    mysql.connection.commit()
    flash("Users Deleted Successfully")
    return redirect(url_for("view_users"))
    

@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")

@app.route("/user_home")
def user_home():
    return render_template("user_home.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
   
#app.run(host="0.0.0.0", port=8070)



if(__name__=='__main__'):
    app.secret_key = '123'
    app.run(debug=True)
    #webview.start()

