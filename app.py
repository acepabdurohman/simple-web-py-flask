from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from config import connection
from flask_bcrypt import Bcrypt
import logging

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'my_secret'

@app.route("/")
def main():
    is_logged_in = session.get('logged_in')
    if is_logged_in:
        username = session.get('username')
        return redirect(url_for('index', username = username))
    return render_template('login.html')

@app.route("/sign_up", methods=['GET', 'POST'])
def show_sign_up():

    if request.method == 'GET':
        return render_template('sign-up.html')
    else:

        conn = connection.get_connection()
        cursor = conn.cursor()

        try:
            username = request.form['username']
            password = request.form['pwd']
            fullname = request.form['fullname']

            hashed_pwd = bcrypt.generate_password_hash(password)

            insert_user(username, hashed_pwd, fullname, cursor)

            conn.commit()

            response = {
                'message': 'success'
            }
            return jsonify(response), 200
        except Exception as e:
            conn.rollback()
            logging.error(e)
        finally:
            cursor.close()
            conn.close()
        response = {
            'message': 'Gagal insert data'
        }
        return jsonify(response), 500
        

def insert_user(username, password, fullname, cursor):

    sql = 'insert into t_user(id, username, password, name) values(%s, %s, %s, %s)'
    param = (None, username, password, fullname)
    cursor.execute(sql, param)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['pwd']

    result = validate_login(username, password)

    if result:
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('index', username = username))
    else:
        return render_template('login.html', message='Username atau password salah')

@app.route('/home/<username>')
def index(username):
    is_logged_in = session.get('logged_in')
    if not is_logged_in:
        return redirect(url_for('main'))
    return render_template('index.html', my_username = username)


def validate_login(username, password):
    conn = connection.get_connection()
    cursor = conn.cursor()
    sql = "select * from t_user where username = %s"
    param = (username,)
    cursor.execute(sql, param)
    user = cursor.fetchone()
    if user == None:
        return False
    if bcrypt.check_password_hash(user[2], password):
        return True
    return False


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('main'))
        
if __name__ == '__main__':
    app.run(debug=True)