from flask import Flask, request, render_template
import mysql.connector
import os

app = Flask(__name__)

# MySQL connection setup using env variables
db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', 'example'),
    database=os.getenv('MYSQL_DATABASE', 'vulndb')
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    name = request.args.get('name', '')
    # VULNERABLE to SQL Injection
    query = f"SELECT username, email FROM users WHERE username LIKE '%{name}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    return render_template('search.html', results=results)

@app.route('/comment', methods=['POST'])
def comment():
    note = request.form['note']
    # VULNERABLE to Reflected XSS
    cursor.execute("INSERT INTO comments (note) VALUES (%s)", (note,))
    db.commit()
    return f"<p>Your note: {note}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)