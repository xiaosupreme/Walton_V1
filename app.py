from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from db_config import init_db
from models import create_user, get_user_by_username, bcrypt
from functools import wraps
import mysql.connector
import requests

app = Flask(__name__)   
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"  # Rasa server webhook endpoint
app.secret_key = 'your_secret_key'

app.config['SESSION_COOKIE_SECURE'] = True  # Use HTTPS for production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript from accessing session cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Helps mitigate CSRF attacks

mysql = init_db(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.json.get("message")
    if user_message:
        response = requests.post(RASA_URL, json={"sender": "user", "message": user_message})
        return jsonify(response.json())
    return jsonify({"error": "No message sent"})


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session.get('role') != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user')  # Default to 'user'
        
        if get_user_by_username(mysql, username):
            flash('Username already exists', 'danger')
        else:
            create_user(mysql, username, password, role)
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(mysql, username)

        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@admin_required
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'], role=session['role'])
    else:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    
    
@app.route('/admin/manual_booking', methods=['GET', 'POST'])
@admin_required
def manual_booking():
    if request.method == 'POST':
        # Get form data
        room_type = request.form.get('room_type')
        room_number = request.form.get('room_number')
        guest_name = request.form.get('guest_name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Validate the dates
        today = datetime.today().strftime('%Y-%m-%d')
        if start_date < today:
            flash('Start date cannot be before the current date.', 'error')
            return redirect(url_for('manual_booking'))

        # Check if the selected room is already booked
        cur = mysql.connection.cursor()
        cur.execute("SELECT status FROM rooms WHERE id = %s", (room_number,))
        room = cur.fetchone()

        if room and room['status'] == 'booked':
            flash(f"Room {room_number} is already booked.", 'error')
            return redirect(url_for('manual_booking'))

        # Calculate the price (assuming price per room type is stored)
        cur.execute("SELECT price FROM rooms WHERE id = %s", (room_number,))
        room = cur.fetchone()
        price_per_night = room['price']
        num_nights = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
        total_price = price_per_night * num_nights

        # Insert booking into bookings table
        cur.execute("""
            INSERT INTO bookings (user_id, room_id, guest_name, start_date, end_date, total_price, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Approved')
        """, (1, room_number, guest_name, start_date, end_date, total_price))

        # Update room status to 'booked'
        cur.execute("UPDATE rooms SET status = 'booked' WHERE id = %s", (room_number,))
        mysql.connection.commit()
        cur.close()

        flash(f'Room {room_number} booked successfully for {guest_name}!', 'success')
        return redirect(url_for('manual_booking'))

    # Fetch rooms by type for displaying available rooms
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT room_type, room_number, price, status FROM rooms
    """)
    rooms = cur.fetchall()
    cur.close()

    # Organize rooms by type
    rooms_by_type = {}
    for room in rooms:
        room_type = room['room_type']
        if room_type not in rooms_by_type:
            rooms_by_type[room_type] = []
        rooms_by_type[room_type].append(room)

    return render_template('manual_booking.html', rooms_by_type=rooms_by_type)


# API endpoint to fetch available rooms based on room type
@app.route('/admin/get_available_rooms', methods=['GET'])
@admin_required
def get_available_rooms():
    room_type = request.args.get('room_type')
    cur = mysql.connection.cursor()
    
    # Fetch available rooms based on selected room type
    cur.execute("""
        SELECT * FROM rooms 
        WHERE room_type = %s AND status = 'available'
    """, (room_type,))
    
    rooms = cur.fetchall()
    cur.close()

    # Return the rooms in JSON format
    available_rooms = [{"id": room['id'], "room_number": room['room_number']} for room in rooms]
    
    return jsonify({"rooms": available_rooms})



@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
