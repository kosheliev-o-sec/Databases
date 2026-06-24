import random
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import execute_values
from faker import Faker

# ====================================================================
# Налаштування підключення (Змінити на свої дані від БД PostgreSQL)
# ====================================================================
HOST = 'localhost' # put your credentials here
USER = 'postgres' # put your credentials here
PASSWORD = '1' # put your credentials here
DATABASE = 'banks' # put your credentials here
PORT = '5432' # put your credentials here

# ====================================================================
# Налаштування обсягу даних 
# ====================================================================
PATIENTS_COUNT = 20_000
DOCTORS_COUNT = 10_000
APPOINTMENTS_COUNT = 100_000
CHUNK_SIZE = 5_000  # Розмір пачки для швидкої вставки

fake = Faker()

def insert_patients(cursor):
    print("Вставка даних у таблицю patients...")

    query = """
        INSERT INTO patients (full_name, date_of_birth, email)
        VALUES %s
        RETURNING patient_id
    """

    patient_ids = []

    for start in range(0, PATIENTS_COUNT, CHUNK_SIZE):
        current_chunk_size = min(CHUNK_SIZE, PATIENTS_COUNT - start)
        patients_data = []
        
        for _ in range(current_chunk_size):
            patients_data.append((
                fake.name(),
                fake.date_of_birth(minimum_age=18, maximum_age=90), # Вік від 18 до 90 років
                fake.unique.email()
            ))

        # Виконуємо вставку пачки даних і відразу збираємо згенеровані patient_id
        results = execute_values(cursor, query, patients_data, fetch=True)
        patient_ids.extend([row[0] for row in results])
        print(f"Вставлено {start + current_chunk_size} рядків у patients...")

    print("Вставку в patients завершено!\n")
    return patient_ids


def insert_doctors(cursor):
    print("Вставка даних у таблицю doctors...")

    query = """
        INSERT INTO doctors (full_name, specialization, work_experience)
        VALUES %s
        RETURNING doctor_id
    """

    specializations = [
        "Cardiology", "Dermatology", "Neurology", "Pediatrics", 
        "Oncology", "Orthopedics", "Psychiatry", "Surgery", "Therapy"
    ]
    
    doctor_ids = []

    for start in range(0, DOCTORS_COUNT, CHUNK_SIZE):
        current_chunk_size = min(CHUNK_SIZE, DOCTORS_COUNT - start)
        doctors_data = []
        
        for _ in range(current_chunk_size):
            doctors_data.append((
                f"Dr. {fake.last_name()}", # Генеруємо ім'я лікаря з префіксом
                random.choice(specializations),
                random.randint(1, 40)      # Стаж від 1 до 40 років
            ))

        results = execute_values(cursor, query, doctors_data, fetch=True)
        doctor_ids.extend([row[0] for row in results])
        print(f"Вставлено {start + current_chunk_size} рядків у doctors...")

    print("Вставку в doctors завершено!\n")
    return doctor_ids


def insert_appointments(cursor, patient_ids, doctor_ids):
    print("Вставка даних у таблицю appointments...")

    query = """
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, status)
        VALUES %s
    """

    statuses = ['completed', 'canceled', 'in_process']
    start_date = datetime.now() - timedelta(days=365 * 3) # Візити за останні 3 роки

    for start in range(0, APPOINTMENTS_COUNT, CHUNK_SIZE):
        current_chunk_size = min(CHUNK_SIZE, APPOINTMENTS_COUNT - start)
        appointments_data = []
        
        for _ in range(current_chunk_size):
            appointments_data.append((
                random.choice(patient_ids),
                random.choice(doctor_ids),
                start_date + timedelta(days=random.randint(0, 365 * 3 + 30)), # Рандомна дата
                random.choices(statuses, weights=[0.6, 0.2, 0.2], k=1)[0]     # 60% завершено
            ))

        execute_values(cursor, query, appointments_data)
        print(f"Вставлено {start + current_chunk_size} рядків у appointments...")

    print("Вставку в appointments завершено!\n")


def main():
    print("Підключення до бази даних PostgreSQL...")
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            dbname=DATABASE,
            port=PORT,
        )

        with connection:
            with connection.cursor() as cursor:
                # Порядок важливий: спочатку створюємо пацієнтів та лікарів, потім візити
                patient_ids = insert_patients(cursor)
                doctor_ids = insert_doctors(cursor)
                insert_appointments(cursor, patient_ids, doctor_ids)
                
        print("Всі фейкові дані успішно згенеровано та збережено!")

    except Exception as e:
        print(f"Виникла помилка: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()


if __name__ == "__main__":
    main()
