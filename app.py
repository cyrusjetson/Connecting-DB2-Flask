# NOTE: Here I took customer care registry project for example
# DESC: in customer care registry customer or agent or admin login if his credentials arevalid he will
# be navigated to his respective page

from flask import Flask, render_template, request, redirect, session, url_for, request
import ibm_db

# DB2 connection
print("Trying to connect...")
global conn

#change according to your credentials
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wpp19;PWD=rDMGL208dK1N;", '', '')
print("connected..")


# app
app = Flask(__name__)


app.secret_key = "anythinguwant" #not fixed you can put anything as app secret key




@app.route('/', methods=['GET'])
def base():
    return redirect(url_for('login'))


def checkauth():   # for checking whether user is authorized
    key_list = list(session.keys())
    if key_list:
        return True
    else:
        return False
      
def clean():
    key_list = list(session.keys())
    for key in key_list:
        session.pop(key)

@app.route('/users')
def user():
  return render_template('user.html')

@app.route('/admin')
def admin():
  return render_template('admin.html)
                  
@app.route('/agent')
def agent():
   return render('agent.html')                   
  
# Login
@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']
        if len(username) == 0 or len(password) == 0:
            msg = 'Details are not filled completely!'
            return render_template('login.html', msg=msg)
        if username == 'admin' and password == 'admin':
            session['userid'] = 'admin'
            session['name'] = 'admin'
            session['email'] = 'imadmin@gmail.com'
            return redirect('/admin')
        else:
                       # executing query
            sql = "select * from agents where username = ? and password = ?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, username)
            ibm_db.bind_param(stmt, 2, password)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            if account:
                session['userid'] = account['USERNAME']
                session['name'] = account['NAME']
                session['email'] = account['EMAIL']
                return redirect('/agent')

        sql = "select * from users where username = ? and password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            session['userid'] = account['USERNAME']
            session['name'] = account['NAME']
            session['email'] = account['EMAIL']
            return redirect('/users')
        else:
            msg = 'Incorrect user credentials'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html', msg=msg)

 if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
