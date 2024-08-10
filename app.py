from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['railway_ticket_reservation']
tickets_collection = db['tickets']
train_details_collection = db['train_details']
ticket_status_collection = db['ticket_status']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    from_station = request.form['from']
    to_station = request.form['to']
    date = request.form['date']
    passengers = int(request.form['passengers'])
    mobile_number = request.form['mobile_number']
    class_type = request.form['class']

    ticket = {
        'from_station': from_station,
        'to_station': to_station,
        'date': date,
        'passengers': passengers,
        'mobile_number': mobile_number,
        'class_type': class_type
    }

    tickets_collection.insert_one(ticket)
    return redirect(url_for('index'))

@app.route('/train_details', methods=['POST'])
def train_details():
    train_name = request.form['train_name']
    departure_time = request.form['departure_time']
    arrival_time = request.form['arrival_time']

    train = {
        'train_name': train_name,
        'departure_time': departure_time,
        'arrival_time': arrival_time
    }

    train_details_collection.insert_one(train)
    return redirect(url_for('index'))

@app.route('/check_status', methods=['POST'])
def check_status():
    ticket_number = request.form['ticket_number']
    passenger_name = request.form['passenger_name']

    ticket = ticket_status_collection.find_one({'ticket_number': ticket_number, 'passenger_name': passenger_name})
    if ticket:
        return 'Ticket status: ' + ticket['status']
    else:
        return 'Ticket not found'

if __name__ == '__main__':
    app.run(debug=True)