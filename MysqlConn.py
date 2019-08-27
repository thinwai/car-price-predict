from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_BB'] = 'demo'

mysql = MySQL(app)

@app.route('/')
def home():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM loginform")
	fetchdata = cur.fetchall()
	cur.close()
	return render_template("modal.html", data=fetchdata)

if __name__ =="__main__":
    app.run(debug="True")