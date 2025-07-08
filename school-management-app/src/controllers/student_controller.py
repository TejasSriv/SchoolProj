import mysql.connector
from .db import get_connection
from models.student import Student

class StudentDBManager:
    
    STUDENT_COLUMNS = [
        "scholar_id",
        "apaar_id",
        "permanent_enrollment_number",
        "name",
        "class",
        "dob",
        "gender",
        "social_category",
        "father",
        "mother",
        "last_school",
        "tc_number",
        "address",
        "city",
        "state",
        "admission_date",
        "contact",
        "alternate_contact",
        "email",
        "aadhaar",
        "birth_certificate"
    ]

    def _execute_query(self, query, params=None, fetch_one=False, fetch_all=False, commit=False):

        conn = None
        cursor = None
        result = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            if commit:
                conn.commit()
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            if conn and commit:
                conn.rollback()
            print(f"Database error: {err}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_students(self):

        select_cols_str = ", ".join(self.STUDENT_COLUMNS)
        query = f"SELECT {select_cols_str} FROM students"
        raw_students = self._execute_query(query, fetch_all=True)
        return [Student.from_dict(s) for s in raw_students] if raw_students else []

    def get_student_by_id(self, scholar_id: int):
        select_cols_str = ", ".join(self.STUDENT_COLUMNS)
        query = f"SELECT {select_cols_str} FROM students WHERE scholar_id = %s"
        raw_student = self._execute_query(query, (scholar_id,), fetch_one=True)
        return Student.from_dict(raw_student) if raw_student else None

    def search_students(self, keyword):
        students = []
        select_cols_str = ", ".join(self.STUDENT_COLUMNS)
        
        try:
            int_keyword = int(keyword)
        except ValueError:
            int_keyword = None

        if int_keyword is not None:
             query = f"SELECT {select_cols_str} FROM students WHERE scholar_id = %s OR name LIKE %s"
             params = (int_keyword, f"%{keyword}%")
        else:
            query = f"SELECT {select_cols_str} FROM students WHERE name LIKE %s"
            params = (f"%{keyword}%",)
            
        raw_students = self._execute_query(query, params, fetch_all=True)
        return [Student.from_dict(s) for s in raw_students] if raw_students else []

    def add_student(self, student: Student):

        data = student.to_dict()
        
        if 'class_name' in data:
            data['class'] = data.pop('class_name')
        
        data['aadhaar'] = 1 if data.get('aadhaar') else 0
        data['birth_certificate'] = 1 if data.get('birth_certificate') else 0

        columns = ", ".join(self.STUDENT_COLUMNS)
        placeholders = ", ".join(["%s"] * len(self.STUDENT_COLUMNS))
        query = f"INSERT INTO students ({columns}) VALUES ({placeholders})"
        
        values = tuple(data.get(col_name) for col_name in self.STUDENT_COLUMNS)
        self._execute_query(query, values, commit=True)

    def update_student(self, student: Student):

        data = student.to_dict()
        
        if 'class_name' in data:
            data['class'] = data.pop('class_name')

        data['aadhaar'] = 1 if data.get('aadhaar') else 0
        data['birth_certificate'] = 1 if data.get('birth_certificate') else 0

        set_clauses = [f"{col}=%s" for col in self.STUDENT_COLUMNS if col != "scholar_id"]
        query = f"UPDATE students SET {', '.join(set_clauses)} WHERE scholar_id=%s"
        
        values = tuple(data.get(k) for k in self.STUDENT_COLUMNS if k != "scholar_id") + (data.get("scholar_id"),)
        
        self._execute_query(query, values, commit=True)

    def delete_student(self, scholar_id: int):
        """Deletes a student record by scholar_id."""
        query = "DELETE FROM students WHERE scholar_id = %s"
        self._execute_query(query, (scholar_id,), commit=True)