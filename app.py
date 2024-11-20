from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import login_required, current_user  
import pandas as pd
import joblib
import requests 

from flask_cors import CORS




app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel_booking'

mysql = MySQL(app)

@app.before_request
def before_request():
  
    if 'user_id' in session:
        g.is_logged_in = True
        g.role = session.get('role', 'user')  
    else:
        g.is_logged_in = False
        g.role = 'user' 



@app.route('/')
def index():
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')  

    return render_template('index.html', is_logged_in=is_logged_in, role=role)

 


@app.route('/login', methods=['GET', 'POST'])
def login():
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')

    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            session['role'] = user[2]  

            if user[2] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', is_logged_in=is_logged_in, role=role)





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                        (username, password, role))
            mysql.connection.commit()
            flash('Registration successful. You can now log in.')
            return redirect(url_for('login'))
        except:
            flash('Username already exists.')
        finally:
            cur.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()  
    flash('You have been logged out.')
    return redirect(url_for('login'))   

model = joblib.load('model/occupancy_model.pkl')

room_type_mapping = {
    'Single': 0,
    'Double': 1,
    'Family': 2,
    'Suite': 3,
    'Deluxe': 4
}

@app.route('/predict', methods=['POST'])
def predict():
    
    room_type = request.form.get('room_type')
    date = request.form.get('date')

   
    year, month, day = map(int, date.split('-'))

   
    if room_type not in room_type_mapping:
        return jsonify({'error': 'Invalid room type'}), 400

    
    data_to_predict = pd.DataFrame({
        'Year': [year],
        'Month': [month],
        'Day': [day],
        'Room Type': [room_type]
    })

    
    data_to_predict['Room Type'] = data_to_predict['Room Type'].map(room_type_mapping)

    features = data_to_predict[['Day', 'Month', 'Year', 'Room Type']]

    prediction = model.predict(features)[0] 

    return jsonify({'prediction': prediction})



