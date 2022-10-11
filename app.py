# from crypt import methods
import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3

project_root = os.path.dirname(__file__)
static_path = os.path.join(project_root, 'static')

app = Flask(__name__, static_folder=static_path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///air-flights.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# create tables in DB
class Ticket_flights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_no = db.Column(db.String(300), nullable=False)
    flight_id = db.Column(db.Integer, nullable=False)
    fare_conditions = db.Column(db.String(300), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Flights(db.Model):
    flight_id = db.Column(db.Integer, primary_key=True)
    flight_no = db.Column(db.String(300), nullable=False)
    sheduled_departure = db.Column(db.DateTime)
    sheduled_arrival = db.Column(db.DateTime)
    departure_airport = db.Column(db.String(300), nullable=False)
    arrival_airport = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(300), nullable=False)
    aircraft_code = db.Column(db.String(300), nullable=False)
    actual_departure = db.Column(db.DateTime)
    actual_arrival = db.Column(db.DateTime)
# ----end create tables


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        if int(request.form['flag']) == 1:
            sd = request.form['sd']
            fc = request.form['fc']
            res = work_with_sqlite(sd, fc, None, 1)
            return jsonify({'res': res})

        if int(request.form['flag']) == 2:
            sd = request.form['sd']
            fc = request.form['fc']
            fn = request.form['fn']
            res = work_with_sqlite(sd, fc, fn, 2)
            return jsonify({'res':res})
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")

def work_with_sqlite(sheduled_departure=None, fare_conditions=None, flight_no=None, flag=None):
    if flag == 1:
        script = f"""
            select DISTINCT f.flight_no  
            from flights f 
            join ticket_flights tf 
            on f.flight_id = tf.flight_id 
            where f.sheduled_departure LIKE '{sheduled_departure}%' 
                and tf.fare_conditions = '{fare_conditions}'"""
    if flag == 2:
        script = f"""
            select f.sheduled_departure,
	               f.sheduled_arrival,
	               f.departure_airport,
	               f.arrival_airport,
	               f.status,
	               f.aircraft_code,
	               f.actual_departure,
	               f.actual_arrival,
	               tf.amount,
	               count(tf.ticket_no) 
            from flights f 
            join ticket_flights tf
            on f.flight_id = tf.flight_id 
            where f.sheduled_departure LIKE '{sheduled_departure}%' 
	            and tf.fare_conditions = '{fare_conditions}' 
	            and f.flight_no = '{flight_no}'
                limit(1)
        """
    con = sqlite3.connect('air-flights.db')
    cur = con.cursor()
    cur_res = cur.execute(script)
    res = []
    for i in cur_res:
        res.append(i)
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    # db.create_all()

