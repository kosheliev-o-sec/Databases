import psycopg2
from psycopg2 import Error

HOST = 'localhost' # put your credentials here
USER = 'postgres' # put your credentials here
PASSWORD = '' # put your credentials here
DATABASE = '' # put your credentials here 
PORT = '5432' # put your credentials here

def create_connection():
    """Create a PostgreSQL database connection."""
    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DATABASE,
        )
        print("Connection to PostgreSQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def execute_query(connection, query, data):
    """Execute a single query."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        connection.rollback()
        print(f"The error '{e}' occurred")

def insert_data():
    connection = create_connection()
    if connection is None:
        return

  
    patients_query = """
    INSERT INTO patients (patient_id, full_name, date_of_birth, email, phone)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (patient_id) DO NOTHING
    """
    patients_data = [
        (1, "Ivan Petrenko", "1990-05-15", "ivan.petrenko@example.com", "+380501234567"),
        (2, "Olena Koval", "1985-11-20", "olena.koval@example.com", "+380671234567"),
        (3, "Andriy Shevchenko", "2000-02-10", "andriy.sh@example.com", "+380931234567")
    ]
    for data in patients_data:
        execute_query(connection, patients_query, data)

    patient_profiles_query = """
    INSERT INTO patient_profiles (patient_id, address, blood_type, emergency_contact)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (patient_id) DO NOTHING
    """
    patient_profiles_data = [
        (1, "Kyiv, Khreshchatyk 1", "A+", "Wife: +380509998877"),
        (2, "Lviv, Rynok Sq 5", "O-", "Brother: +380679998877"),
        (3, "Odesa, Deribasivska 10", "B+", "Mother: +380939998877")
    ]
    for data in patient_profiles_data:
        execute_query(connection, patient_profiles_query, data)


    departments_query = """
    INSERT INTO departments (department_id, department_name, floor)
    VALUES (%s, %s, %s)
    ON CONFLICT (department_id) DO NOTHING
    """
    departments_data = [
        (1, "Cardiology", 2),
        (2, "Neurology", 3),
        (3, "Pediatrics", 1)
    ]
    for data in departments_data:
        execute_query(connection, departments_query, data)

   
    doctors_query = """
    INSERT INTO doctors (doctor_id, department_id, full_name, specialization, work_experience, email)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (doctor_id) DO NOTHING
    """
    doctors_data = [
        (1, 1, "Dr. Gregory House", "Cardiologist", 15, "house@clinic.com"),
        (2, 2, "Dr. Stephen Strange", "Neurologist", 10, "strange@clinic.com"),
        (3, 3, "Dr. John Watson", "Pediatrician", 5, "watson@clinic.com")
    ]
    for data in doctors_data:
        execute_query(connection, doctors_query, data)

    
    appointments_query = """
    INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (appointment_id) DO NOTHING
    """
    appointments_data = [
        (1, 1, 1, "2026-06-30 10:00:00", "scheduled"),
        (2, 2, 2, "2026-06-25 14:30:00", "completed"),
        (3, 3, 3, "2026-06-28 09:15:00", "cancelled")
    ]
    for data in appointments_data:
        execute_query(connection, appointments_query, data)

    medications_query = """
    INSERT INTO medications (medication_id, medication_name, manufacturer, price)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (medication_id) DO NOTHING
    """
    medications_data = [
        (1, "Aspirin", "Bayer", 5.50),
        (2, "Ibuprofen", "Pfizer", 8.20),
        (3, "Amoxicillin", "Sandoz", 15.00)
    ]
    for data in medications_data:
        execute_query(connection, medications_query, data)

   
    prescriptions_query = """
    INSERT INTO prescriptions (prescription_id, appointment_id, medication_id, dosage, duration_days)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (prescription_id) DO NOTHING
    """
    prescriptions_data = [
        (1, 2, 2, "200mg twice a day", 7),
        (2, 2, 1, "100mg once a day", 14),
        (3, 1, 3, "500mg three times a day", 5)
    ]
    for data in prescriptions_data:
        execute_query(connection, prescriptions_query, data)

    connection.close()
    print("Database seeding completed!")

if __name__ == "__main__":
    insert_data()
