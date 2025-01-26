from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__)

# Load data
registration_path = 'registration_users.csv'
logs_path = 'logs.csv'

registration_df = pd.read_csv(registration_path)
logs_df = pd.read_csv(logs_path)

# Convert date and time columns to datetime
logs_df['datetime'] = pd.to_datetime(logs_df['date'] + ' ' + logs_df['time'])
registration_df['register_datetime'] = pd.to_datetime(
    registration_df['register_date'] + ' ' + registration_df['register_time']
)

# Helper function to find absent employees
def find_absent_employees(target_date, registration_df, logs_df):
    target_date = pd.to_datetime(target_date).date()
    registered_users = set(registration_df['user_id'])
    present_users = set(logs_df[logs_df['datetime'].dt.date == target_date]['user_id'])
    absent_users = registered_users - present_users
    return list(absent_users)

# Helper function to calculate late arrivals and early departures
def analyze_timings(target_date, start_time, end_time, logs_df):
    target_date = pd.to_datetime(target_date).date()
    start_datetime = pd.to_datetime(f"{target_date} {start_time}")
    end_datetime = pd.to_datetime(f"{target_date} {end_time}")

    user_logs = logs_df[logs_df['datetime'].dt.date == target_date]
    grouped = user_logs.groupby('user_id')

    late_arrivals = []
    early_departures = []

    for user_id, group in grouped:
        enters = group[group['enter_or_exit'] == 'enter']['datetime']
        exits = group[group['enter_or_exit'] == 'exit']['datetime']

        if not enters.empty and enters.min() > start_datetime:
            late_arrivals.append({
                'user_id': user_id,
                'late_by_minutes': (enters.min() - start_datetime).total_seconds() / 60
            })

        if not exits.empty and exits.max() < end_datetime:
            early_departures.append({
                'user_id': user_id,
                'early_by_minutes': (end_datetime - exits.max()).total_seconds() / 60
            })

    return late_arrivals, early_departures

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.form
    target_date = data['date']
    start_time = data['start_time']
    end_time = data['end_time']

    # Perform analysis
    absent_employees = find_absent_employees(target_date, registration_df, logs_df)
    late_arrivals, early_departures = analyze_timings(target_date, start_time, end_time, logs_df)

    return jsonify({
        'absent_employees': absent_employees,
        'late_arrivals': late_arrivals,
        'early_departures': early_departures
    })


if __name__ == "__main__":
    app.run(debug=True)
