import mysql.connector
from tkinter import messagebox
import random

# Define global variables for database connection
connection = None
cursor = None

def connect_to_database(host, user, password, database):
    global connection, cursor
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            cursor = connection.cursor()
            return True
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return False

def disconnect_database():
    global connection, cursor
    try:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

def execute_query(query):
    global cursor, connection
    try:
        if cursor:
            cursor.execute(query)
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.rowcount
        else:
            messagebox.showerror("Error", "No database connection established")
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None
    
def fetch_patient_data(patient_id):
    global cursor, connection
    query = rf"SELECT * FROM patient WHERE patient_id = '{patient_id}'"
    try:
        if cursor:
            cursor.execute(query)
            patient = cursor.fetchone()
            return patient
        else:
            messagebox.showerror("Error", "No database connection established")
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

def fetch_doctor_data(doctor_id):
    global cursor, connection
    query = rf"SELECT * FROM doctor WHERE id = '{doctor_id}'"
    try:
        if cursor:
            cursor.execute(query)
            doctor = cursor.fetchone()
            return doctor
        else:
            messagebox.showerror("Error", "No database connection established")
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

def assign_random_doctor():
    global cursor, connection
    query = "SELECT * FROM doctor WHERE current_status='free' AND attendance='present'"
    try:
        if cursor:
            cursor.execute(query)
            doctors = cursor.fetchall()
            if doctors:
                return random.choice(doctors)
            return None
        else:
            messagebox.showerror("Error", "No database connection established")
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

def update_doctor_status(doctor_id, status):
    global cursor, connection
    query = rf"UPDATE doctor SET current_status = '{status}' WHERE id = '{doctor_id}'"
    try:
        if cursor:
            cursor.execute(query)
            connection.commit()
        else:
            messagebox.showerror("Error", "No database connection established")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

def update_patient_doctor(patient_id, doctor_id):
    global cursor, connection
    query = rf"UPDATE patient SET visited_to = '{doctor_id}' WHERE patient_id = '{patient_id}'"
    try:
        if cursor:
            cursor.execute(query)
            connection.commit()
        else:
            messagebox.showerror("Error", "No database connection established")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

def insert_or_update_patient(Id, Name, Age, Gender, Phone, Issue, VisitedTo):
    global cursor, connection
    query_check = rf"SELECT * FROM Patient WHERE patient_id = '{Id}'"
    try:
        if cursor:
            cursor.execute(query_check)
            existing_patient = cursor.fetchone()
            if existing_patient:
                # Update existing patient record
                query_update = rf"UPDATE Patient SET name = '{Name}', age = '{Age}', gender = '{Gender}', phone = '{Phone}', problem = '{Issue}', visited_to = '{VisitedTo}' WHERE patient_id = '{Id}'"
                print(query_update)
                cursor.execute(query_update)
            else:
                # Insert new patient record
                query_insert = rf"INSERT INTO Patient (patient_id, name, age, gender, phone, problem, visited_to) VALUES ('{Id}', '{Name}', '{Age}', '{Gender}', '{Phone}', '{Issue}', '{VisitedTo}')"
                print(query_insert)
                cursor.execute(query_insert)
            connection.commit()
        else:
            messagebox.showerror("Error", "No database connection established")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

def getProfile(id):
    global cursor, connection
    query = rf"SELECT * FROM patient WHERE patient_id = '{id}'"
    try:
        if cursor:
            cursor.execute(query)
            profile = cursor.fetchone()
            return profile
        else:
            messagebox.showerror("Error", "No database connection established")
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

def fetch_doctor_location(doctor_id):
    global cursor, connection
    query = rf"""
        SELECT ln.floor_number, ln.room_number
        FROM doctor dt
        JOIN location ln ON dt.location_id = ln.id
        WHERE dt.id = '{doctor_id}'
    """
    try:
        if cursor:
            cursor.execute(query)
            location_info = cursor.fetchone()
            if location_info:
                floor_number, room_number = location_info
                return f"You can meet now in room {room_number} on floor {floor_number}."
            else:
                return "Location information not found for the doctor."
        else:
            messagebox.showerror("Error", "No database connection established")
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None