@app.route('/manual-booking', methods=['GET', 'POST'])
def manual_booking():
    room_types = []
    room_numbers = []
    
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    
    
    if 'role' not in session or session['role'] != 'admin':
        flash('You must be an admin to access this page.', 'error')
        return redirect(url_for('login'))

    room_type_prices = {
        'Standard': 1000,
        'Double': 1600,
        'Family': 2500,
        'Deluxe': 5000,
        'Suite': 7500,
        'Single': 800  
    }

    if 'username' not in session or session['role'] != 'admin':
        flash('You must be logged in as an admin to access this page.', 'error')
        return redirect(url_for('login'))

    print(f"Session Details - Username: {session.get('username')}, Role: {session.get('role')}")

    if request.method == 'POST':
        username = request.form['username']
        room_type = request.form['room_type']
        room_number = request.form['room_number']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        print(f"Form Data - Username: {username}, Room Type: {room_type}, Room Number: {room_number}, Start Date: {start_date}, End Date: {end_date}")

        current_date = datetime.now().date()
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

        print(f"Start Date Object: {start_date_obj}, End Date Object: {end_date_obj}, Current Date: {current_date}")

        if start_date_obj < current_date:
            flash('Start date cannot be before today.', 'error')
            return redirect(url_for('manual_booking'))

        if end_date_obj < start_date_obj:
            flash('End date cannot be before the start date.', 'error')
            return redirect(url_for('manual_booking'))

        cur = mysql.connection.cursor()
        query = '''
        SELECT id FROM rooms 
        WHERE room_number = %s AND room_type = %s
        '''
        print(f"Executing query to fetch room_id: {query} with room_number={room_number} and room_type={room_type}")
        cur.execute(query, (room_number, room_type))
        room_id = cur.fetchone()

        print(f"Room ID fetched: {room_id}")

        if not room_id:
            flash('The selected room does not exist.', 'error')
            return redirect(url_for('manual_booking'))

        room_id = room_id[0]

        query = '''
        SELECT * FROM bookings 
        WHERE room_id = %s
        AND (start_date <= %s AND end_date >= %s)
        '''
        cur.execute(query, (room_id, end_date, start_date))
        conflict = cur.fetchone()

        print(f"Conflict check result: {conflict}")

        if conflict:
            flash('The selected room is not available for the chosen dates.', 'error')
            return redirect(url_for('manual_booking'))

        prediction_response = requests.post(url_for('predict', _external=True), data={
            'room_type': room_type,
            'date': start_date
        })
        prediction_data = prediction_response.json()

        if 'error' in prediction_data:
            flash('Could not retrieve prediction: ' + prediction_data['error'], 'error')
            return redirect(url_for('book_room'))

        occupancy_rate = prediction_data['prediction']

        price_adjustment = 0
        if 0 <= occupancy_rate <= 10:
            price_adjustment = -0.20
        elif 11 <= occupancy_rate <= 20:
            price_adjustment = -0.10
        elif 21 <= occupancy_rate <= 30:
            price_adjustment = -0.05
        elif 31 <= occupancy_rate <= 50:
            price_adjustment = 0
        elif 51 <= occupancy_rate <= 60:
            price_adjustment = 0.05
        elif 61 <= occupancy_rate <= 71:
            price_adjustment = 0.10
        elif 72 <= occupancy_rate <= 80:
            price_adjustment = 0.15
        elif 81 <= occupancy_rate <= 90:
            price_adjustment = 0.15
        elif 91 <= occupancy_rate <= 100:
            price_adjustment = 0.25


        num_days = (end_date_obj - start_date_obj).days
        if room_type in room_type_prices:
            base_price_per_day = room_type_prices[room_type]
            final_price = num_days * base_price_per_day * (1 + price_adjustment)
        else:
            flash('Invalid room type selected.', 'error')
            return redirect(url_for('manual_booking'))

        print(f"Calculated final price: {final_price}")

        try:
            cur.execute(''' 
                INSERT INTO bookings (username, room_id, start_date, end_date, final_price, status)
                VALUES (%s, %s, %s, %s, %s, 'Ongoing')
            ''', (username, room_id, start_date, end_date, final_price))
            mysql.connection.commit()
            print("Booking committed successfully")
        except Exception as e:
            print(f"Error committing to the database: {e}")
            flash('There was an error committing the booking to the database.', 'error')
            return redirect(url_for('manual_booking'))

        cur.close()

        flash(f'Booking for {username} completed successfully. Final price: {final_price}', 'success')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT username FROM users WHERE role = "user"')
        users = [row[0] for row in cur.fetchall()]

        cur.execute('SELECT DISTINCT room_type FROM rooms')
        room_types = [row[0] for row in cur.fetchall()]

        if 'room_type' in request.args:
            room_type = request.args.get('room_type')
            cur.execute('SELECT room_number FROM rooms WHERE room_type = %s', [room_type])
            room_numbers = [row[0] for row in cur.fetchall()]
            return jsonify({'room_numbers': room_numbers})

        cur.close()

    return render_template('manual_booking.html', users=users, room_types=room_types, room_numbers=room_numbers, is_logged_in=is_logged_in, role=role)










