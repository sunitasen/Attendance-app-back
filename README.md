# Attendance-app-back

 https://acm-attendance-app.herokuapp.com/

## Name of the database : Attendance

## Tables: 
1. class = (Names and code of all class )|| code | name
2. routine = (routines) ||  teacher_id | subject_code | class_code |   day   | time_begin | time_end
3. subject = (list of subjects) || code | name
4. Teacher = (list of teachers) ||  id |  name  | department
5. Names of all students of a class -> table name == department_year (eg: cse_3) ||  id  | name
6. Copy of a class for each teacher for attendance -> table name == department_year_teacher_id (eg: cse_3_3) 
                                        ||      id      | name | dt_12_01_2020 | total | dt_13_01_2020 | dt_14_01_2020


## Endpoints

### /getTeacherRoutine
    Input : 
    1. id -> id of the teacher
    Function: Returns all the classes of the particular teacher in routine table

### /addRoutine
    Input :
        1. teacher_id 
        2. subject_code 
        3. class_code 
        4. day  
        5. time_begin 
        6. time_end
    Function: Adds a routine in routine tbale

### /addSubject
    Input :
        1. code 
        2. name
    Function: Adds a subject in subject table

### /addClass
    Input :
        1. code 
        2. name
    Function: Adds a class in class table

### /addTeacher
    Input :
        1. id 
        2. name
        3. Department
    Function: Adds a teacher in teacher table

### /addStudent
    Input :
        1. id 
        2. name
        3. code
    Function: Adds a Student in a particular class table

### /createclass
    Input:
        1. code -- of the form department_year
    Function: Creates a new table for given class

### /addAttendancedate
    Input: 
        1. date -- if the form date_month_year
    Function: adds a new attendance column eg: dt_14_01_2020

### /addAttendance
    Input:
        1. date
        2. class_code
        3. teacher_id
        4. student_id
    Function: adds attendance for student

### /returnattendance
    Input:
        1. class_code
        2. teacher_id
        3. student_id
    Function: Returns the total attendance of the student for a particular teacher











