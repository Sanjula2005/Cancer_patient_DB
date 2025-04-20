from flask import Flask, render_template, request, redirect, url_for, session
from config import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # Replace with real auth
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return "Invalid credentials!"
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Dashboard (View All Patients)
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()

    cursor.execute("SELECT * FROM Doctors")
    doctors = cursor.fetchall()

    db.close()
    return render_template('dashboard.html', patients=patients, doctors=doctors)


# Query Patients and Reports
@app.route('/query', methods=['GET', 'POST'])
def query():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    # Fetch doctors & patients for dropdowns
    cursor.execute("SELECT DoctorID, Name FROM Doctors")
    doctors = cursor.fetchall()

    cursor.execute("SELECT PatientID, Name FROM Patients")
    patients = cursor.fetchall()

    reports = []
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        patient_id = request.form.get('patient_id')

        sql = """SELECT Doctors.Name AS Doctor, Patients.Name AS Patient, Diagnosis, TestType 
                 FROM MedicalReports 
                 JOIN Doctors ON MedicalReports.DoctorID = Doctors.DoctorID
                 JOIN Patients ON MedicalReports.PatientID = Patients.PatientID
                 WHERE 1=1 """
        params = []
        if doctor_id:
            sql += " AND MedicalReports.DoctorID = %s"
            params.append(doctor_id)
        if patient_id:
            sql += " AND MedicalReports.PatientID = %s"
            params.append(patient_id)

        cursor.execute(sql, tuple(params))
        reports = cursor.fetchall()

    custom_results = []
    headers = []

    if request.method == 'POST':
        # ... existing doctor_id/patient_id query logic ...

        # Handle custom query
        custom_sql = request.form.get('custom_sql')
        if custom_sql:
            try:
                cursor.execute(custom_sql)
                custom_results = cursor.fetchall()
                headers = [desc[0] for desc in cursor.description]
            except Exception as e:
                custom_results = [['Error: ' + str(e)]]

    db.close()
    return render_template('query.html', doctors=doctors, patients=patients, reports=reports,
                           custom_results=custom_results, headers=headers)


@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        contact = request.form['contact']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO Doctors (Name, Specialization, Contact) VALUES (%s, %s, %s)",
                       (name, specialization, contact))
        db.commit()
        db.close()
        return redirect(url_for('dashboard'))

    return render_template('add_doctor.html')

import datetime

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT DoctorID, Name FROM Doctors")
    doctors = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        address = request.form['address']
        doctor_id = request.form['doctor_id']
        diagnosis = request.form['diagnosis']
        test_type = request.form['test_type']
        report_date = datetime.date.today()

        # Insert patient
        cursor.execute("INSERT INTO Patients (Name, Age, Gender, Contact, Address) VALUES (%s, %s, %s, %s, %s)",
                       (name, age, gender, contact, address))
        patient_id = cursor.lastrowid

        # Insert medical report with doctor association
        cursor.execute("""INSERT INTO MedicalReports (PatientID, DoctorID, ReportDate, Diagnosis, TestType)
                          VALUES (%s, %s, %s, %s, %s)""",
                       (patient_id, doctor_id, report_date, diagnosis, test_type))
        db.commit()
        db.close()
        return redirect(url_for('dashboard'))

    return render_template('add_patient.html', doctors=doctors)

if __name__ == '__main__':
    app.run(debug=True)