@app.route('/book-room', methods=['GET', 'POST'])
def book_room():
    room_types = []
    room_numbers = []
    
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    
    if 'role' not in session or session['role'] != 'user':
        flash('You must be an user to access this page.', 'error')
        return redirect(url_for('login')) 
    
    room_type_prices = {
        'Single': 1000,
        'Double': 1600,
        'Family': 2500,
        'Deluxe': 5000,
        'Suite': 7500
    }

    

    username = session['username']

    if request.method == 'POST':
        room_type = request.form['room_type']
        room_number = request.form['room_number']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        current_date = datetime.now().date()
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date_obj < current_date:
            flash('Start date cannot be before today.', 'error')
            return redirect(url_for('book_room'))

        if end_date_obj < start_date_obj:
            flash('End date cannot be before the start date.', 'error')
            return redirect(url_for('book_room'))

        cur = mysql.connection.cursor()
        query = '''
        SELECT id FROM rooms 
        WHERE room_number = %s AND room_type = %s
        '''
        cur.execute(query, (room_number, room_type))
        room_id = cur.fetchone()

        if not room_id:
            flash('The selected room does not exist.', 'error')
            return redirect(url_for('book_room'))

        room_id = room_id[0]

        query = '''
        SELECT * FROM bookings 
        WHERE room_id = %s
        AND (start_date <= %s AND end_date >= %s)
        '''
        cur.execute(query, (room_id, end_date, start_date))
        conflict = cur.fetchone()

        if conflict:
            flash('The selected room is not available for the chosen dates.', 'error')
            return redirect(url_for('book_room'))

        prediction_response = requests.post(url_for('predict', _external=True), data={
            'room_type': room_type,
            'date': start_date
        })
        prediction_data = prediction_response.json()

        if 'error' in prediction_data:
            flash('Could not retrieve prediction: ' + prediction_data['error'], 'error')
            return redirect(url_for('book_room'))

        occupancy_rate = prediction_data['prediction']

        price_adjustment = 0
        if 0 <= occupancy_rate <= 10:
            price_adjustment = -0.20
        elif 11 <= occupancy_rate <= 20:
            price_adjustment = -0.10
        elif 21 <= occupancy_rate <= 30:
            price_adjustment = -0.05
        elif 31 <= occupancy_rate <= 50:
            price_adjustment = 0
        elif 51 <= occupancy_rate <= 60:
            price_adjustment = 0.05
        elif 61 <= occupancy_rate <= 71:
            price_adjustment = 0.10
        elif 72 <= occupancy_rate <= 80:
            price_adjustment = 0.15
        elif 81 <= occupancy_rate <= 90:
            price_adjustment = 0.15
        elif 91 <= occupancy_rate <= 100:
            price_adjustment = 0.25

        num_days = (end_date_obj - start_date_obj).days
        base_price_per_day = room_type_prices[room_type]
        final_price = num_days * base_price_per_day * (1 + price_adjustment)

        cur.execute(''' 
            INSERT INTO booking_requests (username, room_id, start_date, end_date, final_price, status)
            VALUES (%s, %s, %s, %s, %s, 'Pending')
        ''', (username, room_id, start_date, end_date, final_price))
        mysql.connection.commit()
        cur.close()

        print(f"Final price for booking: {final_price}") 

        flash('Booking request submitted successfully.', 'success')
        return redirect(url_for('user_bookings'))

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT DISTINCT room_type FROM rooms')
        room_types = [row[0] for row in cur.fetchall()]

        if 'room_type' in request.args:
            room_type = request.args.get('room_type')
            cur.execute('SELECT room_number FROM rooms WHERE room_type = %s', [room_type])
            room_numbers = [row[0] for row in cur.fetchall()]
            return jsonify({'room_numbers': room_numbers})

        cur.close()

    return render_template('book_room.html', room_types=room_types, room_numbers=room_numbers, is_logged_in=is_logged_in, role=role) 





@app.route('/admin-dashboard', methods=['GET'])
def admin_dashboard():
    
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    
    if 'role' not in session or session['role'] != 'admin':
        flash('You must be an admin to access this page.', 'error')
        return redirect(url_for('login'))

 

    cur = mysql.connection.cursor()
    cur.execute("SELECT br.id, br.username, r.room_number, r.room_type, br.start_date, br.end_date, br.final_price "
                "FROM booking_requests br "
                "JOIN rooms r ON br.room_id = r.id")
    booking_requests = cur.fetchall()

    updated_booking_requests = []

   
    for request in booking_requests:
        booking_request_id = request[0]  
        room_number = request[2]         
        start_date = request[4]         
        end_date = request[5]           
        final_price = request[6]         

        cur.execute(''' 
            SELECT * FROM bookings 
            WHERE room_id = (SELECT id FROM rooms WHERE room_number = %s) 
            AND status = 'Ongoing' 
            AND (start_date <= %s AND end_date >= %s)
        ''', (room_number, end_date, start_date))

        conflict = cur.fetchone()

       
        if conflict:
            updated_booking_requests.append(list(request) + ['disabled'])
        else:
            updated_booking_requests.append(list(request) + ['enabled'])

    cur.close()

    return render_template('admin_dashboard.html', booking_requests=updated_booking_requests, is_logged_in=is_logged_in, role=role)


