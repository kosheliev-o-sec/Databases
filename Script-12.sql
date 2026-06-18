DROP TABLE IF EXISTS exam_results CASCADE;
DROP TABLE IF EXISTS exams CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS teachers CASCADE;
DROP TABLE IF EXISTS students CASCADE;

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(100)
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    teacher_id INT REFERENCES teachers(teacher_id)
);

CREATE TABLE exams (
    exam_id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(course_id),
    exam_date DATE
);

CREATE TABLE exam_results (
    result_id SERIAL PRIMARY KEY,
    exam_id INT REFERENCES exams(exam_id),
    student_id INT REFERENCES students(student_id),
    score NUMERIC(5,2)
);

-----------

INSERT INTO students (full_name, email) VALUES
('Anna Kovalenko', 'anna.k@example.com'),
('Dmytro Petrenko', 'd.petrenko@example.com'),
('Olena Shevchenko', 'olena.sh@example.com'),
('Ivan Franko', 'ivan.f@example.com'),
('Maria Tkachenko', 'maria.t@example.com');

INSERT INTO teachers (full_name, department) VALUES
('Dr. Alan Turing', 'Computer Science'),
('Dr. Albert Einstein', 'Physics'),
('Dr. Marie Curie', 'Chemistry'),
('Dr. Ada Lovelace', 'Mathematics');

INSERT INTO courses (course_name, teacher_id) VALUES
('Introduction to Programming', 1),
('Advanced Databases', 1),
('Quantum Physics', 2),
('Organic Chemistry', 3),
('Calculus II', 4);

INSERT INTO exams (course_id, exam_date) VALUES
(1, '2026-05-10'),
(2, '2026-05-15'),
(3, '2026-05-20'),
(4, '2026-05-25'),
(5, '2026-05-30');

INSERT INTO exam_results (exam_id, student_id, score) VALUES
(1, 1, 95.50),
(1, 2, 88.00),
(1, 4, 75.00),
(2, 1, 98.00),
(2, 3, 60.00),
(2, 5, 85.50),
(3, 2, 92.00),
(3, 3, 70.00),
(3, 4, 65.00),
(4, 5, 99.00),
(4, 1, 89.50),
(5, 2, 78.00),
(5, 4, 82.00);
-----------
INSERT INTO students (full_name, email)
SELECT 
    'Student ' || i,
    'student' || i || '@example.com'
FROM generate_series(1, 500) AS i;

INSERT INTO teachers (full_name, department)
SELECT 
    'Teacher ' || i,
    (ARRAY['Computer Science', 'Physics', 'Chemistry', 'Mathematics', 'Biology', 'History'])[floor(random() * 6 + 1)]
FROM generate_series(1, 50) AS i;

INSERT INTO courses (course_name, teacher_id)
SELECT 
    'Course ' || i,
    floor(random() * 50 + 1)::INT
FROM generate_series(1, 100) AS i;

INSERT INTO exams (course_id, exam_date)
SELECT 
    floor(random() * 100 + 1)::INT,
    CURRENT_DATE + (random() * 365)::INT
FROM generate_series(1, 200) AS i;

INSERT INTO exam_results (exam_id, student_id, score)
SELECT 
    floor(random() * 200 + 1)::INT,
    floor(random() * 500 + 1)::INT,
    (random() * 100)::NUMERIC(5,2)
FROM generate_series(1, 10000) AS i;
-----------

select * from courses
select * from exam_results 
select * from exams
select * from students
select * from teachers

with StudentStatistics as(
select s.student_id, s.full_name, 
count(er.result_id) as exams_taken,
round(avg(er.score), 2) as avg_score,
max(er.score) as highest_result 
from students s
join exam_results er on s.student_id=er.student_id
join exams e on er.exam_id=e.exam_id
join courses c on e.course_id=c.course_id 
join teachers t on c.teacher_id=t.teacher_id
where t.teacher_id <=2  -- Обираємо лише вчителів з id 1,2
group by s.student_id, s.full_name)


select * from StudentStatistics ss
where avg_score >= 60
order by highest_result desc;

--------

select 'Students' as staff,
count(*) as total_count
from students s

union all 

select 'Teachers',
count(*) as total_count
from teachers t;

