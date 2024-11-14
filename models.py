from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_user(mysql, username, password, role='user'):
    cur = mysql.connection.cursor()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
    mysql.connection.commit()
    cur.close()

def get_user_by_username(mysql, username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", [username])
    user = cur.fetchone()
    cur.close()
    return user