@app.route('/approve-booking/<int:booking_request_id>', methods=['POST'])
def approve_booking(booking_request_id):

    if 'username' not in session or session['role'] != 'admin':
        flash('You must be logged in as an admin to perform this action.', 'error')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT room_id, start_date, end_date, final_price FROM booking_requests WHERE id = %s", (booking_request_id,))
    booking_request = cur.fetchone()

    if not booking_request:
        flash('Booking request not found.', 'error')
        return redirect(url_for('admin_dashboard'))

    room_id, start_date, end_date, final_price = booking_request

    cur.execute(''' 
        SELECT * FROM bookings
        WHERE room_id = %s 
        AND status = 'Ongoing' 
        AND (start_date <= %s AND end_date >= %s)
    ''', (room_id, end_date, start_date))

    conflict = cur.fetchone()

    if conflict:
        flash('The room is already booked for the requested dates.', 'error')
        return redirect(url_for('admin_dashboard'))

    
    cur.execute(''' 
        INSERT INTO bookings (room_id, username, start_date, end_date, final_price, status)
        VALUES (%s, (SELECT username FROM booking_requests WHERE id = %s), %s, %s, %s, 'Ongoing')
    ''', (room_id, booking_request_id, start_date, end_date, final_price))
    
    
    cur.execute("DELETE FROM booking_requests WHERE id = %s", (booking_request_id,))
    mysql.connection.commit()

    cur.close()

    flash('Booking request approved and moved to bookings.', 'success')
    return redirect(url_for('admin_dashboard'))




@app.route('/reject-booking/<int:booking_request_id>', methods=['POST'])
def reject_booking(booking_request_id):
   
    if 'username' not in session or session['role'] != 'admin':
        flash('You must be logged in as an admin to perform this action.', 'error')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE booking_requests SET status = 'rejected' WHERE id = %s", (booking_request_id,))
    mysql.connection.commit()
    cur.close()

    flash('Booking request rejected.', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/rooms', methods=['GET'])
def rooms():
    
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    
    if 'role' not in session or session['role'] != 'admin':  
        flash('You must be logged in as an admin to access this page.')
        return redirect(url_for('login'))  
    print(f"Session user_id: {session.get('user_id')}, role: {session.get('role')}")

    cur = mysql.connection.cursor()
    
    current_date = datetime.now().date()
    cur.execute('''
        SELECT rooms.id, rooms.room_type, rooms.room_number, 
               IF(EXISTS (
                   SELECT 1 FROM bookings 
                   WHERE bookings.room_id = rooms.id 
                   AND bookings.status = 'Ongoing'
                   AND bookings.start_date <= %s
                   AND bookings.end_date >= %s
               ), 0, 1) AS is_available
        FROM rooms
    ''', (current_date, current_date))

    rooms_data = cur.fetchall()
    cur.close()

    return render_template('rooms.html', rooms=rooms_data, is_logged_in=is_logged_in, role=role)



@app.route('/admin-bookings', methods=['GET', 'POST'])
def admin_bookings():
    
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    
     
    
    if 'role' not in session or session['role'] != 'admin':
        flash('You must be an admin to access this page.', 'error')
        return redirect(url_for('login'))

   
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.id, b.username, r.room_number, r.room_type, b.start_date, b.end_date, b.status, b.final_price "
                "FROM bookings b "
                "JOIN rooms r ON b.room_id = r.id")
    bookings = cur.fetchall()
    cur.close()

   
    if request.method == 'POST' and 'complete_booking' in request.form:
        booking_id = request.form.get('booking_id')

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, status FROM bookings WHERE id = %s", (booking_id,))
        booking = cur.fetchone()

        if booking and booking[1] == 'Ongoing':
        
            cur.execute("UPDATE bookings SET status = 'completed', end_date = %s WHERE id = %s",
                        (datetime.now().date(), booking_id))
            mysql.connection.commit()
            cur.close()

            flash('Booking status has been changed to "Completed".', 'success')
        else:
            flash('Booking is already completed or not found.', 'error')

        return redirect(url_for('admin_bookings'))

    return render_template('admin_bookings.html', bookings=bookings, is_logged_in=is_logged_in, role=role)



