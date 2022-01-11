import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import yaml

##################################################################################

app = Flask(__name__)
app.secret_key = "super secret key"

##################################################################################

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

##################################################################################

@app.route('/', endpoint='func1', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if request.form['activatebutton'] == 'Sign-Up':
            return redirect('/signup')
        elif request.form['activatebutton'] == 'Sign-In':
            return redirect('/signin')



    return render_template('index.html')


##################################################################################

@app.route('/insertppe', endpoint='func2', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        ppeDetails = request.form
        ppesn = ppeDetails['ppesn']
        ppename = ppeDetails['ppename']
        ppebrand = ppeDetails['ppebrand']
        ppesupplier = ppeDetails['ppesupplier']
        ppelocation = ppeDetails['ppelocation']
        ppequantity = ppeDetails['ppequantity']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO PPEDATA(ppeSN, ppeName, ppeBrand, ppeSupplier, ppeLocation, ppeQuantity) VALUES(%s, %s, %s, %s, %s, %s)",(ppesn, ppename, ppebrand, ppesupplier, ppelocation, ppequantity))
        mysql.connection.commit()
        cur.close()
        return redirect('/ppeitems')
    return render_template('insertppe.html')


##################################################################################


@app.route('/updateppe', endpoint='func3', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        # Fetch form data
        ppeDetails = request.form
        ppename = ppeDetails['ppename']
        ppequantity = ppeDetails['ppequantity']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE PPEDATA SET ppeQuantity=%s WHERE ppeName = % s", (ppequantity, ppename))
        mysql.connection.commit()
        cur.close()



        return redirect('/ppeitems')
    return render_template('updateppe.html')


##################################################################################



@app.route('/deleteppe', endpoint='func4', methods=['GET', 'POST'])
def delete():

    if request.method == 'POST':
        # Fetch form data
        ppeDetails = request.form
        ppename = ppeDetails['ppename']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM PPEDATA WHERE ppeName = % s", [ppename])
        mysql.connection.commit()
        cur.close()



        return redirect('/ppeitems')
    return render_template('deleteppe.html')


##################################################################################


@app.route('/ppeitems',  endpoint='func5')
def ppeitems():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM PPEDATA")
    if resultValue > 0:
        ppeItemsDetails = cur.fetchall()
        return render_template('display.html',ppeitems=ppeItemsDetails)

##################################################################################


@app.route('/signup',  endpoint='func6', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Fetch form data
        signupDetails = request.form
        uname = signupDetails['uname']
        upass = signupDetails['upass']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO UsersOriginalCredentials(logUserName, logPassword) VALUES(%s, %s)",(uname, upass))
        mysql.connection.commit()
        cur.close()
        return ('Account Created Successfully, go to the previous page for Sign-In')
    return render_template('signup.html')

##################################################################################



@app.route('/signin',  endpoint='func7', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Fetch form data
        signupDetails = request.form
        uname = signupDetails['uname']
        upass = signupDetails['upass']

##############

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM UsersOriginalCredentials WHERE logUserName = %s AND logPassword = %s', (uname, upass,))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['upass'] = account['logPassword']
            session['uname'] = account['logUserName']
            # Redirect to home page
            return redirect('/crudpanel')
        else:
            # Account doesnt exist or username/password incorrect
            return 'Incorrect User Name or Password!'



    return render_template('signin.html')

##################################################################################

@app.route('/crudpanel', endpoint='func8', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if request.method == 'POST' and request.form['activatebutton'] == 'Create PPE Item':
            return redirect('/insertppe')

        if request.method == 'POST' and request.form['activatebutton'] == 'Read PPE Items':
            return redirect('/ppeitems')

        if request.method == 'POST' and request.form['activatebutton'] == 'Update PPE Item':
            return redirect('/updateppe')

        if request.method == 'POST' and request.form['activatebutton'] == 'Delete PPE Item':
            return redirect('/deleteppe')
        else:
            return redirect('/signup')




    return render_template('crudpanel.html')

##################################################################################

if __name__ == '__main__':
    app.run(debug=True)