@app.route('/my-bookings', methods=['GET'])
def my_bookings():
    
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    
    if 'role' not in session or session['role'] != 'user':
        flash('You must be an user to access this page.', 'error')
        return redirect(url_for('login'))
    
    username = session['username']  

    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT r.room_number, r.room_type, b.start_date, b.end_date, b.status
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        WHERE b.username = %s
        ORDER BY b.start_date DESC
    ''', (username,))
    user_bookings = cur.fetchall()
    cur.close()

    if not user_bookings:
        flash('You have no bookings yet.', 'info')

    return render_template('my_bookings.html', bookings=user_bookings, is_logged_in=is_logged_in, role=role)


@app.route('/admin-revenue', methods=['GET'])
def admin_revenue():
    
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
   
    if 'role' not in session or session['role'] != 'admin':
        flash('You must be an admin to access this page.', 'error')
        return redirect(url_for('login'))

   
    today = datetime.today()
    current_day = today.date()
    current_month = today.month
    current_year = today.year

    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT SUM(final_price) 
        FROM bookings 
        WHERE DATE(end_date) = %s
    """, (current_day,))
    day_revenue = cur.fetchone()[0] or 0.0

    
    cur.execute("""
        SELECT SUM(final_price) 
        FROM bookings 
        WHERE MONTH(end_date) = %s 
        AND YEAR(end_date) = %s
    """, (current_month, current_year))
    month_revenue = cur.fetchone()[0] or 0.0

   
    cur.execute("""
        SELECT SUM(final_price) 
        FROM bookings 
        WHERE YEAR(end_date) = %s
    """, (current_year,))
    year_revenue = cur.fetchone()[0] or 0.0

    
    cur.execute("""
        SELECT COUNT(*) 
        FROM bookings 
        WHERE DATE(end_date) = %s
    """, (current_day,))
    day_bookings = cur.fetchone()[0] or 0

    
    cur.execute("""
        SELECT COUNT(*) 
        FROM bookings 
        WHERE MONTH(end_date) = %s 
        AND YEAR(end_date) = %s
    """, (current_month, current_year))
    month_bookings = cur.fetchone()[0] or 0

    
    cur.execute("""
        SELECT COUNT(*) 
        FROM bookings 
        WHERE YEAR(end_date) = %s
    """, (current_year,))
    year_bookings = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT DATE(end_date), SUM(final_price) 
        FROM bookings 
        WHERE end_date >= CURDATE() - INTERVAL 30 DAY
        GROUP BY DATE(end_date)
        ORDER BY DATE(end_date)
    """)
    daily_revenue_data = cur.fetchall()

    cur.execute("""
        SELECT DATE(end_date), COUNT(*) 
        FROM bookings 
        WHERE end_date >= CURDATE() - INTERVAL 30 DAY
        GROUP BY DATE(end_date)
        ORDER BY DATE(end_date)
    """)
    daily_booking_count_data = cur.fetchall()

    dates = [str(row[0]) for row in daily_revenue_data]
    revenues = [float(row[1]) for row in daily_revenue_data]
    booking_counts = [row[1] for row in daily_booking_count_data]

  
    cur.execute("""
        SELECT r.room_type, COUNT(b.id) 
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        WHERE b.status = 'Ongoing'
        GROUP BY r.room_type
    """)
    room_type_bookings = cur.fetchall()

    cur.close()

   
    return render_template('admin_revenue.html', 
                           day_revenue=day_revenue, 
                           month_revenue=month_revenue, 
                           year_revenue=year_revenue,
                           day_bookings=day_bookings,
                           month_bookings=month_bookings,
                           year_bookings=year_bookings,
                           room_type_bookings=room_type_bookings,
                           dates=dates, revenues=revenues, booking_counts=booking_counts, 
                           is_logged_in=is_logged_in, role=role)


    
    
@app.route('/my-booking-requests', methods=['GET'])
def user_bookings():
    
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
   
    if 'role' not in session or session['role'] != 'user':
        flash('You must be an user to access this page.', 'error')
        return redirect(url_for('login'))

    username = session['username']  
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT br.id, r.room_number, r.room_type, br.start_date, br.end_date, br.status, br.final_price
        FROM booking_requests br
        JOIN rooms r ON br.room_id = r.id
        WHERE br.username = %s
    """, (username,))
    booking_requests = cur.fetchall()
    cur.close()

    return render_template('my_booking_requests.html', booking_requests=booking_requests , is_logged_in=is_logged_in, role=role)

@app.route('/Single_room')
def Single_room():
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    return render_template('standard_room.html', is_logged_in=is_logged_in, role=role)

@app.route('/Double_room')
def Double_room():
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    return render_template('double_room.html', is_logged_in=is_logged_in, role=role)

@app.route('/Deluxe_room')
def Deluxe_room():
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    return render_template('deluxe_room.html', is_logged_in=is_logged_in, role=role)

@app.route('/Family_room')
def Family_room():
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    return render_template('family_room.html', is_logged_in=is_logged_in, role=role)

@app.route('/Suite_room')
def Suite_room():
    is_logged_in = 'user_id' in session
    role = session.get('role', 'user')
    return render_template('suite_room.html', is_logged_in=is_logged_in, role=role)







if __name__ == '__main__':
    app.run(debug=True)
